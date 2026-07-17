# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


def compress_image(uploaded_file, max_size_kb=500):
    """Compress image to under max_size_kb while preserving quality"""
    try:
        # Open the image file
        img = Image.open(BytesIO(uploaded_file.read()))
        
        # Convert to RGB if PNG with alpha channel
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Try saving with different quality settings
        for quality in [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]:
            output_buffer = BytesIO()
            
            # Use JPEG for better compression, but could use original format if preferred
            img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            
            # Check if we're under the size limit
            if len(output_buffer.getvalue()) / 1024 <= max_size_kb:
                return output_buffer.getvalue()
                
        # If still too large after quality reduction, resize dimensions
        original_width, original_height = img.size
        new_width = int(original_width * 0.9)
        new_height = int(original_height * 0.9)
        
        while len(output_buffer.getvalue()) / 1024 > max_size_kb and new_width > 100:
            img = img.resize((new_width, new_height), Image.LANCZOS)
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG', quality=70, optimize=True)
            new_width = int(new_width * 0.9)
            new_height = int(new_height * 0.9)
            
        return output_buffer.getvalue()
        
    except Exception as e:
        return None

def get_client_ip(request):
    # Trust X-Real-IP set by our nginx reverse proxy (the real peer
    # address). X-Forwarded-For is deliberately NOT used: a client can
    # forge it, which would let an attacker spoof an allowed office IP.
    ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR') or ''
    return ip.strip()

def userlogin(request):
     if request.method == "POST":
          userName = request.POST['username']
          password = request.POST['password']

          user = authenticate(request,username=userName,password=password)
          from django.conf import settings as _dj_settings
          allowed_ip = getattr(_dj_settings, 'OFFICE_ALLOWED_IPS', ['110.93.247.168', '124.29.208.36'])
          
          user_ip = get_client_ip(request)

        # Check if the user is a superuser (admin) and allow access
          if user is not None and user.is_superuser:
               login(request, user)
               return redirect('nav')

          if user_ip not in allowed_ip:
               return HttpResponseForbidden("Access denied. Your IP is not allowed.")

          if user is not None:
               login(request, user)
               return redirect('nav')
          else:
               return HttpResponse("User Not Found")
     else:
          if request.user.is_authenticated:
               
               return redirect('nav')
          else:
               return render(request, "LoginForm.html")




def custom_500(request):
     import django
     try:
          import sys
          excep = sys.exc_info()
          if excep[0] is None:
               return redirect("login")
          return render(request,"error.html",context={"error":str(excep[1])})
     except Exception as e:
          return render(request,"error.html",context={"error":str(e)})


@login_required(login_url="/login")     
def home(request):
     if request.GET.get('clear'):
         request.session.pop('search_params', None)
         return HttpResponseRedirect(request.path)
     if request.GET.get('nameInput') or request.GET.get('from_date') or request.GET.get('locationSearch') or request.GET.get('sampleSearch'):
          name_input = request.GET.get('nameInput', '').strip()
          from_date = request.GET.get('from_date', '')
          to_date = request.GET.get('to_date', '')
          location_search = request.GET.get('locationSearch', '').strip()
          sample_search = request.GET.get('sampleSearch', '').strip()
          # Store in session to persist across pagination
          request.session['search_params'] = {
              'name_input': name_input,
              'from_date': from_date,
              'to_date': to_date,
              'location_search': location_search,
              'sample_search': sample_search,
          }
          
          # Search across all models
          all_reports = search_all_reports(
              name_input, from_date, to_date, location_search, sample_search
          )
          
          # Paginate results (20 per page)
          paginator = Paginator(all_reports, 200)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          
          context = {
              'all_reports': page_obj,
              'search_performed': True,
              'total_results': paginator.count,
              'name_input': name_input,
              'from_date': from_date,
              'to_date': to_date,
              'location_search': location_search,
              'sample_search': sample_search,
          }
          return render(request, "index.html", context)
    
     # For pagination clicks - retrieve search params from session
     if request.GET.get('page') and request.session.get('search_params'):
         params = request.session['search_params']
         all_reports = search_all_reports(
             params.get('name_input', ''),
             params.get('from_date', ''),
             params.get('to_date', ''),
             params.get('location_search', ''),
             params.get('sample_search', '')
         )
         paginator = Paginator(all_reports, 200)
         page_number = request.GET.get('page')
         page_obj = paginator.get_page(page_number)
         
         context = {
             'all_reports': page_obj,
             'search_performed': True,
             'total_results': paginator.count,
             'name_input': params.get('name_input', ''),
             'from_date': params.get('from_date', ''),
             'to_date': params.get('to_date', ''),
             'location_search': params.get('location_search', ''),
             'sample_search': params.get('sample_search', ''),
         }
         return render(request, "index.html", context)
     
     return render(request, 'index.html', {'search_performed': False})

