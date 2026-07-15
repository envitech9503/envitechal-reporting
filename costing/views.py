from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import CostParameter, CostingConfig
from .services import compute_cost


def costing_list(request):
    config = CostingConfig.current()
    rows = []
    total_cost = total_price = 0
    for p in CostParameter.objects.filter(active=True):
        r = p.compute(config=config)
        rows.append({'p': p, 'cost': r['cost'], 'price': r['price']})
        total_cost += r['cost']; total_price += r['price']
    ctx = {
        'rows': rows, 'config': config,
        'currency': getattr(settings, 'COSTING_CURRENCY', 'PKR'),
        'count': len(rows),
        'avg_margin': round(config.target_margin * 100, 1),
    }
    return render(request, 'costing/list.html', ctx)


def costing_detail(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    config = CostingConfig.current()
    r = p.compute(config=config)
    return render(request, 'costing/detail.html', {
        'p': p, 'r': r, 'config': config,
        'currency': getattr(settings, 'COSTING_CURRENCY', 'PKR'),
    })


def api_recompute(request, pk):
    p = get_object_or_404(CostParameter, pk=pk)
    batch = request.GET.get('batch')
    try:
        batch = int(batch) if batch else None
    except (TypeError, ValueError):
        batch = None
    return JsonResponse(compute_cost(p, batch_size=batch))
