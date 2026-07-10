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

def _sampling_filter(request, model):
    g=request.GET
    ss=g.get('sampleSearch','').strip(); an=g.get('analysisSearch','').strip()
    sb=g.get('samplingBySearch','').strip(); tp=g.get('typeSearch','').strip()
    cl=g.get('clientSearch','').strip()
    fd=g.get('from_date','').strip(); td=g.get('to_date','').strip()
    if not (ss or an or sb or tp or cl or fd or td):
        return model.objects.none(), False
    qs=model.objects.all()
    if ss: qs=qs.filter(sample_id__icontains=ss)
    if model.__name__=='Sample_registration':
        if an:
            a=an.lower(); q=Q()
            if 'chem' in a: q|=Q(checkinp_chemical=True)
            if 'bact' in a or 'micro' in a or 'bio' in a: q|=Q(checkinp_bacteria=True)
            if q.children: qs=qs.filter(q)
        if sb: qs=qs.filter(Q(inp2__icontains=sb)|Q(inp1__icontains=sb))
        if tp: qs=qs.filter(inp4__icontains=tp)
        datef='inp3'
    else:
        if cl: qs=qs.filter(Q(client_name__icontains=cl)|Q(att_person__icontains=cl))
        if sb: qs=qs.filter(rec_by__icontains=sb)
        if tp: qs=qs.filter(sample_nature__icontains=tp)
        datef='rec_date'
    if fd or td:
        f1=_parse_date(fd) if fd else None
        t1=_parse_date(td) if td else None
        ids=[]
        for r in qs.values('id',datef):
            d=_parse_date(str(r[datef] or ''))
            if d and (f1 is None or d>=f1) and (t1 is None or d<=t1): ids.append(r['id'])
        qs=qs.filter(id__in=ids)
    return qs.order_by('-id'), True