def search_all_reports(name_input, from_date, to_date, location_search, sample_search):
     all_results = []
     search_configs = [
         {
             'model': DrinkingWaterForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'dw'
         },
         {
             'model': GaseousEmissionForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'gae'
         },
         {
             'model': AmbientAirForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'aa'
         },
         {
             'model': WasteWaterSludge,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'ww'
         },
         {
             'model': VehiculEmissionForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 've'
         },
         {
             'model': LuxAnalysisForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'la'
         },
         {
             'model': PackingPolyBagForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'pp'
         },
         {
             'model': MachineOilForm,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'mo'
         },
         {
             'model': MicrobialAnalysis,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'ma'
         },
         {
             'model': ViscousLiquid,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'vl'
         },
         {
             'model': AmbientAir2,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'aa2'
         },
         {
             'model': WasteWaterForm2,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'ww2'
         },
         {
             'model': NoiseAnalysis,
             'name_fields': ['report_to', 'attention', 'customer_id'],
             'date_fields': ['reporting_date', 'created_at'],
             'location_fields': ['city_location', 'location'],
             'sample_fields': ['sample_id', 'lab_report_no', 'invoice_bill_no'],
             'report_type': 'na'
         },
     ]
     
     for config in search_configs:
         _m = config['model']
         _heavy=[f for f in ('pdf_image_1','pdf_image_2','pdf_image_3','pdf_image_4','pdf_image_5','pdf_image_6') if f in [x.name for x in _m._meta.get_fields()]]
         queryset = _m.objects.defer(*_heavy) if _heavy else _m.objects.all()
         q_objects = Q()
         has_filters = False
         
         # Search by name (report_to or attention)
         if name_input:
             name_q = Q()
             for field in config['name_fields']:
                 if hasattr(config['model'], field):
                     name_q |= Q(**{f"{field}__icontains": name_input})
             if name_q:
                 q_objects &= name_q
                 has_filters = True
         
         # Date range filter
         if from_date or to_date:
             date_q = Q()
             date_fields = config['date_fields']
         
             for field in date_fields:
                 if hasattr(config['model'], field):
                     if from_date and to_date:
                         date_q |= Q(**{
                             f"{field}__range": [from_date, to_date]
                         })
                     elif from_date:
                         date_q |= Q(**{
                             f"{field}__gte": from_date
                         })
                     elif to_date:
                         date_q |= Q(**{
                             f"{field}__lte": to_date
                         })
         
             if date_q:
                 q_objects &= date_q
                 has_filters = True
         
         # Search by location
         if location_search:
             location_q = Q()
             for field in config['location_fields']:
                 if hasattr(config['model'], field):
                     location_q |= Q(**{f"{field}__icontains": location_search})
             if location_q:
                 q_objects &= location_q
                 has_filters = True
         
         # Search by sample ID
         if sample_search:
             sample_q = Q()
             for field in config['sample_fields']:
                 if hasattr(config['model'], field):
                     sample_q |= Q(**{f"{field}__icontains": sample_search})
             if sample_q:
                 q_objects &= sample_q
                 has_filters = True
         
         # If no filters provided, return all results (optional)
         if not has_filters and not any([name_input, from_date, to_date, location_search, sample_search]):
             has_filters = True  # Return all
         
         # Apply filters and add to results
         if has_filters:
             try:
                 if has_filters:
                     filtered_results = queryset.filter(q_objects)
                 else:
                     filtered_results = queryset.all()
                     
                 for item in filtered_results:
                     # Add report_type to each item for template identification
                     item.report_type = config['report_type']
                 all_results.extend(list(filtered_results))
             except Exception as e:
                 logger.error(f"Error searching {config['model'].__name__}: {str(e)}")
                 continue
     
     # Sort by reporting_date (most recent first) - handle None values
     all_results.sort(key=lambda x: getattr(x, 'reporting_date', '') or '', reverse=True)
     
     return all_results


def addLogging(request):
     if request.method=='POST':
          city_location = request.POST['city_location']
          sample_id = request.POST['sample_id']
          client_name = request.POST['client_name']
          address = request.POST['address']
          att_person = request.POST['att_person']
          email = request.POST['email']
          sample_nature = request.POST['sample_nature']
          rec_date = datetime.strptime(request.POST['rec_date'], '%Y-%m-%d').date()
          exp_date = datetime.strptime(request.POST['exp_date'], '%Y-%m-%d').date()
          rep_date = datetime.strptime(request.POST['rep_date'], '%Y-%m-%d').date()
          formatted_rec_date = rec_date.strftime('%d-%B-%Y')
          formatted_exp_date = exp_date.strftime('%d-%B-%Y')
          formatted_rep_date = rep_date.strftime('%d-%B-%Y')

          month = datetime.strptime(request.POST['month'], '%Y-%m-%d').date() if request.POST['month'] else None
          rec_by = request.POST['rec_by']
          remarks = request.POST['remarks']
          lab = request.POST['lab']
          issue_no = request.POST['issue_no']
          issue_date = request.POST['issue_date']
          issue = request.POST['issue']


          log = LoggingSheet(city_location=city_location,sample_id=sample_id,client_name=client_name,
                              address=address,att_person=att_person,sample_nature = sample_nature,month=month,
                              email=email,rec_date=formatted_rec_date,exp_date=formatted_exp_date,rep_date=formatted_rep_date,rec_by=rec_by,remarks=remarks,
                              lab=lab,issue_date=issue_date,issue_no=issue_no,issue=issue)

          log.save()
          user = request.user
          action = f'Logging Sheet created by {user.username}'
          # AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Sample successfully added!')
          id = (LoggingSheet.objects.last()).id
          if "submit_and_view" in request.POST:
               return redirect(to='loggingSheet')
          if "submit_and_new" in request.POST:
               
               return render(request, "addLogging.html")  
     return render(request,"addLogging.html")

@login_required(login_url="/login")   
def nav(request):
     return render(request,'nav.html')

