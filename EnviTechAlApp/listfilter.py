from django.db.models import Q
import datetime as _dt

def _parse_date(s):
    s=(s or '').strip()
    s=s.split('(')[0].strip()
    for fmt in ('%Y-%m-%d','%d-%B-%Y','%d-%b-%Y','%d/%m/%Y','%d-%m-%Y'):
        try: return _dt.datetime.strptime(s,fmt).date()
        except Exception: pass
    return None

MODEL_MAP={
 'Sample_registration':{'name':('inp1','inp2','inp4'),'loc':('city_location',),'date':('inp3',)},
 'LoggingSheet':{'name':('client_name','att_person','sample_nature','rec_by'),'loc':('city_location','address'),'date':('rec_date',)},
}
def _list_filter(request, model):
    g=request.GET
    name=g.get('nameInput','').strip()
    fd=g.get('from_date','').strip()
    td=g.get('to_date','').strip()
    loc=g.get('locationSearch','').strip()
    samp=g.get('sampleSearch','').strip()
    if not (name or fd or td or loc or samp):
        return model.objects.none(), False
    names={f.name for f in model._meta.get_fields()}
    mm=MODEL_MAP.get(model.__name__)
    qs=model.objects.all()
    if name:
        q=Q()
        for f in (mm['name'] if mm else ('report_to','attention','lab_report_no','invoice_bill_no','invoice_no','client_name','customer_name','company_name','name','project_name','client','sample_source')):
            if f in names: q|=Q(**{f+'__icontains':name})
        if q.children: qs=qs.filter(q)
    if loc:
        lq=Q()
        for f in (mm['loc'] if mm else ('location',)):
            if f in names: lq|=Q(**{f+'__icontains':loc})
        if lq.children: qs=qs.filter(lq)
    if samp and 'sample_id' in names: qs=qs.filter(sample_id__icontains=samp)
    datef=next((x for x in ((mm['date'] if mm else ())+('reporting_date','sampling_date','date_of_sampling','logging_date','date')) if x in names),None)
    if (fd or td) and datef:
        f1=_parse_date(fd); t1=_parse_date(td)
        ids=[]
        for r in qs.values('id',datef):
            d=_parse_date(str(r[datef] or ''))
            if d and (f1 is None or d>=f1) and (t1 is None or d<=t1): ids.append(r['id'])
        qs=qs.filter(id__in=ids)
    return qs.order_by('-id'), True
