# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403



@login_required(login_url="/login")
def drinkingWaterForm(request):


     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['lab_report_no']
          invoice_bill_no = request.POST['invoice_bill_no']
          reporting_date = request.POST['reporting_date']
          reporting_to = request.POST['reporting_to']
          address = request.POST['address']
          attention = request.POST['attention']
          email = request.POST['email']
          sample_id = request.POST['sample_id']
          collection_date = request.POST['collection_date']
          sample_description = request.POST['sample_description']
          sample_type = request.POST['sample_type']
          sample_collected_by = request.POST['sample_collected_by']
          date_of_analysis_from = request.POST['date_of_analysis_from']
          date_of_analysis_to = request.POST['date_of_analysis_to']
          test_description = request.POST['test_description']
          select = request.POST.get('water-select')
          water_sr1 = request.POST['water_sr1']
          water_sr2 = request.POST['water_sr2']
          water_sr3 = request.POST['water_sr3']
          water_sr4 = request.POST['water_sr4']
          water_sr5 = request.POST['water_sr5']
          water_sr6 = request.POST['water_sr6']
          water_sr7 = request.POST['water_sr7']
          water_sr8 = request.POST['water_sr8']
          water_sr9 = request.POST['water_sr9']
          water_sr10 = request.POST['water_sr10']
          water_sr11 = request.POST['water_sr11']
          water_sr12 = request.POST['water_sr12']
          water_sr13 = request.POST['water_sr13']
          water_sr14 = request.POST['water_sr14']
          water_sr15 = request.POST['water_sr15']
          water_sr16 = request.POST['water_sr16']
          water_sr17 = request.POST['water_sr17']
          water_sr18 = request.POST['water_sr18']
          water_sr19 = request.POST['water_sr19']
          water_sr20 = request.POST['water_sr20']
          water_sr21 = request.POST['water_sr21']
          water_sr22 = request.POST['water_sr22']
          water_sr23 = request.POST['water_sr23']
          water_sr24 = request.POST['water_sr24']
          water_sr25 = request.POST['water_sr25']
          water_sr26 = request.POST['water_sr26']
          water_sr27 = request.POST['water_sr27']
          water_sr28 = request.POST['water_sr28']
          water_sr29 = request.POST['water_sr29']
          water_sr30 = request.POST['water_sr30']
          water_sr31 = request.POST['water_sr31']
          water_sr32 = request.POST['water_sr32']
          method_1 = request.POST['method_1']
          method_2 = request.POST['method_2']
          method_3 = request.POST['method_3']
          method_4 = request.POST['method_4']
          method_5 = request.POST['method_5']
          method_6 = request.POST['method_6']
          method_7 = request.POST['method_7']
          method_8 = request.POST['method_8']
          method_9 = request.POST['method_9']
          method_10 = request.POST['method_10']
          method_11 = request.POST['method_11']
          method_12 = request.POST['method_12']
          method_13 = request.POST['method_13']
          method_14 = request.POST['method_14']
          method_15 = request.POST['method_15']
          method_16 = request.POST['method_16']
          method_17 = request.POST['method_17']
          method_18 = request.POST['method_18']
          method_19 = request.POST['method_19']
          method_20 = request.POST['method_20']
          method_21 = request.POST['method_21']
          method_22 = request.POST['method_22']
          method_23 = request.POST['method_23']
          method_24 = request.POST['method_24']
          method_25 = request.POST['method_25']
          method_26 = request.POST['method_26']
          method_27 = request.POST['method_27']
          method_28 = request.POST['method_28']
          method_29 = request.POST['method_29']
          method_30 = request.POST['method_30']
          method_31 = request.POST['method_31']
          method_32 = request.POST['method_32']
          legend_1 = request.POST['legend-1']
          legend_2 = request.POST['legend-2']
          legend_3 = request.POST['legend-3']
          legend_4 = request.POST['legend-4']
          legend_5 = request.POST['legend-5']
          legend_6 = request.POST['legend-6']
          legend_7 = request.POST['legend-7']
          legend_8 = request.POST['legend-8']
          legend_9 = request.POST['legend-9']
          legend_10 = request.POST['legend-10']
          legend_11 = request.POST['legend-11']
          edit_note = request.POST['edit-note']
          custom_legend = request.POST['custom-legend']
          doc_con_1 = request.POST['doc-con-1']
          doc_con_2 = request.POST['doc-con-2']
          doc_con_3 = request.POST['doc-con-3']
          # analyzed_by_w = request.FILES["analyzedby" ]
          # reviewd_by_w = request.FILES["reviewedby" ]
          # approved_by_w = request.FILES["approvedby" ]
          # approved_by_w1 = request.FILES["approvedby1" ]
          extra_field = request.POST['extra_field'] 
          in_out = request.POST['in_out'] 
          custominput = request.POST['custominput'] 
          custominput1 = request.POST['custominput1'] 
          custominput2 = request.POST['custominput2'] 
          custominput3 = request.POST['custominput3'] 
          custominput4 = request.POST['custominput4'] 
          custominput5 = request.POST['custominput5'] 
          custominput6 = request.POST['custominput6'] 
          custominput7 = request.POST['custominput7'] 
          custominput8 = request.POST['custominput8'] 
          custominput9 = request.POST['custominput9'] 
          custominput10 = request.POST['custominput10'] 
          custominput11 = request.POST['custominput11'] 
          custominput12 = request.POST['custominput12'] 
          custominput13 = request.POST['custominput13'] 
          custominput14 = request.POST['custominput14'] 
          custominput15 = request.POST['custominput15'] 
          custominput16 = request.POST['custominput16'] 
          custominput17 = request.POST['custominput17'] 
          custominput18 = request.POST['custominput18'] 
          custominput19 = request.POST['custominput19'] 
          custominput20 = request.POST['custominput20'] 
          custominput21 = request.POST['custominput21'] 
          custominput22 = request.POST['custominput22'] 
          custominput23 = request.POST['custominput23'] 
          custominput24 = request.POST['custominput24'] 
          custominput25 = request.POST['custominput25'] 
          custominput26 = request.POST['custominput26'] 
          custominput27 = request.POST['custominput27'] 
          custominput28 = request.POST['custominput28'] 
          custominput29 = request.POST['custominput29'] 
          custominput30 = request.POST['custominput30'] 
          custominput31 = request.POST['custominput31'] 
          custominput32 = request.POST['custominput32'] 
          customer_id = request.POST.get('customer_id')
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
          analyst_sign = Signatures.objects.get(id=analyst_sign_id)
          review_sign = Signatures.objects.get(id=review_sign_id)
          approved_sign = Signatures.objects.get(id=approved_sign_id)
          pdf_heading = request.POST.get('pdf_heading')
          image_data = {}

          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               
               if uploaded_file:
                    try:
                         original_size_kb = uploaded_file.size / 1024
                         print(f"Processing {image_key} - Original: {original_size_kb:.2f}KB")
                         
                         if uploaded_file.size > 500 * 1024:
                              uploaded_file.seek(0)
                              compressed_image = compress_image(uploaded_file)
                              
                              if compressed_image:
                                   compressed_size_kb = len(compressed_image) / 1024
                                   print(f"Compressed to: {compressed_size_kb:.2f}KB")
                                   base64_encoded = base64.b64encode(compressed_image).decode('utf-8')
                              else:
                                   print("Compression failed, using original")
                                   uploaded_file.seek(0)
                                   file_bytes = uploaded_file.read()
                                   base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         else:
                              file_bytes = uploaded_file.read()
                              base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                              print("No compression needed")

                         image_data[image_key] = base64_encoded
                         image_data[desc_key] = description or ''

                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
          
          
          
          
          
          waterForm = DrinkingWaterForm(lab_report_no = lab_report_no, invoice_bill_no = invoice_bill_no,
                                             reporting_date = reporting_date,report_to = reporting_to, address =address,
                                             attention = attention, email = email, sample_id = sample_id,
                                             sample_collection_date=collection_date, sample_description = sample_description,
                                             sample_type = sample_type, sample_collected_by = sample_collected_by,
                                             date_of_analysis_from = date_of_analysis_from, date_of_analysis_to =  date_of_analysis_to,
                                             test_description=test_description,select=select, water_sr1 = water_sr1, water_sr2 = water_sr2, water_sr3 =  water_sr3,
                                             water_sr4 = water_sr4, water_sr5=water_sr5, water_sr6 = water_sr6, water_sr7 = water_sr7,
                                             water_sr8=water_sr8,water_sr9=water_sr9,water_sr10=water_sr10,water_sr11=water_sr11,water_sr12=water_sr12,
                                             water_sr13 = water_sr13,water_sr14=water_sr14,water_sr15=water_sr15,water_sr16=water_sr16,
                                             water_sr17=water_sr17,water_sr18=water_sr18,water_sr19=water_sr19,water_sr20=water_sr20,
                                             water_sr21=water_sr21,water_sr22=water_sr22,water_sr23=water_sr23,water_sr24=water_sr24,
                                             water_sr25=water_sr25,water_sr26=water_sr26,water_sr27=water_sr27,water_sr28=water_sr28,
                                             water_sr29=water_sr29,water_sr30=water_sr30,water_sr31=water_sr31,water_sr32=water_sr32,
                                             method_1 = method_1, method_2 = method_2, method_3 =  method_3,
                                             method_4 = method_4, method_5=method_5, method_6 = method_6, method_7 = method_7,
                                             method_8=method_8,method_9=method_9,method_10=method_10,method_11=method_11,method_12=method_12,
                                             method_13 = method_13,method_14=method_14,method_15=method_15,method_16=method_16,
                                             method_17=method_17,method_18=method_18,method_19=method_19,method_20=method_20,
                                             method_21=method_21,method_22=method_22,method_23=method_23,method_24=method_24,
                                             method_25=method_25,method_26=method_26,method_27=method_27,method_28=method_28,
                                             method_29=method_29,method_30=method_30,method_31=method_31,method_32=method_32,
                                             legend_1=legend_1,legend_2=legend_2, legend_3=legend_3,legend_4=legend_4,extra_field=extra_field,
                                             legend_5 = legend_5,legend_6=legend_6,legend_7=legend_7,legend_8=legend_8,legend_9=legend_9,
                                             legend_10=legend_10,legend_11=legend_11,edit_note = edit_note, custom_legend=custom_legend,
                                             doc_controll_1=doc_con_1,doc_controll_2=doc_con_2,doc_controll_3=doc_con_3,location = location,in_out=in_out,custominput=custominput,custominput1=custominput1,
                                             custominput2=custominput2,custominput3=custominput3,custominput4=custominput4,custominput5=custominput5,custominput6=custominput6,custominput7=custominput7,custominput8=custominput8,
                                             custominput9=custominput9,custominput10=custominput10,custominput11=custominput11,custominput12=custominput12,custominput13=custominput13,custominput14=custominput14,custominput15=custominput15,
                                             custominput16=custominput16,custominput17=custominput17,custominput18=custominput18,custominput19=custominput19,custominput20=custominput20,custominput21=custominput21,custominput22=custominput22,
                                             custominput23=custominput23,custominput24=custominput24,custominput25=custominput25,custominput26=custominput26,custominput27=custominput27,custominput28=custominput28,custominput29=custominput29,
                                             custominput30=custominput30,custominput31=custominput31,custominput32=custominput32,city_location=city_location,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,
                                             **image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry
                                            )

          waterForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)
          
          
          user = request.user
          action = f'Drinking Water Form {waterForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (DrinkingWaterForm.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/view-form/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return render(request, "drinkingwaterForm.html")
     else:
          
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json', log)
          
          context = {'customers':log,'signs':signs,'industry':industries}

          return render(request, "drinkingwaterForm.html",context)