@login_required(login_url="/login") 
def certificate(request):
    if request.GET.get("clear"):
        request.session.pop("cert_search_params", None)
        return HttpResponseRedirect(request.path)
    # Check if search parameters are present
    if request.GET.get('nameInput') or request.GET.get('from_date') or request.GET.get('locationSearch') or request.GET.get('sampleSearch'):
        name_input = request.GET.get('nameInput', '').strip()
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        location_search = request.GET.get('locationSearch', '').strip()
        sample_search = request.GET.get('sampleSearch', '').strip()
        
        # Store in session to persist across pagination
        request.session['cert_search_params'] = {
            'name_input': name_input,
            'from_date': from_date,
            'to_date': to_date,
            'location_search': location_search,
            'sample_search': sample_search,
        }
        
        # Search across all certificate models
        all_certificates = search_all_certificates(
            name_input, from_date, to_date, location_search, sample_search
        )
        
        # Paginate results
        all_certificates = _by_date_desc(all_certificates, ('date',))
        paginator = Paginator(all_certificates, 200)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'data': page_obj,
            'search_performed': True,
            'total_results': paginator.count,
            'name_input': name_input,
            'from_date': from_date,
            'to_date': to_date,
            'location_search': location_search,
            'sample_search': sample_search,
        }
        return render(request, 'certificate.html', context)
    
    # For pagination clicks - retrieve search params from session
    if request.GET.get('page') and request.session.get('cert_search_params'):
        params = request.session['cert_search_params']
        all_certificates = search_all_certificates(
            params.get('name_input', ''),
            params.get('from_date', ''),
            params.get('to_date', ''),
            params.get('location_search', ''),
            params.get('sample_search', '')
        )
        all_certificates = _by_date_desc(all_certificates, ('date',))
        paginator = Paginator(all_certificates, 200)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'data': page_obj,
            'search_performed': True,
            'total_results': paginator.count,
            'name_input': params.get('name_input', ''),
            'from_date': params.get('from_date', ''),
            'to_date': params.get('to_date', ''),
            'location_search': params.get('location_search', ''),
            'sample_search': params.get('sample_search', ''),
        }
        return render(request, 'certificate.html', context)
    
    # No search - show all certificates (paginated)
    calib = Calibration.objects.none()
    insp = Inspection.objects.none()
    verif = Verification.objects.none()
    
    all_certificates = list(calib) + list(insp) + list(verif)
    
    # Sort by date (most recent first)
    all_certificates.sort(key=lambda x: getattr(x, 'date', '') or '', reverse=True)
    
    paginator = Paginator(all_certificates, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'data': page_obj,
        'search_performed': False,
        'total_results': paginator.count,
    }
    return render(request, 'certificate.html', context)

def search_all_certificates(name_input, from_date, to_date, location_search, sample_search):
    all_results = []
    search_configs = [
        {
            'model': Calibration,
            'name_fields': ['client'],
            'date_fields': ['date'],
            'location_fields': ['city_location'],
            'sample_fields': ['cert_num'],
            'cert_type': 'calib'
        },
        {
            'model': Inspection,
            'name_fields': ['client'],
            'date_fields': ['date'],
            'location_fields': ['city_location'],
            'sample_fields': ['cert_num'],
            'cert_type': 'insp'
        },
        {
            'model': Verification,
            'name_fields': ['client'],
            'date_fields': ['date'],
            'location_fields': ['city_location'],
            'sample_fields': ['cert_num'],
            'cert_type': 'verif'
        },
    ]
    
    for config in search_configs:
        queryset = config['model'].objects.all()
        q_objects = Q()
        has_filters = False
        
        # Search by name (client)
        if name_input:
            name_q = Q()
            for field in config['name_fields']:
                if hasattr(config['model'], field):
                    name_q |= Q(**{f"{field}__icontains": name_input})
            if name_q:
                q_objects &= name_q
                has_filters = True
        
        # Date range applied in Python after collection (text dates)
        if from_date or to_date:
            has_filters = True

        # Search by location
        if location_search:
            location_q = Q()
            for field in config['location_fields']:
                if hasattr(config['model'], field):
                    location_q |= Q(**{f"{field}__icontains": location_search})
            if location_q:
                q_objects &= location_q
                has_filters = True
        
        # Search by certificate number
        if sample_search:
            sample_q = Q()
            for field in config['sample_fields']:
                if hasattr(config['model'], field):
                    sample_q |= Q(**{f"{field}__icontains": sample_search})
            if sample_q:
                q_objects &= sample_q
                has_filters = True
        
        # Apply filters and add to results
        if has_filters:
            try:
                filtered_results = queryset.filter(q_objects)
                for item in filtered_results:
                    item.cert_type = config['cert_type']
                all_results.extend(list(filtered_results))
            except Exception as e:
                logger.error(f"Error searching {config['model'].__name__}: {str(e)}")
                continue
    
    # Sort by date (most recent first)
    if from_date or to_date:
        _f = _parse_date(from_date) if from_date else None
        _t = _parse_date(to_date) if to_date else None
        _kept = []
        for _o in all_results:
            _d = _parse_date(str(getattr(_o, 'date', '') or ''))
            if _d and (_f is None or _d >= _f) and (_t is None or _d <= _t):
                _kept.append(_o)
        all_results = _kept
    all_results = _by_date_desc(all_results, ('date',))
    
    return all_results

@login_required(login_url="/login")
def deleteDrinkingWaterList(request,pk):
     drinkingWaterList = DrinkingWaterForm.objects.get(id=pk)
     drinkingWaterList.delete()
     user = request.user
     action = f'Drinking Water Form {drinkingWaterList.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("drinkWaterList")

@login_required(login_url="/login")
def editDrinkingWaterList(request,pk):
     drinkingWaterList = DrinkingWaterForm.objects.get(id=pk)
     drinkingWaterList.extra_field = json.loads(drinkingWaterList.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json', log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(drinkingWaterList, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     context = {
         'list': drinkingWaterList,
         'pdf_image_1': image_previews.get('pdf_image_1'),
         'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),
         'customers': log,
         'signs': signs
     }
     # print(editableForm.id)
     return render(request,"drinkingWaterEdit.html",context)

