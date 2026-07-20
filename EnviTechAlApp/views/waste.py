# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def wasteWaterSludge(request):
     if request.method == 'POST':
            location = request.POST['location']
            industry_id = request.POST.get('industry')
            industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
            city_location = request.POST['city_location']
            lab_report_no = request.POST['ww_lab_report_no']
            invoice_bill_no = request.POST['ww_invoice_no']
            reporting_date = request.POST['ww_report_date']
            report_to = request.POST['ww_report_to']
            address = request.POST['ww_address']
            attention = request.POST['ww_attention']
            email = request.POST['ww_email']
            sample_id = request.POST['ww_sampleid']
            ww_sample_colec_Date = request.POST['ww_sample_colec_Date']
            ww_sample_desc = request.POST['ww_sample_desc']
            ww_sample_type = request.POST['ww_sample_type']
            ww_sample_colec_by = request.POST['ww_sample_colec_by']
            ww_date_of_analy_from = request.POST['ww_date_of_analy_from']
            ww_date_of_analy_to = request.POST['ww_date_of_analy_to']
            ww_test_desc = request.POST['ww_test_desc']
            ww_sr1 = request.POST['ww_sr1']
            ww_sr2 = request.POST['ww_sr2']
            ww_sr3 = request.POST['ww_sr3']
            ww_sr4 = request.POST['ww_sr4']
            ww_sr5 = request.POST['ww_sr5']
            ww_sr6 = request.POST['ww_sr6']
            ww_sr7 = request.POST['ww_sr7']
            ww_sr8 = request.POST['ww_sr8']
            ww_sr9 = request.POST['ww_sr9']
            ww_sr10 = request.POST['ww_sr10']
            ww_sr11 = request.POST['ww_sr11']
            ww_sr12 = request.POST['ww_sr12']
            ww_sr13 = request.POST['ww_sr13']
            ww_sr14 = request.POST['ww_sr14']
            ww_sr15 = request.POST['ww_sr15']
            ww_sr16 = request.POST['ww_sr16']
            ww_sr17 = request.POST['ww_sr17']
            ww_legend_1 = request.POST['ww-legend-1']
            ww_legend_2 = request.POST['ww-legend-2']
            ww_legend_3 = request.POST['ww-legend-3']
            ww_legend_4 = request.POST['ww-legend-4']
            ww_legend_5 = request.POST['ww-legend-5']
            ww_legend_6 = request.POST['ww-legend-6']
            ww_legend_7 = request.POST['ww-legend-7']
            ww_legend_8 = request.POST['ww-legend-8']
            ww_legend_9 = request.POST['ww-legend-9']
            ww_legend_10 = request.POST['ww-legend-10']
            ww_legend_11 = request.POST['ww-legend-11']
            ww_editnote = request.POST['ww_editnote']
            ww_custom_legend = request.POST['ww_custom_legend']
            ww_doc_con_1 = request.POST['ww_doc1']
            ww_doc_con_2 = request.POST['ww_doc2']
            ww_doc_con_3 = request.POST['ww_doc3']
          #   ww_analyzed_by = request.FILES["ww_analyzedby" ]
          #   ww_reviewd_by = request.FILES["ww_reviewedby" ]
          #   ww_approved_by = request.FILES["ww_approvedby" ]
          #   ww_approved_by1 = request.FILES["ww_approvedby1" ]
            zdhc = request.POST['zdhc']
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
                         
                         if uploaded_file.size > 500 * 1024:
                              uploaded_file.seek(0)
                              compressed_image = compress_image(uploaded_file)
                              
                              if compressed_image:
                                   compressed_size_kb = len(compressed_image) / 1024
                                   base64_encoded = base64.b64encode(compressed_image).decode('utf-8')
                              else:
                                   uploaded_file.seek(0)
                                   file_bytes = uploaded_file.read()
                                   base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         else:
                              file_bytes = uploaded_file.read()
                              base64_encoded = base64.b64encode(file_bytes).decode('utf-8')

                         image_data[image_key] = base64_encoded
                         image_data[desc_key] = description or ''

                    except Exception as e:
                         pass
            
            wasteWaterForm = WasteWaterSludge(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,
                                              report_to=report_to,address=address,attention=attention,email=email,
                                              sample_id=sample_id,ww_sample_colec_Date=ww_sample_colec_Date,ww_sample_desc=ww_sample_desc,
                                              ww_sample_type=ww_sample_type,ww_sample_colec_by=ww_sample_colec_by,ww_date_of_analy_from=ww_date_of_analy_from,ww_date_of_analy_to=ww_date_of_analy_to,
                                              ww_test_desc=ww_test_desc,ww_sr1=ww_sr1,ww_sr2=ww_sr2,ww_sr3=ww_sr3,ww_sr4=ww_sr4,ww_sr5=ww_sr5,
                                              ww_sr6=ww_sr6,ww_sr7=ww_sr7,ww_sr8=ww_sr8,ww_sr9=ww_sr9,ww_sr10=ww_sr10,ww_sr11=ww_sr11,ww_sr12=ww_sr12,
                                              ww_sr13=ww_sr13,ww_legend_1=ww_legend_1,ww_legend_2=ww_legend_2,location=location,zdhc=zdhc,ww_sr14=ww_sr14,ww_sr15=ww_sr15,ww_sr16=ww_sr16,ww_sr17=ww_sr17,
                                              ww_legend_3=ww_legend_3,ww_legend_4=ww_legend_4,ww_legend_5=ww_legend_5,ww_legend_6=ww_legend_6,ww_legend_7=ww_legend_7,
                                              ww_legend_8=ww_legend_8,ww_legend_9=ww_legend_9,ww_legend_10=ww_legend_10,ww_legend_11=ww_legend_11,ww_editnote=ww_editnote,ww_custom_legend=ww_custom_legend,
                                              ww_doc_con_1=ww_doc_con_1,ww_doc_con_2=ww_doc_con_2,ww_doc_con_3=ww_doc_con_3,city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,
                                              assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
            wasteWaterForm.save()

            
            if customer_id:
                 LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

            user = request.user
            action = f'Waste Water Form {wasteWaterForm.lab_report_no} created by {user.username}'
            AuditLog.objects.create(user=user, action=action, timestamp=local_date)
            messages.success(request, 'Operation was successful!')
            id = (AmbientAirForm.objects.last()).id
            id = (WasteWaterSludge.objects.last()).id
            if "submit_and_view" in request.POST:
               url = f"/wasteWaterSludge-view/{str(id)}/"
               return redirect(to=url)
            if "submit_and_new" in request.POST:
               return redirect("wasteWaterSludge")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"wasteWaterSludge.html",context)

