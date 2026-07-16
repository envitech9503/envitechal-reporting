from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import CostParameter, CostingConfig
from .services import compute_cost
from .forms import CostParameterForm, RecipeChemicalFormSet, RecipeLabourFormSet
from .permissions import can_manage_costing, manage_required

CUR = lambda: getattr(settings, 'COSTING_CURRENCY', 'PKR')


def costing_list(request):
    config = CostingConfig.current()
    rows = []
    for p in CostParameter.objects.all():
        r = p.compute(config=config)
        rows.append({'p': p, 'cost': r['cost'], 'price': r['price']})
    ctx = {
        'rows': rows, 'config': config, 'currency': CUR(),
        'count': len([r for r in rows if r['p'].active]),
        'avg_margin': round(config.target_margin * 100, 1),
        'can_manage': can_manage_costing(request.user),
    }
    return render(request, 'costing/list.html', ctx)


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


def api_recompute(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    batch = request.GET.get('batch')
    try:
        batch = int(batch) if batch else None
    except (TypeError, ValueError):
        batch = None
    return JsonResponse(compute_cost(p, batch_size=batch))
