from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import CostParameter, CostingConfig
from .services import compute_cost
from .forms import CostParameterForm, RecipeChemicalFormSet, RecipeLabourFormSet
from .permissions import can_manage_costing, manage_required

CUR = lambda: getattr(settings, 'COSTING_CURRENCY', 'PKR')


def thin_margin(config):
    try:
        return float(config.thin_margin_pct)
    except (TypeError, ValueError):
        return 15.0

SORT_KEYS = {
    'code': lambda x: x['p'].code,
    'name': lambda x: (x['p'].name or '').lower(),
    'matrix': lambda x: (x['p'].matrix or ''),
    'cost': lambda x: x['cost'],
    'price': lambda x: x['price'],
    'margin': lambda x: x['margin_pct'],
}


def costing_list(request):
    config = CostingConfig.current()
    q = (request.GET.get('q') or '').strip()
    matrix = (request.GET.get('matrix') or '').strip()
    sort = request.GET.get('sort') or 'code'

    qs = CostParameter.objects.all()
    if q:
        qs = qs.filter(Q(code__icontains=q) | Q(name__icontains=q) | Q(method__icontains=q))
    if matrix:
        qs = qs.filter(matrix=matrix)

    thin = thin_margin(config)
    rows = []
    for p in qs.prefetch_related('chemicals__chemical', 'labour__grade'):
        r = p.compute(config=config)
        cost, price = r['cost'], r['price']
        margin_pct = round((price - cost) / price * 100, 1) if price else 0.0
        flag = 'below' if price < cost else ('thin' if margin_pct < thin else '')
        rows.append({'p': p, 'cost': cost, 'price': price,
                     'margin_pct': margin_pct, 'flag': flag,
                     'missing': r['missing_rates']})

    rev = sort.startswith('-')
    keyfn = SORT_KEYS.get(sort.lstrip('-'), SORT_KEYS['code'])
    rows.sort(key=keyfn, reverse=rev)

    matrices = sorted({(p.matrix or '').strip() for p in CostParameter.objects.all() if (p.matrix or '').strip()})
    ctx = {
        'rows': rows, 'config': config, 'currency': CUR(),
        'count': CostParameter.objects.filter(active=True).count(),
        'total': CostParameter.objects.count(),
        'avg_margin': round(config.target_margin * 100, 1),
        'can_manage': can_manage_costing(request.user),
        'q': q, 'matrix': matrix, 'sort': sort, 'matrices': matrices,
        'flagged': sum(1 for r in rows if r['flag']),
        'shown': len(rows), 'thin': thin,
    }
    return render(request, 'costing/list.html', ctx)


def costing_export_csv(request):
    import csv
    from django.http import HttpResponse
    config = CostingConfig.current()
    thin = thin_margin(config)
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="costing_catalogue.csv"'
    w = csv.writer(resp)
    w.writerow(['Code', 'Parameter', 'Matrix', 'Method', 'Batch size',
                'Cost per test (%s)' % CUR(), 'Recommended price (%s)' % CUR(),
                'Gross margin %', 'Flag', 'Active'])
    for p in CostParameter.objects.prefetch_related('chemicals__chemical', 'labour__grade'):
        r = p.compute(config=config)
        cost, price = r['cost'], r['price']
        m = round((price - cost) / price * 100, 1) if price else 0.0
        flag = 'BELOW COST' if price < cost else ('THIN' if m < thin else '')
        w.writerow([p.code, p.name, p.matrix, p.method, p.batch_size,
                    '%.2f' % cost, '%.2f' % price, m, flag,
                    'yes' if p.active else 'no'])
    return resp