@login_required(login_url="/login")
def wasteWater2(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['lab_rep_no']
          invoice_bill_no = request.POST['invoice_no']
          reporting_date = request.POST['repo_date']
          report_to = request.POST['report_to']
          address = request.POST['address']
          attention = request.POST['attention']
          email = request.POST['email']
          sample_id = request.POST['sampleId']
          sample_Col_date = request.POST['sample_Col_date']
          sample_desc = request.POST['sample_desc']
          sampling_method = request.POST['sampling_method']
          sample_type = request.POST['sample_type']
          sample_collected_by = request.POST['sample_collected_by']
          date_of_analysis_from = request.POST['date_of_analysis_from']
          date_of_analysis_to = request.POST['date_of_analysis_to']
          test_description = request.POST['test_description']
          select = request.POST.get('select')
          result_1 = request.POST['result_1']
          result_1_1 = request.POST['result_1_1']
          result_2 = request.POST['result_2']
          result_2_2 = request.POST['result_2_2']
          result_3 = request.POST['result_3']
          result_3_3 = request.POST['result_3_3']
          result_4 = request.POST['result_4']
          result_4_4 = request.POST['result_4_4']
          result_5 = request.POST['result_5']
          result_5_5 = request.POST['result_5_5']
          result_6 = request.POST['result_6']
          result_6_6 = request.POST['result_6_6']
          result_7 = request.POST['result_7']
          result_7_7 = request.POST['result_7_7']
          metho_select = request.POST.get('metho_select')
          result_8 = request.POST['result_8']
          result_8_8 = request.POST['result_8_8']
          result_9 = request.POST['result_9']
          result_9_9 = request.POST['result_9_9']
          result_10 = request.POST['result_10']
          result_10_10 = request.POST['result_10_10']
          result_11 = request.POST['result_11']
          result_11_11= request.POST['result_11_11']
          result_12 = request.POST['result_12']
          result_12_12 = request.POST['result_12_12']
          result_13 = request.POST['result_13']
          result_13_13 = request.POST['result_13_13']
          result_14 = request.POST['result_14']
          result_14_14 = request.POST['result_14_14']
          result_15 = request.POST['result_15']
          result_15_15 = request.POST['result_15_15']
          result_16 = request.POST['result_16']
          result_16_16 = request.POST['result_16_16']
          result_17 = request.POST['result_17']
          result_17_17 = request.POST['result_17_17']
          result_18 = request.POST['result_18']
          result_18_18 = request.POST['result_18_18']
          result_19 = request.POST['result_19']
          result_19_19 = request.POST['result_19_19']
          result_20 = request.POST['result_20']
          result_20_20 = request.POST['result_20_20']
          result_21 = request.POST['result_21']
          result_21_21 = request.POST['result_21_21']
          result_22 = request.POST['result_22']
          result_22_22 = request.POST['result_22_22']
          result_23 = request.POST['result_23']
          result_23_23 = request.POST['result_23_23']
          result_24 = request.POST['result_24']
          result_24_24 = request.POST['result_24_24']
          result_25 = request.POST['result_25']
          result_25_25 = request.POST['result_25_25']
          result_26 = request.POST['result_26']
          result_26_26 = request.POST['result_26_26']
          result_27 = request.POST['result_27']
          result_27_27 = request.POST['result_27_27']
          result_28 = request.POST['result_28']
          result_28_28 = request.POST['result_28_28']
          result_29 = request.POST['result_29']
          result_29_29 = request.POST['result_29_29']
          result_30 = request.POST['result_30']
          result_30_30 = request.POST['result_30_30']
          result_31 = request.POST['result_31']
          result_31_31 = request.POST['result_31_31']
          result_32 = request.POST['result_32']
          result_32_32 = request.POST['result_32_32']
          legend_1 = request.POST['legend_1']
          legend_2 = request.POST['legend_2']
          legend_3 = request.POST['legend_3']
          legend_4 = request.POST['legend_4']
          legend_5 = request.POST['legend_5']
          legend_6 = request.POST['legend_6']
          legend_7 = request.POST['legend_7']
          legend_8 = request.POST['legend_8']
          legend_9 = request.POST['legend_9']
          legend_10 = request.POST['legend_10']
          legend_11 = request.POST['legend_11']
          editNote = request.POST['editNote']
          customlegend = request.POST['customlegend']
          doc1 = request.POST['doc1']
          doc2 = request.POST['doc2']
          doc3 = request.POST['doc3']
          # analyzedby = request.FILES['analyzedby']
          # reviewedby = request.FILES['reviewedby']
          # approvedby = request.FILES['approvedby']
          # approvedby1 = request.FILES['approvedby1']
          in_out = request.POST['in_out']
          inlet_result = request.POST['inlet_result'] 
          outlet_result = request.POST.get('outlet_result')
          extra_field = request.POST['extra_field']
          cutomLimit1 = request.POST['cutomLimit1'] 
          cutomLimit2 = request.POST['cutomLimit2'] 
          cutomLimit3 = request.POST['cutomLimit3'] 
          cutomLimit4 = request.POST['cutomLimit4'] 
          cutomLimit5 = request.POST['cutomLimit5'] 
          cutomLimit6 = request.POST['cutomLimit6'] 
          cutomLimit7 = request.POST['cutomLimit7'] 
          cutomLimit8 = request.POST['cutomLimit8'] 
          cutomLimit9 = request.POST['cutomLimit9'] 
          cutomLimit10 = request.POST['cutomLimit10'] 
          cutomLimit11 = request.POST['cutomLimit11'] 
          cutomLimit12 = request.POST['cutomLimit12'] 
          cutomLimit13 = request.POST['cutomLimit13'] 
          cutomLimit14 = request.POST['cutomLimit14'] 
          cutomLimit15 = request.POST['cutomLimit15'] 
          cutomLimit16 = request.POST['cutomLimit16'] 
          cutomLimit17 = request.POST['cutomLimit17'] 
          cutomLimit18 = request.POST['cutomLimit18'] 
          cutomLimit18 = request.POST['cutomLimit18'] 
          cutomLimit19 = request.POST['cutomLimit19'] 
          cutomLimit20 = request.POST['cutomLimit20'] 
          cutomLimit21 = request.POST['cutomLimit21'] 
          cutomLimit22 = request.POST['cutomLimit22'] 
          cutomLimit23 = request.POST['cutomLimit23'] 
          cutomLimit24 = request.POST['cutomLimit24'] 
          cutomLimit25 = request.POST['cutomLimit25'] 
          cutomLimit26 = request.POST['cutomLimit26'] 
          cutomLimit27 = request.POST['cutomLimit27'] 
          cutomLimit28 = request.POST['cutomLimit28'] 
          cutomLimit29 = request.POST['cutomLimit29'] 
          cutomLimit30 = request.POST['cutomLimit30'] 
          cutomLimit31 = request.POST['cutomLimit31']
          cutomLimit32 = request.POST['cutomLimit32']
          cutomLimit33 = request.POST['cutomLimit33']
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
                         
                         if uploaded_file.size > 500 * 1024:
                              uploaded_file.seek(0)
                              compressed_image = compress_image(uploaded_file)
                              
                              if compressed_image:
                                   compressed_size_kb = len(compressed_image) / 1024
                                   base64_encoded = base64.b64encode(compressed_image).decode('utf-8')
                              else:
                                   uploaded_file.seek(0)
                                   file_bytes = uploaded_file.read()
                                   base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         else:
                              file_bytes = uploaded_file.read()
                              base64_encoded = base64.b64encode(file_bytes).decode('utf-8')

                         image_data[image_key] = base64_encoded
                         image_data[desc_key] = description or ''

                    except Exception as e:
                         pass

          
          structured_data = {
               'standard_parameters': [],
               'extra_parameters': [],
               'report_type': request.POST.get('in_out', 'in-out')
          }
          
          # Collect standard parameters (1-32) with their names
          for i in range(1, 33):
               # Get parameter name from hidden input
               param_name = request.POST.get(f'parameter_{i}', '')
               if not param_name:
                    # Use default names if not provided
                    default_names = [
                         "Temperature 40 °C", "pH", "Sulphide", "Biological Oxygen Demand(BOD)5",
                         "Chemical Oxygen Demand(COD)", "Total Dissolved Solids (TDS)",
                         "Total Suspended Solids (TSS)", "Oil & Grease", "Cadmium", "Copper",
                         "Iron", "Lead", "Manganese", "Mercury", "Nickel", "Selenium",
                         "Chromium", "Zinc", "Arsenic", "Chlorine", "Chloride", "Cyanide",
                         "Fluoride", "Ammonia", "Total Toxic Metals", "Sulphate",
                         "An Ionic Detergent As MBAs", "Pesticides", "Phenolic Compounds(as Phenol)",
                         "Boron", "Barium", "Silver"
                    ]
                    param_name = default_names[i-1] if i-1 < len(default_names) else f"Parameter {i}"
               
               # Get results from form
               inlet_result = request.POST.get(f'result_{i}', '')
               outlet_result = request.POST.get(f'result_{i}_{i}', '')
               
               # Get custom limit (cutomLimit starts from 2, so we use i+1)
               custom_limit = ''
               if i < 32:  # Only 31 custom limit fields for standard parameters
                    custom_limit = request.POST.get(f'cutomLimit{i+1}', '')
               
               # Add to structured data
               structured_data['standard_parameters'].append({
                    'sr_no': i,
                    'parameter': param_name,
                    'inlet_result': inlet_result,
                    'outlet_result': outlet_result,
                    'custom_limit': custom_limit
               })
          
          # Get extra field data (the existing extra_field format)
          extra_field_str = request.POST.get('extra_field', '[]')
          try:
               extra_field_data = json.loads(extra_field_str)
          except Exception:
               try:
                    extra_field_data = ast.literal_eval(extra_field_str)
               except Exception:
                    extra_field_data = []
          
          # Convert extra field data to structured format
          extra_counter = 33  # Start from 33 for extra parameters
          for item in extra_field_data:
               if isinstance(item, dict):
                    structured_extra = {
                         'sr_no': extra_counter,
                         'parameter': item.get('parameters', f'Extra Parameter {extra_counter}'),
                         'methods': item.get('methods', ''),
                         'unit': item.get('unit', '')
                    }
                    
                    # Add results based on report type
                    report_type = request.POST.get('in_out', 'in-out')
                    if report_type == 'in':
                         structured_extra['inlet_result'] = item.get('result', '')
                    elif report_type == 'out':
                         structured_extra['outlet_result'] = item.get('outlet', item.get('result', ''))
                    elif report_type == 'in-out':
                         structured_extra['inlet_result'] = item.get('result', '')
                         structured_extra['outlet_result'] = item.get('outlet', '')
                    elif report_type == 'inlet_customlimits':
                         structured_extra['inlet_result'] = item.get('result', '')
                         structured_extra['custom_limit'] = item.get('customLimits', '')
                    elif report_type == 'outlet_customLimits':
                         structured_extra['outlet_result'] = item.get('outlet', item.get('result', ''))
                         structured_extra['custom_limit'] = item.get('customLimits', '')
                    
                    structured_data['extra_parameters'].append(structured_extra)
                    extra_counter += 1
          
          # Convert structured data to JSON string for structured_data field
          structured_data_json = json.dumps(structured_data)
          
          
          wasteWaterForm2 =  WasteWaterForm2(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,report_to=report_to,address=address,
                                             attention=attention,email=email,sample_id=sample_id,sample_Col_date=sample_Col_date,sample_desc=sample_desc,
                                             sampling_method=sampling_method,sample_type=sample_type,sample_collected_by=sample_collected_by,
                                             date_of_analysis_from=date_of_analysis_from,date_of_analysis_to=date_of_analysis_to,test_description=test_description,select=select,result_1=result_1,
                                             result_1_1=result_1_1,result_2=result_2,result_2_2=result_2_2,result_3=result_3,result_3_3=result_3_3,
                                             result_4=result_4,result_4_4=result_4_4,result_5=result_5,result_5_5=result_5_5,result_6=result_6,result_6_6 =result_6_6,result_7 = result_7,
                                             result_7_7=result_7_7,metho_select=metho_select,result_8=result_8,result_8_8=result_8_8,result_9=result_9,
                                             result_9_9=result_9_9,result_10=result_10,result_10_10=result_10_10,result_11=result_11,result_11_11=result_11_11,
                                             result_12=result_12,result_12_12=result_12_12,result_13=result_13,result_13_13=result_13_13,result_14=result_14,
                                             result_14_14=result_14_14,result_15=result_15,result_15_15=result_15_15,result_16=result_16,result_16_16=result_16_16,
                                             result_17=result_17,result_17_17=result_17_17,result_18=result_18,result_18_18=result_18_18,result_19=result_19,
                                             result_19_19=result_19_19,result_20=result_20,result_20_20=result_20_20,result_21=result_21,result_21_21=result_21_21,
                                             result_22=result_22,result_22_22=result_22_22,result_23=result_23,result_23_23=result_23_23,result_24=result_24,
                                             result_24_24=result_24_24,result_25=result_25,result_25_25=result_25_25,result_26=result_26,result_26_26=result_26_26,
                                             result_27=result_27,result_27_27=result_27_27,result_28=result_28,result_28_28=result_28_28,result_29=result_29,
                                             result_29_29=result_29_29,result_30=result_30,result_30_30=result_30_30,result_31=result_31,result_31_31=result_31_31,
                                             result_32=result_32,result_32_32=result_32_32,legend_1=legend_1,legend_2=legend_2,legend_3=legend_3,extra_field=extra_field,
                                             legend_4=legend_4,legend_5=legend_5,legend_6=legend_6,legend_7=legend_7,legend_8=legend_8,legend_9=legend_9,
                                             legend_10=legend_10,legend_11=legend_11,editNote=editNote,location=location,in_out=in_out,inlet_result=inlet_result,outlet_result=outlet_result,cutomLimit1=cutomLimit1,cutomLimit2=cutomLimit2,
                                             cutomLimit3=cutomLimit3,cutomLimit4=cutomLimit4,cutomLimit5=cutomLimit5,cutomLimit6=cutomLimit6,cutomLimit7=cutomLimit7,cutomLimit8=cutomLimit8,
                                             cutomLimit9=cutomLimit9,cutomLimit10=cutomLimit10,cutomLimit11=cutomLimit11,cutomLimit12=cutomLimit12,cutomLimit13=cutomLimit13,cutomLimit14=cutomLimit14,
                                             cutomLimit15=cutomLimit15,cutomLimit16=cutomLimit16,cutomLimit17=cutomLimit17,cutomLimit18=cutomLimit18,cutomLimit19=cutomLimit19,
                                             cutomLimit20=cutomLimit20,cutomLimit21=cutomLimit21,cutomLimit22=cutomLimit22,cutomLimit23=cutomLimit23,cutomLimit24=cutomLimit24,cutomLimit25=cutomLimit25,
                                             cutomLimit26=cutomLimit26,cutomLimit27=cutomLimit27,cutomLimit28=cutomLimit28,cutomLimit29=cutomLimit29,cutomLimit30=cutomLimit30,cutomLimit31=cutomLimit31,
                                             cutomLimit32=cutomLimit32,cutomLimit33=cutomLimit33,
                                             customlegend=customlegend,doc1=doc1,doc2=doc2,doc3=doc3,city_location=city_location,
                                             customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                             lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry,structured_data=structured_data_json,)
          
          wasteWaterForm2.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Waste Water 2 Form {wasteWaterForm2.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (WasteWaterForm2.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/wasteWater2-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="wasteWater2")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"wasteWater2.html",context)

@login_required(login_url="/login")
def wasteWaterSludgeList(request):
     wasteWaterForm, _srch = _list_filter(request, WasteWaterSludge)
     context = {'searched':_srch, 'data':wasteWaterForm}
     return render(request,'wasteWaterSludgeList.html',context)

@login_required(login_url="/login")
def wasteWaterSludgeDelete(request,pk):
     wastewaterForm = WasteWaterSludge.objects.get(id=pk)
     wastewaterForm.delete()
     user = request.user
     action = f'Waste Water Form {wastewaterForm.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect('wasteWaterSludgeList')

@login_required(login_url="/login")
def wastewaterEdit(request,pk):
     wasteWaterForm = WasteWaterSludge.objects.get(id=pk)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(wasteWaterForm, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     
     context = {'data':wasteWaterForm,'log':log,'signs':signs,'pdf_image_1': image_previews.get('pdf_image_1'),
     'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,'wasteWaterEdit.html',context)

@login_required(login_url="/login")
def wasteWaterUpdate(request,pk):
     wasterWaterForm = WasteWaterSludge.objects.get(id=pk)
     if request.method == 'POST':
          wasterWaterForm.location = request.POST['location']
          industry_id = request.POST.get('industry')
          ambientUpdate.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          wasterWaterForm.lab_report_no = request.POST['ww_lab_report_no']
          wasterWaterForm.invoice_bill_no = request.POST['ww_invoice_no']
          wasterWaterForm.reporting_date = request.POST['ww_report_date']
          wasterWaterForm.report_to = request.POST['ww_report_to']
          wasterWaterForm.address = request.POST['ww_address']
          wasterWaterForm.attention = request.POST['ww_attention']
          wasterWaterForm.email = request.POST['ww_email']
          wasterWaterForm.sample_id = request.POST['ww_sampleid']
          wasterWaterForm.ww_sample_colec_Date = request.POST['ww_sample_colec_Date']
          wasterWaterForm.ww_sample_desc = request.POST['ww_sample_desc']
          wasterWaterForm.ww_sample_type = request.POST['ww_sample_type']
          wasterWaterForm.ww_sample_colec_by = request.POST['ww_sample_colec_by']
          wasterWaterForm.ww_date_of_analy_from = request.POST['ww_date_of_analy_from']
          wasterWaterForm.ww_date_of_analy_to = request.POST['ww_date_of_analy_to']
          wasterWaterForm.ww_test_desc = request.POST['ww_test_desc']
          wasterWaterForm.ww_sr1 = request.POST['ww_sr1']
          wasterWaterForm.ww_sr2 = request.POST['ww_sr2']
          wasterWaterForm.ww_sr3 = request.POST['ww_sr3']
          wasterWaterForm.ww_sr4 = request.POST['ww_sr4']
          wasterWaterForm.ww_sr5 = request.POST['ww_sr5']
          wasterWaterForm.ww_sr6 = request.POST['ww_sr6']
          wasterWaterForm.ww_sr7 = request.POST['ww_sr7']
          wasterWaterForm.ww_sr8 = request.POST['ww_sr8']
          wasterWaterForm.ww_sr9 = request.POST['ww_sr9']
          wasterWaterForm.ww_sr10 = request.POST['ww_sr10']
          wasterWaterForm.ww_sr11 = request.POST['ww_sr11']
          wasterWaterForm.ww_sr12 = request.POST['ww_sr12']
          wasterWaterForm.ww_sr13 = request.POST['ww_sr13']
          wasterWaterForm.ww_sr14 = request.POST['ww_sr14']
          wasterWaterForm.ww_sr15 = request.POST['ww_sr15']
          wasterWaterForm.ww_sr16 = request.POST['ww_sr16']
          wasterWaterForm.ww_sr17 = request.POST['ww_sr17']
          wasterWaterForm.ww_legend_1 = request.POST['ww-legend-1']
          wasterWaterForm.ww_legend_2 = request.POST['ww-legend-2']
          wasterWaterForm.ww_legend_3 = request.POST['ww-legend-3']
          wasterWaterForm.ww_legend_4 = request.POST['ww-legend-4']
          wasterWaterForm.ww_legend_5 = request.POST['ww-legend-5']
          wasterWaterForm.ww_legend_6 = request.POST['ww-legend-6']
          wasterWaterForm.ww_legend_7 = request.POST['ww-legend-7']
          wasterWaterForm.ww_legend_8 = request.POST['ww-legend-8']
          wasterWaterForm.ww_legend_9 = request.POST['ww-legend-9']
          wasterWaterForm.ww_legend_10 = request.POST['ww-legend-10']
          wasterWaterForm.ww_legend_11 = request.POST['ww-legend-11']
          wasterWaterForm.ww_editnote = request.POST['ww_editnote']
          wasterWaterForm.ww_custom_legend = request.POST['ww_custom_legend']
          wasterWaterForm.ww_doc_con_1 = request.POST['ww_doc1']
          wasterWaterForm.ww_doc_con_2 = request.POST['ww_doc2']
          wasterWaterForm.ww_doc_con_3 = request.POST['ww_doc3']
          # wasterWaterForm.ww_analyzed_by = request.FILES["ww_analyzedby" ]
          # wasterWaterForm.ww_reviewd_by = request.FILES["ww_reviewedby" ]
          # wasterWaterForm.ww_approved_by = request.FILES["ww_approvedby" ]
          # wasterWaterForm.ww_approved_by1 = request.FILES["ww_approvedby1"]
          wasterWaterForm.city_location = request.POST['city_location']
          wasterWaterForm.zdhc = request.POST['zdhc']
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          wasterWaterForm.analyst_signature = analyst_sign
          wasterWaterForm.assistant_manager_signature = review_sign
          wasterWaterForm.lab_manager_signature = approved_sign
          wasterWaterForm.created_by = request.user
          
          wasterWaterForm.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(wasterWaterForm, image_key, '')
                    setattr(wasterWaterForm, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(wasterWaterForm, image_key, base64_encoded)
                         setattr(wasterWaterForm, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(wasterWaterForm, desc_key, description)
          
          
          

          wasterWaterForm.save()
          user = request.user
          action = f'Waste Water Form {wasterWaterForm.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id=wasterWaterForm.id
          if "submit_and_view" in request.POST:
               url = f'/wasteWaterSludge-view/{str(id)}/'
               return redirect(to=url)
          else:
               return redirect("wasteWaterSludgeList")
     return render(request,"wasteWaterSludgeList.html")


def wasteWaterView(request,pk):
     wasteWaterForm =  WasteWaterSludge.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{wasteWaterForm.lab_report_no}.png"
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

     context = {'data':wasteWaterForm,'qr':qr_relative_path,'logo':logo}

     return render(request,'wasteWaterReport.html',context)




def wasteWaterPdf0(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_wasteWaterPdf0 as PDFWithPageNumbers



     num_rows = 0
     vem = WasteWaterSludge.objects.get(id=pk)

     
     if vem.zdhc == 'zdhc':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result","ZDHC Limits"],
          ]
          sr_no = 1
          if vem.ww_sr1:
               a = [str(sr_no),"Cadmium (Cd)","*APHA 3111- B","mg/Kg",vem.ww_sr1,"01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr2:
               a = [str(sr_no),"Copper (Cu)","*APHA 3111- B","mg/Kg",vem.ww_sr2,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr3:
               a = [str(sr_no),"Iron (Fe)","*APHA 3111- B","mg/Kg",vem.ww_sr3,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr4:
               a = [str(sr_no),"Boron (B)","HACH 8015","mg/Kg",vem.ww_sr4,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr5:
               a = [str(sr_no),"Lead (Pb)","*APHA 3111- B","mg/Kg",vem.ww_sr5,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr6:
               a = [str(sr_no),"Mercury (Hg)","*APHA 3112- B","mg/Kg",vem.ww_sr6,"01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr7:
               a = [str(sr_no),"Selenium (Se)","*APHA 3114- B","mg/Kg",vem.ww_sr7,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr8:
               a = [str(sr_no),"Silver (Ag)","*APHA 3111- B","mg/Kg",vem.ww_sr8,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr9:
               a = [str(sr_no),"Nickel (Ni)","*APHA 3111- B","mg/Kg",vem.ww_sr9,"20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr10:
               a = [str(sr_no),"Zinc (Zn)","*APHA 3111- B","mg/Kg",vem.ww_sr10,"400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr11:
               a = [str(sr_no),"Arsenic (As)","*APHA 3114- B","mg/Kg",vem.ww_sr11,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr12:
               a = [str(sr_no),"Manganese (Mn)","*APHA 3111- B","mg/Kg",vem.ww_sr12,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr13:
               a = [str(sr_no),"Chromium","*APHA 3111- B","mg/Kg",vem.ww_sr13,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr14:
               a = [str(sr_no),"Antimony","*APHA 3111- B","mg/Kg",vem.ww_sr14,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr15:
               a = [str(sr_no),"Cobalt","*APHA 3111- B","mg/Kg",vem.ww_sr15,"400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr16:
               a = [str(sr_no),"Barium","HACH 8014","mg/Kg",vem.ww_sr16,"200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr17:
               a = [str(sr_no),"Chromium (VI)","HACH 8023","mg/Kg",vem.ww_sr17,"20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)                              




          pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                   address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                   ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                   ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                   )
          pdf._rq_request, pdf._rq_pk = request, pk
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)










          num_rows = 0
          #report data table
          with pdf.table(col_widths=(6, 45, 30,30,30,20),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows+=1
                    # if k == 0:
                    #      data_row[4] = vem.ambienAir_select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     
     else:
          if vem.zdhc == 'no-zdhc':
               TABLE_DATA = [
               ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result"],
               ]
               sr_no = 1
               if vem.ww_sr1:
                    a = [str(sr_no),"Cadmium (Cd)","*APHA 3111- B","mg/Kg",vem.ww_sr1]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr2:
                    a = [str(sr_no),"Copper (Cu)","*APHA 3111- B","mg/Kg",vem.ww_sr2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr3:
                    a = [str(sr_no),"Iron (Fe)","*APHA 3111- B","mg/Kg",vem.ww_sr3]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr4:
                    a = [str(sr_no),"Boron (B)","HACH 8015","mg/Kg",vem.ww_sr4]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr5:
                    a = [str(sr_no),"Lead (Pb)","*APHA 3111- B","mg/Kg",vem.ww_sr5]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr6:
                    a = [str(sr_no),"Mercury (Hg)","*APHA 3112- B","mg/Kg",vem.ww_sr6]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr7:
                    a = [str(sr_no),"Selenium (Se)","*APHA 3114- B","mg/Kg",vem.ww_sr7]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr8:
                    a = [str(sr_no),"Silver (Ag)","*APHA 3111- B","mg/Kg",vem.ww_sr8]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr9:
                    a = [str(sr_no),"Nickel (Ni)","*APHA 3111- B","mg/Kg",vem.ww_sr9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr10:
                    a = [str(sr_no),"Zinc (Zn)","*APHA 3111- B","mg/Kg",vem.ww_sr10]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr11:
                    a = [str(sr_no),"Arsenic (As)","*APHA 3114- B","mg/Kg",vem.ww_sr11]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr12:
                    a = [str(sr_no),"Manganese (Mn)","*APHA 3111- B","mg/Kg",vem.ww_sr12]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr13:
                    a = [str(sr_no),"Chromium","*APHA 3111- B","mg/Kg",vem.ww_sr13]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr14:
                    a = [str(sr_no),"Antimony","*APHA 3111- B","mg/Kg",vem.ww_sr14]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr15:
                    a = [str(sr_no),"Cobalt","*APHA 3111- B","mg/Kg",vem.ww_sr15]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr16:
                    a = [str(sr_no),"Barium","HACH 8014","mg/Kg",vem.ww_sr16]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr17:
                    a = [str(sr_no),"Chromium (VI)","HACH 8023","mg/Kg",vem.ww_sr17]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)                              




               pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                        address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                        ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                        ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                        )
               pdf._rq_request, pdf._rq_pk = request, pk
               pdf.add_page()
               font_path = "static/fonts/calibri.ttf"
               font_path_bold = "static/fonts/calibrib.ttf"
               pdf.add_font("Calibri","",font_path,uni=True)
               pdf.add_font("Calibri","B",font_path_bold,uni=True)
               pdf.set_font("Calibri","", 9)
               pdf.set_auto_page_break(auto=True,margin=5)










               
               #report data table
               with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




                    for k in range(0,len(TABLE_DATA)):
                         data_row = TABLE_DATA[k]
                         num_rows+=1
                         # if k == 0:
                         #      data_row[4] = vem.ambienAir_select + " Limits"

                         # watwer mark
                         # pdf.set_page_background("static/assets/Capture.PNG")
                         row = table.row()
                         for i in range(0,len(data_row)):
                              datum = data_row[i]

                              row.cell(datum)


     # data after Table

     # if num_rows >=10 and num_rows <=14:

     #      pdf.add_page()

     if 'pdf' not in locals():
         pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                  address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                  ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                  ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                  )
         pdf._rq_request, pdf._rq_pk = request, pk
         pdf.add_page()
         font_path = "static/fonts/calibri.ttf"
         font_path_bold = "static/fonts/calibrib.ttf"
         pdf.add_font("Calibri","",font_path,uni=True)
         pdf.add_font("Calibri","B",font_path_bold,uni=True)
         pdf.set_font("Calibri","", 9)
         pdf.set_auto_page_break(auto=True,margin=5)
     if num_rows >=16:
               pdf.add_page()
     
     Table_Data1 = [
          ["Note: " + vem.ww_editnote]
     ]

     with pdf.table(col_widths=(190,), line_height=2, text_align=("LEFT")) as table:
          for data_row in Table_Data1:
               row = table.row()
               for datum in data_row:
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')
               
          
     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if vem.ww_legend_1:
          a = [vem.ww_legend_1]
          Table_data_legend.append(a)
          
     if vem.ww_legend_2:
          a = [vem.ww_legend_2]
          Table_data_legend.append(a)
          
     if vem.ww_legend_3:
          a = [vem.ww_legend_3]
          Table_data_legend.append(a)
          
     if vem.ww_legend_4:
          a = [vem.ww_legend_4]
          Table_data_legend.append(a)
     

     if vem.ww_legend_5:
          a = [vem.ww_legend_5]
          Table_data_legend.append(a)
          
     if vem.ww_legend_6:
          a = [vem.ww_legend_6]
          Table_data_legend.append(a)
          
     if vem.ww_legend_7:
          a = [vem.ww_legend_7]
          Table_data_legend.append(a)
          
     if vem.ww_legend_8:
          a = [vem.ww_legend_8]
          Table_data_legend.append(a)
          
     if vem.ww_legend_9:
          a = [vem.ww_legend_9]
          Table_data_legend.append(a)
          
     if vem.ww_legend_10:
          a = [vem.ww_legend_10]
          Table_data_legend.append(a)
          
     if vem.ww_legend_11:
          a = [vem.ww_legend_11]
          Table_data_legend.append(a)
          

     if vem.ww_custom_legend:
          a = [vem.ww_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L') 


     # pdf.image(vem.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,256,36+pdf.get_string_width("Analyzed By (Analyst)"),256)
     # pdf.text(26,259,"Analyzed By (Analyst)")
     # pdf.image(vem.assistant_manager_signature.signature,100,238,20.32,20.32)
     # pdf.line(126,256,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),256)
     # pdf.text(87.5,259,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(vem.lab_manager_signature.signature,178,238,20.32,20.32)
     # pdf.line(155,256,165+pdf.get_string_width("Approved By (Lab Manager)"),256)
     # pdf.text(160,259,"Approved By (Lab Manager)")
     
     if vem.analyst_signature:
         pdf.image(vem.analyst_signature.signature,30,238,20.32,20.32)
         pdf.line(19,256,36+pdf.get_string_width(f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})"),256)
         pdf.text(26,259,f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})")
     if vem.assistant_manager_signature:
         pdf.image(vem.assistant_manager_signature.signature,100,238,20.32,20.32)
         pdf.line(126,256,47.5+pdf.get_string_width(f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})"),256)
         pdf.text(87.5,259,f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if vem.lab_manager_signature:
         pdf.image(vem.lab_manager_signature.signature,178,235,20.32,20.32)
         pdf.line(155,256,165+pdf.get_string_width(f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})"),256)
         pdf.text(160,259,f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})")

     
     


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,260,-10+pdf.w,260)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,271,txt="• Report is valid for current batch (sample).")
     pdf.text(10,274.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(275.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(279)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(282)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,263,19,15)
     # if vem.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)
     # if vem.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if vem.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)
     # if vem.location =='PEQS':
     #      pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,263,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,280,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,280,txt="(Certificate # 080177424-EMS)")
     
     
     if vem.location == "NEQS" and (vem.city_location or "").lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vem.location == "NEQS" and (vem.city_location or "").lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 262, 25, 16)
          pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif vem.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vem.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 262, 25, 16)
          pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,263,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:     
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     pdf.text(128.5,280,txt="(Certificate # 080177324-QMS)")
     pdf.text(182,280,txt="(Certificate # 080177424-EMS)")
     
     
     

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,281,25,5)
     pdf.text(128,284,txt=vem.ww_doc_con_1)
     pdf.rect(151,281,29,5)
     pdf.text(155,284,txt=vem.ww_doc_con_2)
     pdf.rect(180,281,25,5)
     pdf.text(186.5,284,txt=vem.ww_doc_con_3)

     
     if vem.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(vem, f'pdf_image_{i}')
               desc = getattr(vem, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         pass

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=vem.pdf_heading,align="C")
          pdf.set_font("Arial", size=10)
          
          pdf.set_y(85)
          

          if count == 1:
               img = images[0]
               # pdf.multi_cell(0, 10, txt=img['desc'], align='C')
               pdf.image(img['path'], x=(pdf.w-180)/2, y=pdf.get_y(), w=180,h=160)
               pdf.set_y(246)
               text = img['desc']
               text_width = pdf.get_string_width(text) + 4  # Add some padding

               # Calculate X to center the text box
               x_centered = (pdf.w - text_width) / 2

               # Set X and write the centered text
               pdf.set_x(x_centered)
               pdf.multi_cell(text_width, 10, txt=text, align='C')
          
          elif count == 2:
               w, h = 80, 80
               spacing = 3  # Space between image and text
               for img in images:
                    pdf.set_font("Arial", size=10)

                    # Get current Y
                    y_current = pdf.get_y()

                    # Center image
                    x_image = (pdf.w - w) / 2
                    pdf.image(img['path'], x=x_image, y=y_current, w=w, h=h)

                    # Move below image
                    pdf.set_y(y_current + h + spacing)

                    # Prepare text
                    text = img['desc']
                    text_width = pdf.get_string_width(text) + 4  # Padding
                    x_text = (pdf.w - text_width) / 2

                    # Center text
                    pdf.set_x(x_text)
                    pdf.multi_cell(text_width, 10, txt=text, align='C')

                    # Add vertical space before next image-text pair
                    pdf.ln(10)


          elif count == 4:
               w, h = 90, 60
               x_coords = [10, 110]
               y_base = pdf.get_y()
               spacing = 3  # space between image and text

               for i, img in enumerate(images):
                    x = x_coords[i % 2]
                    y = y_base + (i // 2) * (h + 20 + 10)  # Extra space for text
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Move below image for text
                    text_y = y + h + spacing
                    pdf.set_xy(x, text_y)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(w, 8, txt=img['desc'], align='C')

          elif count in [3, 5, 6]:
               w, h = 60, 50
               spacing = 10  # Vertical spacing between image-text blocks
               col_spacing = 10  # Horizontal spacing between columns
               num_cols = 2

               total_width = (w * num_cols) + col_spacing
               page_width = pdf.w - 20  # Adjust for left/right margins
               start_x = (page_width - total_width) / 2 + 10  # +10 for left margin
               x_coords = [start_x, start_x + w + col_spacing]

               y_base = pdf.get_y()

               for idx, img in enumerate(images):
                    col = idx % 2
                    row = idx // 2

                    x = x_coords[col]
                    y = y_base + row * (h + spacing + 10)  # 10 for text height

                    # Draw image
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Draw description
                    if img['desc']:
                         pdf.set_xy(x, y + h + 2)
                         pdf.set_font("Arial", size=9)
                         pdf.multi_cell(w, 5, txt=img['desc'], border=0, align='C')


          else:
               # Fallback: One below another
               for img in images:
                    pdf.cell(0, 10, txt=img['desc'], ln=True)
                    pdf.image(img['path'], x=10, y=pdf.get_y(), w=40)
                    pdf.ln(60)


     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)

     # file_path = './wasteWater/'
     # pdf.output(file_path + vem.lab_report_no +'.pdf')
     # pdf = open(file_path + vem.lab_report_no +'.pdf', 'rb')

     # response = FileResponse(pdf)
     # return response
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={vem.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response
     
     
     
     
def wasteWaterPdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_wasteWaterPdf1 as PDFWithPageNumbers




     vem = WasteWaterSludge.objects.get(id=pk)
     num_rows = 0
     row=None
     table=None
     if vem.zdhc == 'zdhc':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result","ZDHC Limits"],
          ]
          sr_no = 1
          if vem.ww_sr1:
               a = [str(sr_no),"Cadmium (Cd)","*APHA 3111- B","mg/Kg",vem.ww_sr1,"01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr2:
               a = [str(sr_no),"Copper (Cu)","*APHA 3111- B","mg/Kg",vem.ww_sr2,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr3:
               a = [str(sr_no),"Iron (Fe)","*APHA 3111- B","mg/Kg",vem.ww_sr3,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr4:
               a = [str(sr_no),"Boron (B)","HACH 8015","mg/Kg",vem.ww_sr4,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr5:
               a = [str(sr_no),"Lead (Pb)","*APHA 3111- B","mg/Kg",vem.ww_sr5,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr6:
               a = [str(sr_no),"Mercury (Hg)","*APHA 3112- B","mg/Kg",vem.ww_sr6,"01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr7:
               a = [str(sr_no),"Selenium (Se)","*APHA 3114- B","mg/Kg",vem.ww_sr7,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr8:
               a = [str(sr_no),"Silver (Ag)","*APHA 3111- B","mg/Kg",vem.ww_sr8,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr9:
               a = [str(sr_no),"Nickel (Ni)","*APHA 3111- B","mg/Kg",vem.ww_sr9,"20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr10:
               a = [str(sr_no),"Zinc (Zn)","*APHA 3111- B","mg/Kg",vem.ww_sr10,"400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr11:
               a = [str(sr_no),"Arsenic (As)","*APHA 3114- B","mg/Kg",vem.ww_sr11,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr12:
               a = [str(sr_no),"Manganese (Mn)","*APHA 3111- B","mg/Kg",vem.ww_sr12,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr13:
               a = [str(sr_no),"Chromium","*APHA 3111- B","mg/Kg",vem.ww_sr13,"50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr14:
               a = [str(sr_no),"Antimony","*APHA 3111- B","mg/Kg",vem.ww_sr14,"05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr15:
               a = [str(sr_no),"Cobalt","*APHA 3111- B","mg/Kg",vem.ww_sr15,"400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr16:
               a = [str(sr_no),"Barium","HACH 8014","mg/Kg",vem.ww_sr16,"200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if vem.ww_sr17:
               a = [str(sr_no),"Chromium (VI)","HACH 8023","mg/Kg",vem.ww_sr17,"20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)                              




          pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                   address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                   ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                   ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                   )
          pdf._rq_request, pdf._rq_pk = request, pk
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)










          
          #report data table
          with pdf.table(col_widths=(6, 45, 30,30,30,20),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows+=1
                    # if k == 0:
                    #      data_row[4] = vem.ambienAir_select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     
     else:
          if vem.zdhc == 'no-zdhc':
               TABLE_DATA = [
               ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result"],
               ]
               sr_no = 1
               if vem.ww_sr1:
                    a = [str(sr_no),"Cadmium (Cd)","*APHA 3111- B","mg/Kg",vem.ww_sr1]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr2:
                    a = [str(sr_no),"Copper (Cu)","*APHA 3111- B","mg/Kg",vem.ww_sr2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr3:
                    a = [str(sr_no),"Iron (Fe)","*APHA 3111- B","mg/Kg",vem.ww_sr3]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr4:
                    a = [str(sr_no),"Boron (B)","HACH 8015","mg/Kg",vem.ww_sr4]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr5:
                    a = [str(sr_no),"Lead (Pb)","*APHA 3111- B","mg/Kg",vem.ww_sr5]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr6:
                    a = [str(sr_no),"Mercury (Hg)","*APHA 3112- B","mg/Kg",vem.ww_sr6]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr7:
                    a = [str(sr_no),"Selenium (Se)","*APHA 3114- B","mg/Kg",vem.ww_sr7]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr8:
                    a = [str(sr_no),"Silver (Ag)","*APHA 3111- B","mg/Kg",vem.ww_sr8]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr9:
                    a = [str(sr_no),"Nickel (Ni)","*APHA 3111- B","mg/Kg",vem.ww_sr9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr10:
                    a = [str(sr_no),"Zinc (Zn)","*APHA 3111- B","mg/Kg",vem.ww_sr10]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr11:
                    a = [str(sr_no),"Arsenic (As)","*APHA 3114- B","mg/Kg",vem.ww_sr11]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr12:
                    a = [str(sr_no),"Manganese (Mn)","*APHA 3111- B","mg/Kg",vem.ww_sr12]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr13:
                    a = [str(sr_no),"Chromium","*APHA 3111- B","mg/Kg",vem.ww_sr13]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr14:
                    a = [str(sr_no),"Antimony","*APHA 3111- B","mg/Kg",vem.ww_sr14]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr15:
                    a = [str(sr_no),"Cobalt","*APHA 3111- B","mg/Kg",vem.ww_sr15]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr16:
                    a = [str(sr_no),"Barium","HACH 8014","mg/Kg",vem.ww_sr16]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
               if vem.ww_sr17:
                    a = [str(sr_no),"Chromium (VI)","HACH 8023","mg/Kg",vem.ww_sr17]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)                              




               pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                        address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                        ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                        ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                        )
               pdf._rq_request, pdf._rq_pk = request, pk
               pdf.add_page()
               font_path = "static/fonts/calibri.ttf"
               font_path_bold = "static/fonts/calibrib.ttf"
               pdf.add_font("Calibri","",font_path,uni=True)
               pdf.add_font("Calibri","B",font_path_bold,uni=True)
               pdf.set_font("Calibri","", 9)
               pdf.set_auto_page_break(auto=True,margin=5)










               
               #report data table
               with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




                    for k in range(0,len(TABLE_DATA)):
                         data_row = TABLE_DATA[k]
                         num_rows+=1
                         # if k == 0:
                         #      data_row[4] = vem.ambienAir_select + " Limits"

                         # watwer mark
                         # pdf.set_page_background("static/assets/Capture.PNG")
                         row = table.row()
                         for i in range(0,len(data_row)):
                              datum = data_row[i]

                              row.cell(datum)


     # data after Table

     # if num_rows >=10 and num_rows <=14:

     #      pdf.add_page()

     if 'pdf' not in locals():
         pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                                  address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,ww_sample_colec_Date=vem.ww_sample_colec_Date,
                                  ww_sample_desc=vem.ww_sample_desc,ww_sample_type=vem.ww_sample_type,ww_sample_colec_by=vem.ww_sample_colec_by,ww_date_of_analy_from=vem.ww_date_of_analy_from,
                                  ww_date_of_analy_to=vem.ww_date_of_analy_to,ww_test_desc=vem.ww_test_desc

                                  )
         pdf._rq_request, pdf._rq_pk = request, pk
         pdf.add_page()
         font_path = "static/fonts/calibri.ttf"
         font_path_bold = "static/fonts/calibrib.ttf"
         pdf.add_font("Calibri","",font_path,uni=True)
         pdf.add_font("Calibri","B",font_path_bold,uni=True)
         pdf.set_font("Calibri","", 9)
         pdf.set_auto_page_break(auto=True,margin=5)
     if num_rows >=16:
               pdf.add_page()
     
     
     Table_Data1 = [
          
     ]
     if vem.ww_editnote:
          a=["Note: "+vem.ww_editnote] 
          Table_Data1.append(a)
          
     
     with pdf.table(col_widths=(190,), line_height=2, text_align=("LEFT")) as table:
          for data_row in Table_Data1:
               row = table.row()
               for datum in data_row:
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')
               
     
     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if vem.ww_legend_1:
          a = [vem.ww_legend_1]
          Table_data_legend.append(a)
          
     if vem.ww_legend_2:
          a = [vem.ww_legend_2]
          Table_data_legend.append(a)
          
     if vem.ww_legend_3:
          a = [vem.ww_legend_3]
          Table_data_legend.append(a)
          
     if vem.ww_legend_4:
          a = [vem.ww_legend_4]
          Table_data_legend.append(a)
     

     if vem.ww_legend_5:
          a = [vem.ww_legend_5]
          Table_data_legend.append(a)
          
     if vem.ww_legend_6:
          a = [vem.ww_legend_6]
          Table_data_legend.append(a)
          
     if vem.ww_legend_7:
          a = [vem.ww_legend_7]
          Table_data_legend.append(a)
          
     if vem.ww_legend_8:
          a = [vem.ww_legend_8]
          Table_data_legend.append(a)
          
     if vem.ww_legend_9:
          a = [vem.ww_legend_9]
          Table_data_legend.append(a)
          
     if vem.ww_legend_10:
          a = [vem.ww_legend_10]
          Table_data_legend.append(a)
          
     if vem.ww_legend_11:
          a = [vem.ww_legend_11]
          Table_data_legend.append(a)
          

     if vem.ww_custom_legend:
          a = [vem.ww_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L') 


     if vem.analyst_signature:
         pdf.image(vem.analyst_signature.signature,30,238,20.32,20.32)
         pdf.line(19,256,36+pdf.get_string_width(f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})"),256)
         pdf.text(26,259,f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})")
     if vem.assistant_manager_signature:
         pdf.image(vem.assistant_manager_signature.signature,100,238,20.32,20.32)
         pdf.line(126,256,47.5+pdf.get_string_width(f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})"),256)
         pdf.text(87.5,259,f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if vem.lab_manager_signature:
         pdf.image(vem.lab_manager_signature.signature,178,235,20.32,20.32)
         pdf.line(155,256,165+pdf.get_string_width(f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})"),256)
         pdf.text(160,259,f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,260,-10+pdf.w,260)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,271,txt="• Report is valid for current batch (sample).")
     pdf.text(10,274.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(275.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(279)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(282)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,263,19,15)
     # if vem.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)
     # if vem.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if vem.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)
     # if vem.location =='PEQS':
     #      pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,263,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,280,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,280,txt="(Certificate # 080177424-EMS)")
     
     
     if vem.location == "NEQS" and (vem.city_location or "").lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vem.location == "NEQS" and (vem.city_location or "").lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 262, 25, 16)
          pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif vem.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vem.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 262, 25, 16)
          pdf.text(155,280,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,263,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,263,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:     
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     pdf.text(128.5,280,txt="(Certificate # 080177324-QMS)")
     pdf.text(182,280,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,281,25,5)
     pdf.text(128,284,txt=vem.ww_doc_con_1)
     pdf.rect(151,281,29,5)
     pdf.text(155,284,txt=vem.ww_doc_con_2)
     pdf.rect(180,281,25,5)
     pdf.text(186.5,284,txt=vem.ww_doc_con_3)

     if vem.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(vem, f'pdf_image_{i}')
               desc = getattr(vem, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         pass

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=vem.pdf_heading,align="C")
          pdf.set_font("Arial", size=10)
          
          pdf.set_y(85)
          

          if count == 1:
               img = images[0]
               # pdf.multi_cell(0, 10, txt=img['desc'], align='C')
               pdf.image(img['path'], x=(pdf.w-180)/2, y=pdf.get_y(), w=180,h=160)
               pdf.set_y(246)
               text = img['desc']
               text_width = pdf.get_string_width(text) + 4  # Add some padding

               # Calculate X to center the text box
               x_centered = (pdf.w - text_width) / 2

               # Set X and write the centered text
               pdf.set_x(x_centered)
               pdf.multi_cell(text_width, 10, txt=text, align='C')
          
          elif count == 2:
               w, h = 80, 80
               spacing = 3  # Space between image and text
               for img in images:
                    pdf.set_font("Arial", size=10)

                    # Get current Y
                    y_current = pdf.get_y()

                    # Center image
                    x_image = (pdf.w - w) / 2
                    pdf.image(img['path'], x=x_image, y=y_current, w=w, h=h)

                    # Move below image
                    pdf.set_y(y_current + h + spacing)

                    # Prepare text
                    text = img['desc']
                    text_width = pdf.get_string_width(text) + 4  # Padding
                    x_text = (pdf.w - text_width) / 2

                    # Center text
                    pdf.set_x(x_text)
                    pdf.multi_cell(text_width, 10, txt=text, align='C')

                    # Add vertical space before next image-text pair
                    pdf.ln(10)


          elif count == 4:
               w, h = 90, 60
               x_coords = [10, 110]
               y_base = pdf.get_y()
               spacing = 3  # space between image and text

               for i, img in enumerate(images):
                    x = x_coords[i % 2]
                    y = y_base + (i // 2) * (h + 20 + 10)  # Extra space for text
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Move below image for text
                    text_y = y + h + spacing
                    pdf.set_xy(x, text_y)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(w, 8, txt=img['desc'], align='C')

          elif count in [3, 5, 6]:
               w, h = 60, 50
               spacing = 10  # Vertical spacing between image-text blocks
               col_spacing = 10  # Horizontal spacing between columns
               num_cols = 2

               total_width = (w * num_cols) + col_spacing
               page_width = pdf.w - 20  # Adjust for left/right margins
               start_x = (page_width - total_width) / 2 + 10  # +10 for left margin
               x_coords = [start_x, start_x + w + col_spacing]

               y_base = pdf.get_y()

               for idx, img in enumerate(images):
                    col = idx % 2
                    row = idx // 2

                    x = x_coords[col]
                    y = y_base + row * (h + spacing + 10)  # 10 for text height

                    # Draw image
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Draw description
                    if img['desc']:
                         pdf.set_xy(x, y + h + 2)
                         pdf.set_font("Arial", size=9)
                         pdf.multi_cell(w, 5, txt=img['desc'], border=0, align='C')


          else:
               # Fallback: One below another
               for img in images:
                    pdf.cell(0, 10, txt=img['desc'], ln=True)
                    pdf.image(img['path'], x=10, y=pdf.get_y(), w=40)
                    pdf.ln(60)

     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)

     # file_path = '/home/django/EnviTechAlApp/ww_pdf/'

     # pdf.output(file_path + vem.lab_report_no +'.pdf')

     # pdf = open(file_path + vem.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={vem.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response



@login_required(login_url="/login")
def wasteWAter2List(request):
     ww, _srch = _list_filter(request, WasteWaterForm2)
     context = {'searched':_srch, 'data':ww}
     return render(request,"wasteWater2List.html",context)

@login_required(login_url="/login")
def wasteWAter2Delete(request,pk):
     ww = WasteWaterForm2.objects.get(id=pk)
     ww.delete()
     user = request.user
     action = f'Waste Water 2 Form {ww.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("wasteWater2List")

@login_required(login_url="/login")
def wasteWAter2Edit(request,pk):
     ww = WasteWaterForm2.objects.get(id=pk)
     # ww.extra_field = ww.extra_field.replace("'", "\"")
     ww.extra_field = json.loads(ww.extra_field)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(ww, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':ww,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"wasteWater2Edit.html",context)

@login_required(login_url="/login")
def wasteWAter2Update(request,pk):
     ww = WasteWaterForm2.objects.get(id=pk)
     if request.method == 'POST':
          ww.location = request.POST['location']
          industry_id = request.POST.get('industry')
          ww.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          ww.lab_report_no = request.POST['lab_rep_no']
          ww.invoice_bill_no = request.POST['invoice_no']
          ww.reporting_date = request.POST['repo_date']
          ww.report_to = request.POST['report_to']
          ww.address = request.POST['address']
          ww.attention = request.POST['attention']
          ww.email = request.POST['email']
          ww.sample_id = request.POST['sampleId']
          ww.sample_Col_date = request.POST['sample_Col_date']
          ww.sample_desc = request.POST['sample_desc']
          ww.sampling_method = request.POST['sampling_method']
          ww.sample_type = request.POST['sample_type']
          ww.sample_collected_by = request.POST['sample_collected_by']
          ww.date_of_analysis_from = request.POST['date_of_analysis_from']
          ww.date_of_analysis_to = request.POST['date_of_analysis_to']
          ww.test_description = request.POST['test_description']
          ww.select = request.POST.get('select')
          ww.result_1 = request.POST['result_1']
          ww.result_1_1 = request.POST['result_1_1']
          ww.result_2 = request.POST['result_2']
          ww.result_2_2 = request.POST['result_2_2']
          ww.result_3 = request.POST['result_3']
          ww.result_3_3 = request.POST['result_3_3']
          ww.result_4 = request.POST['result_4']
          ww.result_4_4 = request.POST['result_4_4']
          ww.result_5 = request.POST['result_5']
          ww.result_5_5 = request.POST['result_5_5']
          ww.result_6 = request.POST['result_6']
          ww.result_6_6 = request.POST['result_6_6']
          ww.result_7 = request.POST['result_7']
          ww.result_7_7 = request.POST['result_7_7']
          ww.metho_select = request.POST.get('metho_select')
          ww.result_8 = request.POST['result_8']
          ww.result_8_8 = request.POST['result_8_8']
          ww.result_9 = request.POST['result_9']
          ww.result_9_9 = request.POST['result_9_9']
          ww.result_10 = request.POST['result_10']
          ww.result_10_10 = request.POST['result_10_10']
          ww.result_11 = request.POST['result_11']
          ww.result_11_11= request.POST['result_11_11']
          ww.result_12 = request.POST['result_12']
          ww.result_12_12 = request.POST['result_12_12']
          ww.result_13 = request.POST['result_13']
          ww.result_13_13 = request.POST['result_13_13']
          ww.result_14 = request.POST['result_14']
          ww.result_14_14 = request.POST['result_14_14']
          ww.result_15 = request.POST['result_15']
          ww.result_15_15 = request.POST['result_15_15']
          ww.result_16 = request.POST['result_16']
          ww.result_16_16 = request.POST['result_16_16']
          ww.result_17 = request.POST['result_17']
          ww.result_17_17 = request.POST['result_17_17']
          ww.result_18 = request.POST['result_18']
          ww.result_18_18 = request.POST['result_18_18']
          ww.result_19 = request.POST['result_19']
          ww.result_19_19 = request.POST['result_19_19']
          ww.result_20 = request.POST['result_20']
          ww.result_20_20 = request.POST['result_20_20']
          ww.result_21 = request.POST['result_21']
          ww.result_21_21 = request.POST['result_21_21']
          ww.result_22 = request.POST['result_22']
          ww.result_22_22 = request.POST['result_22_22']
          ww.result_23 = request.POST['result_23']
          ww.result_23_23 = request.POST['result_23_23']
          ww.result_24 = request.POST['result_24']
          ww.result_24_24 = request.POST['result_24_24']
          ww.result_25 = request.POST['result_25']
          ww.result_25_25 = request.POST['result_25_25']
          ww.result_26 = request.POST['result_26']
          ww.result_26_26 = request.POST['result_26_26']
          ww.result_27 = request.POST['result_27']
          ww.result_27_27 = request.POST['result_27_27']
          ww.result_28 = request.POST['result_28']
          ww.result_28_28 = request.POST['result_28_28']
          ww.result_29 = request.POST['result_29']
          ww.result_29_29 = request.POST['result_29_29']
          ww.result_30 = request.POST['result_30']
          ww.result_30_30 = request.POST['result_30_30']
          ww.result_31 = request.POST['result_31']
          ww.result_31_31 = request.POST['result_31_31']
          ww.result_32 = request.POST['result_32']
          ww.result_32_32 = request.POST['result_32_32']
          ww.legend_1 = request.POST['legend_1']
          ww.legend_2 = request.POST['legend_2']
          ww.legend_3 = request.POST['legend_3']
          ww.legend_4 = request.POST['legend_4']
          ww.legend_5 = request.POST['legend_5']
          ww.legend_6 = request.POST['legend_6']
          ww.legend_7 = request.POST['legend_7']
          ww.legend_8 = request.POST['legend_8']
          ww.legend_9 = request.POST['legend_9']
          ww.legend_10 = request.POST['legend_10']
          ww.legend_11 = request.POST['legend_11']
          ww.editNote = request.POST['editNote']
          ww.customlegend = request.POST['customlegend']
          ww.doc1 = request.POST['doc1']
          ww.doc2 = request.POST['doc2']
          ww.doc3 = request.POST['doc3']
          ww.created_by = request.user
          # ww.analyzedby = request.FILES['analyzedby']
          # ww.reviewedby = request.FILES['reviewedby']
          # ww.approvedby = request.FILES['approvedby']
          # ww.approvedby1 = request.FILES['approvedby1']
          ww.in_out = request.POST['in_out']
          ww.inlet_result = request.POST['inlet_result']
          ww.outlet_result = request.POST.get('outlet_result')
          ww.extra_field = json.loads(request.POST['extra_field'])
          if ww.in_out == 'in-out':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    ww.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "outlet":outlet,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })
          elif ww.in_out == 'in':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    ww.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })
          elif ww.in_out == 'out':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    ww.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "outlet": outlet,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })          

          elif ww.in_out == 'inlet_customlimits':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    customLimits = request.POST.getlist('customLimits[]')[i]

                    ww.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "customLimits":customLimits
                    }) 
          elif ww.in_out == 'outlet_customLimits':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    customLimits = request.POST.getlist('customLimits[]')[i]

                    ww.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "outlet": outlet,
                         "customLimits":customLimits
                    })           
          ww.extra_field = json.dumps(ww.extra_field)          
          ww.cutomLimit1 = request.POST['cutomLimit1'] 
          ww.cutomLimit2 = request.POST['cutomLimit2'] 
          ww.cutomLimit3 = request.POST['cutomLimit3'] 
          ww.cutomLimit4 = request.POST['cutomLimit4'] 
          ww.cutomLimit5 = request.POST['cutomLimit5'] 
          ww.cutomLimit6 = request.POST['cutomLimit6'] 
          ww.cutomLimit7 = request.POST['cutomLimit7'] 
          ww.cutomLimit8 = request.POST['cutomLimit8'] 
          ww.cutomLimit9 = request.POST['cutomLimit9'] 
          ww.cutomLimit10 = request.POST['cutomLimit10'] 
          ww.cutomLimit11 = request.POST['cutomLimit11'] 
          ww.cutomLimit12 = request.POST['cutomLimit12'] 
          ww.cutomLimit13 = request.POST['cutomLimit13'] 
          ww.cutomLimit14 = request.POST['cutomLimit14'] 
          ww.cutomLimit15 = request.POST['cutomLimit15'] 
          ww.cutomLimit16 = request.POST['cutomLimit16'] 
          ww.cutomLimit17 = request.POST['cutomLimit17'] 
          ww.cutomLimit18 = request.POST['cutomLimit18'] 
          ww.cutomLimit18 = request.POST['cutomLimit18'] 
          ww.cutomLimit19 = request.POST['cutomLimit19'] 
          ww.cutomLimit20 = request.POST['cutomLimit20'] 
          ww.cutomLimit21 = request.POST['cutomLimit21'] 
          ww.cutomLimit22 = request.POST['cutomLimit22'] 
          ww.cutomLimit23 = request.POST['cutomLimit23'] 
          ww.cutomLimit24 = request.POST['cutomLimit24'] 
          ww.cutomLimit25 = request.POST['cutomLimit25'] 
          ww.cutomLimit26 = request.POST['cutomLimit26'] 
          ww.cutomLimit27 = request.POST['cutomLimit27'] 
          ww.cutomLimit28 = request.POST['cutomLimit28'] 
          ww.cutomLimit29 = request.POST['cutomLimit29'] 
          ww.cutomLimit30 = request.POST['cutomLimit30'] 
          ww.cutomLimit31 = request.POST['cutomLimit31']
          ww.cutomLimit32 = request.POST['cutomLimit32']
          ww.cutomLimit33 = request.POST['cutomLimit33']
          ww.city_location = request.POST['city_location']
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          ww.analyst_signature = analyst_sign
          ww.assistant_manager_signature = review_sign
          ww.lab_manager_signature = approved_sign

          
          ww.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(ww, image_key, '')
                    setattr(ww, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(ww, image_key, base64_encoded)
                         setattr(ww, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(ww, desc_key, description)

          ww.save()
          user = request.user
          action = f'Waste Water 2 Form {ww.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = ww.id
          if "submit_and_view" in request.POST:
               url = f"/wasteWater2-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="wasteWater2List")
     return redirect("wasteWater2List")



def wasteWAter2View(request,pk):
     ww = WasteWaterForm2.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     ww.extra_field = ww.extra_field.replace("'", "\"")
     ww.extra_field = json.loads(ww.extra_field)

     # Generate a unique file name for the QR code
     qr_filename = f"qr_{ww.lab_report_no}.png"
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
     context = {'data': ww,'qr':qr_relative_path,'logo':logo}

     return render(request,'wasteWater2Report.html',context)



def wasteWater2Pdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_wasteWater2Pdf as PDFWithPageNumbers




     ww = WasteWaterForm2.objects.get(id=pk)
     ww.extra_field = ww.extra_field.replace("'", "\"")
     ww.extra_field = json.loads(ww.extra_field)

     pdf = PDFWithPageNumbers(lab_report_no=ww.lab_report_no,invoice_bill_no=ww.invoice_bill_no,reporting_date=ww.reporting_date,report_to=ww.report_to,
                                   address=ww.address,attention=ww.attention,email=ww.email,sample_id=ww.sample_id,sample_Col_date=ww.sample_Col_date,
                                   sample_desc=ww.sample_desc,sample_type=ww.sample_type,sample_collected_by=ww.sample_collected_by,test_description = ww.test_description,
                                   date_of_analysis_from=ww.date_of_analysis_from,date_of_analysis_to=ww.date_of_analysis_to,sampling_method = ww.sampling_method
                                   )
     pdf._rq_request, pdf._rq_pk = request, pk
     table = None
     if ww.in_out == 'in':
          
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",ww.inlet_result,"","",""],
     ]
          sr_no = 1

          if ww.result_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2 and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2 and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2 and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_3 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif  ww.result_3 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_4 and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4 and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4 and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5 and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5 and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5 and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_6 and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6 and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6 and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7 and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7 and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7 and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9 and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9 and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9 and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_10 and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10 and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10 and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_11 and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11 and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11 and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_12 and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12 and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12 and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_13 and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13 and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13 and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_14 and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14 and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14 and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_15 and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15 and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15 and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16 and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16 and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16 and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17 and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17 and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17 and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18 and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18 and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18 and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_19 and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19 and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19 and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20 and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20 and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20 and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_21 and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21 and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21 and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22 and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22 and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22 and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23 and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23 and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23 and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_24 and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24 and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24 and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25 and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_26 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27 and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27 and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27 and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_28 and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28 and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28 and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_29 and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29 and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29 and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30 and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30 and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30 and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31 and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31 and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31 and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_32 and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32 and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32 and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          #      a = [str(sr_no), extra_field.get("parameters"), extra_field.get("methods"), extra_field.get("unit"), extra_field.get("result"), extra_field.get("lim1"),extra_field.get("lim2"),extra_field.get("lim3")]
          #      sr_no = sr_no+1
          #      TABLE_DATA.append(a)
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               lim1 = extra_field.get("lim1")
               lim2 = extra_field.get("lim2")
               lim3 = extra_field.get("lim3")

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, lim1,lim2,lim3]
                    sr_no += 1
                    TABLE_DATA.append(a)






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)








          num_rows =0

          
          with pdf.table(col_widths=(10, 50, 30,15,30,9,9,9),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
              

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[5] = ww.select + " 1"
                         data_row[6] = ww.select + " 2"
                         data_row[7] = ww.select + " 3"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     
     elif ww.in_out == 'out':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",(ww.outlet_result or "Outlet Results"),"","",""],
     ]
          sr_no = 1

          if ww.result_1_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2_2 and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2_2 and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2_2 and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3_3 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_3_3 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif  ww.result_3_3 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_4_4 and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4_4 and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4_4 and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5_5 and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5_5 and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5_5 and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_6_6 and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6_6 and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6_6 and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7_7 and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7_7 and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7_7 and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9_9 and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9_9 and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9_9 and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_10_10 and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10_10 and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10_10 and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_11_11 and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11_11 and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11_11 and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_12_12 and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12_12 and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12_12 and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_13_13 and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13_13 and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13_13 and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_14_14 and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14_14 and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14_14 and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_15_15 and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15_15 and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15_15 and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16_16 and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16_16 and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16_16 and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17_17 and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17_17 and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17_17 and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18_18 and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18_18 and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18_18 and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_19_19 and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19_19 and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19_19 and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20_20 and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20_20 and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20_20 and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_21_21 and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21_21 and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21_21 and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22_22 and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22_22 and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22_22 and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23_23 and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23_23 and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23_23 and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_24_24 and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24_24 and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24_24 and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25_25 and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_26_26 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26_26 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26_26 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27_27 and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27_27 and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27_27 and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_28_28 and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28_28 and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28_28 and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_29_29 and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29_29 and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29_29 and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30_30 and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30_30 and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30_30 and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31_31 and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31_31 and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31_31 and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_32_32 and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32_32 and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32_32 and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               outlet = extra_field.get("outlet")
               lim1 = extra_field.get("lim1")
               lim2 = extra_field.get("lim2")
               lim3 = extra_field.get("lim3")

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, outlet, lim1,lim2,lim3]
                    sr_no += 1
                    TABLE_DATA.append(a)     






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,15,15,15),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[5] = ww.select + ' 1'
                         data_row[6] = ww.select + ' 2'
                         data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)



     elif ww.in_out == 'outlet_customLimits':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",(ww.outlet_result or "Outlet Results"),ww.cutomLimit1],
     ]
          sr_no = 1

          if ww.result_1_1:
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,ww.cutomLimit2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2_2:
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2_2,ww.cutomLimit3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3_3:
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,ww.cutomLimit4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_4_4:
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,ww.cutomLimit5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5_5:
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,ww.cutomLimit6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_6_6:
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,ww.cutomLimit7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7_7:
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,ww.cutomLimit8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8_8:
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8_8:
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8_8:
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9_9:
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,ww.cutomLimit10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
     

          if ww.result_10_10:
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,ww.cutomLimit11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_11_11:
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,ww.cutomLimit12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

         
          if ww.result_12_12:
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,ww.cutomLimit13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          if ww.result_13_13:
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,ww.cutomLimit14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_14_14:
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,ww.cutomLimit15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)



          if ww.result_15_15:
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,ww.cutomLimit16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16_16:
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,ww.cutomLimit17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17_17:
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,ww.cutomLimit18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18_18:
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,ww.cutomLimit19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_19_19:
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,ww.cutomLimit20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20_20:
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,ww.cutomLimit21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_21_21:
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,ww.cutomLimit22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22_22:
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,ww.cutomLimit23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23_23:
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,ww.cutomLimit24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_24_24:
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,ww.cutomLimit25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25_25:
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,ww.cutomLimit26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_26_26:
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,ww.cutomLimit27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27_27:
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,ww.cutomLimit28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_28_28:
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,ww.cutomLimit29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_29_29:
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,ww.cutomLimit30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30_30:
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,ww.cutomLimit31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31_31:
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,ww.cutomLimit32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_32_32:
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,ww.cutomLimit33]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               outlet = extra_field.get("outlet")
               customLimits = extra_field.get("customLimits")
               

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, outlet, customLimits]
                    sr_no += 1
                    TABLE_DATA.append(a)





     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    # if k == 0:
                    #      data_row[5] = ww.select + ' 1'
                    #      data_row[6] = ww.select + ' 2'
                    #      data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)





     elif ww.in_out == 'inlet_customlimits':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",ww.inlet_result,ww.cutomLimit1],
     ]
          sr_no = 1

          if ww.result_1:
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.cutomLimit2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2:
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,ww.cutomLimit3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3:
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.cutomLimit4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_4:
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.cutomLimit5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5:
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.cutomLimit6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_6:
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.cutomLimit7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7:
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.cutomLimit8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8:
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8:
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8:
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9:
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.cutomLimit10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
     

          if ww.result_10:
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.cutomLimit11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_11:
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.cutomLimit12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

         
          if ww.result_12:
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.cutomLimit13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          if ww.result_13:
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.cutomLimit14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_14:
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.cutomLimit15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)



          if ww.result_15:
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.cutomLimit16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16:
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.cutomLimit17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17:
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.cutomLimit18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18:
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.cutomLimit19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_19:
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.cutomLimit20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20:
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.cutomLimit21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_21:
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.cutomLimit22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22:
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.cutomLimit23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23:
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.cutomLimit24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_24:
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.cutomLimit25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25:
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.cutomLimit26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_26:
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.cutomLimit27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27:
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.cutomLimit28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_28:
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.cutomLimit29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_29:
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.cutomLimit30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30:
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.cutomLimit31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31:
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.cutomLimit32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_32:
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.cutomLimit33]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               customLimits = extra_field.get("customLimits")
               

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, customLimits]
                    sr_no += 1
                    TABLE_DATA.append(a)     






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    # if k == 0:
                    #      data_row[5] = ww.select + ' 1'
                    #      data_row[6] = ww.select + ' 2'
                    #      data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)



     
     else:
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Inlet Results",(ww.outlet_result or "Outlet Result"),"","",""],
     ]
          sr_no = 1

          if ww.result_1 or ww.result_1_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if (ww.result_2 or ww.result_2_2) and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_2 or ww.result_2_2) and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_2 or ww.result_2_2) and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_3 or ww.result_3_3) and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_3 or ww.result_3_3) and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_3 or ww.result_3_3) and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_4 or ww.result_4_4) and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_4 or ww.result_4_4) and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_4 or ww.result_4_4) and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_5 or ww.result_5_5) and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_5 or ww.result_5_5) and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif(ww.result_5 or ww.result_5_5) and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_6 or ww.result_6_6) and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_6 or ww.result_6_6) and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_6 or ww.result_6_6) and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_7 or ww.result_7_7) and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_7 or ww.result_7_7) and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_7 or ww.result_7_7) and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if (ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if (ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if(ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if (ww.result_9 or ww.result_9_9) and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_9 or ww.result_9_9) and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_9 or ww.result_9_9) and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if (ww.result_10 or ww.result_10_10) and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_10 or ww.result_10_10) and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_10 or ww.result_10_10) and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_11 or ww.result_11_11) and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_11 or ww.result_11_11) and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_11 or ww.result_11_11) and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_12 or ww.result_12_12) and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_12 or ww.result_12_12) and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_12 or ww.result_12_12) and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_13 or ww.result_13_13) and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_13 or ww.result_13_13) and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_13 or ww.result_13_13) and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_14 or ww.result_14_14) and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_14 or ww.result_14_14) and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_14 or ww.result_14_14) and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_15 or ww.result_15_15) and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_15 or ww.result_15_15) and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_15 or ww.result_15_15) and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_16 or ww.result_16_16) and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_16 or ww.result_16_16) and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_16 or ww.result_16_16) and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_17 or ww.result_17_17) and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_17 or ww.result_17_17) and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_17 or ww.result_17_17) and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_18 or ww.result_18_18) and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_18 or ww.result_18_18) and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_18 or ww.result_18_18) and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_19 or ww.result_19_19) and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_19 or ww.result_19_19) and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_19 or ww.result_19_19) and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if (ww.result_20 or ww.result_20_20) and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_20 or ww.result_20_20) and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          
          elif (ww.result_20 or ww.result_20_20) and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_21 or ww.result_21_21) and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_21 or ww.result_21_21) and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_21 or ww.result_21_21) and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_22 or ww.result_22_22) and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_22 or ww.result_22_22) and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_22 or ww.result_22_22) and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_23 or ww.result_23_23) and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_23 or ww.result_23_23) and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_23 or ww.result_23_23) and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_24 or ww.result_24_24) and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_24 or ww.result_24_24) and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_24 or ww.result_24_24) and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_25 or ww.result_25_25) and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_26 or ww.result_26_26) and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_26 or ww.result_26_26) and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_26 or ww.result_26_26) and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_27 or ww.result_27_27) and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_27 or ww.result_27_27) and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_27 or ww.result_27_27) and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_28 or ww.result_28_28) and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_28 or ww.result_28_28) and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_28 or ww.result_28_28) and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_29 or ww.result_29_29) and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_29 or ww.result_29_29) and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_29 or ww.result_29_29) and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_30 or ww.result_30_30) and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_30 or ww.result_30_30) and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_30 or ww.result_30_30) and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_31 or ww.result_31_31) and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_31 or ww.result_31_31) and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_31 or ww.result_31_31) and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_32 or ww.result_32_32) and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_32 or ww.result_32_32) and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_32 or ww.result_32_32) and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          # for extra_field in ww.extra_field:
          #      a = [str(sr_no), extra_field.get("parameters"), extra_field.get("methods"), extra_field.get("unit"),extra_field.get("result"), extra_field.get("outlet"), extra_field.get("lim1"),extra_field.get("lim2"),extra_field.get("lim3")]
          #      sr_no = sr_no+1
          #      TABLE_DATA.append(a)

          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               outlet = extra_field.get("outlet")
               lim1 = extra_field.get("lim1")
               lim2 = extra_field.get("lim2")
               lim3 = extra_field.get("lim3")
               

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result,outlet,lim1,lim2,lim3]
                    sr_no += 1
                    TABLE_DATA.append(a)          
          

          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=5)








          
          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30,10,10,10),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[6] = ww.select + ' 1'
                         data_row[7] = ww.select + ' 2'
                         data_row[8] = ww.select + ' 3'
                              

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     

                                          
     number_of_rows = len(TABLE_DATA)  # Replace with the actual number of rows
     row_height = 8  # Replace with the actual row height in your table
     table_height = (number_of_rows) * row_height   
     
     if pdf.y + number_of_rows * row_height >= pdf.h:
          pdf.add_page()        
         
     Table_Data1 = [
          
     ]
     if ww.editNote:
          a=["Note: "+ww.editNote] 
          Table_Data1.append(a)
          
     
     # with pdf.table(col_widths=(190),width=190,line_height=6,text_align=("LEFT")) as table:
         
          for k in range(0,len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if ww.legend_1:
          a = [ww.legend_1]
          Table_data_legend.append(a)
          
     if ww.legend_2:
          a = [ww.legend_2]
          Table_data_legend.append(a)
          
     if ww.legend_3:
          a = [ww.legend_3]
          Table_data_legend.append(a)
          
     if ww.legend_4:
          a = [ww.legend_4]
          Table_data_legend.append(a)
          
     if ww.legend_5:
          a = [ww.legend_5]
          Table_data_legend.append(a)
          
     if ww.legend_6:
          a = [ww.legend_6]
          Table_data_legend.append(a)
          
     if ww.legend_7:
          a = [ww.legend_7]
          Table_data_legend.append(a)
          
     if ww.legend_8:
          a = [ww.legend_8]
          Table_data_legend.append(a)
          
     if ww.legend_9:
          a = [ww.legend_9]
          Table_data_legend.append(a)
          
     if ww.legend_10:
          a = [ww.legend_10]
          Table_data_legend.append(a)
          
     if ww.legend_11:
          a = [ww.legend_11]
          Table_data_legend.append(a)
          

     if ww.customlegend:
          a = [ww.customlegend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L') 
                          

    
     # pdf.image(ww.analyst_signature.signature,30,235,20.32,20.32)
     # pdf.line(19,253,36+pdf.get_string_width("Analyzed By (Analyst)"),253)
     # pdf.text(26,257,"Analyzed By (Analyst)")
     # pdf.image(ww.assistant_manager_signature.signature,100,235,20.32,20.32)
     # pdf.line(126,253,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),253)
     # pdf.text(87.5,257,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,150,231,22,22)
     # pdf.image(ww.lab_manager_signature.signature,178,235,20.32,20.32)
     # pdf.line(155,253,165+pdf.get_string_width("Approved By (Lab Manager)"),253)
     # pdf.text(160,257,"Approved By (Lab Manager)")
     
     
     if ww.analyst_signature:
         pdf.image(ww.analyst_signature.signature,30,235,20.32,20.32)
     pdf.line(19,253,36+pdf.get_string_width(f"Analyzed By ({(ww.analyst_signature.role if ww.analyst_signature else '')})"),253)
     pdf.text(26,257,f"Analyzed By ({(ww.analyst_signature.role if ww.analyst_signature else '')})")
     if ww.assistant_manager_signature:
         pdf.image(ww.assistant_manager_signature.signature,100,235,20.32,20.32)
     pdf.line(126,253,47.5+pdf.get_string_width(f"Reviewed By ({(ww.assistant_manager_signature.role if ww.assistant_manager_signature else '')})"),253)
     pdf.text(87.5,257,f"Reviewed By ({(ww.assistant_manager_signature.role if ww.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,231,22,22)
     if ww.lab_manager_signature:
         pdf.image(ww.lab_manager_signature.signature,178,231,20.32,20.32)
     pdf.line(155,253,165+pdf.get_string_width(f"Approved By ({(ww.lab_manager_signature.role if ww.lab_manager_signature else '')})"),253)
     pdf.text(160,257,f"Approved By ({(ww.lab_manager_signature.role if ww.lab_manager_signature else '')})")

    

     pdf.set_font("Calibri","B", 9)
     pdf.line(10,259,-10+pdf.w,259)
     pdf.text(10,262,txt="Disclaimer:")
     pdf.set_font("Calibri","", 8)
     pdf.text(10,266,txt="• Report is valid for current batch (sample).")
     pdf.text(10,269.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(270.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(274)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(278)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,260,19,15)
     # if ww.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,260,19,15)
     # if ww.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,259,21,17) 
     # if ww.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,260,19,15)
     # if ww.location =='PEQS':
     #      pdf.text(155,277,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,277,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,260,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,277,txt="(Certificate # 080177324-QMS)")
     # pdf.text(183,277,txt="(Certificate # 080177424-EMS)")
     
     
     if ww.location == "NEQS" and ww.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 260, 19, 15)
          pdf.text(152,277,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")

     elif ww.location == "NEQS" and ww.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 155, 259, 21, 17)
          pdf.text(155,277,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     elif ww.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,260,19,15)
          pdf.text(152,277,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     elif ww.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',155,259,21,17)
          pdf.text(155,277,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,260,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,260,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,277,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,277,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(128.5,277,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,277,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,278,25,5)
     pdf.text(128,281,txt=ww.doc1)
     pdf.rect(151,278,29,5)
     pdf.text(155,281,txt=ww.doc2)
     pdf.rect(180,278,25,5)
     pdf.text(184.5,281,txt=ww.doc3)
     
     if ww.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ww, f'pdf_image_{i}')
               desc = getattr(ww, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         pass

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=ww.pdf_heading,align="C")
          pdf.set_font("Arial", size=10)
          
          pdf.set_y(85)
          

          if count == 1:
               img = images[0]
               # pdf.multi_cell(0, 10, txt=img['desc'], align='C')
               pdf.image(img['path'], x=(pdf.w-180)/2, y=pdf.get_y(), w=180,h=160)
               pdf.set_y(246)
               text = img['desc']
               text_width = pdf.get_string_width(text) + 4  # Add some padding

               # Calculate X to center the text box
               x_centered = (pdf.w - text_width) / 2

               # Set X and write the centered text
               pdf.set_x(x_centered)
               pdf.multi_cell(text_width, 10, txt=text, align='C')
          
          elif count == 2:
               w, h = 80, 80
               spacing = 3  # Space between image and text
               for img in images:
                    pdf.set_font("Arial", size=10)

                    # Get current Y
                    y_current = pdf.get_y()

                    # Center image
                    x_image = (pdf.w - w) / 2
                    pdf.image(img['path'], x=x_image, y=y_current, w=w, h=h)

                    # Move below image
                    pdf.set_y(y_current + h + spacing)

                    # Prepare text
                    text = img['desc']
                    text_width = pdf.get_string_width(text) + 4  # Padding
                    x_text = (pdf.w - text_width) / 2

                    # Center text
                    pdf.set_x(x_text)
                    pdf.multi_cell(text_width, 10, txt=text, align='C')

                    # Add vertical space before next image-text pair
                    pdf.ln(10)


          elif count == 4:
               w, h = 90, 60
               x_coords = [10, 110]
               y_base = pdf.get_y()
               spacing = 3  # space between image and text

               for i, img in enumerate(images):
                    x = x_coords[i % 2]
                    y = y_base + (i // 2) * (h + 20 + 10)  # Extra space for text
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Move below image for text
                    text_y = y + h + spacing
                    pdf.set_xy(x, text_y)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(w, 8, txt=img['desc'], align='C')

          elif count in [3, 5, 6]:
               w, h = 60, 50
               spacing = 10  # Vertical spacing between image-text blocks
               col_spacing = 10  # Horizontal spacing between columns
               num_cols = 2

               total_width = (w * num_cols) + col_spacing
               page_width = pdf.w - 20  # Adjust for left/right margins
               start_x = (page_width - total_width) / 2 + 10  # +10 for left margin
               x_coords = [start_x, start_x + w + col_spacing]

               y_base = pdf.get_y()

               for idx, img in enumerate(images):
                    col = idx % 2
                    row = idx // 2

                    x = x_coords[col]
                    y = y_base + row * (h + spacing + 10)  # 10 for text height

                    # Draw image
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Draw description
                    if img['desc']:
                         pdf.set_xy(x, y + h + 2)
                         pdf.set_font("Arial", size=9)
                         pdf.multi_cell(w, 5, txt=img['desc'], border=0, align='C')


          else:
               # Fallback: One below another
               for img in images:
                    pdf.cell(0, 10, txt=img['desc'], ln=True)
                    pdf.image(img['path'], x=10, y=pdf.get_y(), w=40)
                    pdf.ln(60)



     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)

     # file_path = '/home/django/EnviTechAlApp/wasteWater2/'
     # pdf.output(file_path + ww.lab_report_no +'.pdf')
     # pdf = open(file_path + ww.lab_report_no +'.pdf', 'rb')

     
     # response = FileResponse(pdf)
     # return response
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ww.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def wasteWater2Pdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_wasteWater2Pdf1 as PDFWithPageNumbers




     ww = WasteWaterForm2.objects.get(id=pk)
     ww.extra_field = ww.extra_field.replace("'", "\"")
     ww.extra_field = json.loads(ww.extra_field)

     pdf = PDFWithPageNumbers(lab_report_no=ww.lab_report_no,invoice_bill_no=ww.invoice_bill_no,reporting_date=ww.reporting_date,report_to=ww.report_to,
                                   address=ww.address,attention=ww.attention,email=ww.email,sample_id=ww.sample_id,sample_Col_date=ww.sample_Col_date,
                                   sample_desc=ww.sample_desc,sample_type=ww.sample_type,sample_collected_by=ww.sample_collected_by,test_description = ww.test_description,
                                   date_of_analysis_from=ww.date_of_analysis_from,date_of_analysis_to=ww.date_of_analysis_to,sampling_method = ww.sampling_method
                                   )
     pdf._rq_request, pdf._rq_pk = request, pk
     table = None
     if ww.in_out == 'in':
          
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",ww.inlet_result,"","",""],
     ]
          sr_no = 1

          if ww.result_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2 and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2 and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2 and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_3 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif  ww.result_3 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_4 and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4 and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4 and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5 and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5 and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5 and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_6 and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6 and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6 and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7 and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7 and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7 and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8 and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8 and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9 and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9 and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9 and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_10 and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10 and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10 and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_11 and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11 and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11 and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_12 and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12 and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12 and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_13 and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13 and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13 and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_14 and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14 and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14 and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_15 and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15 and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15 and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16 and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16 and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16 and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17 and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17 and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17 and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18 and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18 and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18 and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_19 and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19 and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19 and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20 and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20 and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20 and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_21 and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21 and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21 and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22 and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22 and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22 and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23 and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23 and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23 and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_24 and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24 and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24 and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25 and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_26 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27 and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27 and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27 and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_28 and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28 and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28 and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_29 and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29 and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29 and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30 and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30 and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30 and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31 and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31 and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31 and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_32 and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32 and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32 and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          #      a = [str(sr_no), extra_field.get("parameters"), extra_field.get("methods"), extra_field.get("unit"), extra_field.get("result"), extra_field.get("lim1"),extra_field.get("lim2"),extra_field.get("lim3")]
          #      sr_no = sr_no+1
          #      TABLE_DATA.append(a)
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               lim1 = extra_field.get("lim1")
               lim2 = extra_field.get("lim2")
               lim3 = extra_field.get("lim3")

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, lim1,lim2,lim3]
                    sr_no += 1
                    TABLE_DATA.append(a)






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=15)








          num_rows =0

          
          with pdf.table(col_widths=(10, 50, 30,15,30,9,9,9),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
              

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[5] = ww.select + " 1"
                         data_row[6] = ww.select + " 2"
                         data_row[7] = ww.select + " 3"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     
     elif ww.in_out == 'out':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",(ww.outlet_result or "Outlet Results"),"","",""],
     ]
          sr_no = 1

          if ww.result_1_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2_2 and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2_2 and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_2_2 and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3_3 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_3_3 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif  ww.result_3_3 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_4_4 and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4_4 and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_4_4 and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5_5 and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5_5 and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_5_5 and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_6_6 and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6_6 and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_6_6 and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7_7 and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7_7 and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_7_7 and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8_8 and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif ww.result_8_8 and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9_9 and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9_9 and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_9_9 and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_10_10 and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10_10 and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_10_10 and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_11_11 and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11_11 and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_11_11 and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_12_12 and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12_12 and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_12_12 and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_13_13 and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13_13 and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_13_13 and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_14_14 and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14_14 and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_14_14 and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_15_15 and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15_15 and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_15_15 and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16_16 and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16_16 and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_16_16 and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17_17 and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17_17 and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_17_17 and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18_18 and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18_18 and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_18_18 and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_19_19 and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19_19 and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_19_19 and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20_20 and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20_20 and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_20_20 and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_21_21 and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21_21 and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_21_21 and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22_22 and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22_22 and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_22_22 and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23_23 and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23_23 and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_23_23 and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_24_24 and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24_24 and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_24_24 and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25_25 and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_26_26 and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26_26 and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_26_26 and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27_27 and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27_27 and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_27_27 and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_28_28 and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28_28 and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_28_28 and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_29_29 and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29_29 and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_29_29 and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30_30 and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30_30 and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_30_30 and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31_31 and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31_31 and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_31_31 and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_32_32 and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32_32 and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_32_32 and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               outlet = extra_field.get("outlet")
               lim1 = extra_field.get("lim1")
               lim2 = extra_field.get("lim2")
               lim3 = extra_field.get("lim3")

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, outlet, lim1,lim2,lim3]
                    sr_no += 1
                    TABLE_DATA.append(a)     






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=15)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,15,15,15),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[5] = ww.select + ' 1'
                         data_row[6] = ww.select + ' 2'
                         data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)



     elif ww.in_out == 'outlet_customLimits':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",(ww.outlet_result or "Outlet Results"),ww.cutomLimit1],
     ]
          sr_no = 1

          if ww.result_1_1:
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1_1,ww.cutomLimit2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2_2:
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2_2,ww.cutomLimit3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3_3:
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3_3,ww.cutomLimit4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_4_4:
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4_4,ww.cutomLimit5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5_5:
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5_5,ww.cutomLimit6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_6_6:
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6_6,ww.cutomLimit7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7_7:
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7_7,ww.cutomLimit8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8_8:
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8_8:
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8_8:
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9_9:
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9_9,ww.cutomLimit10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
     

          if ww.result_10_10:
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10_10,ww.cutomLimit11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_11_11:
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11_11,ww.cutomLimit12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

         
          if ww.result_12_12:
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12_12,ww.cutomLimit13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          if ww.result_13_13:
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13_13,ww.cutomLimit14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_14_14:
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14_14,ww.cutomLimit15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)



          if ww.result_15_15:
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15_15,ww.cutomLimit16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16_16:
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16_16,ww.cutomLimit17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17_17:
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17_17,ww.cutomLimit18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18_18:
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18_18,ww.cutomLimit19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_19_19:
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19_19,ww.cutomLimit20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20_20:
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20_20,ww.cutomLimit21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_21_21:
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21_21,ww.cutomLimit22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22_22:
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22_22,ww.cutomLimit23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23_23:
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23_23,ww.cutomLimit24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_24_24:
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24_24,ww.cutomLimit25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25_25:
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25_25,ww.cutomLimit26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_26_26:
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26_26,ww.cutomLimit27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27_27:
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27_27,ww.cutomLimit28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_28_28:
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28_28,ww.cutomLimit29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_29_29:
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29_29,ww.cutomLimit30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30_30:
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30_30,ww.cutomLimit31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31_31:
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31_31,ww.cutomLimit32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_32_32:
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32_32,ww.cutomLimit33]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               outlet = extra_field.get("outlet")
               customLimits = extra_field.get("customLimits")
               

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, outlet, customLimits]
                    sr_no += 1
                    TABLE_DATA.append(a)





     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=15)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    # if k == 0:
                    #      data_row[5] = ww.select + ' 1'
                    #      data_row[6] = ww.select + ' 2'
                    #      data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)





     elif ww.in_out == 'inlet_customlimits':
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit",ww.inlet_result,ww.cutomLimit1],
     ]
          sr_no = 1

          if ww.result_1:
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.cutomLimit2]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if ww.result_2:
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,ww.cutomLimit3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_3:
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.cutomLimit4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_4:
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.cutomLimit5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_5:
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.cutomLimit6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_6:
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.cutomLimit7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if ww.result_7:
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.cutomLimit8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if ww.result_8:
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if ww.result_8:
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if ww.result_8:
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.cutomLimit9]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if ww.result_9:
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.cutomLimit10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
     

          if ww.result_10:
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.cutomLimit11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if ww.result_11:
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.cutomLimit12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

         
          if ww.result_12:
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.cutomLimit13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          if ww.result_13:
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.cutomLimit14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_14:
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.cutomLimit15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)



          if ww.result_15:
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.cutomLimit16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_16:
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.cutomLimit17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_17:
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.cutomLimit18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_18:
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.cutomLimit19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_19:
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.cutomLimit20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_20:
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.cutomLimit21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_21:
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.cutomLimit22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_22:
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.cutomLimit23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_23:
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.cutomLimit24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_24:
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.cutomLimit25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_25:
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.cutomLimit26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_26:
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.cutomLimit27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_27:
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.cutomLimit28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_28:
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.cutomLimit29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_29:
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.cutomLimit30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_30:
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.cutomLimit31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if ww.result_31:
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.cutomLimit32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          if ww.result_32:
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.cutomLimit33]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          
          for extra_field in ww.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               customLimits = extra_field.get("customLimits")
               

               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, customLimits]
                    sr_no += 1
                    TABLE_DATA.append(a)     






     
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=12)








          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    # if k == 0:
                    #      data_row[5] = ww.select + ' 1'
                    #      data_row[6] = ww.select + ' 2'
                    #      data_row[7] = ww.select + ' 3'

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)



     
     else:
          TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Inlet Results",(ww.outlet_result or "Outlet Result"),"","",""],
     ]
          sr_no = 1

          if ww.result_1 or ww.result_1_1:
               if ww.select =="SEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","≤ 3C"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="PEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

               elif ww.select =="NEQS":
                    a = [str(sr_no),"Temperature 40°C","*APHA 2550","°C",ww.result_1,ww.result_1_1,"≤ 3C","≤ 3C","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          

          if (ww.result_2 or ww.result_2_2) and ww.select =="SEQS":
               a = [str(sr_no),"pH","*APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","6-9"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_2 or ww.result_2_2) and ww.select =="PEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_2 or ww.result_2_2) and ww.select =="NEQS":
               a = [str(sr_no),"pH","APHA 4500 H-B","-",ww.result_2,ww.result_2_2,"6-9","6-9","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_3 or ww.result_3_3) and ww.select =="SEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_3 or ww.result_3_3) and ww.select =="PEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_3 or ww.result_3_3) and ww.select =="NEQS":
               a = [str(sr_no),"Sulphide","*APHA 4500-S2-D","mg/L",ww.result_3,ww.result_3_3,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_4 or ww.result_4_4) and ww.select =="SEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","80"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_4 or ww.result_4_4) and ww.select =="PEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_4 or ww.result_4_4) and ww.select =="NEQS":
               a = [str(sr_no),"Biological Oxygen Demand(BOD)5","HACH 10099","mg/L",ww.result_4,ww.result_4_4,"80","250","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_5 or ww.result_5_5) and ww.select =="SEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","400"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_5 or ww.result_5_5) and ww.select =="PEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif(ww.result_5 or ww.result_5_5) and ww.select =="NEQS":
               a = [str(sr_no),"Chemical Oxygen Demand(COD)","*HACH 8000","mg/L",ww.result_5,ww.result_5_5,"150","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          

          if (ww.result_6 or ww.result_6_6) and ww.select =="SEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","3500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_6 or ww.result_6_6) and ww.select =="PEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_6 or ww.result_6_6) and ww.select =="NEQS":
               a = [str(sr_no),"Total Dissolved Solids (TDS)","*APHA 2540-C","mg/L",ww.result_6,ww.result_6_6,"3500","3500","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_7 or ww.result_7_7) and ww.select =="SEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","200"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_7 or ww.result_7_7) and ww.select =="PEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_7 or ww.result_7_7) and ww.select =="NEQS":
               a = [str(sr_no),"Total Suspended Solids (TSS)","*APHA 2540-D","mg/L",ww.result_7,ww.result_7_7,"200","400","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if (ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="ASTM":
                    a = [str(sr_no),"Oil & Grease","ASTM D-3291","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
                    

          if (ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="USEPA":
                    a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)
          if(ww.result_8 or ww.result_8_8) and ww.select =="SEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","10"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="PEQS":
               if ww.metho_select == "APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          elif (ww.result_8 or ww.result_8_8) and ww.select =="NEQS":
               if ww.metho_select =="APHA":
                    a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",ww.result_8,ww.result_8_8,"10","10","-"]
                    sr_no = sr_no+1
                    TABLE_DATA.append(a)

          

          if (ww.result_9 or ww.result_9_9) and ww.select =="SEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","0.1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_9 or ww.result_9_9) and ww.select =="PEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_9 or ww.result_9_9) and ww.select =="NEQS":
               a = [str(sr_no),"Cadmium","*APHA 3111-B","mg/L",ww.result_9,ww.result_9_9,"0.1","0.1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

     

          if (ww.result_10 or ww.result_10_10) and ww.select =="SEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_10 or ww.result_10_10) and ww.select =="PEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_10 or ww.result_10_10) and ww.select =="NEQS":
               a = [str(sr_no),"Copper","*APHA 3111-B","mg/L",ww.result_10,ww.result_10_10,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          

          if (ww.result_11 or ww.result_11_11) and ww.select =="SEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","8"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_11 or ww.result_11_11) and ww.select =="PEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_11 or ww.result_11_11) and ww.select =="NEQS":
               a = [str(sr_no),"Iron","*APHA 3111-B","mg/L",ww.result_11,ww.result_11_11,"8","8","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_12 or ww.result_12_12) and ww.select =="SEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_12 or ww.result_12_12) and ww.select =="PEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_12 or ww.result_12_12) and ww.select =="NEQS":
               a = [str(sr_no),"Lead","*APHA 3111-B","mg/L",ww.result_12,ww.result_12_12,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_13 or ww.result_13_13) and ww.select =="SEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_13 or ww.result_13_13) and ww.select =="PEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_13 or ww.result_13_13) and ww.select =="NEQS":
               a = [str(sr_no),"Manganese","*APHA 3111-B","mg/L",ww.result_13,ww.result_13_13,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_14 or ww.result_14_14) and ww.select =="SEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_14 or ww.result_14_14) and ww.select =="PEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_14 or ww.result_14_14) and ww.select =="NEQS":
               a = [str(sr_no),"Mercury","*APHA 3112-B","mg/L",ww.result_14,ww.result_14_14,"0.01","0.01","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_15 or ww.result_15_15) and ww.select =="SEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_15 or ww.result_15_15) and ww.select =="PEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_15 or ww.result_15_15) and ww.select =="NEQS":
               a = [str(sr_no),"Nickel","*APHA 3111-B","mg/L",ww.result_15,ww.result_15_15,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_16 or ww.result_16_16) and ww.select =="SEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_16 or ww.result_16_16) and ww.select =="PEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_16 or ww.result_16_16) and ww.select =="NEQS":
               a = [str(sr_no),"Selenium","*APHA 3114-B","mg/L",ww.result_16,ww.result_16_16,"0.5","0.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_17 or ww.result_17_17) and ww.select =="SEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_17 or ww.result_17_17) and ww.select =="PEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_17 or ww.result_17_17) and ww.select =="NEQS":
               a = [str(sr_no),"Chromium","*APHA 3111-B","mg/L",ww.result_17,ww.result_17_17,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_18 or ww.result_18_18) and ww.select =="SEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_18 or ww.result_18_18) and ww.select =="PEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_18 or ww.result_18_18) and ww.select =="NEQS":
               a = [str(sr_no),"Zinc","*APHA 3111-B","mg/L",ww.result_18,ww.result_18_18,"5","5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_19 or ww.result_19_19) and ww.select =="SEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_19 or ww.result_19_19) and ww.select =="PEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_19 or ww.result_19_19) and ww.select =="NEQS":
               a = [str(sr_no),"Arsenic","*APHA 3114-B","mg/L",ww.result_19,ww.result_19_19,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_20 or ww.result_20_20) and ww.select =="SEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_20 or ww.result_20_20) and ww.select =="PEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_20 or ww.result_20_20) and ww.select =="NEQS":
               a = [str(sr_no),"Chlorine","HACH 10069","mg/L",ww.result_20,ww.result_20_20,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_21 or ww.result_21_21) and ww.select =="SEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_21 or ww.result_21_21) and ww.select =="PEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_21 or ww.result_21_21) and ww.select =="NEQS":
               a = [str(sr_no),"Chloride","*APHA 4500 CL-B","mg/L",ww.result_21,ww.result_21_21,"1000","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_22 or ww.result_22_22) and ww.select =="SEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_22 or ww.result_22_22) and ww.select =="PEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_22 or ww.result_22_22) and ww.select =="NEQS":
               a = [str(sr_no),"Cyanide","HACH 8027","mg/L",ww.result_22,ww.result_22_22,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_23 or ww.result_23_23) and ww.select =="SEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","10"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_23 or ww.result_23_23) and ww.select =="PEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_23 or ww.result_23_23) and ww.select =="NEQS":
               a = [str(sr_no),"Fluoride","*HACH 8029","mg/L",ww.result_23,ww.result_23_23,"10","10","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_24 or ww.result_24_24) and ww.select =="SEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","40"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_24 or ww.result_24_24) and ww.select =="PEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_24 or ww.result_24_24) and ww.select =="NEQS":
               a = [str(sr_no),"Ammonia","*HACH 8038","mg/L",ww.result_24,ww.result_24_24,"40","40","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_25 or ww.result_25_25) and ww.select =="SEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="PEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif ww.result_25 and ww.select =="NEQS":
               a = [str(sr_no),"Total Toxic Metals","APHA 3111","mg/L",ww.result_25,ww.result_25_25,"2","2","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_26 or ww.result_26_26) and ww.select =="SEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","**SC"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_26 or ww.result_26_26) and ww.select =="PEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_26 or ww.result_26_26) and ww.select =="NEQS":
               a = [str(sr_no),"Sulphate","HACH 8051","mg/L",ww.result_26,ww.result_26_26,"600","1000","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_27 or ww.result_27_27) and ww.select =="SEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","20"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_27 or ww.result_27_27) and ww.select =="PEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_27 or ww.result_27_27) and ww.select =="NEQS":
               a = [str(sr_no),"An Ionic Detergent As MBAs","*APHA 5540 C","mg/L",ww.result_27,ww.result_27_27,"20","20","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_28 or ww.result_28_28) and ww.select =="SEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","0.15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_28 or ww.result_28_28) and ww.select =="PEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_28 or ww.result_28_28) and ww.select =="NEQS":
               a = [str(sr_no),"Pesticides","USEPA-614.1","mg/L",ww.result_28,ww.result_28_28,"0.15","0.15","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_29 or ww.result_29_29) and ww.select =="SEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_29 or ww.result_29_29) and ww.select =="PEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_29 or ww.result_29_29) and ww.select =="NEQS":
               a = [str(sr_no),"Phenolic Compounds(as Phenol)","HACH 8047","mg/L",ww.result_29,ww.result_29_29,"0.1","0.3","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_30 or ww.result_30_30) and ww.select =="SEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","6"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_30 or ww.result_30_30) and ww.select =="PEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_30 or ww.result_30_30) and ww.select =="NEQS":
               a = [str(sr_no),"Boron","HACH 8015","mg/L",ww.result_30,ww.result_30_30,"6","6","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_31 or ww.result_31_31) and ww.select =="SEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_31 or ww.result_31_31) and ww.select =="PEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_31 or ww.result_31_31) and ww.select =="NEQS":
               a = [str(sr_no),"Barium","HACH 8014","mg/L",ww.result_31,ww.result_31_31,"1.5","1.5","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)


          if (ww.result_32 or ww.result_32_32) and ww.select =="SEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","1"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_32 or ww.result_32_32) and ww.select =="PEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          elif (ww.result_32 or ww.result_32_32) and ww.select =="NEQS":
               a = [str(sr_no),"Silver","*APHA 3111-B","mg/L",ww.result_32,ww.result_32_32,"1","1","-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          for extra_field in ww.extra_field:
               a = [str(sr_no), extra_field.get("parameters"), extra_field.get("methods"), extra_field.get("unit"),extra_field.get("result"), extra_field.get("outlet"), extra_field.get("lim1"),extra_field.get("lim2"),extra_field.get("lim3")]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          # for extra_field in ww.extra_field:
          #      parameters = extra_field.get("parameters")
          #      methods = extra_field.get("methods")
          #      unit = extra_field.get("unit")
          #      result = extra_field.get("result")
          #      outlet = extra_field.get("outlet")
          #      lim1 = extra_field.get("lim1")
          #      lim2 = extra_field.get("lim2")
          #      lim3 = extra_field.get("lim3")
               

          #      # Check if the "parameters" field is not empty before adding the row
          #      if parameters:
          #           a = [str(sr_no), parameters, methods, unit, result,outlet,lim1,lim2,lim3]
          #           sr_no += 1
          #           TABLE_DATA.append(a)          
          

          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True,margin=15)








          
          num_rows =0
          
          with pdf.table(col_widths=(10, 50, 30,15,30,30,10,10,10),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER')) as table:
               # row = table.row()
               # row.cell(7,colspan=2)

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")

               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    if k == 0:
                         data_row[6] = ww.select + ' 1'
                         data_row[7] = ww.select + ' 2'
                         data_row[8] = ww.select + ' 3'
                              

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)

     
     number_of_rows = len(TABLE_DATA)  # Replace with the actual number of rows
     row_height = 4  # Replace with the actual row height in your table
     table_height = (number_of_rows) * row_height  
     
     if pdf.y + number_of_rows * row_height >= pdf.h:
          pdf.add_page()             
     
                                          
     num_rows =0
     if num_rows >= 11 or num_rows >=30:
          pdf.add_page()
         
     Table_Data1 = [
          
     ]
     if ww.editNote:
          a=["Note: "+ww.editNote] 
          Table_Data1.append(a)
          
     
     # with pdf.table(col_widths=(190),width=190,line_height=6,text_align=("LEFT")) as table:
         
          for k in range(0,len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     Table_data_legend = []

     # Set font size
     pdf.set_font_size(8)

     # Build the table data
     if ww.legend_1:
          Table_data_legend.append([ww.legend_1])
     if ww.legend_2:
          Table_data_legend.append([ww.legend_2])
     if ww.legend_3:
          Table_data_legend.append([ww.legend_3])
     if ww.legend_4:
          Table_data_legend.append([ww.legend_4])
     if ww.legend_5:
          Table_data_legend.append([ww.legend_5])
     if ww.legend_6:
          Table_data_legend.append([ww.legend_6])
     if ww.legend_7:
          Table_data_legend.append([ww.legend_7])
     if ww.legend_8:
          Table_data_legend.append([ww.legend_8])
     if ww.legend_9:
          Table_data_legend.append([ww.legend_9])
     if ww.legend_10:
          Table_data_legend.append([ww.legend_10])
     if ww.legend_11:
          Table_data_legend.append([ww.legend_11])
     if ww.customlegend:
          Table_data_legend.append([ww.customlegend])

     # Set bottom margin (space to leave before page break)
     bottom_margin = 50  # Adjust as needed

     # Process each row
     for k in range(0, len(Table_data_legend)):
          data_row = Table_data_legend[k]
          
          # Check if adding this row would exceed the page bottom
          current_y = pdf.get_y()
          row_height = 4  # Height of each row in mm
          
          if current_y + row_height > pdf.h - bottom_margin:
               pdf.add_page()  # Add new page
               
          
          # Add to table and PDF
          row = table.row()
          for i in range(0, len(data_row)):
               datum = data_row[i]
               row.cell(datum)
               pdf.cell(190, row_height, datum, border=0, ln=True, align='L')

          
     # pdf.image(ww.analyst_signature.signature,30,234,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(ww.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,150,229,22,22)
     # pdf.image(ww.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if ww.analyst_signature:
         pdf.image(ww.analyst_signature.signature,30,234,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(ww.analyst_signature.role if ww.analyst_signature else '')})"),252)
     pdf.text(26,256,f"Analyzed By ({(ww.analyst_signature.role if ww.analyst_signature else '')})")
     if ww.assistant_manager_signature:
         pdf.image(ww.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(ww.assistant_manager_signature.role if ww.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,256,f"Reviewed By ({(ww.assistant_manager_signature.role if ww.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,229,22,22)
     if ww.lab_manager_signature:
         pdf.image(ww.lab_manager_signature.signature,178,229,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(ww.lab_manager_signature.role if ww.lab_manager_signature else '')})"),252)
     pdf.text(160,256,f"Approved By ({(ww.lab_manager_signature.role if ww.lab_manager_signature else '')})")

    

     pdf.set_font("Calibri","B", 9)
     pdf.line(10,258,-10+pdf.w,258)
     pdf.text(10,261,txt="Disclaimer:")
     pdf.set_font("Calibri","", 8)
     pdf.text(10,265,txt="• Report is valid for current batch (sample).")
     pdf.text(10,268.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(269.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(273)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(277)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,259,19,15)
     # if ww.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if ww.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if ww.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if ww.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(183,276,txt="(Certificate # 080177424-EMS)")
     
     
     if ww.location == "NEQS" and ww.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")

     elif ww.location == "NEQS" and ww.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 155, 258, 21, 17)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     elif ww.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     elif ww.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',155,258,21,17)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=ww.doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=ww.doc2)
     pdf.rect(180,277,25,5)
     pdf.text(184.5,280,txt=ww.doc3)
     
     if ww.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ww, f'pdf_image_{i}')
               desc = getattr(ww, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         pass

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=ww.pdf_heading,align="C")
          pdf.set_font("Arial", size=10)
          
          pdf.set_y(85)
          

          if count == 1:
               img = images[0]
               # pdf.multi_cell(0, 10, txt=img['desc'], align='C')
               pdf.image(img['path'], x=(pdf.w-180)/2, y=pdf.get_y(), w=180,h=160)
               pdf.set_y(246)
               text = img['desc']
               text_width = pdf.get_string_width(text) + 4  # Add some padding

               # Calculate X to center the text box
               x_centered = (pdf.w - text_width) / 2

               # Set X and write the centered text
               pdf.set_x(x_centered)
               pdf.multi_cell(text_width, 10, txt=text, align='C')
          
          elif count == 2:
               w, h = 80, 80
               spacing = 3  # Space between image and text
               for img in images:
                    pdf.set_font("Arial", size=10)

                    # Get current Y
                    y_current = pdf.get_y()

                    # Center image
                    x_image = (pdf.w - w) / 2
                    pdf.image(img['path'], x=x_image, y=y_current, w=w, h=h)

                    # Move below image
                    pdf.set_y(y_current + h + spacing)

                    # Prepare text
                    text = img['desc']
                    text_width = pdf.get_string_width(text) + 4  # Padding
                    x_text = (pdf.w - text_width) / 2

                    # Center text
                    pdf.set_x(x_text)
                    pdf.multi_cell(text_width, 10, txt=text, align='C')

                    # Add vertical space before next image-text pair
                    pdf.ln(10)


          elif count == 4:
               w, h = 90, 60
               x_coords = [10, 110]
               y_base = pdf.get_y()
               spacing = 3  # space between image and text

               for i, img in enumerate(images):
                    x = x_coords[i % 2]
                    y = y_base + (i // 2) * (h + 20 + 10)  # Extra space for text
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Move below image for text
                    text_y = y + h + spacing
                    pdf.set_xy(x, text_y)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(w, 8, txt=img['desc'], align='C')

          elif count in [3, 5, 6]:
               w, h = 60, 50
               spacing = 10  # Vertical spacing between image-text blocks
               col_spacing = 10  # Horizontal spacing between columns
               num_cols = 2

               total_width = (w * num_cols) + col_spacing
               page_width = pdf.w - 20  # Adjust for left/right margins
               start_x = (page_width - total_width) / 2 + 10  # +10 for left margin
               x_coords = [start_x, start_x + w + col_spacing]

               y_base = pdf.get_y()

               for idx, img in enumerate(images):
                    col = idx % 2
                    row = idx // 2

                    x = x_coords[col]
                    y = y_base + row * (h + spacing + 10)  # 10 for text height

                    # Draw image
                    pdf.image(img['path'], x=x, y=y, w=w, h=h)

                    # Draw description
                    if img['desc']:
                         pdf.set_xy(x, y + h + 2)
                         pdf.set_font("Arial", size=9)
                         pdf.multi_cell(w, 5, txt=img['desc'], border=0, align='C')


          else:
               # Fallback: One below another
               for img in images:
                    pdf.cell(0, 10, txt=img['desc'], ln=True)
                    pdf.image(img['path'], x=10, y=pdf.get_y(), w=40)
                    pdf.ln(60)



     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)

     # file_path ='/home/django/EnviTechAlApp/ww2_pdf/'
     # pdf.output(file_path + ww.lab_report_no +'.pdf')

     # pdf = open(file_path + ww.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ww.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response


def wasteWater2clone(request,pk):
     existing_form = WasteWaterForm2.objects.get(id=pk)
     existing_form.extra_field = existing_form.extra_field.replace("'", "\"")
     existing_form.extra_field = json.loads(existing_form.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(existing_form, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':existing_form,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"WasteWaterForm2Clone.html",context)

def wasteWater2cloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = WasteWaterForm2.objects.get(id=pk)
     except WasteWaterForm2.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['invoice_no']
          existing_Form.reporting_date = request.POST['repo_date']
          existing_Form.report_to = request.POST['report_to']
          existing_Form.address = request.POST['address']
          existing_Form.attention = request.POST['attention']
          existing_Form.email = request.POST['email']
          existing_Form.sample_id = request.POST['sampleId']
          existing_Form.sample_Col_date = request.POST['sample_Col_date']
          existing_Form.sample_desc = request.POST['sample_desc']
          existing_Form.sampling_method = request.POST['sampling_method']
          existing_Form.sample_type = request.POST['sample_type']
          existing_Form.sample_collected_by = request.POST['sample_collected_by']
          existing_Form.date_of_analysis_from = request.POST['date_of_analysis_from']
          existing_Form.date_of_analysis_to = request.POST['date_of_analysis_to']
          existing_Form.test_description = request.POST['test_description']
          existing_Form.select = request.POST.get('select')
          existing_Form.result_1 = request.POST['result_1']
          existing_Form.result_1_1 = request.POST['result_1_1']
          existing_Form.result_2 = request.POST['result_2']
          existing_Form.result_2_2 = request.POST['result_2_2']
          existing_Form.result_3 = request.POST['result_3']
          existing_Form.result_3_3 = request.POST['result_3_3']
          existing_Form.result_4 = request.POST['result_4']
          existing_Form.result_4_4 = request.POST['result_4_4']
          existing_Form.result_5 = request.POST['result_5']
          existing_Form.result_5_5 = request.POST['result_5_5']
          existing_Form.result_6 = request.POST['result_6']
          existing_Form.result_6_6 = request.POST['result_6_6']
          existing_Form.result_7 = request.POST['result_7']
          existing_Form.result_7_7 = request.POST['result_7_7']
          existing_Form.metho_select = request.POST.get('metho_select')
          existing_Form.result_8 = request.POST['result_8']
          existing_Form.result_8_8 = request.POST['result_8_8']
          existing_Form.result_9 = request.POST['result_9']
          existing_Form.result_9_9 = request.POST['result_9_9']
          existing_Form.result_10 = request.POST['result_10']
          existing_Form.result_10_10 = request.POST['result_10_10']
          existing_Form.result_11 = request.POST['result_11']
          existing_Form.result_11_11= request.POST['result_11_11']
          existing_Form.result_12 = request.POST['result_12']
          existing_Form.result_12_12 = request.POST['result_12_12']
          existing_Form.result_13 = request.POST['result_13']
          existing_Form.result_13_13 = request.POST['result_13_13']
          existing_Form.result_14 = request.POST['result_14']
          existing_Form.result_14_14 = request.POST['result_14_14']
          existing_Form.result_15 = request.POST['result_15']
          existing_Form.result_15_15 = request.POST['result_15_15']
          existing_Form.result_16 = request.POST['result_16']
          existing_Form.result_16_16 = request.POST['result_16_16']
          existing_Form.result_17 = request.POST['result_17']
          existing_Form.result_17_17 = request.POST['result_17_17']
          existing_Form.result_18 = request.POST['result_18']
          existing_Form.result_18_18 = request.POST['result_18_18']
          existing_Form.result_19 = request.POST['result_19']
          existing_Form.result_19_19 = request.POST['result_19_19']
          existing_Form.result_20 = request.POST['result_20']
          existing_Form.result_20_20 = request.POST['result_20_20']
          existing_Form.result_21 = request.POST['result_21']
          existing_Form.result_21_21 = request.POST['result_21_21']
          existing_Form.result_22 = request.POST['result_22']
          existing_Form.result_22_22 = request.POST['result_22_22']
          existing_Form.result_23 = request.POST['result_23']
          existing_Form.result_23_23 = request.POST['result_23_23']
          existing_Form.result_24 = request.POST['result_24']
          existing_Form.result_24_24 = request.POST['result_24_24']
          existing_Form.result_25 = request.POST['result_25']
          existing_Form.result_25_25 = request.POST['result_25_25']
          existing_Form.result_26 = request.POST['result_26']
          existing_Form.result_26_26 = request.POST['result_26_26']
          existing_Form.result_27 = request.POST['result_27']
          existing_Form.result_27_27 = request.POST['result_27_27']
          existing_Form.result_28 = request.POST['result_28']
          existing_Form.result_28_28 = request.POST['result_28_28']
          existing_Form.result_29 = request.POST['result_29']
          existing_Form.result_29_29 = request.POST['result_29_29']
          existing_Form.result_30 = request.POST['result_30']
          existing_Form.result_30_30 = request.POST['result_30_30']
          existing_Form.result_31 = request.POST['result_31']
          existing_Form.result_31_31 = request.POST['result_31_31']
          existing_Form.result_32 = request.POST['result_32']
          existing_Form.result_32_32 = request.POST['result_32_32']
          existing_Form.legend_1 = request.POST['legend_1']
          existing_Form.legend_2 = request.POST['legend_2']
          existing_Form.legend_3 = request.POST['legend_3']
          existing_Form.legend_4 = request.POST['legend_4']
          existing_Form.legend_5 = request.POST['legend_5']
          existing_Form.legend_6 = request.POST['legend_6']
          existing_Form.legend_7 = request.POST['legend_7']
          existing_Form.legend_8 = request.POST['legend_8']
          existing_Form.legend_9 = request.POST['legend_9']
          existing_Form.legend_10 = request.POST['legend_10']
          existing_Form.legend_11 = request.POST['legend_11']
          existing_Form.editNote = request.POST['editNote']
          existing_Form.customlegend = request.POST['customlegend']
          existing_Form.doc1 = request.POST['doc1']
          existing_Form.doc2 = request.POST['doc2']
          existing_Form.doc3 = request.POST['doc3']
          existing_Form.created_by = request.user
          # existing_Form.analyzedby = request.FILES['analyzedby']
          # existing_Form.reviewedby = request.FILES['reviewedby']
          # existing_Form.approvedby = request.FILES['approvedby']
          # existing_Form.approvedby1 = request.FILES['approvedby1']
          existing_Form.in_out = request.POST['in_out']
          existing_Form.inlet_result = request.POST['inlet_result']
          existing_Form.outlet_result = request.POST.get('outlet_result')
          existing_Form.extra_field = json.loads(request.POST['extra_field'])
          if existing_Form.in_out == 'in-out':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "outlet":outlet,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })
          elif existing_Form.in_out == 'in':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })
          elif existing_Form.in_out == 'out':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    lim1 = request.POST.getlist('lim1[]')[i]
                    lim2 = request.POST.getlist('lim2[]')[i]
                    lim3 = request.POST.getlist('lim3[]')[i]

                    existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "outlet": outlet,
                         "lim1":lim1,
                         "lim2":lim2,
                         "lim3":lim3,
                    })          

          elif existing_Form.in_out == 'inlet_customlimits':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    result = request.POST.getlist('result[]')[i]
                    customLimits = request.POST.getlist('customLimits[]')[i]

                    existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "customLimits":customLimits
                    }) 
          elif existing_Form.in_out == 'outlet_customLimits':
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    parameters = request.POST.getlist('parameters[]')[i]
                    methods = request.POST.getlist('methods[]')[i]
                    unit = request.POST.getlist('unit[]')[i]
                    outlet = request.POST.getlist('outlet[]')[i]
                    customLimits = request.POST.getlist('customLimits[]')[i]

                    existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "methods": methods,
                         "unit": unit,
                         "outlet": outlet,
                         "customLimits":customLimits
                    })           
          existing_Form.extra_field = json.dumps(existing_Form.extra_field) 
          existing_Form.cutomLimit1 = request.POST['cutomLimit1'] 
          existing_Form.cutomLimit2 = request.POST['cutomLimit2'] 
          existing_Form.cutomLimit3 = request.POST['cutomLimit3'] 
          existing_Form.cutomLimit4 = request.POST['cutomLimit4'] 
          existing_Form.cutomLimit5 = request.POST['cutomLimit5'] 
          existing_Form.cutomLimit6 = request.POST['cutomLimit6'] 
          existing_Form.cutomLimit7 = request.POST['cutomLimit7'] 
          existing_Form.cutomLimit8 = request.POST['cutomLimit8'] 
          existing_Form.cutomLimit9 = request.POST['cutomLimit9'] 
          existing_Form.cutomLimit10 = request.POST['cutomLimit10'] 
          existing_Form.cutomLimit11 = request.POST['cutomLimit11'] 
          existing_Form.cutomLimit12 = request.POST['cutomLimit12'] 
          existing_Form.cutomLimit13 = request.POST['cutomLimit13'] 
          existing_Form.cutomLimit14 = request.POST['cutomLimit14'] 
          existing_Form.cutomLimit15 = request.POST['cutomLimit15'] 
          existing_Form.cutomLimit16 = request.POST['cutomLimit16'] 
          existing_Form.cutomLimit17 = request.POST['cutomLimit17'] 
          existing_Form.cutomLimit18 = request.POST['cutomLimit18'] 
          existing_Form.cutomLimit18 = request.POST['cutomLimit18'] 
          existing_Form.cutomLimit19 = request.POST['cutomLimit19'] 
          existing_Form.cutomLimit20 = request.POST['cutomLimit20'] 
          existing_Form.cutomLimit21 = request.POST['cutomLimit21'] 
          existing_Form.cutomLimit22 = request.POST['cutomLimit22'] 
          existing_Form.cutomLimit23 = request.POST['cutomLimit23'] 
          existing_Form.cutomLimit24 = request.POST['cutomLimit24'] 
          existing_Form.cutomLimit25 = request.POST['cutomLimit25'] 
          existing_Form.cutomLimit26 = request.POST['cutomLimit26'] 
          existing_Form.cutomLimit27 = request.POST['cutomLimit27'] 
          existing_Form.cutomLimit28 = request.POST['cutomLimit28'] 
          existing_Form.cutomLimit29 = request.POST['cutomLimit29'] 
          existing_Form.cutomLimit30 = request.POST['cutomLimit30'] 
          existing_Form.cutomLimit31 = request.POST['cutomLimit31']
          existing_Form.cutomLimit32 = request.POST['cutomLimit32']
          existing_Form.cutomLimit33 = request.POST['cutomLimit33']
          existing_Form.city_location = request.POST['city_location']
          
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
  
          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None
  
          # Assign to ambientUpdate if needed
          existing_Form.analyst_signature = analyst_sign
          existing_Form.assistant_manager_signature = review_sign
          existing_Form.lab_manager_signature = approved_sign
          
          existing_Form.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(existing_Form, image_key, '')
                    setattr(existing_Form, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(existing_Form, image_key, base64_encoded)
                         setattr(existing_Form, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(existing_Form, desc_key, description)



          existing_Form.id = None
          existing_Form.save()
          user = request.user
          action = f'Waste Water 2 Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/wasteWater2-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='wasteWater2List')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "WasteWaterForm2Clone.html")

def wasteWaterclone(request,pk):
     existing_form = WasteWaterSludge.objects.get(id=pk)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(existing_form, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':existing_form,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"WasteWaterSludgeClone.html",context)

def wasteWatercloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = WasteWaterSludge.objects.get(id=pk)
     except WasteWaterSludge.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
            existing_Form.location = request.POST['location']
            industry_id = request.POST.get('industry')
            existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
            existing_Form.lab_report_no = request.POST['ww_lab_report_no']
            existing_Form.invoice_bill_no = request.POST['ww_invoice_no']
            existing_Form.reporting_date = request.POST['ww_report_date']
            existing_Form.report_to = request.POST['ww_report_to']
            existing_Form.address = request.POST['ww_address']
            existing_Form.attention = request.POST['ww_attention']
            existing_Form.email = request.POST['ww_email']
            existing_Form.sample_id = request.POST['ww_sampleid']
            existing_Form.ww_sample_colec_Date = request.POST['ww_sample_colec_Date']
            existing_Form.ww_sample_desc = request.POST['ww_sample_desc']
            existing_Form.ww_sample_type = request.POST['ww_sample_type']
            existing_Form.ww_sample_colec_by = request.POST['ww_sample_colec_by']
            existing_Form.ww_date_of_analy_from = request.POST['ww_date_of_analy_from']
            existing_Form.ww_date_of_analy_to = request.POST['ww_date_of_analy_to']
            existing_Form.ww_test_desc = request.POST['ww_test_desc']
            existing_Form.ww_sr1 = request.POST['ww_sr1']
            existing_Form.ww_sr2 = request.POST['ww_sr2']
            existing_Form.ww_sr3 = request.POST['ww_sr3']
            existing_Form.ww_sr4 = request.POST['ww_sr4']
            existing_Form.ww_sr5 = request.POST['ww_sr5']
            existing_Form.ww_sr6 = request.POST['ww_sr6']
            existing_Form.ww_sr7 = request.POST['ww_sr7']
            existing_Form.ww_sr8 = request.POST['ww_sr8']
            existing_Form.ww_sr9 = request.POST['ww_sr9']
            existing_Form.ww_sr10 = request.POST['ww_sr10']
            existing_Form.ww_sr11 = request.POST['ww_sr11']
            existing_Form.ww_sr12 = request.POST['ww_sr12']
            existing_Form.ww_sr13 = request.POST['ww_sr13']
            existing_Form.ww_sr14 = request.POST['ww_sr14']
            existing_Form.ww_sr15 = request.POST['ww_sr15']
            existing_Form.ww_sr16 = request.POST['ww_sr16']
            existing_Form.ww_sr17 = request.POST['ww_sr17']
            existing_Form.ww_legend_1 = request.POST['ww-legend-1']
            existing_Form.ww_legend_2 = request.POST['ww-legend-2']
            existing_Form.ww_legend_3 = request.POST['ww-legend-3']
            existing_Form.ww_legend_4 = request.POST['ww-legend-4']
            existing_Form.ww_legend_5 = request.POST['ww-legend-5']
            existing_Form.ww_legend_6 = request.POST['ww-legend-6']
            existing_Form.ww_legend_7 = request.POST['ww-legend-7']
            existing_Form.ww_legend_8 = request.POST['ww-legend-8']
            existing_Form.ww_legend_9 = request.POST['ww-legend-9']
            existing_Form.ww_legend_10 = request.POST['ww-legend-10']
            existing_Form.ww_legend_11 = request.POST['ww-legend-11']
            existing_Form.ww_editnote = request.POST['ww_editnote']
            existing_Form.ww_custom_legend = request.POST['ww_custom_legend']
            existing_Form.ww_doc_con_1 = request.POST['ww_doc1']
            existing_Form.ww_doc_con_2 = request.POST['ww_doc2']
            existing_Form.ww_doc_con_3 = request.POST['ww_doc3']
            existing_Form.created_by = request.userAacha
          #   existing_Form.ww_analyzed_by = request.FILES["ww_analyzedby" ]
          #   existing_Form.ww_reviewd_by = request.FILES["ww_reviewedby" ]
          #   existing_Form.ww_approved_by = request.FILES["ww_approvedby" ]
          #   existing_Form.ww_approved_by1 = request.FILES["ww_approvedby1" ]
            existing_Form.zdhc = request.POST['zdhc']
            existing_Form.city_location = request.POST['city_location']
            
            analyst_sign_id = request.POST.get('analyst_sign')
            review_sign_id = request.POST.get('review_sign')
            approved_sign_id = request.POST.get('approved_sign')
    
            analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
            review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
            approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None
    
            # Assign to ambientUpdate if needed
            existing_Form.analyst_signature = analyst_sign
            existing_Form.assistant_manager_signature = review_sign
            existing_Form.lab_manager_signature = approved_sign

          
            existing_Form.pdf_heading=request.POST.get('pdf_heading')
          
            for i in range(1, 7):
                 image_key = f'pdf_image_{i}'
                 desc_key = f'pdf_desc_{i}'
                 remove_key = f'remove_image_{i}'
  
                 uploaded_file = request.FILES.get(image_key)
                 description = request.POST.get(desc_key)
                 remove_requested = request.POST.get(remove_key)
  
  
                 if remove_requested == "on":
                      setattr(existing_Form, image_key, '')
                      setattr(existing_Form, desc_key, '')
                 elif uploaded_file:
                      try:
                           file_bytes = uploaded_file.read()
                           base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                           setattr(existing_Form, image_key, base64_encoded)
                           setattr(existing_Form, desc_key, description or '')
                      except Exception as e:
                           pass
                 else:
                      if description is not None:
                           setattr(existing_Form, desc_key, description)

            existing_Form.id = None
            existing_Form.save()
            id = existing_Form.id
            user = request.user
            action = f'Waste Water Form {existing_Form.lab_report_no} cloned by {user.username}'
            AuditLog.objects.create(user=user, action=action, timestamp=local_date)
            messages.success(request, 'Operation was successful!')
            if "submit_and_view" in request.POST:
                url = f"/wasteWaterSludge-view/{str(id)}/"
                return redirect(to=url)
          
            if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
                return redirect(to='wasteWaterSludgeList')
            else:
                return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "WasteWaterSludgeClone.html")

__all__ = [
    'wasteWaterSludge',
    'wasteWater2',
    'wasteWaterSludgeList',
    'wasteWaterSludgeDelete',
    'wastewaterEdit',
    'wasteWaterUpdate',
    'wasteWaterView',
    'wasteWaterPdf0',
    'wasteWaterPdf1',
    'wasteWAter2List',
    'wasteWAter2Delete',
    'wasteWAter2Edit',
    'wasteWAter2Update',
    'wasteWAter2View',
    'wasteWater2Pdf',
    'wasteWater2Pdf1',
    'wasteWater2clone',
    'wasteWater2cloneSave',
    'wasteWaterclone',
    'wasteWatercloneSave',
]