@login_required(login_url="/login")
def editDrinkingWaterListRecord(request,pk):
     updatedata = DrinkingWaterForm.objects.get(id=pk)
     if request.method == 'POST':
          updatedata.location = request.POST['location']
          industry_id = request.POST.get('industry')
          updatedata.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          updatedata.lab_report_no = request.POST['lab_report_no']
          updatedata.invoice_bill_no = request.POST['invoice_bill_no']
          updatedata.reporting_date = request.POST['reporting_date']
          updatedata.report_to = request.POST['reporting_to']
          updatedata.address = request.POST['address']
          updatedata.attention = request.POST['attention']
          updatedata.email = request.POST['email']
          updatedata.customer_id = request.POST.get('customer_id')
          updatedata.sample_id = request.POST['sample_id']
          updatedata.sample_collection_date = request.POST['collection_date']
          updatedata.sample_description = request.POST['sample_description']
          updatedata.sample_type = request.POST['sample_type']
          updatedata.sample_collected_by = request.POST['sample_collected_by']
          updatedata.date_of_analysis_from = request.POST['date_of_analysis_from']
          updatedata.date_of_analysis_to = request.POST['date_of_analysis_to']
          updatedata.test_description = request.POST['test_description']
          updatedata.select = request.POST.get('water-select')
          updatedata.water_sr1 = request.POST['water_sr1']
          updatedata.water_sr2 = request.POST['water_sr2']
          updatedata.water_sr3 = request.POST['water_sr3']
          updatedata.water_sr4 = request.POST['water_sr4']
          updatedata.water_sr5 = request.POST['water_sr5']
          updatedata.water_sr6 = request.POST['water_sr6']
          updatedata.water_sr7 = request.POST['water_sr7']
          updatedata.water_sr8 = request.POST['water_sr8']
          updatedata.water_sr9 = request.POST['water_sr9']
          updatedata.water_sr10 = request.POST['water_sr10']
          updatedata.water_sr11 = request.POST['water_sr11']
          updatedata.water_sr12 = request.POST['water_sr12']
          updatedata.water_sr13 = request.POST['water_sr13']
          updatedata.water_sr14 = request.POST['water_sr14']
          updatedata.water_sr15 = request.POST['water_sr15']
          updatedata.water_sr16 = request.POST['water_sr16']
          updatedata.water_sr17 = request.POST['water_sr17']
          updatedata.water_sr18 = request.POST['water_sr18']
          updatedata.water_sr19 = request.POST['water_sr19']
          updatedata.water_sr20 = request.POST['water_sr20']
          updatedata.water_sr21 = request.POST['water_sr21']
          updatedata.water_sr22 = request.POST['water_sr22']
          updatedata.water_sr23 = request.POST['water_sr23']
          updatedata.water_sr24 = request.POST['water_sr24']
          updatedata.water_sr25 = request.POST['water_sr25']
          updatedata.water_sr26 = request.POST['water_sr26']
          updatedata.water_sr27 = request.POST['water_sr27']
          updatedata.water_sr28 = request.POST['water_sr28']
          updatedata.water_sr29 = request.POST['water_sr29']
          updatedata.water_sr30 = request.POST['water_sr30']
          updatedata.water_sr31 = request.POST['water_sr31']
          updatedata.water_sr32 = request.POST['water_sr32']
          updatedata.method_1 = request.POST['method_1']
          updatedata.method_2 = request.POST['method_2']
          updatedata.method_3 = request.POST['method_3']
          updatedata.method_4 = request.POST['method_4']
          updatedata.method_5 = request.POST['method_5']
          updatedata.method_6 = request.POST['method_6']
          updatedata.method_7 = request.POST['method_7']
          updatedata.method_8 = request.POST['method_8']
          updatedata.method_9 = request.POST['method_9']
          updatedata.method_10 = request.POST['method_10']
          updatedata.method_11 = request.POST['method_11']
          updatedata.method_12 = request.POST['method_12']
          updatedata.method_13 = request.POST['method_13']
          updatedata.method_14 = request.POST['method_14']
          updatedata.method_15 = request.POST['method_15']
          updatedata.method_16 = request.POST['method_16']
          updatedata.method_17 = request.POST['method_17']
          updatedata.method_18 = request.POST['method_18']
          updatedata.method_19 = request.POST['method_19']
          updatedata.method_20 = request.POST['method_20']
          updatedata.method_21 = request.POST['method_21']
          updatedata.method_22 = request.POST['method_22']
          updatedata.method_23 = request.POST['method_23']
          updatedata.method_24 = request.POST['method_24']
          updatedata.method_25 = request.POST['method_25']
          updatedata.method_26 = request.POST['method_26']
          updatedata.method_27 = request.POST['method_27']
          updatedata.method_28 = request.POST['method_28']
          updatedata.method_29 = request.POST['method_29']
          updatedata.method_30 = request.POST['method_30']
          updatedata.method_31 = request.POST['method_31']
          updatedata.method_32 = request.POST['method_32']
          updatedata.legend_1 = request.POST['legend-1']
          updatedata.legend_2 = request.POST['legend-2']
          updatedata.legend_3 = request.POST['legend-3']
          updatedata.legend_4 = request.POST['legend-4']
          updatedata.legend_5 = request.POST['legend-5']
          updatedata.legend_6 = request.POST['legend-6']
          updatedata.legend_7 = request.POST['legend-7']
          updatedata.legend_8 = request.POST['legend-8']
          updatedata.legend_9 = request.POST['legend-9']
          updatedata.legend_10 = request.POST['legend-10']
          updatedata.legend_11 = request.POST['legend-11']
          updatedata.edit_note = request.POST['edit-note']
          updatedata.custom_legend = request.POST['custom-legend']
          updatedata.doc_controll_1 = request.POST['doc-con-1']
          updatedata.doc_controll_2 = request.POST['doc-con-2']
          updatedata.doc_controll_3 = request.POST['doc-con-3']
          # updatedata.analyzed_by = request.FILES["analyzedby" ]
          # updatedata.reviewed_by = request.FILES["reviewedby" ]
          # updatedata.approved_by = request.FILES["approvedby" ]
          # updatedata.approved_by1 = request.FILES["approvedby1" ]
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          updatedata.analyst_signature = analyst_sign
          updatedata.assistant_manager_signature = review_sign
          updatedata.lab_manager_signature = approved_sign
          
           
          
          updatedata.extra_field = json.loads(request.POST["extra_field"])
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameters = request.POST.getlist('parameters[]')[i]
               methods = request.POST.getlist('methods[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]

               updatedata.extra_field.append({
                    "sr": sr,
                    "parameters": parameters,
                    "methods": methods,
                    "unit": unit,
                    "result": result,
                    "limit": limit,
               })
          
          updatedata.extra_field = json.dumps(updatedata.extra_field)
          updatedata.custominput = request.POST['custominput'] 
          updatedata.custominput1 = request.POST['custominput1'] 
          updatedata.custominput2 = request.POST['custominput2'] 
          updatedata.custominput3 = request.POST['custominput3'] 
          updatedata.custominput4 = request.POST['custominput4'] 
          updatedata.custominput5 = request.POST['custominput5'] 
          updatedata.custominput6 = request.POST['custominput6'] 
          updatedata.custominput7 = request.POST['custominput7'] 
          updatedata.custominput8 = request.POST['custominput8'] 
          updatedata.custominput9 = request.POST['custominput9'] 
          updatedata.custominput10 = request.POST['custominput10'] 
          updatedata.custominput11 = request.POST['custominput11'] 
          updatedata.custominput12 = request.POST['custominput12'] 
          updatedata.custominput13 = request.POST['custominput13'] 
          updatedata.custominput14 = request.POST['custominput14'] 
          updatedata.custominput15 = request.POST['custominput15'] 
          updatedata.custominput16 = request.POST['custominput16'] 
          updatedata.custominput17 = request.POST['custominput17'] 
          updatedata.custominput18 = request.POST['custominput18'] 
          updatedata.custominput19 = request.POST['custominput19'] 
          updatedata.custominput20 = request.POST['custominput20'] 
          updatedata.custominput21 = request.POST['custominput21'] 
          updatedata.custominput22 = request.POST['custominput22'] 
          updatedata.custominput23 = request.POST['custominput23'] 
          updatedata.custominput24 = request.POST['custominput24'] 
          updatedata.custominput25 = request.POST['custominput25'] 
          updatedata.custominput26 = request.POST['custominput26'] 
          updatedata.custominput27 = request.POST['custominput27'] 
          updatedata.custominput28 = request.POST['custominput28'] 
          updatedata.custominput29 = request.POST['custominput29'] 
          updatedata.custominput30 = request.POST['custominput30'] 
          updatedata.custominput31 = request.POST['custominput31'] 
          updatedata.custominput32 = request.POST['custominput32']
          updatedata.city_location = request.POST['city_location']
          updatedata.pdf_heading=request.POST.get('pdf_heading')
          updatedata.created_by = request.user
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(updatedata, image_key, '')
                    setattr(updatedata, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(updatedata, image_key, base64_encoded)
                         setattr(updatedata, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(updatedata, desc_key, description)

          
          



          updatedata.save()
          user = request.user
          if updatedata.customer_id:
               LoggingSheet.objects.filter(id=updatedata.customer_id).update(rep_date=updatedata.reporting_date)
          action = f'Drinking Water Form {updatedata.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = updatedata.id
          if "submit_and_view" in request.POST:
               url = f'/view-form/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('drinkWaterList')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     
     return render(request,"drinkWaterList.html")          



def drinkWaterReport(request, pk):
    try:
        # Retrieve the water report instance
        waterReport = DrinkingWaterForm.objects.get(id=pk)
    except DrinkingWaterForm.DoesNotExist:
        raise Http404("Drinking water report not found.")
    
    current_url = request.build_absolute_uri()
    
    # Process extra_field safely
    try:
        waterReport.extra_field = waterReport.extra_field.replace("'", "\"")
        waterReport.extra_field = json.loads(waterReport.extra_field)
    except (ValueError, AttributeError):
        waterReport.extra_field = {}

    # Generate a unique file name for the QR code
    qr_filename = f"qr_{waterReport.lab_report_no}.png"
    qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)

    # Create and save the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=6,
    )
    qr.add_data(current_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_file_path)
    qr_relative_path = f"{settings.MEDIA_URL}{qr_filename}"

    # Prepare context
    context = {
        'list': waterReport,
        'qr': qr_relative_path,
        'logo':logo
    }

    # Return response or render template here (not provided in the function)
    return render(request,"drinkingWaterReport.html",context)  # Replace with appropriate render function

@login_required(login_url="/login")
def deleteGaseousList(request,pk):
     gaseous_Emission = GaseousEmissionForm.objects.get(id=pk)
     gaseous_Emission.delete()
     user = request.user
     action = f'Gaseous Emission Form {gaseous_Emission.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')

     return redirect('gaseousEmissionList')

     