@manage_required
def costing_archive(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    if request.method == 'POST':
        p.active = not p.active
        p.save()
        messages.success(request, 'Parameter "%s" %s.' %
                         (p.code, 'restored' if p.active else 'archived'))
    return redirect('costing:list')


def costing_detail(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    config = CostingConfig.current()
    r = p.compute(config=config)
    return render(request, 'costing/detail.html', {
        'p': p, 'r': r, 'config': config, 'currency': CUR(),
        'can_manage': can_manage_costing(request.user),
    })


def _edit(request, p, mode):
    if request.method == 'POST':
        form = CostParameterForm(request.POST, instance=p)
        chem_fs = RecipeChemicalFormSet(request.POST, instance=p, prefix='chem')
        lab_fs = RecipeLabourFormSet(request.POST, instance=p, prefix='lab')
        if form.is_valid() and chem_fs.is_valid() and lab_fs.is_valid():
            with transaction.atomic():
                obj = form.save()
                chem_fs.instance = obj
                chem_fs.save()
                lab_fs.instance = obj
                lab_fs.save()
            messages.success(request, 'Parameter "%s" saved.' % obj.code)
            return redirect('costing:detail', pk=obj.pk)
        messages.error(request, 'Please correct the highlighted errors.')
    else:
        form = CostParameterForm(instance=p)
        chem_fs = RecipeChemicalFormSet(instance=p, prefix='chem')
        lab_fs = RecipeLabourFormSet(instance=p, prefix='lab')
    return render(request, 'costing/form.html', {
        'form': form, 'chem_fs': chem_fs, 'lab_fs': lab_fs,
        'mode': mode, 'p': p if p.pk else None, 'currency': CUR(),
    })


@manage_required
def costing_add(request):
    return _edit(request, CostParameter(), 'New')


@manage_required
def costing_edit(request, pk):
    return _edit(request, get_object_or_404(CostParameter, pk=pk), 'Edit')


@manage_required
def costing_clone(request, pk):
    src = get_object_or_404(CostParameter, pk=pk)
    if request.method != 'POST':
        return redirect('costing:detail', pk=pk)
    base = src.code
    code = ('%s-COPY' % base)[:32]
    i = 2
    while CostParameter.objects.filter(code=code).exists():
        code = ('%s-%d' % (base, i))[:32]
        i += 1
    with transaction.atomic():
        clone = get_object_or_404(CostParameter, pk=src.pk)
        clone.pk = None
        clone.code = code
        clone.name = (src.name + ' (copy)')[:255]
        clone.save()
        for rc in src.chemicals.all():
            rc.pk = None
            rc.parameter = clone
            rc.save()
        for rl in src.labour.all():
            rl.pk = None
            rl.parameter = clone
            rl.save()
    messages.success(request, 'Cloned "%s" to a new draft "%s".' % (src.code, clone.code))
    return redirect('costing:edit', pk=clone.pk)


@manage_required
def costing_delete(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    if request.method == 'POST':
        code = p.code
        p.delete()
        messages.success(request, 'Parameter "%s" deleted.' % code)
        return redirect('costing:list')
    return render(request, 'costing/confirm_delete.html', {'p': p, 'currency': CUR()})


@manage_required
def costing_history(request, pk):
    from .models import RecipeChemical, RecipeLabour
    p = get_object_or_404(CostParameter, pk=pk)
    tmap = {'+': 'Created', '~': 'Changed', '-': 'Deleted'}
    records = list(p.history.all()[:60])
    entries = []
    for i, rec in enumerate(records):
        changes = []
        if rec.history_type == '~' and i + 1 < len(records):
            try:
                for ch in rec.diff_against(records[i + 1]).changes:
                    changes.append({'field': ch.field, 'old': ch.old, 'new': ch.new})
            except Exception:
                pass
        entries.append({'when': rec.history_date, 'user': rec.history_user,
                        'type': tmap.get(rec.history_type, rec.history_type),
                        'label': 'Parameter', 'changes': changes})
    for rec in RecipeChemical.history.filter(parameter_id=pk)[:40]:
        entries.append({'when': rec.history_date, 'user': rec.history_user,
                        'type': tmap.get(rec.history_type, rec.history_type),
                        'label': 'Recipe chemical #%s' % rec.id,
                        'changes': [{'field': 'qty/sample', 'old': '', 'new': rec.qty_sample},
                                    {'field': 'qty/batch', 'old': '', 'new': rec.qty_batch}]})
    for rec in RecipeLabour.history.filter(parameter_id=pk)[:40]:
        entries.append({'when': rec.history_date, 'user': rec.history_user,
                        'type': tmap.get(rec.history_type, rec.history_type),
                        'label': 'Recipe labour #%s' % rec.id,
                        'changes': [{'field': 'minutes/sample', 'old': '', 'new': rec.minutes_sample}]})
    entries.sort(key=lambda e: e['when'], reverse=True)
    return render(request, 'costing/history.html',
                  {'p': p, 'entries': entries[:80], 'currency': CUR()})


def api_recompute(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    batch = request.GET.get('batch')
    try:
        batch = int(batch) if batch else None
    except (TypeError, ValueError):
        batch = None
    return JsonResponse(compute_cost(p, batch_size=batch))
