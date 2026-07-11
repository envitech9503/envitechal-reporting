from django.db.models import Q
import datetime as _dt

def _parse_date(s):
    s=(s or '').strip()
    s=s.split('(')[0].strip()
    for fmt in ('%Y-%m-%d','%d-%B-%Y','%d-%b-%Y','%d/%m/%Y','%d-%m-%Y'):
        try: return _dt.datetime.strptime(s,fmt).date()
        except Exception: pass
    return None


def _date_key(o, fields):
    import datetime as _d2
    for f in fields:
        v = getattr(o, f, None)
        if not v: continue
        if isinstance(v, _d2.datetime): return (1, v.date(), o.id)
        if isinstance(v, _d2.date): return (1, v, o.id)
        d = _parse_date(str(v))
        if d: return (1, d, o.id)
    import datetime as _d3
    return (0, _d3.date.min, o.id)

def _by_date_desc(qs, fields):
    return sorted(list(qs), key=lambda o: _date_key(o, fields), reverse=True)

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
    return _by_date_desc(qs, ('reporting_date','sampling_date','date_of_sampling','logging_date','date')), True

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
    return _by_date_desc(qs, ('inp3','rec_date','date')), True

def _cert_filter(request, model):
    g=request.GET
    cn=g.get('certSearch','').strip(); cl=g.get('clientSearch','').strip()
    eq=g.get('equipSearch','').strip(); loc=g.get('locationSearch','').strip()
    fd=g.get('from_date','').strip(); td=g.get('to_date','').strip()
    if not (cn or cl or eq or loc or fd or td):
        return model.objects.none(), False
    names={f.name for f in model._meta.get_fields()}
    qs=model.objects.all()
    if cn: qs=qs.filter(cert_num__icontains=cn)
    if cl: qs=qs.filter(Q(client__icontains=cl)|Q(address__icontains=cl))
    if eq:
        q=Q(equipment__icontains=eq)|Q(manufacturer__icontains=eq)
        if 'equip_id' in names: q|=Q(equip_id__icontains=eq)
        qs=qs.filter(q)
    if loc: qs=qs.filter(city_location__icontains=loc)
    if fd or td:
        f1=_parse_date(fd) if fd else None
        t1=_parse_date(td) if td else None
        ids=[]
        for r in qs.values('id','date'):
            d=_parse_date(str(r['date'] or ''))
            if d and (f1 is None or d>=f1) and (t1 is None or d<=t1): ids.append(r['id'])
        qs=qs.filter(id__in=ids)
    return _by_date_desc(qs, ('date',)), True

def _work_filter(request, model):
    g=request.GET
    jn=g.get('jobSearch','').strip(); iv=g.get('invoiceSearch','').strip()
    co=g.get('companySearch','').strip(); loc=g.get('locationSearch','').strip()
    fd=g.get('from_date','').strip(); td=g.get('to_date','').strip()
    if not (jn or iv or co or loc or fd or td):
        return model.objects.none(), False
    qs=model.objects.all()
    if jn: qs=qs.filter(job_number__icontains=jn)
    if iv: qs=qs.filter(Q(invoice_ref__icontains=iv)|Q(po_reference__icontains=iv))
    if co:
        q=Q(representative_name__icontains=co)|Q(service_receiver__icontains=co)
        for f in ('company__company_name','company__name','company__client_name'):
            try:
                model.objects.filter(**{f+'__icontains':'x'})
                q|=Q(**{f+'__icontains':co}); break
            except Exception: pass
        qs=qs.filter(q)
    if loc: qs=qs.filter(location__icontains=loc)
    if fd:
        d=_parse_date(fd)
        if d: qs=qs.filter(created_at__date__gte=d)
    if td:
        d=_parse_date(td)
        if d: qs=qs.filter(created_at__date__lte=d)
    return _by_date_desc(qs, ('created_at',)), True