@login_required(login_url="/login")
def drinkingWaterList(request):
     drinkingWaterList, _srch = _list_filter(request, DrinkingWaterForm)
     context = {'searched':_srch, 'list':drinkingWaterList}

     return render(request,"drinkingWaterList.html",context)









@login_required(login_url="/login")
def drinkingWaterClone(request,pk):
     dw = DrinkingWaterForm.objects.get(id=pk)
     dw.extra_field = dw.extra_field.replace("'", "\"")
     dw.extra_field = json.loads(dw.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json', log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(dw, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'list':dw,'customers':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"drinkingWaterFormClone.html",context)

@login_required(login_url="/login")
def drinkingWaterCloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_dw = DrinkingWaterForm.objects.get(id=pk)
     except DrinkingWaterForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          # new_dw = deepcopy(existing_dw)
          existing_dw.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_dw.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_dw.lab_report_no = request.POST['lab_report_no']
          existing_dw.invoice_bill_no = request.POST['invoice_bill_no']
          existing_dw.reporting_date = request.POST['reporting_date']
          existing_dw.report_to = request.POST['reporting_to']
          existing_dw.address = request.POST['address']
          existing_dw.attention = request.POST['attention']
          existing_dw.email = request.POST['email']
          existing_dw.sample_id = request.POST['sample_id']
          existing_dw.sample_collection_date = request.POST['collection_date']
          existing_dw.sample_description = request.POST['sample_description']
          existing_dw.sample_type = request.POST['sample_type']
          existing_dw.sample_collected_by = request.POST['sample_collected_by']
          existing_dw.date_of_analysis_from = request.POST['date_of_analysis_from']
          existing_dw.date_of_analysis_to = request.POST['date_of_analysis_to']
          existing_dw.test_description = request.POST['test_description']
          existing_dw.select = request.POST.get('water-select')
          existing_dw.water_sr1 = request.POST['water_sr1']
          existing_dw.water_sr2 = request.POST['water_sr2']
          existing_dw.water_sr3 = request.POST['water_sr3']
          existing_dw.water_sr4 = request.POST['water_sr4']
          existing_dw.water_sr5 = request.POST['water_sr5']
          existing_dw.water_sr6 = request.POST['water_sr6']
          existing_dw.water_sr7 = request.POST['water_sr7']
          existing_dw.water_sr8 = request.POST['water_sr8']
          existing_dw.water_sr9 = request.POST['water_sr9']
          existing_dw.water_sr10 = request.POST['water_sr10']
          existing_dw.water_sr11 = request.POST['water_sr11']
          existing_dw.water_sr12 = request.POST['water_sr12']
          existing_dw.water_sr13 = request.POST['water_sr13']
          existing_dw.water_sr14 = request.POST['water_sr14']
          existing_dw.water_sr15 = request.POST['water_sr15']
          existing_dw.water_sr16 = request.POST['water_sr16']
          existing_dw.water_sr17 = request.POST['water_sr17']
          existing_dw.water_sr18 = request.POST['water_sr18']
          existing_dw.water_sr19 = request.POST['water_sr19']
          existing_dw.water_sr20 = request.POST['water_sr20']
          existing_dw.water_sr21 = request.POST['water_sr21']
          existing_dw.water_sr22 = request.POST['water_sr22']
          existing_dw.water_sr23 = request.POST['water_sr23']
          existing_dw.water_sr24 = request.POST['water_sr24']
          existing_dw.water_sr25 = request.POST['water_sr25']
          existing_dw.water_sr26 = request.POST['water_sr26']
          existing_dw.water_sr27 = request.POST['water_sr27']
          existing_dw.water_sr28 = request.POST['water_sr28']
          existing_dw.water_sr29 = request.POST['water_sr29']
          existing_dw.water_sr30 = request.POST['water_sr30']
          existing_dw.water_sr31 = request.POST['water_sr31']
          existing_dw.water_sr32 = request.POST['water_sr32']
          existing_dw.method_1 = request.POST['method_1']
          existing_dw.method_2 = request.POST['method_2']
          existing_dw.method_3 = request.POST['method_3']
          existing_dw.method_4 = request.POST['method_4']
          existing_dw.method_5 = request.POST['method_5']
          existing_dw.method_6 = request.POST['method_6']
          existing_dw.method_7 = request.POST['method_7']
          existing_dw.method_8 = request.POST['method_8']
          existing_dw.method_9 = request.POST['method_9']
          existing_dw.method_10 = request.POST['method_10']
          existing_dw.method_11 = request.POST['method_11']
          existing_dw.method_12 = request.POST['method_12']
          existing_dw.method_13 = request.POST['method_13']
          existing_dw.method_14 = request.POST['method_14']
          existing_dw.method_15 = request.POST['method_15']
          existing_dw.method_16 = request.POST['method_16']
          existing_dw.method_17 = request.POST['method_17']
          existing_dw.method_18 = request.POST['method_18']
          existing_dw.method_19 = request.POST['method_19']
          existing_dw.method_20 = request.POST['method_20']
          existing_dw.method_21 = request.POST['method_21']
          existing_dw.method_22 = request.POST['method_22']
          existing_dw.method_23 = request.POST['method_23']
          existing_dw.method_24 = request.POST['method_24']
          existing_dw.method_25 = request.POST['method_25']
          existing_dw.method_26 = request.POST['method_26']
          existing_dw.method_27 = request.POST['method_27']
          existing_dw.method_28 = request.POST['method_28']
          existing_dw.method_29 = request.POST['method_29']
          existing_dw.method_30 = request.POST['method_30']
          existing_dw.method_31 = request.POST['method_31']
          existing_dw.method_32 = request.POST['method_32']
          existing_dw.legend_1 = request.POST['legend-1']
          existing_dw.legend_2 = request.POST['legend-2']
          existing_dw.legend_3 = request.POST['legend-3']
          existing_dw.legend_4 = request.POST['legend-4']
          existing_dw.legend_5 = request.POST['legend-5']
          existing_dw.legend_6 = request.POST['legend-6']
          existing_dw.legend_7 = request.POST['legend-7']
          existing_dw.legend_8 = request.POST['legend-8']
          existing_dw.legend_9 = request.POST['legend-9']
          existing_dw.legend_10 = request.POST['legend-10']
          existing_dw.legend_11 = request.POST['legend-11']
          existing_dw.edit_note = request.POST['edit-note']
          existing_dw.custom_legend = request.POST['custom-legend']
          existing_dw.doc_controll_1 = request.POST['doc-con-1']
          existing_dw.doc_controll_2 = request.POST['doc-con-2']
          existing_dw.doc_controll_3 = request.POST['doc-con-3']
          # existing_dw.analyzed_by = request.FILES["analyzedby" ]
          # existing_dw.reviewed_by = request.FILES["reviewedby" ]
          # existing_dw.approved_by = request.FILES["approvedby" ]
          # existing_dw.approved_by1 = request.FILES["approvedby1" ]
          existing_dw.city_location = request.POST['city_location']
          existing_dw.extra_field = json.loads(request.POST["extra_field"])
          
          existing_dw.pdf_heading=request.POST.get('pdf_heading')
          existing_dw.created_by = request.user
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)

               print(f"Image {i} remove_requested: {remove_requested}")  # Debug

               if remove_requested == "on":
                    print(f"Removing image {i}")
                    setattr(existing_dw, image_key, '')
                    setattr(existing_dw, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(existing_dw, image_key, base64_encoded)
                         setattr(existing_dw, desc_key, description or '')
                         print(f"Updated image {i}")
                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
               else:
                    if description is not None:
                         setattr(existing_dw, desc_key, description)
                         print(f"Updated description {i}")
     
          
          if existing_dw.in_out == 'customLimits':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    limit = request.POST.getlist('limit[]')[i]

                    existing_dw.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })
          else:
               for i in range(len(request.POST.getlist("sr[]"))):
                    sr = request.POST.getlist("sr[]")[i]
                    parameters = request.POST.getlist("parameters[]")[i]
                    methods = request.POST.getlist("methods[]")[i]
                    unit = request.POST.getlist("unit[]")[i]
                    result = request.POST.getlist("result[]")[i]
                    limit = request.POST.getlist("limit[]")[i]

                    existing_dw.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })
          existing_dw.extra_field = json.dumps(existing_dw.extra_field)
          existing_dw.in_out = request.POST['in_out'] 
          existing_dw.custominput = request.POST['custominput'] 
          existing_dw.custominput1 = request.POST['custominput1'] 
          existing_dw.custominput2 = request.POST['custominput2'] 
          existing_dw.custominput3 = request.POST['custominput3'] 
          existing_dw.custominput4 = request.POST['custominput4'] 
          existing_dw.custominput5 = request.POST['custominput5'] 
          existing_dw.custominput6 = request.POST['custominput6'] 
          existing_dw.custominput7 = request.POST['custominput7'] 
          existing_dw.custominput8 = request.POST['custominput8'] 
          existing_dw.custominput9 = request.POST['custominput9'] 
          existing_dw.custominput10 = request.POST['custominput10'] 
          existing_dw.custominput11 = request.POST['custominput11'] 
          existing_dw.custominput12 = request.POST['custominput12'] 
          existing_dw.custominput13 = request.POST['custominput13'] 
          existing_dw.custominput14 = request.POST['custominput14'] 
          existing_dw.custominput15 = request.POST['custominput15'] 
          existing_dw.custominput16 = request.POST['custominput16'] 
          existing_dw.custominput17 = request.POST['custominput17'] 
          existing_dw.custominput18 = request.POST['custominput18'] 
          existing_dw.custominput19 = request.POST['custominput19'] 
          existing_dw.custominput20 = request.POST['custominput20'] 
          existing_dw.custominput21 = request.POST['custominput21'] 
          existing_dw.custominput22 = request.POST['custominput22'] 
          existing_dw.custominput23 = request.POST['custominput23'] 
          existing_dw.custominput24 = request.POST['custominput24'] 
          existing_dw.custominput25 = request.POST['custominput25'] 
          existing_dw.custominput26 = request.POST['custominput26'] 
          existing_dw.custominput27 = request.POST['custominput27'] 
          existing_dw.custominput28 = request.POST['custominput28'] 
          existing_dw.custominput29 = request.POST['custominput29'] 
          existing_dw.custominput30 = request.POST['custominput30'] 
          existing_dw.custominput31 = request.POST['custominput31'] 
          existing_dw.custominput32 = request.POST['custominput32']
          existing_dw.city_location = request.POST['city_location']
          existing_dw.created_by = request.user
          
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          existing_dw.analyst_signature = analyst_sign
          existing_dw.assistant_manager_signature = review_sign
          existing_dw.lab_manager_signature = approved_sign
          

          existing_dw.id = None
          existing_dw.save()
          user = request.user
          action = f'Drinking Water Form {existing_dw.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_dw.id
          # id = (DrinkingWaterForm.objects.last()).id
          if "submit_and_view" in request.POST:
            url = f"/view-form/{str(id)}/"
            return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
               return redirect(to='drinkWaterList')
          else:
               return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "drinkingWaterFormClone.html")

__all__ = [
    'drinkingWaterForm',
    'drinkingWaterList',
    'drinkingWaterClone',
    'drinkingWaterCloneSave',
]