@login_required(login_url="/login")
def editGaseousList(request,pk):
     gaseous_Emission =  GaseousEmissionForm.objects.get(id=pk)
     gaseous_Emission.extra_field = gaseous_Emission.extra_field.replace("'", "\"")
     gaseous_Emission.extra_field = json.loads(gaseous_Emission.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(gaseous_Emission, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     
     context = {'data':gaseous_Emission,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"gaseousEmissionEditForm.html",context)


@login_required(login_url="/login")
def updateGaseousRecord(request,pk):
     update_data = GaseousEmissionForm.objects.get(id=pk)
     if request.method=='POST':
          industry_id = request.POST.get('industry')
          update_data.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          update_data.location = request.POST['location']
          update_data.lab_report_no = request.POST['GasEm-lab_report_no']
          update_data.invoice_bill_no = request.POST['GasEm-invoice-bill-no']
          update_data.reporting_date = request.POST['GasEm-reporting-date']
          update_data.report_to = request.POST['GasEm-report-to']
          update_data.address = request.POST['GasEm-address']
          update_data.attention = request.POST['GasEm-attention']
          update_data.email = request.POST['GasEm-email']
          update_data.sample_id = request.POST['GasEm-test-id']
          update_data.GaseEm_test_perf_date = request.POST['GasEm-test-perf-date']
          update_data.GaseEm_test_type = request.POST['GasEm-test-type']
          update_data.GasEm_test_type_extra = request.POST['GasEm-test-type-extra']
          update_data.GaseEm_test_perf_by = request.POST['GasEm-test-perf-by']
          update_data.GasEm_test_desc = request.POST['GasEm-test-desc']
          update_data.GaseEm_types = request.POST.get('GasEm-type')
          update_data.GaseEm_select = request.POST.get('select')
          update_data.GaseEm_sr1 = request.POST['GasEm-sr1']
          update_data.GaseEm_sr2 = request.POST['GasEm-sr2']
          update_data.GaseEm_sr3 = request.POST['GasEm-sr3']
          update_data.GaseEm_sr4 = request.POST['GasEm-sr4']
          update_data.GaseEm_sr5 = request.POST['GasEm-sr5']
          update_data.GaseEm_sr6 = request.POST['GasEm-sr6']
          update_data.GaseEm_sr7 = request.POST['GasEm-sr7']
          update_data.GaseEm_sr8 = request.POST['GasEm-sr8']
          update_data.GaseEm_sr9 = request.POST['GasEm-sr9']
          update_data.GaseEm_sr10 = request.POST['GasEm-sr10']
          update_data.GaseEm_sr11 = request.POST['GasEm-sr11']
          update_data.GaseEm_sr12 = request.POST['GasEm-sr12']
          update_data.GaseEm_sr13 = request.POST['GasEm-sr13']
          update_data.GaseEm_sr14 = request.POST['GasEm-sr14']
          update_data.GaseEm_sr15 = request.POST['GasEm-sr15']
          update_data.GaseEm_sr16 = request.POST['GasEm-sr16']
          update_data.GaseEm_sr17 = request.POST['GasEm-sr17']
          update_data.GaseEm_sr18 = request.POST['GasEm-sr18']
          update_data.GaseEm_sr19 = request.POST['GasEm-sr19']
          update_data.GaseEm_sr20 = request.POST['GasEm-sr20']
          update_data.GaseEm_sr21 = request.POST['GasEm-sr21']
          update_data.GaseEm_sr22 = request.POST['GasEm-sr22']
          update_data.GaseEm_legend_1 = request.POST['GasEm-legend-1']
          update_data.GaseEm_legend_2 = request.POST['GasEm-legend-2']
          update_data.GaseEm_legend_3 = request.POST['GasEm-legend-3']
          update_data.GaseEm_legend_4 = request.POST['GasEm-legend-4']
          update_data.GaseEm_legend_5 = request.POST['GasEm-legend-5']
          update_data.GaseEm_legend_6 = request.POST['GasEm-legend-6']
          update_data.GaseEm_legend_7 = request.POST['GasEm-legend-7']
          update_data.GaseEm_legend_8 = request.POST['GasEm-legend-8']
          update_data.GaseEm_legend_9 = request.POST['GasEm-legend-9']
          update_data.GaseEm_legend_10 = request.POST['GasEm-legend-10']
          update_data.GaseEm_legend_11 = request.POST['GasEm-legend-11']
          update_data.GaseEm_edit_note = request.POST['GasEm-editnote']
          update_data.GaseEm_custom_legend = request.POST['GasEm-custom-legend']
          update_data.GaseEm_doc_con_1 = request.POST['GasEm-doc1']
          update_data.GaseEm_doc_con_2 = request.POST['GasEm-doc2']
          update_data.GaseEm_doc_con_3 = request.POST['GasEm-doc3']
          update_data.created_by = request.user
          # update_data.GaseEm_analyzed_by = request.FILES["GasEm-analyzedby" ]
          # update_data.GaseEm_reviewd_by = request.FILES["GasEm-reviewedby" ]
          # update_data.GaseEm_approved_by = request.FILES["GasEm-approvedby" ]
          # update_data.GaseEm_approved_by1 = request.FILES["GasEm-approvedby1" ]
          update_data.extra_field = json.loads(request.POST['extra_field'])
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          update_data.analyst_signature = analyst_sign
          update_data.assistant_manager_signature = review_sign
          update_data.lab_manager_signature = approved_sign
          
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameters = request.POST.getlist('parameters[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               update_data.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        

          update_data.city_location =request.POST['city_location']  
          
          
          
                       
            

          
          update_data.extra_field = json.dumps(update_data.extra_field)
          update_data.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(update_data, image_key, '')
                    setattr(update_data, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(update_data, image_key, base64_encoded)
                         setattr(update_data, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(update_data, desc_key, description)

          update_data.save()
          user = request.user
          action = f'Gaseous Emission Form {update_data.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = update_data.id
          if "submit_and_view" in request.POST:
               url = f'/GaseousForm-view-form/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('gaseousEmissionList')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return redirect('gaseousEmissionList')

def calculate_leq(start_time, end_time, interval, table_data):
    fmt = "%I:%M %p" if any(x in str(start_time).upper() for x in ["AM", "PM"]) else "%H:%M"

    def parse_time(t):
        if isinstance(t, datetime):
            return t
        elif isinstance(t, time):
            return datetime.combine(datetime.today(), t)
        elif isinstance(t, str):
            return datetime.strptime(t.strip(), fmt)
        else:
            raise ValueError("Unsupported time format")

    start = parse_time(start_time)
    end = parse_time(end_time)
    total_seconds = (end - start).total_seconds()
    total_minutes = total_seconds / 60
    total_hours = total_seconds / 3600

    # Interval in minutes
    if interval == "15mins":
        ti = 15
    elif interval == "30mins":
        ti = 30
    else:
        ti = 60

    # Extract Li values
    li_values = [float(row["result"]) for row in table_data if row.get("result")]
    n = len(li_values)

    if not li_values:
        return 0

    # ✅ Recalculate total duration based on actual number of readings
    # because sometimes the number of intervals defines total time
    T = n * ti  # total time in minutes (same unit as ti)

    numerator = sum(ti * (10 ** (0.1 * Li)) for Li in li_values)
    leq = 10 * math.log10(numerator / T)

    return round(leq, 4)  


def save_client_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client, created = ClientDetails.objects.update_or_create(
                company_name=data.get('company_name'),
                defaults={
                    'address': data.get('address', ''),
                    'contact_person': data.get('contact_person', ''),
                    'contact_number': data.get('contact_number', ''),
                    'email': data.get('email', ''),
                    'po_reference': data.get('po_reference', ''),  # Save main PO reference
                    'custom_po_fields': data.get('custom_po_fields', []),  # Save custom PO fields
                }
            )
            return JsonResponse({'success': True, 'created': created})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An internal error occurred. Please try again or contact the administrator.'})


def get_client_details(request):
    if request.method == 'GET':
        company_name = request.GET.get('company_name')
        try:
            client = ClientDetails.objects.get(company_name=company_name)
            data = {
                'success': True,
                'address': client.address,
                'contact_person': client.contact_person,
                'contact_number': client.contact_number,
                'email': client.email,
                'po_reference': client.po_reference or '',  # Send main PO reference
                'custom_po_fields': client.custom_po_fields or [],  # Send custom PO fields
            }
        except ClientDetails.DoesNotExist:
            data = {'success': False, 'error': 'Company not found'}
        
        return JsonResponse(data)


def get_all_companies(request):
    companies = ClientDetails.objects.values_list('company_name', flat=True)
    return JsonResponse({'companies': list(companies)})
     
def update_job_completion(request, pk):
    try:
        # Get the existing job
        job = get_object_or_404(JobCompletionForm, id=pk)
        
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Get form data
        company_name = data.get('company_name')
        address = data.get('address')
        contact_person = data.get('contact_person')
        contact_number = data.get('contact_number')
        email = data.get('email')
        invoice_ref = data.get('invoice_ref')
        po_reference = data.get('po_reference')
        custom_po_fields = data.get('custom_po_fields', [])
        representative_sign = data.get('sign')
        receiver_name = data.get('receiver_name')
        location = data.get('location')
        
        # Get or create company
        company, created = ClientDetails.objects.update_or_create(
            company_name=company_name,
            defaults={
                'address': address,
                'contact_person': contact_person,
                'contact_number': contact_number,
                'email': email,
                'po_reference': po_reference,
                'custom_po_fields': custom_po_fields,
            }
        )
        
        # Collect service details
        service_details = []
        services = data.get('services', [])
        
        for idx, service in enumerate(services, 1):
            if service.get('service'):
                service_details.append({
                    'sr_no': idx,
                    'service': service.get('service', ''),
                    'site_location': service.get('site_location', ''),
                    'qty': int(service.get('qty', 0)),
                    'date': service.get('date', '')
                })
        
        # Update the job
        job.company = company
        job.invoice_ref = invoice_ref
        job.po_reference = po_reference
        job.custom_po_fields = custom_po_fields
        job.service_details = service_details
        job.service_receiver = receiver_name
        job.representative_sign = representative_sign
        job.location = location
        job.save()
        
        # Generate PDF
        return JsonResponse({
                'success': True,
                'job_id': job.id,
                'job_number': job.job_number,
                'message': 'Job created successfully'
            })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': 'An internal error occurred. Please try again or contact the administrator.'
        }, status=400)


def clone_job_completion(request, pk):
    """Clone existing job completion - POST request"""
    try:
        # Get the original job
        original_job = get_object_or_404(JobCompletionForm, id=pk)
        
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Get form data
        company_name = data.get('company_name')
        address = data.get('address')
        contact_person = data.get('contact_person')
        contact_number = data.get('contact_number')
        email = data.get('email')
        invoice_ref = data.get('invoice_ref')
        po_reference = data.get('po_reference')
        custom_po_fields = data.get('custom_po_fields', [])
        representative_sign = data.get('sign')
        receiver_name = data.get('receiver_name')
        location = data.get('location')
        
        # Get or create company
        company, created = ClientDetails.objects.update_or_create(
            company_name=company_name,
            defaults={
                'address': address,
                'contact_person': contact_person,
                'contact_number': contact_number,
                'email': email,
                'po_reference': po_reference,
                'custom_po_fields': custom_po_fields,
            }
        )
        
        # Collect service details
        service_details = []
        services = data.get('services', [])
        
        for idx, service in enumerate(services, 1):
            if service.get('service'):
                service_details.append({
                    'sr_no': idx,
                    'service': service.get('service', ''),
                    'site_location': service.get('site_location', ''),
                    'qty': int(service.get('qty', 0)),
                    'date': service.get('date', '')
                })
        
        # Create new job (clone) - this will auto-generate new job number
        new_job = JobCompletionForm.objects.create(
            company=company,
            invoice_ref=invoice_ref,
            po_reference=po_reference,
            custom_po_fields=custom_po_fields,
            service_details=service_details,
            service_receiver=receiver_name,
            representative_sign=representative_sign,
            location=location,
        )
        
        # Generate PDF
        return JsonResponse({
                'success': True,
                'job_id': new_job.id,
                'job_number': new_job.job_number,
                'message': 'Job created successfully'
            })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': 'An internal error occurred. Please try again or contact the administrator.'
        }, status=400)

# --- etal bulk PDF download (added 12-07-2026) ---
@login_required(login_url="/login")
def etal_bulk_pdf(request):
    """Merge the selected list records into one downloadable PDF."""
    import json as _json
    from django.http import JsonResponse as _JR, HttpResponse as _HR
    if request.method != 'POST':
        return _JR({'error': 'POST required'}, status=405)
    try:
        model_key = (request.POST.get('model') or '').strip()
        ids = [int(i) for i in _json.loads(request.POST.get('ids') or '[]')][:60]
    except Exception:
        return _JR({'error': 'Bad request'}, status=400)
    if not ids:
        return _JR({'error': 'No records selected'}, status=400)
    try:
        if model_key in ('calib', 'insp', 'verif'):
            from EnviTechAlApp.merger_cert import get_certificate_mapping, merge_pdfs_cert
            model = get_certificate_mapping()[model_key][0]
            objs = {o.id: o for o in model.objects.filter(id__in=ids)}
            nums = [getattr(objs[i], 'cert_num', None) for i in ids if i in objs]
            nums = [n for n in nums if n]
            if not nums:
                return _JR({'error': 'No matching certificates found'}, status=404)
            merged = merge_pdfs_cert(nums, request)
        elif model_key in ('dtx', 'nm'):
            # etal-dtx-direct: id-based merge (lab_report_no not unique here)
            from io import BytesIO as _BIO
            from PyPDF2 import PdfReader as _PR, PdfWriter as _PW
            from EnviTechAlApp.merger_pdf import compress_pdf as _cmp
            if model_key == 'dtx':
                from detox.models import Detox as _M
                from detox.views import detox_pdf as _fn
            else:
                _M, _fn = NoiseMonitoring, noiseMonitoring_print
            writer = _PW(); added = 0
            for i in ids:
                obj = _M.objects.filter(id=i).first()
                if not obj:
                    continue
                try:
                    resp = _fn(request, obj.id)
                    content = getattr(resp, 'content', b'')
                    if not content.startswith(b'%PDF'):
                        continue
                    reader = _PR(_BIO(content))
                    if reader.is_encrypted:
                        reader.decrypt('1234')
                    for pg in reader.pages:
                        writer.add_page(pg)
                    added += 1
                except Exception:
                    continue
            if not added:
                return _JR({'error': 'No PDFs could be generated for the selected records'}, status=500)
            raw = _BIO(); writer.write(raw); raw.seek(0)
            buf = _cmp(raw, target_mb=5.0); buf.seek(0)
            er = _PR(buf); ew = _PW()
            for pg in er.pages:
                ew.add_page(pg)
            ew.encrypt(user_password='1234', owner_password='karachi123', use_128bit=False)
            merged = _BIO(); ew.write(merged); merged.seek(0)
        else:
            from EnviTechAlApp.merger_pdf import get_report_mapping, merge_pdfs
            mapping = get_report_mapping()
            if model_key not in mapping:
                return _JR({'error': 'Bulk PDF is not available for this list'}, status=400)
            model = mapping[model_key][0]
            objs = {o.id: o for o in model.objects.filter(id__in=ids)}
            nos = [getattr(objs[i], 'lab_report_no', None) for i in ids if i in objs]
            nos = [n for n in nos if n]
            if not nos:
                return _JR({'error': 'Selected records have no report numbers'}, status=404)
            merged = merge_pdfs(nos, request)
        data = merged.read()
        if not data.startswith(b'%PDF'):
            return _JR({'error': 'PDF generation failed'}, status=500)
        response = _HR(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="EnviTechAL_merged.pdf"'
        return response
    except Exception:
        return _JR({'error': 'PDF generation failed for one or more selected records'}, status=500)


# --- Phase 1 approval endpoints (12-07-2026) ---
@login_required(login_url="/login")
def etal_bulk_approve(request):
    """Approve or unapprove selected records (superuser only)."""
    import json as _json
    from django.http import JsonResponse as _JR
    if request.method != 'POST':
        return _JR({'error': 'POST required'}, status=405)
    if not request.user.is_superuser:
        return _JR({'error': 'Only an administrator can approve or unapprove records'}, status=403)
    try:
        model_key = (request.POST.get('model') or '').strip()
        action = (request.POST.get('action') or 'approve').strip()
        ids = [int(i) for i in _json.loads(request.POST.get('ids') or '[]')][:200]
    except Exception:
        return _JR({'error': 'Bad request'}, status=400)
    from EnviTechAlApp.approval import MODEL_KEYS
    from EnviTechAlApp.models import ApprovalStatus
    if model_key not in set(MODEL_KEYS.values()) or not ids:
        return _JR({'error': 'Approval is not available for this list'}, status=400)
    if action == 'approve':
        for i in ids:
            ApprovalStatus.objects.get_or_create(model_key=model_key, record_id=i,
                                                 defaults={'approved_by': request.user})
        return _JR({'ok': True, 'approved': len(ids)})
    n, _d = ApprovalStatus.objects.filter(model_key=model_key, record_id__in=ids).delete()
    return _JR({'ok': True, 'unapproved': n})


@login_required(login_url="/login")
def etal_approval_state(request):
    import json as _json
    from django.http import JsonResponse as _JR
    from EnviTechAlApp.models import ApprovalStatus
    model_key = (request.GET.get('model') or '').strip()
    try:
        ids = [int(i) for i in _json.loads(request.GET.get('ids') or '[]')][:500]
    except Exception:
        return _JR({'approved': []})
    rows = ApprovalStatus.objects.filter(model_key=model_key, record_id__in=ids).values_list('record_id', flat=True)
    return _JR({'approved': list(rows)})

__all__ = [
    'compress_image',
    'get_client_ip',
    'userlogin',
    'custom_500',
    'home',
    'search_all_reports',
    'addLogging',
    'nav',
    'certificate',
    'search_all_certificates',
    'deleteDrinkingWaterList',
    'editDrinkingWaterList',
    'editDrinkingWaterListRecord',
    'drinkWaterReport',
    'deleteGaseousList',
    'editGaseousList',
    'updateGaseousRecord',
    'calculate_leq',
    'save_client_details',
    'get_client_details',
    'get_all_companies',
    'update_job_completion',
    'clone_job_completion',
    'etal_bulk_pdf',
    'etal_bulk_approve',
    'etal_approval_state',
]
