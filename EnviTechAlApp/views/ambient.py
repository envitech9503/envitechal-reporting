# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def ambientAirForm(request):
        if request.method == 'POST':
            location = request.POST['location']
            industry_id = request.POST.get('industry')
            industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
            city_location = request.POST['city_location']
            lab_report_no = request.POST['ambient_Air_lab_report_no']
            invoice_bill_no = request.POST['ambientAir_invoice_no']
            reporting_date = request.POST['ambientAir_rep_date']
            report_to = request.POST['ambientAir_rep_to']
            address = request.POST['ambientAir_address']
            attention = request.POST['ambientAir_attention']
            email = request.POST['ambientAir_email']
            sample_id = request.POST['ambientAir_testid']
            ambientAir_test_perf_date = request.POST['ambientAir_test_perf_date']
            ambientAir_test_type_location = request.POST['ambientAir_testtype_location']
            ambientAir_test_perf_by = request.POST['ambientAir_test_perf_by']
            ambientAir_test_desc = request.POST['ambientAir_test_desc']
            ambienAir_select = request.POST['select']
            ambientAir_sr1 = request.POST['ambientAir_sr1']
            ambientAir_sr2 = request.POST['ambientAir_sr2']
            ambientAir_sr3 = request.POST['ambientAir_sr3']
            ambientAir_sr4 = request.POST['ambientAir_sr4']
            ambientAir_sr5 = request.POST['ambientAir_sr5']
            ambientAir_sr6 = request.POST['ambientAir_sr6']
            ambientAir_sr7 = request.POST['ambientAir_sr7']
            ambientAir_sr8 = request.POST['ambientAir_sr8']
            ambientAir_sr9 = request.POST['ambientAir_sr9']
            ambientAir_sr10 = request.POST['ambientAir_sr10']
            ambientAir_sr11 = request.POST['ambientAir_sr11']
            ambientAir_sr12 = request.POST['ambientAir_sr12']
            ambientAir_sr13 = request.POST['ambientAir_sr13']
            ambientAir_sr14 = request.POST['ambientAir_sr14']
            ambientAir_legend_1 = request.POST['ambientAir-legend-1']
            ambientAir_legend_2 = request.POST['ambientAir-legend-2']
            ambientAir_legend_3 = request.POST['ambientAir-legend-3']
            ambientAir_legend_4 = request.POST['ambientAir-legend-4']
            ambientAir_legend_5 = request.POST['ambientAir-legend-5']
            ambientAir_legend_6 = request.POST['ambientAir-legend-6']
            ambientAir_edit_note = request.POST['ambientAir_editNote']
            ambientAir_custom_legend = request.POST['ambientAir_customlegend']
            ambientAir_doc_con_1 = request.POST['ambientAir_doc1']
            ambientAir_doc_con_2 = request.POST['ambientAir_doc2']
            ambientAir_doc_con_3 = request.POST['ambientAir_doc3']
          #   ambientAir_analyzed_by = request.FILES["ambientAir_analyzedby" ]
          #   ambientAir_reviewd_by = request.FILES["ambientAir_reviewedby" ]
          #   ambientAir_approved_by = request.FILES["ambientAir_approvedby" ]
          #   ambientAir_approved_by1 = request.FILES["ambientAir_approvedby1" ]
            extra_field = request.POST['extra_field']
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
            
            ambientAir = AmbientAirForm(lab_report_no = lab_report_no,invoice_bill_no=invoice_bill_no,
                                        reporting_date = reporting_date,report_to=report_to,
                                        address=address,attention=attention,email=email,
                                        sample_id=sample_id,ambientAir_test_perf_date=ambientAir_test_perf_date,ambientAir_test_type_location =
                                        ambientAir_test_type_location,ambientAir_test_perf_by=ambientAir_test_perf_by,ambienAir_test_desc=ambientAir_test_desc,
                                        ambienAir_select=ambienAir_select,ambientAir_sr1 =ambientAir_sr1,ambientAir_sr2=ambientAir_sr2,ambientAir_sr3=ambientAir_sr3,ambientAir_sr4=ambientAir_sr4,
                                        ambientAir_sr5=ambientAir_sr5,ambientAir_sr6=ambientAir_sr6,ambientAir_sr7=ambientAir_sr7,ambientAir_sr8=ambientAir_sr8,
                                        ambientAir_sr9=ambientAir_sr9,ambientAir_sr10=ambientAir_sr10,ambientAir_sr11=ambientAir_sr11,ambientAir_sr12=ambientAir_sr12,
                                        ambientAir_sr13=ambientAir_sr13,ambientAir_sr14=ambientAir_sr14,ambientAir_legend_1=
                                        ambientAir_legend_1,ambientAir_legend_2=ambientAir_legend_2,ambientAir_legend_3=ambientAir_legend_3,ambientAir_legend_4=ambientAir_legend_4,
                                        ambientAir_legend_5=ambientAir_legend_5,ambientAir_legend_6=ambientAir_legend_6,extra_field=extra_field,
                                        ambientAir_edit_note=ambientAir_edit_note,ambientAir_custom_legend=ambientAir_custom_legend,ambientAir_doc_con_1=ambientAir_doc_con_1,ambientAir_doc_con_2=ambientAir_doc_con_2,
                                        ambientAir_doc_con_3=ambientAir_doc_con_3,location=location,city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,
                                        **image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
            ambientAir.save()
            
            
            if customer_id:
                 LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

            user = request.user
            action = f'Ambient Air Form {ambientAir.lab_report_no} created by {user.username}'
            AuditLog.objects.create(user=user, action=action, timestamp=local_date)
            messages.success(request, 'Operation was successful!')
            id = (AmbientAirForm.objects.last()).id
            if "submit_and_view" in request.POST:
               url = f"/ambientAir-view/{str(id)}/"
               return redirect(to=url)
            if "submit_and_new" in request.POST:
               return render(request, "ambientAirForm.html")
        else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context={"log":log,'signs':signs,'industry':industries}

          return render(request,"ambientAirForm.html",context)


@login_required(login_url="/login")
def ambientAirQuality2(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          # hours_checkBox = request.POST['hours_checkBox']
          lab_report_no = request.POST['lab_rep_no']
          invoice_bill_no = request.POST['invoice_no']
          reporting_date = request.POST['report_date']
          report_to = request.POST['report_to']
          address = request.POST['address']
          attention = request.POST['attention']
          email = request.POST['email']
          sample_id = request.POST['testId']
          test_perf_date = request.POST['test_perf_date']
          test_type = request.POST['test_type']
          test_desc = request.POST['test_desc']
          test_test_perf_by = request.POST['test_test_perf_by']
          sr1_1 = request.POST['sr1_1']
          sr1_2 = request.POST['sr1_2']
          sr1_3 = request.POST['sr1_3']
          sr1_4 = request.POST['sr1_4']
          sr1_5 = request.POST['sr1_5']
          sr1_6 = request.POST['sr1_6']
          sr1_7 = request.POST['sr1_7']
          sr1_8 = request.POST['sr1_8']
          sr1_9 = request.POST['sr1_9']
          sr1_10 = request.POST['sr1_10']
          sr2_0 = request.POST['sr2_0']
          sr2_1 = request.POST['sr2_1']
          sr2_2 = request.POST['sr2_2']
          sr2_3 = request.POST['sr2_3']
          sr2_4 = request.POST['sr2_4']
          sr2_5 = request.POST['sr2_5']
          sr2_6 = request.POST['sr2_6']
          sr2_7 = request.POST['sr2_7']
          sr2_8 = request.POST['sr2_8']
          sr2_9 = request.POST['sr2_9']
          sr3_0 = request.POST['sr3_0']
          sr3_1 = request.POST['sr3_1']
          sr3_2 = request.POST['sr3_2']
          sr3_3 = request.POST['sr3_3']
          sr3_4 = request.POST['sr3_4']
          sr3_5 = request.POST['sr3_5']
          sr3_6 = request.POST['sr3_6']
          sr3_7 = request.POST['sr3_7']
          sr3_8 = request.POST['sr3_8']
          sr3_9 = request.POST['sr3_9']
          sr4_0 = request.POST['sr4_0']
          sr4_1 = request.POST['sr4_1']
          sr4_2 = request.POST['sr4_2']
          sr4_3 = request.POST['sr4_3']
          sr4_4 = request.POST['sr4_4']
          sr4_5 = request.POST['sr4_5']
          sr4_6 = request.POST['sr4_6']
          sr4_7 = request.POST['sr4_7']
          sr4_8 = request.POST['sr4_8']
          sr4_9 = request.POST['sr4_9']
          sr5_0 = request.POST['sr5_0']
          sr5_1 = request.POST['sr5_1']
          sr5_2 = request.POST['sr5_2']
          sr5_3 = request.POST['sr5_3']
          sr5_4 = request.POST['sr5_4']
          sr5_5 = request.POST['sr5_5']
          sr5_6 = request.POST['sr5_6']
          sr5_7 = request.POST['sr5_7']
          sr5_8 = request.POST['sr5_8']
          sr5_9 = request.POST['sr5_9']
          sr6_0 = request.POST['sr6_0']
          sr6_1 = request.POST['sr6_1']
          sr6_2 = request.POST['sr6_2']
          sr6_3 = request.POST['sr6_3']
          sr6_4 = request.POST['sr6_4']
          sr6_5 = request.POST['sr6_5']
          sr6_6 = request.POST['sr6_6']
          sr6_7 = request.POST['sr6_7']
          sr6_8 = request.POST['sr6_8']
          sr6_9 = request.POST['sr6_9']
          sr7_0 = request.POST['sr7_0']
          sr7_1 = request.POST['sr7_1']
          sr7_2 = request.POST['sr7_2']
          sr7_3 = request.POST['sr7_3']
          sr7_4 = request.POST['sr7_4']
          sr7_5 = request.POST['sr7_5']
          sr7_6 = request.POST['sr7_6']
          sr7_7 = request.POST['sr7_7']
          sr7_8 = request.POST['sr7_8']
          sr7_9 = request.POST['sr7_9']
          sr8_0 = request.POST['sr8_0']
          sr8_1 = request.POST['sr8_1']
          sr8_2 = request.POST['sr8_2']
          sr8_3 = request.POST['sr8_3']
          sr8_4 = request.POST['sr8_4']
          sr8_5 = request.POST['sr8_5']
          sr8_6 = request.POST['sr8_6']
          sr8_7 = request.POST['sr8_7']
          sr8_8 = request.POST['sr8_8']
          sr8_9 = request.POST['sr8_9']
          sr9_0 = request.POST['sr9_0']
          sr9_1 = request.POST['sr9_1']
          sr9_2 = request.POST['sr9_2']
          sr9_3 = request.POST['sr9_3']
          sr9_4 = request.POST['sr9_4']
          sr9_5 = request.POST['sr9_5']
          sr9_6 = request.POST['sr9_6']
          sr9_7 = request.POST['sr9_7']
          sr9_8 = request.POST['sr9_8']
          sr9_9 = request.POST['sr9_9']
          sr10_0 = request.POST['sr10_0']
          sr10_1 = request.POST['sr10_1']
          sr10_2 = request.POST['sr10_2']
          sr10_3 = request.POST['sr10_3']
          sr10_4 = request.POST['sr10_4']
          sr10_5 = request.POST['sr10_5']
          sr10_6 = request.POST['sr10_6']
          sr10_7 = request.POST['sr10_7']
          sr10_8 = request.POST['sr10_8']
          sr10_9 = request.POST['sr10_9']
          sr11_0 = request.POST['sr11_0']
          sr11_1 = request.POST['sr11_1']
          sr11_2 = request.POST['sr11_2']
          sr11_3 = request.POST['sr11_3']
          sr11_4 = request.POST['sr11_4']
          sr11_5 = request.POST['sr11_5']
          sr11_6 = request.POST['sr11_6']
          sr11_7 = request.POST['sr11_7']
          sr11_8 = request.POST['sr11_8']
          sr11_9 = request.POST['sr11_9']
          sr12_0 = request.POST['sr12_0']
          sr12_1 = request.POST['sr12_1']
          sr12_2 = request.POST['sr12_2']
          sr12_3 = request.POST['sr12_3']
          sr12_4 = request.POST['sr12_4']
          sr12_5 = request.POST['sr12_5']
          sr12_6 = request.POST['sr12_6']
          sr12_7 = request.POST['sr12_7']
          sr12_8 = request.POST['sr12_8']
          sr12_9 = request.POST['sr12_9']
          sr13_0 = request.POST['sr13_0']
          sr13_1 = request.POST['sr13_1']
          sr13_2 = request.POST['sr13_2']
          sr13_3 = request.POST['sr13_3']
          sr13_4 = request.POST['sr13_4']
          sr13_5 = request.POST['sr13_5']
          sr13_6 = request.POST['sr13_6']
          sr13_7 = request.POST['sr13_7']
          sr13_8 = request.POST['sr13_8']
          sr13_9 = request.POST['sr13_9']
          sr14_0 = request.POST['sr14_0']
          sr14_1 = request.POST['sr14_1']
          sr14_2 = request.POST['sr14_2']
          sr14_3 = request.POST['sr14_3']
          sr14_4 = request.POST['sr14_4']
          sr14_5 = request.POST['sr14_5']
          sr14_6 = request.POST['sr14_6']
          sr14_7 = request.POST['sr14_7']
          sr14_8 = request.POST['sr14_8']
          sr14_9 = request.POST['sr14_9']
          sr15_0 = request.POST['sr15_0']
          sr15_1 = request.POST['sr15_1']
          sr15_2 = request.POST['sr15_2']
          sr15_3 = request.POST['sr15_3']
          sr15_4 = request.POST['sr15_4']
          sr15_5 = request.POST['sr15_5']
          sr15_6 = request.POST['sr15_6']
          sr15_7 = request.POST['sr15_7']
          sr15_8 = request.POST['sr15_8']
          sr15_9 = request.POST['sr15_9']
          sr16_0 = request.POST['sr16_0']
          sr16_1 = request.POST['sr16_1']
          sr16_2 = request.POST['sr16_2']
          sr16_3 = request.POST['sr16_3']
          sr16_4 = request.POST['sr16_4']
          sr16_5 = request.POST['sr16_5']
          sr16_6 = request.POST['sr16_6']
          sr16_7 = request.POST['sr16_7']
          sr16_8 = request.POST['sr16_8']
          sr16_9 = request.POST['sr16_9']
          sr17_0 = request.POST['sr17_0']
          sr17_1 = request.POST['sr17_1']
          sr17_2 = request.POST['sr17_2']
          sr17_3 = request.POST['sr17_3']
          sr17_4 = request.POST['sr17_4']
          sr17_5 = request.POST['sr17_5']
          sr17_6 = request.POST['sr17_6']
          sr17_7 = request.POST['sr17_7']
          sr17_8 = request.POST['sr17_8']
          sr17_9 = request.POST['sr17_9']
          sr18_0 = request.POST['sr18_0']
          sr18_1 = request.POST['sr18_1']
          sr18_2 = request.POST['sr18_2']
          sr18_3 = request.POST['sr18_3']
          sr18_4 = request.POST['sr18_4']
          sr18_5 = request.POST['sr18_5']
          sr18_6 = request.POST['sr18_6']
          sr18_7 = request.POST['sr18_7']
          sr18_8 = request.POST['sr18_8']
          sr18_9 = request.POST['sr18_9']
          sr19_0 = request.POST['sr19_0']
          sr19_1 = request.POST['sr19_1']
          sr19_2 = request.POST['sr19_2']
          sr19_3 = request.POST['sr19_3']
          sr19_4 = request.POST['sr19_4']
          sr19_5 = request.POST['sr19_5']
          sr19_6 = request.POST['sr19_6']
          sr19_7 = request.POST['sr19_7']
          sr19_8 = request.POST['sr19_8']
          sr19_9 = request.POST['sr19_9']
          sr20_0 = request.POST['sr20_0']
          sr20_1 = request.POST['sr20_1']
          sr20_2 = request.POST['sr20_2']
          sr20_3 = request.POST['sr20_3']
          sr20_4 = request.POST['sr20_4']
          sr20_5 = request.POST['sr20_5']
          sr20_6 = request.POST['sr20_6']
          sr20_7 = request.POST['sr20_7']
          sr20_8 = request.POST['sr20_8']
          sr20_9 = request.POST['sr20_9']
          sr21_0 = request.POST['sr21_0']
          sr21_1 = request.POST['sr21_1']
          sr21_2 = request.POST['sr21_2']
          sr21_3 = request.POST['sr21_3']
          sr21_4 = request.POST['sr21_4']
          sr21_5 = request.POST['sr21_5']
          sr21_6 = request.POST['sr21_6']
          sr21_7 = request.POST['sr21_7']
          sr21_8 = request.POST['sr21_8']
          sr21_9 = request.POST['sr21_9']
          sr22_0 = request.POST['sr22_0']
          sr22_1 = request.POST['sr22_1']
          sr21_2 = request.POST['sr21_2']
          sr21_3 = request.POST['sr21_3']
          sr21_4 = request.POST['sr21_4']
          sr21_5 = request.POST['sr21_5']
          sr21_6 = request.POST['sr21_6']
          sr21_7 = request.POST['sr21_7']
          sr21_8 = request.POST['sr21_8']
          sr21_9 = request.POST['sr21_9']
          sr22_0 = request.POST['sr22_0']
          sr22_1 = request.POST['sr22_1']
          sr22_2 = request.POST['sr22_2']
          sr22_3 = request.POST['sr22_3']
          sr22_4 = request.POST['sr22_4']
          sr22_5 = request.POST['sr22_5']
          sr22_6 = request.POST['sr22_6']
          sr22_7 = request.POST['sr22_7']
          sr22_8 = request.POST['sr22_8']
          sr22_9 = request.POST['sr22_9']
          sr23_0 = request.POST['sr23_0']
          sr23_1 = request.POST['sr23_1']
          sr23_2 = request.POST['sr23_2']
          sr23_3 = request.POST['sr23_3']
          sr23_4 = request.POST['sr23_4']
          sr23_5 = request.POST['sr23_5']
          sr23_6 = request.POST['sr23_6']
          sr23_7 = request.POST['sr23_7']
          sr23_8 = request.POST['sr23_8']
          sr23_9 = request.POST['sr23_9']
          sr24_0 = request.POST['sr24_0']
          sr24_1 = request.POST['sr24_1']
          sr24_2 = request.POST['sr24_2']
          sr24_3 = request.POST['sr24_3']
          sr24_4 = request.POST['sr24_4']
          sr24_5 = request.POST['sr24_5']
          sr24_6 = request.POST['sr24_6']
          sr24_7 = request.POST['sr24_7']
          sr24_8 = request.POST['sr24_8']
          sr24_9 = request.POST['sr24_9']
          sr25_0 = request.POST['sr25_0']
          sr25_1 = request.POST['sr25_1']
          sr25_2 = request.POST['sr25_2']
          sr25_3 = request.POST['sr25_3']
          sr25_4 = request.POST['sr25_4']
          sr25_5 = request.POST['sr25_5']
          sr25_6 = request.POST['sr25_6']
          sr25_7 = request.POST['sr25_7']
          sr25_8 = request.POST['sr25_8']
          seqs_lim_1 = request.POST.get('seqs_lim_1')
          seqs_lim_2 = request.POST.get('seqs_lim_2')
          seqs_lim_3 = request.POST.get('seqs_lim_3')
          seqs_lim_4 = request.POST.get('seqs_lim_4')
          seqs_lim_5 = request.POST.get('seqs_lim_5')
          seqs_lim_6 = request.POST.get('seqs_lim_6')
          seqs_lim_7 = request.POST.get('seqs_lim_7')
          seqs_lim_8 = request.POST.get('seqs_lim_8')
          seqs_lim_9 = request.POST.get('seqs_lim_9')
          
          peqs_lim_1 = request.POST.get('peqs_lim_1')
          peqs_lim_2 = request.POST.get('peqs_lim_2')
          peqs_lim_3 = request.POST.get('peqs_lim_3')
          peqs_lim_4 = request.POST.get('peqs_lim_4')
          peqs_lim_5 = request.POST.get('peqs_lim_5')
          peqs_lim_6 = request.POST.get('peqs_lim_6')
          peqs_lim_7 = request.POST.get('peqs_lim_7')
          peqs_lim_8 = request.POST.get('peqs_lim_8')
          peqs_lim_9 = request.POST.get('peqs_lim_9')
          
          neqs_lim_1 = request.POST.get('neqs_lim_1')
          neqs_lim_2 = request.POST.get('neqs_lim_2')
          neqs_lim_3 = request.POST.get('neqs_lim_3')
          neqs_lim_4 = request.POST.get('neqs_lim_4')
          neqs_lim_5 = request.POST.get('neqs_lim_5')
          neqs_lim_6 = request.POST.get('neqs_lim_6')
          neqs_lim_7 = request.POST.get('neqs_lim_7')
          neqs_lim_8 = request.POST.get('neqs_lim_8')
          neqs_lim_9 = request.POST.get('neqs_lim_9')
          select = request.POST.get('select')
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
          edit_note = request.POST['edit_note']
          custom_legend = request.POST['custom_legend']
          doc1 = request.POST['doc1']
          doc2 = request.POST['doc2']
          doc3 = request.POST['doc3']
          # analyzedby = request.FILES['analyzedby']
          # reviewedby = request.FILES['reviewedby']
          # approvedby = request.FILES['approvedby']
          # approvedby1 = request.FILES['approvedby1']
          customer_id = request.POST.get('customer_id')
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
          analyst_sign = Signatures.objects.get(id=analyst_sign_id)
          review_sign = Signatures.objects.get(id=review_sign_id)
          approved_sign = Signatures.objects.get(id=approved_sign_id)
          pdf_heading = request.POST.get('pdf_heading')
          col_head_1 = request.POST.get('col_head_1')
          col_head_2 = request.POST.get('col_head_2')
          col_head_3 = request.POST.get('col_head_3')
          col_head_4 = request.POST.get('col_head_4')
          col_head_5 = request.POST.get('col_head_5')
          col_head_6 = request.POST.get('col_head_6')
          col_head_7 = request.POST.get('col_head_7')
          col_head_8 = request.POST.get('col_head_8')
          col_head_9 = request.POST.get('col_head_9')
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
          
          ambientAirForm2 = AmbientAir2(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,report_to=report_to,address=address,
                                        attention=attention,email=email,sample_id=sample_id,test_perf_date=test_perf_date,test_type=test_type,
                                        test_desc=test_desc,test_test_perf_by=test_test_perf_by,sr1_1=sr1_1,sr1_2=sr1_2,sr1_3=sr1_3,sr1_4=sr1_4,
                                        sr1_5=sr1_5,sr1_6=sr1_6,sr1_7=sr1_7,sr1_8=sr1_8,sr1_9=sr1_9,sr1_10=sr1_10,sr2_0=sr2_0,sr2_1=sr2_1,sr2_2=sr2_2,sr2_3=sr2_3,
                                        sr2_4=sr2_4,sr2_5=sr2_5,sr2_6=sr2_6,sr2_7=sr2_7,sr2_8=sr2_8,sr2_9=sr2_9,sr3_0=sr3_0,sr3_1=sr3_1,sr3_2=sr3_2,
                                        sr3_3=sr3_3,sr3_4=sr3_4,sr3_5=sr3_5,sr3_6=sr3_6,sr3_7=sr3_7,sr3_8=sr3_8,sr3_9=sr3_9,sr4_0=sr4_0,sr4_1=sr4_1,sr4_2=sr4_2,
                                        sr4_3=sr4_3,sr4_4=sr4_4,sr4_5=sr4_5,sr4_6=sr4_6,sr4_7=sr4_7,sr4_8=sr4_8,sr4_9=sr4_9,sr5_0=sr5_0,sr5_1=sr5_1,sr5_2=sr5_2,
                                        sr5_3=sr5_3,sr5_4=sr5_4,sr5_5=sr5_5,sr5_6=sr5_6,sr5_7=sr5_7,sr5_8=sr5_8,sr5_9=sr5_9,sr6_0=sr6_0,sr6_1=sr6_1,sr6_2=sr6_2,
                                        sr6_3=sr6_3,sr6_4=sr6_4,sr6_5=sr6_5,sr6_6=sr6_6,sr6_7=sr6_7,sr6_8=sr6_8,sr6_9=sr6_9,sr7_0=sr7_0,sr7_1=sr7_1,sr7_2=sr7_2,
                                        sr7_3=sr7_3,sr7_4=sr7_4,sr7_5=sr7_5,sr7_6=sr7_6,sr7_7=sr7_7,sr7_8=sr7_8,sr7_9=sr7_9,sr8_0=sr8_0,sr8_1=sr8_1,sr8_2=sr8_2,
                                        sr8_3=sr8_3,sr8_4=sr8_4,sr8_5=sr8_5,sr8_6=sr8_6,sr8_7=sr8_7,sr8_8=sr8_8,sr8_9=sr8_9,sr9_0=sr9_0,sr9_1=sr9_1,sr9_2=sr9_2,
                                        sr9_3=sr9_3,sr9_4=sr9_4,sr9_5=sr9_5,sr9_6=sr9_6,sr9_7=sr9_7,sr9_8=sr9_8,sr9_9=sr9_9,sr10_0=sr10_0,sr10_1=sr10_1,sr10_2=sr10_2,
                                        sr10_3=sr10_3,sr10_4=sr10_4,sr10_5=sr10_5,sr10_6=sr10_6,sr10_7=sr10_7,sr10_8=sr10_8,sr10_9=sr10_9,sr11_0=sr11_0,
                                        sr11_1=sr11_1,sr11_2=sr11_2,sr11_3=sr11_3,sr11_4=sr11_4,sr11_5=sr11_5,sr11_6=sr11_6,sr11_7=sr11_7,sr11_8=sr11_8,sr11_9=sr11_9,
                                        sr12_0=sr12_0,sr12_1=sr12_1,sr12_2=sr12_2,sr12_3=sr12_3,sr12_4=sr12_4,sr12_5=sr12_5,sr12_6=sr12_6,sr12_7=sr12_7,sr12_8=sr12_8,
                                        sr12_9=sr12_9,sr13_0=sr13_0,sr13_1=sr13_1,sr13_2=sr13_2,sr13_3=sr13_3,sr13_4=sr13_4,sr13_5=sr13_5,sr13_6=sr13_6,sr13_7=sr13_7,
                                        sr13_8=sr13_8,sr13_9=sr13_9,sr14_0=sr14_0,sr14_1=sr14_1,sr14_2=sr14_2,sr14_3=sr14_3,sr14_4=sr14_4,sr14_5=sr14_5,sr14_6=sr14_6,
                                        sr14_7=sr14_7,sr14_8=sr14_8,sr14_9=sr14_9,sr15_0=sr15_0,sr15_1=sr15_1,sr15_2=sr15_2,sr15_3=sr15_3,sr15_4=sr15_4,sr15_5=sr15_5,
                                        sr15_6=sr15_6,sr15_7=sr15_7,sr15_8=sr15_8,sr15_9=sr15_9,sr16_0=sr16_0,sr16_1=sr16_1,sr16_2=sr16_2,sr16_3=sr16_3,sr16_4=sr16_4,
                                        sr16_5=sr16_5,sr16_6=sr16_6,sr16_7=sr16_7,sr16_8=sr16_8,sr16_9=sr16_9,sr17_0=sr17_0,sr17_1=sr17_1,sr17_2=sr17_2,sr17_3=sr17_3,sr17_4=sr17_4,
                                        sr17_5=sr17_5,sr17_6=sr17_6,sr17_7=sr17_7,sr17_8=sr17_8,sr17_9=sr17_9,sr18_0=sr18_0,sr18_1=sr18_1,sr18_2=sr18_2,sr18_3=sr18_3,
                                        sr18_4=sr18_4,sr18_5=sr18_5,sr18_6=sr18_6,sr18_7=sr18_7,sr18_8=sr18_8,sr18_9=sr18_9,sr19_0=sr19_0,sr19_1=sr19_1,sr19_2=sr19_2,
                                        sr19_3=sr19_3,sr19_4=sr19_4,sr19_5=sr19_5,sr19_6=sr19_6,sr19_7=sr19_7,sr19_8=sr19_8,sr19_9=sr19_9,sr20_0=sr20_0,sr20_1=sr20_1,
                                        sr20_2=sr20_2,sr20_3=sr20_3,sr20_4=sr20_4,sr20_5=sr20_5,sr20_6=sr20_6,sr20_7=sr20_7,sr20_8=sr20_8,sr20_9=sr20_9,sr21_0=sr21_0,
                                        sr21_1=sr21_1,sr21_2=sr21_2,sr21_3=sr21_3,sr21_4=sr21_4,sr21_5=sr21_5,sr21_6=sr21_6,sr21_7=sr21_7,sr21_8=sr21_8,sr21_9=sr21_9,
                                        sr22_0=sr22_0,sr22_1=sr22_1,sr22_2=sr22_2,sr22_3=sr22_3,sr22_4=sr22_4,sr22_5=sr22_5,sr22_6=sr22_6,sr22_7=sr22_7,sr22_8=sr22_8,
                                        sr22_9=sr22_9,sr23_0=sr23_0,sr23_1=sr23_1,sr23_2=sr23_2,sr23_3=sr23_3,sr23_4=sr23_4,sr23_5=sr23_5,sr23_6=sr23_6,sr23_7=sr23_7,
                                        sr23_8=sr23_8,sr23_9=sr23_9,sr24_0=sr24_0,sr24_1=sr24_1,sr24_2=sr24_2,sr24_3=sr24_3,sr24_4=sr24_4,sr24_5=sr24_5,sr24_6=sr24_6,
                                        sr24_7=sr24_7,sr24_8=sr24_8,sr24_9=sr24_9,sr25_0=sr25_0,sr25_1=sr25_1,sr25_2=sr25_2,sr25_3=sr25_3,sr25_4=sr25_4,sr25_5=sr25_5,
                                        sr25_6=sr25_6,sr25_7=sr25_7,sr25_8=sr25_8,select=select,seqs_lim_1=seqs_lim_1,seqs_lim_2=seqs_lim_2,seqs_lim_3=seqs_lim_3,seqs_lim_4=seqs_lim_4,seqs_lim_5=seqs_lim_5,seqs_lim_6=seqs_lim_6,seqs_lim_7=seqs_lim_7,seqs_lim_8=seqs_lim_8,seqs_lim_9=seqs_lim_9,peqs_lim_1=peqs_lim_1,peqs_lim_2=peqs_lim_2,peqs_lim_3=peqs_lim_3,peqs_lim_4=peqs_lim_4,peqs_lim_5=peqs_lim_5,peqs_lim_6=peqs_lim_6,peqs_lim_7=peqs_lim_7,peqs_lim_8=peqs_lim_8,peqs_lim_9=peqs_lim_9, neqs_lim_1=neqs_lim_1,neqs_lim_2=neqs_lim_2,neqs_lim_3=neqs_lim_3,neqs_lim_4=neqs_lim_4,neqs_lim_5=neqs_lim_5,neqs_lim_6=neqs_lim_6,neqs_lim_7=neqs_lim_7,neqs_lim_8=neqs_lim_8,neqs_lim_9=neqs_lim_9,legend_1=legend_1,legend_2=legend_2,legend_3=legend_3,
                                        legend_4=legend_4,legend_5=legend_5,legend_6=legend_6,legend_7=legend_7,legend_8=legend_8,legend_9=legend_9,legend_10=legend_10,
                                        legend_11=legend_11,edit_note=edit_note,custom_legend=custom_legend,location=location,
                                        doc1=doc1,doc2=doc2,doc3=doc3,city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,
                                        assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,col_head_1=col_head_1,col_head_2=col_head_2,col_head_3=col_head_3,col_head_4=col_head_4,col_head_5=col_head_5,col_head_6=col_head_6,col_head_7=col_head_7,col_head_8=col_head_8,col_head_9=col_head_9,created_by = request.user,industry=industry)
          ambientAirForm2.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Ambient Air 2 Form {ambientAirForm2.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (AmbientAir2.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/ambientAir2-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="ambientAir2")


     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
     return render(request,"ambientAir2.html",context)



@login_required(login_url="/login")
def ambientAirList(request):
     ambientAir, _srch = _list_filter(request, AmbientAirForm)
     context = {'searched':_srch, 'data':ambientAir}
     return render(request,"ambientAirList.html",context)


@login_required(login_url="/login")
def ambientAirDelete(request,pk):
     ambientDelete = AmbientAirForm.objects.get(id=pk)
     ambientDelete.delete()
     user = request.user
     action = f'Ambient Air Form {ambientDelete.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect('ambientAirList')

@login_required(login_url="/login")
def ambientAirEdit(request,pk):
     ambientEdit = AmbientAirForm.objects.get(id=pk)
     try:
        ambientEdit.extra_field = json.loads(ambientEdit.extra_field) if ambientEdit.extra_field else []
     except Exception:
          ambientEdit.extra_field = []
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(ambientEdit, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     context = {'data':ambientEdit,"log":log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"ambientAirEdit.html",context)


@login_required(login_url="/login")
def ambientAirUpdateRecord(request,pk):
     ambientUpdate = AmbientAirForm.objects.get(id=pk)
     if request.method == 'POST':
          # data = JsonResponse(request.POST)
          # return data
          ambientUpdate.location = request.POST['location']
          industry_id = request.POST.get('industry')
          ambientUpdate.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          ambientUpdate.lab_report_no = request.POST['ambient_Air_lab_report_no']
          ambientUpdate.invoice_bill_no = request.POST['ambientAir_invoice_no']
          ambientUpdate.reporting_date = request.POST['ambientAir_rep_date']
          ambientUpdate.report_to = request.POST['ambientAir_rep_to']
          ambientUpdate.address = request.POST['ambientAir_address']
          ambientUpdate.attention = request.POST['ambientAir_attention']
          ambientUpdate.email = request.POST['ambientAir_email']
          ambientUpdate.sample_id = request.POST['ambientAir_testid']
          ambientUpdate.ambientAir_test_perf_date = request.POST['ambientAir_test_perf_date']
          ambientUpdate.ambientAir_test_type_location = request.POST['ambientAir_testtype_location']
          ambientUpdate.ambientAir_test_perf_by = request.POST['ambientAir_test_perf_by']
          ambientUpdate.ambienAir_test_desc = request.POST['ambientAir_test_desc']
          ambientUpdate.ambientAir_sr1 = request.POST['ambientAir_sr1']
          ambientUpdate.ambientAir_sr2 = request.POST['ambientAir_sr2']
          ambientUpdate.ambientAir_sr3 = request.POST['ambientAir_sr3']
          ambientUpdate.ambientAir_sr4 = request.POST['ambientAir_sr4']
          ambientUpdate.ambientAir_sr5 = request.POST['ambientAir_sr5']
          ambientUpdate.ambientAir_sr6 = request.POST['ambientAir_sr6']
          ambientUpdate.ambientAir_sr7 = request.POST['ambientAir_sr7']
          ambientUpdate.ambientAir_sr8 = request.POST['ambientAir_sr8']
          ambientUpdate.ambientAir_sr9 = request.POST['ambientAir_sr9']
          ambientUpdate.ambientAir_sr10 = request.POST['ambientAir_sr10']
          ambientUpdate.ambientAir_sr11 = request.POST['ambientAir_sr11']
          ambientUpdate.ambientAir_sr12 = request.POST['ambientAir_sr12']
          ambientUpdate.ambientAir_sr13 = request.POST['ambientAir_sr13']
          ambientUpdate.ambientAir_sr14 = request.POST['ambientAir_sr14']
          ambientUpdate.ambientAir_legend_1 = request.POST['ambientAir-legend-1']
          ambientUpdate.ambientAir_legend_2 = request.POST['ambientAir-legend-2']
          ambientUpdate.ambientAir_legend_3 = request.POST['ambientAir-legend-3']
          ambientUpdate.ambientAir_legend_4 = request.POST['ambientAir-legend-4']
          ambientUpdate.ambientAir_legend_5 = request.POST['ambientAir-legend-5']
          ambientUpdate.ambientAir_legend_6 = request.POST['ambientAir-legend-6']
          ambientUpdate.ambientAir_edit_note = request.POST['ambientAir_editNote']
          ambientUpdate.ambientAir_custom_legend = request.POST['ambientAir_customlegend']
          ambientUpdate.ambientAir_doc_con_1 = request.POST['ambientAir_doc1']
          ambientUpdate.ambientAir_doc_con_2 = request.POST['ambientAir_doc2']
          ambientUpdate.ambientAir_doc_con_3 = request.POST['ambientAir_doc3']
          # ambientUpdate.ambientAir_analyzed_by = request.FILES["ambientAir_analyzedby" ]
          # ambientUpdate.ambientAir_reviewd_by = request.FILES["ambientAir_reviewedby" ]
          # ambientUpdate.ambientAir_approved_by = request.FILES["ambientAir_approvedby" ]
          # ambientUpdate.ambientAir_approved_by1 = request.FILES["ambientAir_approvedby1" ]
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          ambientUpdate.analyst_signature = analyst_sign
          ambientUpdate.assistant_manager_signature = review_sign
          ambientUpdate.lab_manager_signature = approved_sign
          ambientUpdate.created_by = request.user

          extra_field_list = []  # always start empty

          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i].strip()
               parameters = request.POST.getlist('parameters[]')[i].strip()
               unit = request.POST.getlist('unit[]')[i].strip()
               result = request.POST.getlist('result[]')[i].strip()
               limit = request.POST.getlist('limit[]')[i].strip()

               # only add if at least one field is filled (avoid empty rows)
               if sr or parameters or unit or result or limit:
                    extra_field_list.append({
                         "sr": sr,
                         "parameters": parameters,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })

          ambientUpdate.extra_field = json.dumps(extra_field_list)
          
          ambientUpdate.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(ambientUpdate, image_key, '')
                    setattr(ambientUpdate, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(ambientUpdate, image_key, base64_encoded)
                         setattr(ambientUpdate, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(ambientUpdate, desc_key, description)
          
          
          ambientUpdate.save()
          user = request.user
          action = f'Ambient Air Form {ambientUpdate.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')

          id = ambientUpdate.id
          if "update_and_view" in request.POST:
               url = f"/ambientAir-view/{str(id)}/"
               return redirect(to=url)
          else:
               # url = f"/{str(id)}/"
               return redirect(to="ambientAirList")
     else:
          return redirect('ambientAirList')




def ambientAirview(request,pk):
     ambientAir = AmbientAirForm.objects.get(id=pk)
     ambientAir.extra_field = ambientAir.extra_field.replace("'", "\"")
     ambientAir.extra_field = json.loads(ambientAir.extra_field)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{ambientAir.lab_report_no}.png"
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
     context = {'data':ambientAir,'qr':qr_relative_path,'logo':logo}

     return render(request,'ambientAirReport.html',context)


def ambientAirGeneratePDF(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ambientAirGeneratePDF as PDFWithPageNumbers




     ambientAirForm = AmbientAirForm.objects.get(id=pk)
     ambientAirForm.extra_field = ambientAirForm.extra_field.replace("'", "\"")
     ambientAirForm.extra_field = json.loads(ambientAirForm.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Test Result",""],
     ]
     sr_no = 1
     if ambientAirForm.ambientAir_sr1:
          a = [str(sr_no),"Temperature","°C",ambientAirForm.ambientAir_sr1,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr2:
          a = [str(sr_no),"Humidity","%",ambientAirForm.ambientAir_sr2,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr3:
          a = [str(sr_no),"Suspended Particular Matter (SPM)","µg/m³",ambientAirForm.ambientAir_sr3,"500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "SEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "PEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"35"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "NEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"35"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr5:
          a = [str(sr_no),"Particulate matter (PM 10)","µg/m³",ambientAirForm.ambientAir_sr5,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr6:
          a = [str(sr_no),"Carbon Monoxide (CO)","mg/m³",ambientAirForm.ambientAir_sr6,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr7:
          a = [str(sr_no),"Sulphur Dioxide (SO₂)","µg/m³",ambientAirForm.ambientAir_sr7,"120"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr8:
          a = [str(sr_no),"Nitrogen Dioxide (NO₂)","µg/m³",ambientAirForm.ambientAir_sr8,"80"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr9:
          a = [str(sr_no),"Nitrogen Oxide (NO)","µg/m³",ambientAirForm.ambientAir_sr9,"40"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr10:
          a = [str(sr_no),"Oxygen (O₂)","%",ambientAirForm.ambientAir_sr10,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr11:
          a = [str(sr_no),"Formaldehyde","mg/m³",ambientAirForm.ambientAir_sr11,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr12:
          a = [str(sr_no),"Total Volatile Organic Compounds (TVOC)","mg/m³",ambientAirForm.ambientAir_sr12,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr13:
          a = [str(sr_no),"Ozone (O₃)","µg/m³",ambientAirForm.ambientAir_sr13,"130"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr14:
          a = [str(sr_no),"Lead (Pb)","µg/m³",ambientAirForm.ambientAir_sr14,"1.5"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     
     extra_fields = ambientAirForm.extra_field

     for extra_field in extra_fields:
          parameters = extra_field.get("parameters")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")

          if parameters:
               a = [str(sr_no), parameters, unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)                



     pdf = PDFWithPageNumbers(lab_report_no=ambientAirForm.lab_report_no,invoice_bill_no=ambientAirForm.invoice_bill_no,reporting_date=ambientAirForm.reporting_date,report_to=ambientAirForm.report_to,
                              address=ambientAirForm.address,attention=ambientAirForm.attention,email=ambientAirForm.email,sample_id=ambientAirForm.sample_id,ambientAir_test_perf_date=ambientAirForm.ambientAir_test_perf_date,
                              ambienAir_test_desc=ambientAirForm.ambienAir_test_desc,ambientAir_test_type_location=ambientAirForm.ambientAir_test_type_location,ambientAir_test_perf_by=ambientAirForm.ambientAir_test_perf_by,

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True)











     #report data table
     num_rows = 0
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows+=1
               if k == 0: 
                    data_row[4] = ambientAirForm.ambienAir_select + " Limits"

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

    
     if num_rows >=18 and num_rows <=23:
          pdf.add_page()
     Table_Data1 = [
          
     ]
     if ambientAirForm.ambientAir_edit_note:
          a=["Note: "+ambientAirForm.ambientAir_edit_note] 
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
     if ambientAirForm.ambientAir_legend_1:
          a = [ambientAirForm.ambientAir_legend_1]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_2:
          a = [ambientAirForm.ambientAir_legend_2]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_3:
          a = [ambientAirForm.ambientAir_legend_3]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_4:
          a = [ambientAirForm.ambientAir_legend_4]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_5:
          a = [ambientAirForm.ambientAir_legend_5]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_6:
          a = [ambientAirForm.ambientAir_legend_6]
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')





     if ambientAirForm.analyst_signature:
         pdf.image(ambientAirForm.analyst_signature.signature,30,231,20.32,20.32)
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(ambientAirForm.analyst_signature.role if ambientAirForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(ambientAirForm.analyst_signature.role if ambientAirForm.analyst_signature else '')})")
     if ambientAirForm.assistant_manager_signature:
         pdf.image(ambientAirForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({(ambientAirForm.assistant_manager_signature.role if ambientAirForm.assistant_manager_signature else '')})"),250)
     pdf.text(87.5,253,f"Reviewed By ({(ambientAirForm.assistant_manager_signature.role if ambientAirForm.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if ambientAirForm.lab_manager_signature:
         pdf.image(ambientAirForm.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(ambientAirForm.lab_manager_signature.role if ambientAirForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(ambientAirForm.lab_manager_signature.role if ambientAirForm.lab_manager_signature else '')})")



     pdf.line(10,255,-10+pdf.w,255)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,266,txt="• Report is valid for current batch (sample).")
     pdf.text(10,269,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(269.8)
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
     if ambientAirForm.location == "NEQS" and ambientAirForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif ambientAirForm.location == "NEQS" and ambientAirForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
          
     elif ambientAirForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif ambientAirForm.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
     # if ambientAirForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if ambientAirForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:     
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")



     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=ambientAirForm.ambientAir_doc_con_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=ambientAirForm.ambientAir_doc_con_2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,ambientAirForm.ambientAir_doc_con_3)

     if ambientAirForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ambientAirForm, f'pdf_image_{i}')
               desc = getattr(ambientAirForm, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=ambientAirForm.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/ambientAir/'
     # pdf.output(file_path + ambientAirForm.lab_report_no +'.pdf')
     # pdf = open(file_path + ambientAirForm.lab_report_no +'.pdf', 'rb')

     
     # response = FileResponse(pdf)
     # return response
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ambientAirForm.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def ambientAirGeneratePDF1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ambientAirGeneratePDF1 as PDFWithPageNumbers




     ambientAirForm = AmbientAirForm.objects.get(id=pk)
     ambientAirForm.extra_field = ambientAirForm.extra_field.replace("'", "\"")
     ambientAirForm.extra_field = json.loads(ambientAirForm.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Test Result",""],
     ]
     sr_no = 1
     if ambientAirForm.ambientAir_sr1:
          a = [str(sr_no),"Temperature","°C",ambientAirForm.ambientAir_sr1,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr2:
          a = [str(sr_no),"Humidity","%",ambientAirForm.ambientAir_sr2,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr3:
          a = [str(sr_no),"Suspended Particular Matter (SPM)","µg/m³",ambientAirForm.ambientAir_sr3,"500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "SEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "PEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"35"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif ambientAirForm.ambientAir_sr4 and ambientAirForm.ambienAir_select == "NEQS":
          a = [str(sr_no),"Particulate matter (PM 2.5)","µg/m³",ambientAirForm.ambientAir_sr4,"35"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr5:
          a = [str(sr_no),"Particulate matter (PM 10)","µg/m³",ambientAirForm.ambientAir_sr5,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr6:
          a = [str(sr_no),"Carbon Monoxide (CO)","mg/m³",ambientAirForm.ambientAir_sr6,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr7:
          a = [str(sr_no),"Sulphur Dioxide (SO₂)","µg/m³",ambientAirForm.ambientAir_sr7,"120"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr8:
          a = [str(sr_no),"Nitrogen Dioxide (NO₂)","µg/m³",ambientAirForm.ambientAir_sr8,"80"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr9:
          a = [str(sr_no),"Nitrogen Oxide (NO)","µg/m³",ambientAirForm.ambientAir_sr9,"40"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr10:
          a = [str(sr_no),"Oxygen (O₂)","%",ambientAirForm.ambientAir_sr10,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr11:
          a = [str(sr_no),"Formaldehyde","mg/m³",ambientAirForm.ambientAir_sr11,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr12:
          a = [str(sr_no),"Total Volatile Organic Compounds (TVOC)","mg/m³",ambientAirForm.ambientAir_sr12,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr13:
          a = [str(sr_no),"Ozone (O₃)","µg/m³",ambientAirForm.ambientAir_sr13,"130"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ambientAirForm.ambientAir_sr14:
          a = [str(sr_no),"Lead (Pb)","µg/m³",ambientAirForm.ambientAir_sr14,"1.5"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
          
          
          
     extra_fields = ambientAirForm.extra_field

     for extra_field in extra_fields:
          parameters = extra_field.get("parameters")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")

          if parameters:
               a = [str(sr_no), parameters, unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)      


     
     pdf = PDFWithPageNumbers(lab_report_no=ambientAirForm.lab_report_no,invoice_bill_no=ambientAirForm.invoice_bill_no,reporting_date=ambientAirForm.reporting_date,report_to=ambientAirForm.report_to,
                              address=ambientAirForm.address,attention=ambientAirForm.attention,email=ambientAirForm.email,sample_id=ambientAirForm.sample_id,ambientAir_test_perf_date=ambientAirForm.ambientAir_test_perf_date,
                              ambienAir_test_desc=ambientAirForm.ambienAir_test_desc,ambientAir_test_type_location=ambientAirForm.ambientAir_test_type_location,ambientAir_test_perf_by=ambientAirForm.ambientAir_test_perf_by,

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True)











     #report data table
     num_rows = 0
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows+=1
               if k == 0: 
                    data_row[4] = ambientAirForm.ambienAir_select + " Limits"

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

    
     if num_rows >=18 and num_rows <=23:
          pdf.add_page()
     Table_Data1 = [
          
     ]
     if ambientAirForm.ambientAir_edit_note:
          a=["Note: "+ambientAirForm.ambientAir_edit_note] 
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
     if ambientAirForm.ambientAir_legend_1:
          a = [ambientAirForm.ambientAir_legend_1]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_2:
          a = [ambientAirForm.ambientAir_legend_2]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_3:
          a = [ambientAirForm.ambientAir_legend_3]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_4:
          a = [ambientAirForm.ambientAir_legend_4]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_5:
          a = [ambientAirForm.ambientAir_legend_5]
          Table_data_legend.append(a)
          
     if ambientAirForm.ambientAir_legend_6:
          a = [ambientAirForm.ambientAir_legend_6]
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')



     # if ambientAirForm.ambientAir_edit_note:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,210.5,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(208)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=ambientAirForm.ambientAir_edit_note)
     # line_height = 4
     # y = 218
     # if ambientAirForm.ambientAir_legend_1:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_1)
     #      y = y+line_height
     # if ambientAirForm.ambientAir_legend_2:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_2)
     #      y = y+line_height
     # if ambientAirForm.ambientAir_legend_3:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_3)
     #      y = y+line_height
     # if ambientAirForm.ambientAir_legend_4:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_4)
     #      y = y+line_height
     # if ambientAirForm.ambientAir_legend_5:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_5)
     #      y = y+line_height
     # if ambientAirForm.ambientAir_legend_6:
     #      pdf.text(10,y,txt=ambientAirForm.ambientAir_legend_6)


     if ambientAirForm.analyst_signature:
         pdf.image(ambientAirForm.analyst_signature.signature,30,231,20.32,20.32)
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(ambientAirForm.analyst_signature.role if ambientAirForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(ambientAirForm.analyst_signature.role if ambientAirForm.analyst_signature else '')})")
     if ambientAirForm.assistant_manager_signature:
         pdf.image(ambientAirForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({(ambientAirForm.assistant_manager_signature.role if ambientAirForm.assistant_manager_signature else '')})"),250)
     pdf.text(87.5,253,f"Reviewed By ({(ambientAirForm.assistant_manager_signature.role if ambientAirForm.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if ambientAirForm.lab_manager_signature:
         pdf.image(ambientAirForm.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(ambientAirForm.lab_manager_signature.role if ambientAirForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(ambientAirForm.lab_manager_signature.role if ambientAirForm.lab_manager_signature else '')})")



     pdf.line(10,255,-10+pdf.w,255)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,266,txt="• Report is valid for current batch (sample).")
     pdf.text(10,269,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(269.8)
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
     if ambientAirForm.location == "NEQS" and ambientAirForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif ambientAirForm.location == "NEQS" and ambientAirForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
          
     elif ambientAirForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif ambientAirForm.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
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

     # pdf.set_font("Calibri","", 7)
     # pdf.rect(130,277,25,5)
     # pdf.text(132,280,txt=ambientAirForm.ambientAir_doc_con_1)
     # pdf.rect(155,277,25,5)
     # pdf.text(157,280,txt=ambientAirForm.ambientAir_doc_con_2)
     # pdf.rect(180,277,25,5)
     # pdf.text(186.5,280,txt=ambientAirForm.ambientAir_doc_con_3)

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=ambientAirForm.ambientAir_doc_con_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=ambientAirForm.ambientAir_doc_con_2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,ambientAirForm.ambientAir_doc_con_3)
     
     
     if ambientAirForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ambientAirForm, f'pdf_image_{i}')
               desc = getattr(ambientAirForm, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=ambientAirForm.pdf_heading,align="C")
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
     # file_path = '/home/django/EnviTechAlApp/aa_pdf/'
     # pdf.output(file_path + ambientAirForm.lab_report_no +'.pdf')

     # pdf = open(file_path + ambientAirForm.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ambientAirForm.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response




@login_required(login_url="/login")
def ambientAir2List(request):
     AA, _srch = _list_filter(request, AmbientAir2)
     context = {'searched':_srch, "data":AA}
     return render(request,"ambientAir2List.html",context)

@login_required(login_url="/login")
def ambientAir2Delete(request,pk):
     AA = AmbientAir2.objects.get(id=pk)
     AA.delete()
     user = request.user
     action = f'Ambient Air 2 Form {AA.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("ambientAir2List")

@login_required(login_url="/login")
def ambientAir2Edit(request,pk):
     AA = AmbientAir2.objects.get(id=pk)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(AA, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data': AA,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"ambientAir2Edit.html",context)

@login_required(login_url="/login")
def ambientAir2Update(request,pk):
     AA = AmbientAir2.objects.get(id=pk)
     if request.method == 'POST':
          AA.location = request.POST['location']
          industry_id = request.POST.get('industry')
          AA.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          # AA.hours_checkBox = request.POST['hours_checkBox']
          AA.lab_report_no = request.POST['lab_rep_no']
          AA.invoice_bill_no = request.POST['invoice_no']
          AA.reporting_date = request.POST['report_date']
          AA.report_to = request.POST['report_to']
          AA.address = request.POST['address']
          AA.attention = request.POST['attention']
          AA.email = request.POST['email']
          AA.sample_id = request.POST['testId']
          AA.test_perf_date = request.POST['test_perf_date']
          AA.test_type = request.POST['test_type']
          AA.test_desc = request.POST['test_desc']
          AA.test_test_perf_by = request.POST['test_test_perf_by']
          AA.sr1_1 = request.POST['sr1_1']
          AA.sr1_2 = request.POST['sr1_2']
          AA.sr1_3 = request.POST['sr1_3']
          AA.sr1_4 = request.POST['sr1_4']
          AA.sr1_5 = request.POST['sr1_5']
          AA.sr1_6 = request.POST['sr1_6']
          AA.sr1_7 = request.POST['sr1_7']
          AA.sr1_8 = request.POST['sr1_8']
          AA.sr1_9 = request.POST['sr1_9']
          AA.sr1_10 = request.POST['sr1_10']
          AA.sr2_0 = request.POST['sr2_0']
          AA.sr2_1 = request.POST['sr2_1']
          AA.sr2_2 = request.POST['sr2_2']
          AA.sr2_3 = request.POST['sr2_3']
          AA.sr2_4 = request.POST['sr2_4']
          AA.sr2_5 = request.POST['sr2_5']
          AA.sr2_6 = request.POST['sr2_6']
          AA.sr2_7 = request.POST['sr2_7']
          AA.sr2_8 = request.POST['sr2_8']
          AA.sr2_9 = request.POST['sr2_9']
          AA.sr3_0 = request.POST['sr3_0']
          AA.sr3_1 = request.POST['sr3_1']
          AA.sr3_2 = request.POST['sr3_2']
          AA.sr3_3 = request.POST['sr3_3']
          AA.sr3_4 = request.POST['sr3_4']
          AA.sr3_5 = request.POST['sr3_5']
          AA.sr3_6 = request.POST['sr3_6']
          AA.sr3_7 = request.POST['sr3_7']
          AA.sr3_8 = request.POST['sr3_8']
          AA.sr3_9 = request.POST['sr3_9']
          AA.sr4_0 = request.POST['sr4_0']
          AA.sr4_1 = request.POST['sr4_1']
          AA.sr4_2 = request.POST['sr4_2']
          AA.sr4_3 = request.POST['sr4_3']
          AA.sr4_4 = request.POST['sr4_4']
          AA.sr4_5 = request.POST['sr4_5']
          AA.sr4_6 = request.POST['sr4_6']
          AA.sr4_7 = request.POST['sr4_7']
          AA.sr4_8 = request.POST['sr4_8']
          AA.sr4_9 = request.POST['sr4_9']
          AA.sr5_0 = request.POST['sr5_0']
          AA.sr5_1 = request.POST['sr5_1']
          AA.sr5_2 = request.POST['sr5_2']
          AA.sr5_3 = request.POST['sr5_3']
          AA.sr5_4 = request.POST['sr5_4']
          AA.sr5_5 = request.POST['sr5_5']
          AA.sr5_6 = request.POST['sr5_6']
          AA.sr5_7 = request.POST['sr5_7']
          AA.sr5_8 = request.POST['sr5_8']
          AA.sr5_9 = request.POST['sr5_9']
          AA.sr6_0 = request.POST['sr6_0']
          AA.sr6_1 = request.POST['sr6_1']
          AA.sr6_2 = request.POST['sr6_2']
          AA.sr6_3 = request.POST['sr6_3']
          AA.sr6_4 = request.POST['sr6_4']
          AA.sr6_5 = request.POST['sr6_5']
          AA.sr6_6 = request.POST['sr6_6']
          AA.sr6_7 = request.POST['sr6_7']
          AA.sr6_8 = request.POST['sr6_8']
          AA.sr6_9 = request.POST['sr6_9']
          AA.sr7_0 = request.POST['sr7_0']
          AA.sr7_1 = request.POST['sr7_1']
          AA.sr7_2 = request.POST['sr7_2']
          AA.sr7_3 = request.POST['sr7_3']
          AA.sr7_4 = request.POST['sr7_4']
          AA.sr7_5 = request.POST['sr7_5']
          AA.sr7_6 = request.POST['sr7_6']
          AA.sr7_7 = request.POST['sr7_7']
          AA.sr7_8 = request.POST['sr7_8']
          AA.sr7_9 = request.POST['sr7_9']
          AA.sr8_0 = request.POST['sr8_0']
          AA.sr8_1 = request.POST['sr8_1']
          AA.sr8_2 = request.POST['sr8_2']
          AA.sr8_3 = request.POST['sr8_3']
          AA.sr8_4 = request.POST['sr8_4']
          AA.sr8_5 = request.POST['sr8_5']
          AA.sr8_6 = request.POST['sr8_6']
          AA.sr8_7 = request.POST['sr8_7']
          AA.sr8_8 = request.POST['sr8_8']
          AA.sr8_9 = request.POST['sr8_9']
          AA.sr9_0 = request.POST['sr9_0']
          AA.sr9_1 = request.POST['sr9_1']
          AA.sr9_2 = request.POST['sr9_2']
          AA.sr9_3 = request.POST['sr9_3']
          AA.sr9_4 = request.POST['sr9_4']
          AA.sr9_5 = request.POST['sr9_5']
          AA.sr9_6 = request.POST['sr9_6']
          AA.sr9_7 = request.POST['sr9_7']
          AA.sr9_8 = request.POST['sr9_8']
          AA.sr9_9 = request.POST['sr9_9']
          AA.sr10_0 = request.POST['sr10_0']
          AA.sr10_1 = request.POST['sr10_1']
          AA.sr10_2 = request.POST['sr10_2']
          AA.sr10_3 = request.POST['sr10_3']
          AA.sr10_4 = request.POST['sr10_4']
          AA.sr10_5 = request.POST['sr10_5']
          AA.sr10_6 = request.POST['sr10_6']
          AA.sr10_7 = request.POST['sr10_7']
          AA.sr10_8 = request.POST['sr10_8']
          AA.sr10_9 = request.POST['sr10_9']
          AA.sr11_0 = request.POST['sr11_0']
          AA.sr11_1 = request.POST['sr11_1']
          AA.sr11_2 = request.POST['sr11_2']
          AA.sr11_3 = request.POST['sr11_3']
          AA.sr11_4 = request.POST['sr11_4']
          AA.sr11_5 = request.POST['sr11_5']
          AA.sr11_6 = request.POST['sr11_6']
          AA.sr11_7 = request.POST['sr11_7']
          AA.sr11_8 = request.POST['sr11_8']
          AA.sr11_9 = request.POST['sr11_9']
          AA.sr12_0 = request.POST['sr12_0']
          AA.sr12_1 = request.POST['sr12_1']
          AA.sr12_2 = request.POST['sr12_2']
          AA.sr12_3 = request.POST['sr12_3']
          AA.sr12_4 = request.POST['sr12_4']
          AA.sr12_5 = request.POST['sr12_5']
          AA.sr12_6 = request.POST['sr12_6']
          AA.sr12_7 = request.POST['sr12_7']
          AA.sr12_8 = request.POST['sr12_8']
          AA.sr12_9 = request.POST['sr12_9']
          AA.sr13_0 = request.POST['sr13_0']
          AA.sr13_1 = request.POST['sr13_1']
          AA.sr13_2 = request.POST['sr13_2']
          AA.sr13_3 = request.POST['sr13_3']
          AA.sr13_4 = request.POST['sr13_4']
          AA.sr13_5 = request.POST['sr13_5']
          AA.sr13_6 = request.POST['sr13_6']
          AA.sr13_7 = request.POST['sr13_7']
          AA.sr13_8 = request.POST['sr13_8']
          AA.sr13_9 = request.POST['sr13_9']
          AA.sr14_0 = request.POST['sr14_0']
          AA.sr14_1 = request.POST['sr14_1']
          AA.sr14_2 = request.POST['sr14_2']
          AA.sr14_3 = request.POST['sr14_3']
          AA.sr14_4 = request.POST['sr14_4']
          AA.sr14_5 = request.POST['sr14_5']
          AA.sr14_6 = request.POST['sr14_6']
          AA.sr14_7 = request.POST['sr14_7']
          AA.sr14_8 = request.POST['sr14_8']
          AA.sr14_9 = request.POST['sr14_9']
          AA.sr15_0 = request.POST['sr15_0']
          AA.sr15_1 = request.POST['sr15_1']
          AA.sr15_2 = request.POST['sr15_2']
          AA.sr15_3 = request.POST['sr15_3']
          AA.sr15_4 = request.POST['sr15_4']
          AA.sr15_5 = request.POST['sr15_5']
          AA.sr15_6 = request.POST['sr15_6']
          AA.sr15_7 = request.POST['sr15_7']
          AA.sr15_8 = request.POST['sr15_8']
          AA.sr15_9 = request.POST['sr15_9']
          AA.sr16_0 = request.POST['sr16_0']
          AA.sr16_1 = request.POST['sr16_1']
          AA.sr16_2 = request.POST['sr16_2']
          AA.sr16_3 = request.POST['sr16_3']
          AA.sr16_4 = request.POST['sr16_4']
          AA.sr16_5 = request.POST['sr16_5']
          AA.sr16_6 = request.POST['sr16_6']
          AA.sr16_7 = request.POST['sr16_7']
          AA.sr16_8 = request.POST['sr16_8']
          AA.sr16_9 = request.POST['sr16_9']
          AA.sr17_0 = request.POST['sr17_0']
          AA.sr17_1 = request.POST['sr17_1']
          AA.sr17_2 = request.POST['sr17_2']
          AA.sr17_3 = request.POST['sr17_3']
          AA.sr17_4 = request.POST['sr17_4']
          AA.sr17_5 = request.POST['sr17_5']
          AA.sr17_6 = request.POST['sr17_6']
          AA.sr17_7 = request.POST['sr17_7']
          AA.sr17_8 = request.POST['sr17_8']
          AA.sr17_9 = request.POST['sr17_9']
          AA.sr18_0 = request.POST['sr18_0']
          AA.sr18_1 = request.POST['sr18_1']
          AA.sr18_2 = request.POST['sr18_2']
          AA.sr18_3 = request.POST['sr18_3']
          AA.sr18_4 = request.POST['sr18_4']
          AA.sr18_5 = request.POST['sr18_5']
          AA.sr18_6 = request.POST['sr18_6']
          AA.sr18_7 = request.POST['sr18_7']
          AA.sr18_8 = request.POST['sr18_8']
          AA.sr18_9 = request.POST['sr18_9']
          AA.sr19_0 = request.POST['sr19_0']
          AA.sr19_1 = request.POST['sr19_1']
          AA.sr19_2 = request.POST['sr19_2']
          AA.sr19_3 = request.POST['sr19_3']
          AA.sr19_4 = request.POST['sr19_4']
          AA.sr19_5 = request.POST['sr19_5']
          AA.sr19_6 = request.POST['sr19_6']
          AA.sr19_7 = request.POST['sr19_7']
          AA.sr19_8 = request.POST['sr19_8']
          AA.sr19_9 = request.POST['sr19_9']
          AA.sr20_0 = request.POST['sr20_0']
          AA.sr20_1 = request.POST['sr20_1']
          AA.sr20_2 = request.POST['sr20_2']
          AA.sr20_3 = request.POST['sr20_3']
          AA.sr20_4 = request.POST['sr20_4']
          AA.sr20_5 = request.POST['sr20_5']
          AA.sr20_6 = request.POST['sr20_6']
          AA.sr20_7 = request.POST['sr20_7']
          AA.sr20_8 = request.POST['sr20_8']
          AA.sr20_9 = request.POST['sr20_9']
          AA.sr21_0 = request.POST['sr21_0']
          AA.sr21_1 = request.POST['sr21_1']
          AA.sr21_2 = request.POST['sr21_2']
          AA.sr21_3 = request.POST['sr21_3']
          AA.sr21_4 = request.POST['sr21_4']
          AA.sr21_5 = request.POST['sr21_5']
          AA.sr21_6 = request.POST['sr21_6']
          AA.sr21_7 = request.POST['sr21_7']
          AA.sr21_8 = request.POST['sr21_8']
          AA.sr21_9 = request.POST['sr21_9']
          AA.sr22_0 = request.POST['sr22_0']
          AA.sr22_1 = request.POST['sr22_1']
          AA.sr21_2 = request.POST['sr21_2']
          AA.sr21_3 = request.POST['sr21_3']
          AA.sr21_4 = request.POST['sr21_4']
          AA.sr21_5 = request.POST['sr21_5']
          AA.sr21_6 = request.POST['sr21_6']
          AA.sr21_7 = request.POST['sr21_7']
          AA.sr21_8 = request.POST['sr21_8']
          AA.sr21_9 = request.POST['sr21_9']
          AA.sr22_0 = request.POST['sr22_0']
          AA.sr22_1 = request.POST['sr22_1']
          AA.sr22_2 = request.POST['sr22_2']
          AA.sr22_3 = request.POST['sr22_3']
          AA.sr22_4 = request.POST['sr22_4']
          AA.sr22_5 = request.POST['sr22_5']
          AA.sr22_6 = request.POST['sr22_6']
          AA.sr22_7 = request.POST['sr22_7']
          AA.sr22_8 = request.POST['sr22_8']
          AA.sr22_9 = request.POST['sr22_9']
          AA.sr23_0 = request.POST['sr23_0']
          AA.sr23_1 = request.POST['sr23_1']
          AA.sr23_2 = request.POST['sr23_2']
          AA.sr23_3 = request.POST['sr23_3']
          AA.sr23_4 = request.POST['sr23_4']
          AA.sr23_5 = request.POST['sr23_5']
          AA.sr23_6 = request.POST['sr23_6']
          AA.sr23_7 = request.POST['sr23_7']
          AA.sr23_8 = request.POST['sr23_8']
          AA.sr23_9 = request.POST['sr23_9']
          AA.sr24_0 = request.POST['sr24_0']
          AA.sr24_1 = request.POST['sr24_1']
          AA.sr24_2 = request.POST['sr24_2']
          AA.sr24_3 = request.POST['sr24_3']
          AA.sr24_4 = request.POST['sr24_4']
          AA.sr24_5 = request.POST['sr24_5']
          AA.sr24_6 = request.POST['sr24_6']
          AA.sr24_7 = request.POST['sr24_7']
          AA.sr24_8 = request.POST['sr24_8']
          AA.sr24_9 = request.POST['sr24_9']
          AA.sr25_0 = request.POST['sr25_0']
          AA.sr25_1 = request.POST['sr25_1']
          AA.sr25_2 = request.POST['sr25_2']
          AA.sr25_3 = request.POST['sr25_3']
          AA.sr25_4 = request.POST['sr25_4']
          AA.sr25_5 = request.POST['sr25_5']
          AA.sr25_6 = request.POST['sr25_6']
          AA.sr25_7 = request.POST['sr25_7']
          AA.sr25_8 = request.POST['sr25_8']
          AA.seqs_lim_1 = request.POST.get('seqs_lim_1')
          AA.seqs_lim_2 = request.POST.get('seqs_lim_2')
          AA.seqs_lim_3 = request.POST.get('seqs_lim_3')
          AA.seqs_lim_4 = request.POST.get('seqs_lim_4')
          AA.seqs_lim_5 = request.POST.get('seqs_lim_5')
          AA.seqs_lim_6 = request.POST.get('seqs_lim_6')
          AA.seqs_lim_7 = request.POST.get('seqs_lim_7')
          AA.seqs_lim_8 = request.POST.get('seqs_lim_8')
          AA.seqs_lim_9 = request.POST.get('seqs_lim_9')
          
          AA.peqs_lim_1 = request.POST.get('peqs_lim_1')
          AA.peqs_lim_2 = request.POST.get('peqs_lim_2')
          AA.peqs_lim_3 = request.POST.get('peqs_lim_3')
          AA.peqs_lim_4 = request.POST.get('peqs_lim_4')
          AA.peqs_lim_5 = request.POST.get('peqs_lim_5')
          AA.peqs_lim_6 = request.POST.get('peqs_lim_6')
          AA.peqs_lim_7 = request.POST.get('peqs_lim_7')
          AA.peqs_lim_8 = request.POST.get('peqs_lim_8')
          AA.peqs_lim_9 = request.POST.get('peqs_lim_9')
          
          AA.neqs_lim_1 = request.POST.get('neqs_lim_1')
          AA.neqs_lim_2 = request.POST.get('neqs_lim_2')
          AA.neqs_lim_3 = request.POST.get('neqs_lim_3')
          AA.neqs_lim_4 = request.POST.get('neqs_lim_4')
          AA.neqs_lim_5 = request.POST.get('neqs_lim_5')
          AA.neqs_lim_6 = request.POST.get('neqs_lim_6')
          AA.neqs_lim_7 = request.POST.get('neqs_lim_7')
          AA.neqs_lim_8 = request.POST.get('neqs_lim_8')
          AA.neqs_lim_9 = request.POST.get('neqs_lim_9')
          AA.select = request.POST.get('select')
          AA.legend_1 = request.POST['legend_1']
          AA.legend_2 = request.POST['legend_2']
          AA.legend_3 = request.POST['legend_3']
          AA.legend_4 = request.POST['legend_4']
          AA.legend_5 = request.POST['legend_5']
          AA.legend_6 = request.POST['legend_6']
          AA.legend_7 = request.POST['legend_7']
          AA.legend_8 = request.POST['legend_8']
          AA.legend_9 = request.POST['legend_9']
          AA.legend_10 = request.POST['legend_10']
          AA.legend_11 = request.POST['legend_11']
          AA.edit_note = request.POST['edit_note']
          AA.custom_legend = request.POST['custom_legend']
          AA.doc1 = request.POST['doc1']
          AA.doc2 = request.POST['doc2']
          AA.doc3 = request.POST['doc3']
          AA.created_by = request.user
          # AA.analyzedby = request.FILES['analyzedby']
          # AA.reviewedby = request.FILES['reviewedby']
          # AA.approvedby = request.FILES['approvedby']
          # AA.approvedby1 = request.FILES['approvedby1']
          AA.city_location = request.POST['city_location']
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          AA.analyst_signature = analyst_sign
          AA.assistant_manager_signature = review_sign
          AA.lab_manager_signature = approved_sign

          AA.pdf_heading=request.POST.get('pdf_heading')
          AA.col_head_1=request.POST.get('col_head_1')
          AA.col_head_2=request.POST.get('col_head_2')
          AA.col_head_3=request.POST.get('col_head_3')
          AA.col_head_4=request.POST.get('col_head_4')
          AA.col_head_5=request.POST.get('col_head_5')
          AA.col_head_6=request.POST.get('col_head_6')
          AA.col_head_7=request.POST.get('col_head_7')
          AA.col_head_8=request.POST.get('col_head_8')
          AA.col_head_9=request.POST.get('col_head_9')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(AA, image_key, '')
                    setattr(AA, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(AA, image_key, base64_encoded)
                         setattr(AA, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(AA, desc_key, description)

          AA.save()
          user = request.user
          action = f'Ambient Air 2 Form {AA.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = AA.id
          if "submit_and_view" in request.POST:
               url = f"/ambientAir2-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="ambientAir2List")


     return render(request,"ambientAir2List.html")


def ambientAir2View(request,pk):
     AA = AmbientAir2.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{AA.lab_report_no}.png"
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

     context = {'data': AA,'qr':qr_relative_path,'logo':logo}

     return render(request,'ambientAir2Report.html',context)


def ambientAir2Pdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ambientAir2Pdf as PDFWithPageNumbers




     AA2 = AmbientAir2.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#", "Time", (AA2.col_head_1 or "CO")+"\nmg/m³", (AA2.col_head_2 or "NO")+"\nµg/m³", (AA2.col_head_3 or "NO₂")+"\nµg/m³", (AA2.col_head_4 or "SO₂")+"\nµg/m³", (AA2.col_head_5 or "O₃")+"\nµg/m³", (AA2.col_head_6 or "SPM")+"\nµg/m³", (AA2.col_head_7 or "PM10")+"\nµg/m³", (AA2.col_head_8 or "PM2.5")+"\nµg/m³", (AA2.col_head_9 or "Lead")+"\nµg/m³"],
     ]
     sr_no = 1
     if AA2.sr1_2 or AA2.sr1_3 or AA2.sr1_4 or AA2.sr1_5 or AA2.sr1_6 or AA2.sr1_7 or AA2.sr1_8 or AA2.sr1_9 or AA2.sr1_10:
          a = [str(sr_no), AA2.sr1_1, AA2.sr1_2, AA2.sr1_3, AA2.sr1_4, AA2.sr1_5, AA2.sr1_6, AA2.sr1_7, AA2.sr1_8, AA2.sr1_9, AA2.sr1_10]
          
          if AA2.sr1_2 is None:
               a[2] = "N.A."
          if AA2.sr1_3 is None:
               a[3] = "N.A."
          
          sr_no = sr_no + 1
          TABLE_DATA.append(a)
     
          

     if AA2.sr2_1 or  AA2.sr2_2 or AA2.sr2_3 or AA2.sr2_4 or AA2.sr2_5 or AA2.sr2_6 or AA2.sr2_7 or AA2.sr2_8 or AA2.sr2_9:
          a = [str(sr_no),AA2.sr2_0,AA2.sr2_1,AA2.sr2_2,AA2.sr2_3,AA2.sr2_4,AA2.sr2_5,AA2.sr2_6,AA2.sr2_7,AA2.sr2_8,AA2.sr2_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr3_1 or  AA2.sr3_2 or AA2.sr3_3 or AA2.sr3_4 or AA2.sr3_5 or AA2.sr3_6 or AA2.sr3_7 or AA2.sr3_8 or AA2.sr3_9:
          a = [str(sr_no),AA2.sr3_0,AA2.sr3_1,AA2.sr3_2,AA2.sr3_3,AA2.sr3_4,AA2.sr3_5,AA2.sr3_6,AA2.sr3_7,AA2.sr3_8,AA2.sr3_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr4_1 or  AA2.sr4_2 or AA2.sr4_3 or AA2.sr4_4 or AA2.sr4_5 or AA2.sr4_6 or AA2.sr4_7 or AA2.sr4_8 or AA2.sr4_9:
          a = [str(sr_no),AA2.sr4_0,AA2.sr4_1,AA2.sr4_2,AA2.sr4_3,AA2.sr4_4,AA2.sr4_5,AA2.sr4_6,AA2.sr4_7,AA2.sr4_8,AA2.sr4_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr5_1 or  AA2.sr5_2 or AA2.sr5_3 or AA2.sr5_4 or AA2.sr5_5 or AA2.sr5_6 or AA2.sr5_7 or AA2.sr5_8 or AA2.sr5_9:
          a = [str(sr_no),AA2.sr5_0,AA2.sr5_1,AA2.sr5_2,AA2.sr5_3,AA2.sr5_4,AA2.sr5_5,AA2.sr5_6,AA2.sr5_7,AA2.sr5_8,AA2.sr5_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr6_1 or  AA2.sr6_2 or AA2.sr6_3 or AA2.sr6_4 or AA2.sr6_5 or AA2.sr6_6 or AA2.sr6_7 or AA2.sr6_8 or AA2.sr6_9:
          a = [str(sr_no),AA2.sr6_0,AA2.sr6_1,AA2.sr6_2,AA2.sr6_3,AA2.sr6_4,AA2.sr6_5,AA2.sr6_6,AA2.sr6_7,AA2.sr6_8,AA2.sr6_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr7_1 or  AA2.sr7_2 or AA2.sr7_3 or AA2.sr7_4 or AA2.sr7_5 or AA2.sr7_6 or AA2.sr7_7 or AA2.sr7_8 or AA2.sr7_9:
          a = [str(sr_no),AA2.sr7_0,AA2.sr7_1,AA2.sr7_2,AA2.sr7_3,AA2.sr7_4,AA2.sr7_5,AA2.sr7_6,AA2.sr7_7,AA2.sr7_8,AA2.sr7_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr8_1 or  AA2.sr8_2 or AA2.sr8_3 or AA2.sr8_4 or AA2.sr8_5 or AA2.sr8_6 or AA2.sr8_7 or AA2.sr8_8 or AA2.sr8_9:
          a = [str(sr_no),AA2.sr8_0,AA2.sr8_1,AA2.sr8_2,AA2.sr8_3,AA2.sr8_4,AA2.sr8_5,AA2.sr8_6,AA2.sr8_7,AA2.sr8_8,AA2.sr8_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr9_1 or  AA2.sr9_2 or AA2.sr9_3 or AA2.sr9_4 or AA2.sr9_5 or AA2.sr9_6 or AA2.sr9_7 or AA2.sr9_8 or AA2.sr9_9:
          a = [str(sr_no),AA2.sr9_0,AA2.sr9_1,AA2.sr9_2,AA2.sr9_3,AA2.sr9_4,AA2.sr9_5,AA2.sr9_6,AA2.sr9_7,AA2.sr9_8,AA2.sr9_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr10_1 or  AA2.sr10_2 or AA2.sr10_3 or AA2.sr10_4 or AA2.sr10_5 or AA2.sr10_6 or AA2.sr10_7 or AA2.sr10_8 or AA2.sr10_9 :
          a = [str(sr_no),AA2.sr10_0,AA2.sr10_1,AA2.sr10_2,AA2.sr10_3,AA2.sr10_4,AA2.sr10_5,AA2.sr10_6,AA2.sr10_7,AA2.sr10_8,AA2.sr10_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr11_1 or  AA2.sr11_2 or AA2.sr11_3 or AA2.sr11_4 or AA2.sr11_5 or AA2.sr11_6 or AA2.sr11_7 or AA2.sr11_8 or AA2.sr11_9 :
          a = [str(sr_no),AA2.sr11_0,AA2.sr11_1,AA2.sr11_2,AA2.sr11_3,AA2.sr11_4,AA2.sr11_5,AA2.sr11_6,AA2.sr11_7,AA2.sr11_8,AA2.sr11_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if  AA2.sr12_1 or  AA2.sr12_2 or AA2.sr12_3 or AA2.sr12_4 or AA2.sr12_5 or AA2.sr12_6 or AA2.sr12_7 or AA2.sr12_8 or AA2.sr12_9 :
          a = [str(sr_no),AA2.sr12_0,AA2.sr12_1,AA2.sr12_2,AA2.sr12_3,AA2.sr12_4,AA2.sr12_5,AA2.sr12_6,AA2.sr12_7,AA2.sr12_8,AA2.sr12_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr13_1 or  AA2.sr13_2 or AA2.sr13_3 or AA2.sr13_4 or AA2.sr13_5 or AA2.sr13_6 or AA2.sr13_7 or AA2.sr13_8 or AA2.sr13_9 :
          a = [str(sr_no),AA2.sr13_0,AA2.sr13_1,AA2.sr13_2,AA2.sr13_3,AA2.sr13_4,AA2.sr13_5,AA2.sr13_6,AA2.sr13_7,AA2.sr13_8,AA2.sr13_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr14_1 or  AA2.sr14_2 or AA2.sr14_3 or AA2.sr14_4 or AA2.sr14_5 or AA2.sr14_6 or AA2.sr14_7 or AA2.sr14_8 or AA2.sr14_9 :
          a = [str(sr_no),AA2.sr14_0,AA2.sr14_1,AA2.sr14_2,AA2.sr14_3,AA2.sr14_4,AA2.sr14_5,AA2.sr14_6,AA2.sr14_7,AA2.sr14_8,AA2.sr14_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr15_1 or  AA2.sr15_2 or AA2.sr15_3 or AA2.sr15_4 or AA2.sr15_5 or AA2.sr15_6 or AA2.sr15_7 or AA2.sr15_8 or AA2.sr15_9 :
          a = [str(sr_no),AA2.sr15_0,AA2.sr15_1,AA2.sr15_2,AA2.sr15_3,AA2.sr15_4,AA2.sr15_5,AA2.sr15_6,AA2.sr15_7,AA2.sr15_8,AA2.sr15_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr16_1 or  AA2.sr16_2 or AA2.sr16_3 or AA2.sr16_4 or AA2.sr16_5 or AA2.sr16_6 or AA2.sr16_7 or AA2.sr16_8 or AA2.sr16_9 :
          a = [str(sr_no),AA2.sr16_0,AA2.sr16_1,AA2.sr16_2,AA2.sr16_3,AA2.sr16_4,AA2.sr16_5,AA2.sr16_6,AA2.sr16_7,AA2.sr16_8,AA2.sr16_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr17_1 or  AA2.sr17_2 or AA2.sr17_3 or AA2.sr17_4 or AA2.sr17_5 or AA2.sr17_6 or AA2.sr17_7 or AA2.sr17_8 or AA2.sr17_9 :
          a = [str(sr_no),AA2.sr17_0,AA2.sr17_1,AA2.sr17_2,AA2.sr17_3,AA2.sr17_4,AA2.sr17_5,AA2.sr17_6,AA2.sr17_7,AA2.sr17_8,AA2.sr17_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr18_1 or  AA2.sr18_2 or AA2.sr18_3 or AA2.sr18_4 or AA2.sr18_5 or AA2.sr18_6 or AA2.sr18_7 or AA2.sr18_8 or AA2.sr18_9 :
          a = [str(sr_no),AA2.sr18_0,AA2.sr18_1,AA2.sr18_2,AA2.sr18_3,AA2.sr18_4,AA2.sr18_5,AA2.sr18_6,AA2.sr18_7,AA2.sr18_8,AA2.sr18_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr19_1 or  AA2.sr19_2 or AA2.sr19_3 or AA2.sr19_4 or AA2.sr19_5 or AA2.sr19_6 or AA2.sr19_7 or AA2.sr19_8 or AA2.sr19_9 :
          a = [str(sr_no),AA2.sr19_0,AA2.sr19_1,AA2.sr19_2,AA2.sr19_3,AA2.sr19_4,AA2.sr19_5,AA2.sr19_6,AA2.sr19_7,AA2.sr19_8,AA2.sr19_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr20_1 or  AA2.sr20_2 or AA2.sr20_3 or AA2.sr20_4 or AA2.sr20_5 or AA2.sr20_6 or AA2.sr20_7 or AA2.sr20_8 or AA2.sr20_9 :
          a = [str(sr_no),AA2.sr20_0,AA2.sr20_1,AA2.sr20_2,AA2.sr20_3,AA2.sr20_4,AA2.sr20_5,AA2.sr20_6,AA2.sr20_7,AA2.sr20_8,AA2.sr20_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr21_1 or  AA2.sr21_2 or AA2.sr21_3 or AA2.sr21_4 or AA2.sr21_5 or AA2.sr21_6 or AA2.sr21_7 or AA2.sr21_8 or AA2.sr21_9 :
          a = [str(sr_no),AA2.sr21_0,AA2.sr21_1,AA2.sr21_2,AA2.sr21_3,AA2.sr21_4,AA2.sr21_5,AA2.sr21_6,AA2.sr21_7,AA2.sr21_8,AA2.sr21_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr22_1 or  AA2.sr22_2 or AA2.sr22_3 or AA2.sr22_4 or AA2.sr22_5 or AA2.sr22_6 or AA2.sr22_7 or AA2.sr22_8 or AA2.sr22_9 :
          a = [str(sr_no),AA2.sr22_0,AA2.sr22_1,AA2.sr22_2,AA2.sr22_3,AA2.sr22_4,AA2.sr22_5,AA2.sr22_6,AA2.sr22_7,AA2.sr22_8,AA2.sr22_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr23_1 or  AA2.sr23_2 or AA2.sr23_3 or AA2.sr23_4 or AA2.sr23_5 or AA2.sr23_6 or AA2.sr23_7 or AA2.sr23_8 or AA2.sr23_9 :
          a = [str(sr_no),AA2.sr23_0,AA2.sr23_1,AA2.sr23_2,AA2.sr23_3,AA2.sr23_4,AA2.sr23_5,AA2.sr23_6,AA2.sr23_7,AA2.sr23_8,AA2.sr23_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr24_1 or  AA2.sr24_2 or AA2.sr24_3 or AA2.sr24_4 or AA2.sr24_5 or AA2.sr24_6 or AA2.sr24_7 or AA2.sr24_8 or AA2.sr24_9 :
          a = [str(sr_no),AA2.sr24_0,AA2.sr24_1,AA2.sr24_2,AA2.sr24_3,AA2.sr24_4,AA2.sr24_5,AA2.sr24_6,AA2.sr24_7,AA2.sr24_8,AA2.sr24_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr25_1 or  AA2.sr25_2 or AA2.sr25_3 or AA2.sr25_4 or AA2.sr25_5 or AA2.sr25_6 or AA2.sr25_7 or AA2.sr25_8:
          a=["Average","-",AA2.sr25_0,AA2.sr25_1,AA2.sr25_2,AA2.sr25_3,AA2.sr25_4,AA2.sr25_5,AA2.sr25_6,AA2.sr25_7,AA2.sr25_8]
          
          TABLE_DATA.append(a)
     if AA2.location == "SEQS":
          a=["SEQS","",f"{AA2.seqs_lim_1}",f"{AA2.seqs_lim_2}",f"{AA2.seqs_lim_3}",f"{AA2.seqs_lim_4}",f"{AA2.seqs_lim_5}",f"{AA2.seqs_lim_6}",f"{AA2.seqs_lim_7}",f"{AA2.seqs_lim_8}",f"{AA2.seqs_lim_9}"]
          
          TABLE_DATA.append(a)
     if AA2.location == "PEQS":
          a=["PEQS","",f"{AA2.peqs_lim_1}",f"{AA2.peqs_lim_2}",f"{AA2.peqs_lim_3}",f"{AA2.peqs_lim_4}",f"{AA2.peqs_lim_5}",f"{AA2.peqs_lim_6}",f"{AA2.peqs_lim_7}",f"{AA2.peqs_lim_8}",f"{AA2.peqs_lim_9}"]
          
          TABLE_DATA.append(a)
     if AA2.location == "NEQS":
          a=["NEQS","",f"{AA2.peqs_lim_1}",f"{AA2.neqs_lim_2}",f"{AA2.neqs_lim_3}",f"{AA2.neqs_lim_4}",f"{AA2.neqs_lim_5}",f"{AA2.neqs_lim_6}",f"{AA2.neqs_lim_7}",f"{AA2.neqs_lim_8}",f"{AA2.neqs_lim_9}"]
          
          TABLE_DATA.append(a) 







     last_row_index = len(TABLE_DATA) - 1
     pdf = PDFWithPageNumbers(lab_report_no=AA2.lab_report_no,invoice_bill_no=AA2.invoice_bill_no,reporting_date=AA2.reporting_date,report_to=AA2.report_to,
                              address=AA2.address,attention=AA2.attention,email=AA2.email,sample_id=AA2.sample_id,test_perf_date=AA2.test_perf_date,
                              test_desc=AA2.test_desc,test_type=AA2.test_type,test_test_perf_by=AA2.test_test_perf_by

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=12)










     num_rows=0
     #report data table
     with pdf.table(col_widths=(15, 20, 20,20,20,20,20,20,20,20,20),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER','CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows = num_rows+1

               # if k == 0:
               #      data_row[4] = AA2.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)
     
     if num_rows >=15 and num_rows <=18:
          pdf.add_page()   
     Table_Data1 = [
          
     ]
     
     pdf.set_font_size(8)
     if AA2.edit_note:
          a=["Note: "+AA2.edit_note] 
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
     if AA2.legend_1:
          a = [AA2.legend_1]
          Table_data_legend.append(a)
          
     if AA2.legend_2:
          a = [AA2.legend_2]
          Table_data_legend.append(a)
          
     if AA2.legend_3:
          a = [AA2.legend_3]
          Table_data_legend.append(a)
          
     if AA2.legend_4:
          a = [AA2.legend_4]
          Table_data_legend.append(a)
          
     if AA2.legend_5:
          a = [AA2.legend_5]
          Table_data_legend.append(a)
          
     if AA2.legend_6:
          a = [AA2.legend_6]
          Table_data_legend.append(a)
          
     if AA2.legend_7:
          a = [AA2.legend_7]
          Table_data_legend.append(a)
          
     if AA2.legend_8:
          a = [AA2.legend_8]
          Table_data_legend.append(a)
          
     if AA2.legend_9:
          a = [AA2.legend_9]
          Table_data_legend.append(a)
          
     if AA2.legend_10:
          a = [AA2.legend_10]
          Table_data_legend.append(a)
          
     if AA2.legend_11:
          a = [AA2.legend_11]
          Table_data_legend.append(a)
          

     if AA2.custom_legend:
          a = [AA2.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')  
                    
                    
                      


     

     # pdf.image(AA2.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(AA2.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(AA2.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     
     if AA2.analyst_signature:
         pdf.image(AA2.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(AA2.analyst_signature.role if AA2.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(AA2.analyst_signature.role if AA2.analyst_signature else '')})")
     if AA2.assistant_manager_signature:
         pdf.image(AA2.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(AA2.assistant_manager_signature.role if AA2.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(AA2.assistant_manager_signature.role if AA2.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if AA2.lab_manager_signature:
         pdf.image(AA2.lab_manager_signature.signature,178,235,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(AA2.lab_manager_signature.role if AA2.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(AA2.lab_manager_signature.role if AA2.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,261,-10+pdf.w,261)
     pdf.set_font("Calibri","", 8)
     pdf.text(10,270,txt="• Report is valid for current batch (sample).")
     pdf.text(10,273.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(274.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(278)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(282)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,264,19,15)
     # if AA2.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if AA2.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17)  
     # if AA2.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)        
     # if AA2.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     if AA2.location == "NEQS" and AA2.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif AA2.location == "NEQS" and AA2.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif AA2.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif AA2.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,281,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,282,25,5)
     pdf.text(128,285,txt=AA2.doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=AA2.doc2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=AA2.doc3)
     
     if AA2.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(AA2, f'pdf_image_{i}')
               desc = getattr(AA2, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=AA2.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/ambientAir2/'
     # pdf.output(file_path + AA2.lab_report_no +'.pdf')
     # pdf = open(file_path + AA2.lab_report_no +'.pdf', 'rb')
     # # pdf.output(AA2.lab_report_no +'.pdf')

     # # pdf = open(AA2.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={AA2.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response


def ambientAir2Pdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ambientAir2Pdf1 as PDFWithPageNumbers




     AA2 = AmbientAir2.objects.get(id=pk)


     TABLE_DATA = [
                ["Sr.#", "Time", (AA2.col_head_1 or "CO")+"\nmg/m³", (AA2.col_head_2 or "NO")+"\nµg/m³", (AA2.col_head_3 or "NO₂")+"\nµg/m³", (AA2.col_head_4 or "SO₂")+"\nµg/m³", (AA2.col_head_5 or "O₃")+"\nµg/m³", (AA2.col_head_6 or "SPM")+"\nµg/m³", (AA2.col_head_7 or "PM10")+"\nµg/m³", (AA2.col_head_8 or "PM2.5")+"\nµg/m³", (AA2.col_head_9 or "Lead")+"\nµg/m³"],
     ]
     sr_no = 1
     if AA2.sr1_2 or AA2.sr1_3 or AA2.sr1_4 or AA2.sr1_5 or AA2.sr1_6 or AA2.sr1_7 or AA2.sr1_8 or AA2.sr1_9 or AA2.sr1_10:
          a = [str(sr_no), AA2.sr1_1, AA2.sr1_2, AA2.sr1_3, AA2.sr1_4, AA2.sr1_5, AA2.sr1_6, AA2.sr1_7, AA2.sr1_8, AA2.sr1_9, AA2.sr1_10]
          
          if AA2.sr1_2 is None:
               a[2] = "N.A."
          if AA2.sr1_3 is None:
               a[3] = "N.A."
          
          sr_no = sr_no + 1
          TABLE_DATA.append(a)
     
          

     if AA2.sr2_1 or  AA2.sr2_2 or AA2.sr2_3 or AA2.sr2_4 or AA2.sr2_5 or AA2.sr2_6 or AA2.sr2_7 or AA2.sr2_8 or AA2.sr2_9:
          a = [str(sr_no),AA2.sr2_0,AA2.sr2_1,AA2.sr2_2,AA2.sr2_3,AA2.sr2_4,AA2.sr2_5,AA2.sr2_6,AA2.sr2_7,AA2.sr2_8,AA2.sr2_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr3_1 or  AA2.sr3_2 or AA2.sr3_3 or AA2.sr3_4 or AA2.sr3_5 or AA2.sr3_6 or AA2.sr3_7 or AA2.sr3_8 or AA2.sr3_9:
          a = [str(sr_no),AA2.sr3_0,AA2.sr3_1,AA2.sr3_2,AA2.sr3_3,AA2.sr3_4,AA2.sr3_5,AA2.sr3_6,AA2.sr3_7,AA2.sr3_8,AA2.sr3_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr4_1 or  AA2.sr4_2 or AA2.sr4_3 or AA2.sr4_4 or AA2.sr4_5 or AA2.sr4_6 or AA2.sr4_7 or AA2.sr4_8 or AA2.sr4_9:
          a = [str(sr_no),AA2.sr4_0,AA2.sr4_1,AA2.sr4_2,AA2.sr4_3,AA2.sr4_4,AA2.sr4_5,AA2.sr4_6,AA2.sr4_7,AA2.sr4_8,AA2.sr4_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr5_1 or  AA2.sr5_2 or AA2.sr5_3 or AA2.sr5_4 or AA2.sr5_5 or AA2.sr5_6 or AA2.sr5_7 or AA2.sr5_8 or AA2.sr5_9:
          a = [str(sr_no),AA2.sr5_0,AA2.sr5_1,AA2.sr5_2,AA2.sr5_3,AA2.sr5_4,AA2.sr5_5,AA2.sr5_6,AA2.sr5_7,AA2.sr5_8,AA2.sr5_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr6_1 or  AA2.sr6_2 or AA2.sr6_3 or AA2.sr6_4 or AA2.sr6_5 or AA2.sr6_6 or AA2.sr6_7 or AA2.sr6_8 or AA2.sr6_9:
          a = [str(sr_no),AA2.sr6_0,AA2.sr6_1,AA2.sr6_2,AA2.sr6_3,AA2.sr6_4,AA2.sr6_5,AA2.sr6_6,AA2.sr6_7,AA2.sr6_8,AA2.sr6_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr7_1 or  AA2.sr7_2 or AA2.sr7_3 or AA2.sr7_4 or AA2.sr7_5 or AA2.sr7_6 or AA2.sr7_7 or AA2.sr7_8 or AA2.sr7_9:
          a = [str(sr_no),AA2.sr7_0,AA2.sr7_1,AA2.sr7_2,AA2.sr7_3,AA2.sr7_4,AA2.sr7_5,AA2.sr7_6,AA2.sr7_7,AA2.sr7_8,AA2.sr7_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr8_1 or  AA2.sr8_2 or AA2.sr8_3 or AA2.sr8_4 or AA2.sr8_5 or AA2.sr8_6 or AA2.sr8_7 or AA2.sr8_8 or AA2.sr8_9:
          a = [str(sr_no),AA2.sr8_0,AA2.sr8_1,AA2.sr8_2,AA2.sr8_3,AA2.sr8_4,AA2.sr8_5,AA2.sr8_6,AA2.sr8_7,AA2.sr8_8,AA2.sr8_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr9_1 or  AA2.sr9_2 or AA2.sr9_3 or AA2.sr9_4 or AA2.sr9_5 or AA2.sr9_6 or AA2.sr9_7 or AA2.sr9_8 or AA2.sr9_9:
          a = [str(sr_no),AA2.sr9_0,AA2.sr9_1,AA2.sr9_2,AA2.sr9_3,AA2.sr9_4,AA2.sr9_5,AA2.sr9_6,AA2.sr9_7,AA2.sr9_8,AA2.sr9_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr10_1 or  AA2.sr10_2 or AA2.sr10_3 or AA2.sr10_4 or AA2.sr10_5 or AA2.sr10_6 or AA2.sr10_7 or AA2.sr10_8 or AA2.sr10_9 :
          a = [str(sr_no),AA2.sr10_0,AA2.sr10_1,AA2.sr10_2,AA2.sr10_3,AA2.sr10_4,AA2.sr10_5,AA2.sr10_6,AA2.sr10_7,AA2.sr10_8,AA2.sr10_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr11_1 or  AA2.sr11_2 or AA2.sr11_3 or AA2.sr11_4 or AA2.sr11_5 or AA2.sr11_6 or AA2.sr11_7 or AA2.sr11_8 or AA2.sr11_9 :
          a = [str(sr_no),AA2.sr11_0,AA2.sr11_1,AA2.sr11_2,AA2.sr11_3,AA2.sr11_4,AA2.sr11_5,AA2.sr11_6,AA2.sr11_7,AA2.sr11_8,AA2.sr11_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if  AA2.sr12_1 or  AA2.sr12_2 or AA2.sr12_3 or AA2.sr12_4 or AA2.sr12_5 or AA2.sr12_6 or AA2.sr12_7 or AA2.sr12_8 or AA2.sr12_9 :
          a = [str(sr_no),AA2.sr12_0,AA2.sr12_1,AA2.sr12_2,AA2.sr12_3,AA2.sr12_4,AA2.sr12_5,AA2.sr12_6,AA2.sr12_7,AA2.sr12_8,AA2.sr12_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr13_1 or  AA2.sr13_2 or AA2.sr13_3 or AA2.sr13_4 or AA2.sr13_5 or AA2.sr13_6 or AA2.sr13_7 or AA2.sr13_8 or AA2.sr13_9 :
          a = [str(sr_no),AA2.sr13_0,AA2.sr13_1,AA2.sr13_2,AA2.sr13_3,AA2.sr13_4,AA2.sr13_5,AA2.sr13_6,AA2.sr13_7,AA2.sr13_8,AA2.sr13_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr14_1 or  AA2.sr14_2 or AA2.sr14_3 or AA2.sr14_4 or AA2.sr14_5 or AA2.sr14_6 or AA2.sr14_7 or AA2.sr14_8 or AA2.sr14_9 :
          a = [str(sr_no),AA2.sr14_0,AA2.sr14_1,AA2.sr14_2,AA2.sr14_3,AA2.sr14_4,AA2.sr14_5,AA2.sr14_6,AA2.sr14_7,AA2.sr14_8,AA2.sr14_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr15_1 or  AA2.sr15_2 or AA2.sr15_3 or AA2.sr15_4 or AA2.sr15_5 or AA2.sr15_6 or AA2.sr15_7 or AA2.sr15_8 or AA2.sr15_9 :
          a = [str(sr_no),AA2.sr15_0,AA2.sr15_1,AA2.sr15_2,AA2.sr15_3,AA2.sr15_4,AA2.sr15_5,AA2.sr15_6,AA2.sr15_7,AA2.sr15_8,AA2.sr15_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr16_1 or  AA2.sr16_2 or AA2.sr16_3 or AA2.sr16_4 or AA2.sr16_5 or AA2.sr16_6 or AA2.sr16_7 or AA2.sr16_8 or AA2.sr16_9 :
          a = [str(sr_no),AA2.sr16_0,AA2.sr16_1,AA2.sr16_2,AA2.sr16_3,AA2.sr16_4,AA2.sr16_5,AA2.sr16_6,AA2.sr16_7,AA2.sr16_8,AA2.sr16_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr17_1 or  AA2.sr17_2 or AA2.sr17_3 or AA2.sr17_4 or AA2.sr17_5 or AA2.sr17_6 or AA2.sr17_7 or AA2.sr17_8 or AA2.sr17_9 :
          a = [str(sr_no),AA2.sr17_0,AA2.sr17_1,AA2.sr17_2,AA2.sr17_3,AA2.sr17_4,AA2.sr17_5,AA2.sr17_6,AA2.sr17_7,AA2.sr17_8,AA2.sr17_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr18_1 or  AA2.sr18_2 or AA2.sr18_3 or AA2.sr18_4 or AA2.sr18_5 or AA2.sr18_6 or AA2.sr18_7 or AA2.sr18_8 or AA2.sr18_9 :
          a = [str(sr_no),AA2.sr18_0,AA2.sr18_1,AA2.sr18_2,AA2.sr18_3,AA2.sr18_4,AA2.sr18_5,AA2.sr18_6,AA2.sr18_7,AA2.sr18_8,AA2.sr18_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr19_1 or  AA2.sr19_2 or AA2.sr19_3 or AA2.sr19_4 or AA2.sr19_5 or AA2.sr19_6 or AA2.sr19_7 or AA2.sr19_8 or AA2.sr19_9 :
          a = [str(sr_no),AA2.sr19_0,AA2.sr19_1,AA2.sr19_2,AA2.sr19_3,AA2.sr19_4,AA2.sr19_5,AA2.sr19_6,AA2.sr19_7,AA2.sr19_8,AA2.sr19_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr20_1 or  AA2.sr20_2 or AA2.sr20_3 or AA2.sr20_4 or AA2.sr20_5 or AA2.sr20_6 or AA2.sr20_7 or AA2.sr20_8 or AA2.sr20_9 :
          a = [str(sr_no),AA2.sr20_0,AA2.sr20_1,AA2.sr20_2,AA2.sr20_3,AA2.sr20_4,AA2.sr20_5,AA2.sr20_6,AA2.sr20_7,AA2.sr20_8,AA2.sr20_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr21_1 or  AA2.sr21_2 or AA2.sr21_3 or AA2.sr21_4 or AA2.sr21_5 or AA2.sr21_6 or AA2.sr21_7 or AA2.sr21_8 or AA2.sr21_9 :
          a = [str(sr_no),AA2.sr21_0,AA2.sr21_1,AA2.sr21_2,AA2.sr21_3,AA2.sr21_4,AA2.sr21_5,AA2.sr21_6,AA2.sr21_7,AA2.sr21_8,AA2.sr21_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr22_1 or  AA2.sr22_2 or AA2.sr22_3 or AA2.sr22_4 or AA2.sr22_5 or AA2.sr22_6 or AA2.sr22_7 or AA2.sr22_8 or AA2.sr22_9 :
          a = [str(sr_no),AA2.sr22_0,AA2.sr22_1,AA2.sr22_2,AA2.sr22_3,AA2.sr22_4,AA2.sr22_5,AA2.sr22_6,AA2.sr22_7,AA2.sr22_8,AA2.sr22_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr23_1 or  AA2.sr23_2 or AA2.sr23_3 or AA2.sr23_4 or AA2.sr23_5 or AA2.sr23_6 or AA2.sr23_7 or AA2.sr23_8 or AA2.sr23_9 :
          a = [str(sr_no),AA2.sr23_0,AA2.sr23_1,AA2.sr23_2,AA2.sr23_3,AA2.sr23_4,AA2.sr23_5,AA2.sr23_6,AA2.sr23_7,AA2.sr23_8,AA2.sr23_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr24_1 or  AA2.sr24_2 or AA2.sr24_3 or AA2.sr24_4 or AA2.sr24_5 or AA2.sr24_6 or AA2.sr24_7 or AA2.sr24_8 or AA2.sr24_9 :
          a = [str(sr_no),AA2.sr24_0,AA2.sr24_1,AA2.sr24_2,AA2.sr24_3,AA2.sr24_4,AA2.sr24_5,AA2.sr24_6,AA2.sr24_7,AA2.sr24_8,AA2.sr24_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if AA2.sr25_1 or  AA2.sr25_2 or AA2.sr25_3 or AA2.sr25_4 or AA2.sr25_5 or AA2.sr25_6 or AA2.sr25_7 or AA2.sr25_8:
          a=["Average","-",AA2.sr25_0,AA2.sr25_1,AA2.sr25_2,AA2.sr25_3,AA2.sr25_4,AA2.sr25_5,AA2.sr25_6,AA2.sr25_7,AA2.sr25_8]
          
          TABLE_DATA.append(a)
     if AA2.location == "SEQS":
          a=["SEQS","",f"{AA2.seqs_lim_1}",f"{AA2.seqs_lim_2}",f"{AA2.seqs_lim_3}",f"{AA2.seqs_lim_4}",f"{AA2.seqs_lim_5}",f"{AA2.seqs_lim_6}",f"{AA2.seqs_lim_7}",f"{AA2.seqs_lim_8}",f"{AA2.seqs_lim_9}"]
          
          TABLE_DATA.append(a)
     if AA2.location == "PEQS":
          a=["PEQS","",f"{AA2.peqs_lim_1}",f"{AA2.peqs_lim_2}",f"{AA2.peqs_lim_3}",f"{AA2.peqs_lim_4}",f"{AA2.peqs_lim_5}",f"{AA2.peqs_lim_6}",f"{AA2.peqs_lim_7}",f"{AA2.peqs_lim_8}",f"{AA2.peqs_lim_9}"]
          
          TABLE_DATA.append(a)
     if AA2.location == "NEQS":
          a=["NEQS","",f"{AA2.peqs_lim_1}",f"{AA2.neqs_lim_2}",f"{AA2.neqs_lim_3}",f"{AA2.neqs_lim_4}",f"{AA2.neqs_lim_5}",f"{AA2.neqs_lim_6}",f"{AA2.neqs_lim_7}",f"{AA2.neqs_lim_8}",f"{AA2.neqs_lim_9}"]
          
          TABLE_DATA.append(a)
       







     last_row_index = len(TABLE_DATA) - 1
     pdf = PDFWithPageNumbers(lab_report_no=AA2.lab_report_no,invoice_bill_no=AA2.invoice_bill_no,reporting_date=AA2.reporting_date,report_to=AA2.report_to,
                              address=AA2.address,attention=AA2.attention,email=AA2.email,sample_id=AA2.sample_id,test_perf_date=AA2.test_perf_date,
                              test_desc=AA2.test_desc,test_type=AA2.test_type,test_test_perf_by=AA2.test_test_perf_by

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=12)










     num_rows=0
     #report data table
     with pdf.table(col_widths=(15, 20, 20,20,20,20,20,20,20,20,20),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER','CENTER','CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows = num_rows+1

               # if k == 0:
               #      data_row[4] = AA2.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)
     
     if num_rows >=15 and num_rows <=18:
          pdf.add_page()   
     Table_Data1 = [
          
     ]
     
     pdf.set_font_size(8)
     if AA2.edit_note:
          a=["Note: "+AA2.edit_note] 
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
     if AA2.legend_1:
          a = [AA2.legend_1]
          Table_data_legend.append(a)
          
     if AA2.legend_2:
          a = [AA2.legend_2]
          Table_data_legend.append(a)
          
     if AA2.legend_3:
          a = [AA2.legend_3]
          Table_data_legend.append(a)
          
     if AA2.legend_4:
          a = [AA2.legend_4]
          Table_data_legend.append(a)
          
     if AA2.legend_5:
          a = [AA2.legend_5]
          Table_data_legend.append(a)
          
     if AA2.legend_6:
          a = [AA2.legend_6]
          Table_data_legend.append(a)
          
     if AA2.legend_7:
          a = [AA2.legend_7]
          Table_data_legend.append(a)
          
     if AA2.legend_8:
          a = [AA2.legend_8]
          Table_data_legend.append(a)
          
     if AA2.legend_9:
          a = [AA2.legend_9]
          Table_data_legend.append(a)
          
     if AA2.legend_10:
          a = [AA2.legend_10]
          Table_data_legend.append(a)
          
     if AA2.legend_11:
          a = [AA2.legend_11]
          Table_data_legend.append(a)
          

     if AA2.custom_legend:
          a = [AA2.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')  
                    
                    
                      


     # y = 193
     # if num_rows == 19:
     #      pdf.add_page()
     # # data after Table
     # print("Y",pdf.y + num_rows )
     # # data after Table
     # print("ROWS",num_rows)



     # if AA2.edit_note and num_rows == 10:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,y,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(y-2.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=AA2.edit_note)

     # elif AA2.edit_note and num_rows <= 12:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,y+12,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(y+9.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=AA2.edit_note)

     # elif AA2.edit_note and num_rows >= 25:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,y-42,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(148.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=AA2.edit_note)

     # line_height = 4
     # if num_rows == 10:
     #      y=204
     # elif num_rows >= 25:
     #      y=159
     # elif num_rows <= 12:
     #      y=214
     # if AA2.legend_1:
     #      pdf.text(10,y,txt=AA2.legend_1)
     #      y = y+line_height
     # if AA2.legend_2:
     #      pdf.text(10,y,txt=AA2.legend_2)
     #      y = y+line_height
     # if AA2.legend_3:
     #      pdf.text(10,y,txt=AA2.legend_3)
     #      y = y+line_height
     # if AA2.legend_4:
     #      pdf.text(10,y,txt=AA2.legend_4)
     #      y = y+line_height
     # if AA2.legend_5:
     #      pdf.text(10,y,txt=AA2.legend_5)
     #      y = y+line_height
     # if AA2.legend_6:
     #      pdf.text(10,y,txt=AA2.legend_6)
     #      y = y+line_height
     # if AA2.legend_7:
     #      pdf.text(10,y,txt=AA2.legend_7)
     #      y = y+line_height
     # if AA2.legend_8:
     #      pdf.text(10,y,txt=AA2.legend_8)
     #      y = y+line_height
     # if AA2.legend_9:
     #      pdf.text(10,y,txt=AA2.legend_9)
     #      y = y+line_height
     # if AA2.legend_10:
     #      pdf.text(10,y,txt=AA2.legend_10)
     #      y = y+line_height
     # if AA2.legend_11:
     #      pdf.text(10,y,txt=AA2.legend_11)
     #      y = y+line_height

     # if AA2.custom_legend:
     #      pdf.text(10,y,txt=AA2.custom_legend)
     #      y = y+line_height


     # pdf.image(AA2.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(AA2.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,230,22,22)
     # pdf.image(AA2.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if AA2.analyst_signature:
         pdf.image(AA2.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(AA2.analyst_signature.role if AA2.analyst_signature else '')})"),252)
     pdf.text(26,254.5,f"Analyzed By ({(AA2.analyst_signature.role if AA2.analyst_signature else '')})")
     if AA2.assistant_manager_signature:
         pdf.image(AA2.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(AA2.assistant_manager_signature.role if AA2.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,254.5,f"Reviewed By ({(AA2.assistant_manager_signature.role if AA2.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,230,22,22)
     if AA2.lab_manager_signature:
         pdf.image(AA2.lab_manager_signature.signature,178,230,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(AA2.lab_manager_signature.role if AA2.lab_manager_signature else '')})"),252)
     pdf.text(160,254.5,f"Approved By ({(AA2.lab_manager_signature.role if AA2.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,256,-10+pdf.w,256)
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
     # if AA2.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if AA2.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17)  
     # if AA2.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)        
     # if AA2.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     if AA2.location == "NEQS" and AA2.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif AA2.location == "NEQS" and AA2.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif AA2.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif AA2.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
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
     pdf.text(128,280,txt=AA2.doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=AA2.doc2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=AA2.doc3)
     
     if AA2.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(AA2, f'pdf_image_{i}')
               desc = getattr(AA2, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=AA2.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/aa2_pdf/'
     # pdf.output(file_path + AA2.lab_report_no +'.pdf')

     # pdf = open(file_path + AA2.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={AA2.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response


def ambientAir2Clone(request,pk):
     existing_form = AmbientAir2.objects.get(id=pk)
     
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json', log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(existing_form, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':existing_form,'customers':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"ambientAir2Clone.html",context)

def ambientAir2cloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = AmbientAir2.objects.get(id=pk)
     except AmbientAir2.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          # existing_Form.hours_checkBox = request.POST['hours_checkBox']
          existing_Form.lab_report_no = request.POST['lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['invoice_no']
          existing_Form.reporting_date = request.POST['report_date']
          existing_Form.report_to = request.POST['report_to']
          existing_Form.address = request.POST['address']
          existing_Form.attention = request.POST['attention']
          existing_Form.email = request.POST['email']
          existing_Form.sample_id = request.POST['testId']
          existing_Form.test_perf_date = request.POST['test_perf_date']
          existing_Form.test_type = request.POST['test_type']
          existing_Form.test_desc = request.POST['test_desc']
          existing_Form.test_test_perf_by = request.POST['test_test_perf_by']
          existing_Form.sr1_1 = request.POST['sr1_1']
          existing_Form.sr1_2 = request.POST['sr1_2']
          existing_Form.sr1_3 = request.POST['sr1_3']
          existing_Form.sr1_4 = request.POST['sr1_4']
          existing_Form.sr1_5 = request.POST['sr1_5']
          existing_Form.sr1_6 = request.POST['sr1_6']
          existing_Form.sr1_7 = request.POST['sr1_7']
          existing_Form.sr1_8 = request.POST['sr1_8']
          existing_Form.sr1_9 = request.POST['sr1_9']
          existing_Form.sr1_10 = request.POST['sr1_10']
          existing_Form.sr2_0 = request.POST['sr2_0']
          existing_Form.sr2_1 = request.POST['sr2_1']
          existing_Form.sr2_2 = request.POST['sr2_2']
          existing_Form.sr2_3 = request.POST['sr2_3']
          existing_Form.sr2_4 = request.POST['sr2_4']
          existing_Form.sr2_5 = request.POST['sr2_5']
          existing_Form.sr2_6 = request.POST['sr2_6']
          existing_Form.sr2_7 = request.POST['sr2_7']
          existing_Form.sr2_8 = request.POST['sr2_8']
          existing_Form.sr2_9 = request.POST['sr2_9']
          existing_Form.sr3_0 = request.POST['sr3_0']
          existing_Form.sr3_1 = request.POST['sr3_1']
          existing_Form.sr3_2 = request.POST['sr3_2']
          existing_Form.sr3_3 = request.POST['sr3_3']
          existing_Form.sr3_4 = request.POST['sr3_4']
          existing_Form.sr3_5 = request.POST['sr3_5']
          existing_Form.sr3_6 = request.POST['sr3_6']
          existing_Form.sr3_7 = request.POST['sr3_7']
          existing_Form.sr3_8 = request.POST['sr3_8']
          existing_Form.sr3_9 = request.POST['sr3_9']
          existing_Form.sr4_0 = request.POST['sr4_0']
          existing_Form.sr4_1 = request.POST['sr4_1']
          existing_Form.sr4_2 = request.POST['sr4_2']
          existing_Form.sr4_3 = request.POST['sr4_3']
          existing_Form.sr4_4 = request.POST['sr4_4']
          existing_Form.sr4_5 = request.POST['sr4_5']
          existing_Form.sr4_6 = request.POST['sr4_6']
          existing_Form.sr4_7 = request.POST['sr4_7']
          existing_Form.sr4_8 = request.POST['sr4_8']
          existing_Form.sr4_9 = request.POST['sr4_9']
          existing_Form.sr5_0 = request.POST['sr5_0']
          existing_Form.sr5_1 = request.POST['sr5_1']
          existing_Form.sr5_2 = request.POST['sr5_2']
          existing_Form.sr5_3 = request.POST['sr5_3']
          existing_Form.sr5_4 = request.POST['sr5_4']
          existing_Form.sr5_5 = request.POST['sr5_5']
          existing_Form.sr5_6 = request.POST['sr5_6']
          existing_Form.sr5_7 = request.POST['sr5_7']
          existing_Form.sr5_8 = request.POST['sr5_8']
          existing_Form.sr5_9 = request.POST['sr5_9']
          existing_Form.sr6_0 = request.POST['sr6_0']
          existing_Form.sr6_1 = request.POST['sr6_1']
          existing_Form.sr6_2 = request.POST['sr6_2']
          existing_Form.sr6_3 = request.POST['sr6_3']
          existing_Form.sr6_4 = request.POST['sr6_4']
          existing_Form.sr6_5 = request.POST['sr6_5']
          existing_Form.sr6_6 = request.POST['sr6_6']
          existing_Form.sr6_7 = request.POST['sr6_7']
          existing_Form.sr6_8 = request.POST['sr6_8']
          existing_Form.sr6_9 = request.POST['sr6_9']
          existing_Form.sr7_0 = request.POST['sr7_0']
          existing_Form.sr7_1 = request.POST['sr7_1']
          existing_Form.sr7_2 = request.POST['sr7_2']
          existing_Form.sr7_3 = request.POST['sr7_3']
          existing_Form.sr7_4 = request.POST['sr7_4']
          existing_Form.sr7_5 = request.POST['sr7_5']
          existing_Form.sr7_6 = request.POST['sr7_6']
          existing_Form.sr7_7 = request.POST['sr7_7']
          existing_Form.sr7_8 = request.POST['sr7_8']
          existing_Form.sr7_9 = request.POST['sr7_9']
          existing_Form.sr8_0 = request.POST['sr8_0']
          existing_Form.sr8_1 = request.POST['sr8_1']
          existing_Form.sr8_2 = request.POST['sr8_2']
          existing_Form.sr8_3 = request.POST['sr8_3']
          existing_Form.sr8_4 = request.POST['sr8_4']
          existing_Form.sr8_5 = request.POST['sr8_5']
          existing_Form.sr8_6 = request.POST['sr8_6']
          existing_Form.sr8_7 = request.POST['sr8_7']
          existing_Form.sr8_8 = request.POST['sr8_8']
          existing_Form.sr8_9 = request.POST['sr8_9']
          existing_Form.sr9_0 = request.POST['sr9_0']
          existing_Form.sr9_1 = request.POST['sr9_1']
          existing_Form.sr9_2 = request.POST['sr9_2']
          existing_Form.sr9_3 = request.POST['sr9_3']
          existing_Form.sr9_4 = request.POST['sr9_4']
          existing_Form.sr9_5 = request.POST['sr9_5']
          existing_Form.sr9_6 = request.POST['sr9_6']
          existing_Form.sr9_7 = request.POST['sr9_7']
          existing_Form.sr9_8 = request.POST['sr9_8']
          existing_Form.sr9_9 = request.POST['sr9_9']
          existing_Form.sr10_0 = request.POST['sr10_0']
          existing_Form.sr10_1 = request.POST['sr10_1']
          existing_Form.sr10_2 = request.POST['sr10_2']
          existing_Form.sr10_3 = request.POST['sr10_3']
          existing_Form.sr10_4 = request.POST['sr10_4']
          existing_Form.sr10_5 = request.POST['sr10_5']
          existing_Form.sr10_6 = request.POST['sr10_6']
          existing_Form.sr10_7 = request.POST['sr10_7']
          existing_Form.sr10_8 = request.POST['sr10_8']
          existing_Form.sr10_9 = request.POST['sr10_9']
          existing_Form.sr11_0 = request.POST['sr11_0']
          existing_Form.sr11_1 = request.POST['sr11_1']
          existing_Form.sr11_2 = request.POST['sr11_2']
          existing_Form.sr11_3 = request.POST['sr11_3']
          existing_Form.sr11_4 = request.POST['sr11_4']
          existing_Form.sr11_5 = request.POST['sr11_5']
          existing_Form.sr11_6 = request.POST['sr11_6']
          existing_Form.sr11_7 = request.POST['sr11_7']
          existing_Form.sr11_8 = request.POST['sr11_8']
          existing_Form.sr11_9 = request.POST['sr11_9']
          existing_Form.sr12_0 = request.POST['sr12_0']
          existing_Form.sr12_1 = request.POST['sr12_1']
          existing_Form.sr12_2 = request.POST['sr12_2']
          existing_Form.sr12_3 = request.POST['sr12_3']
          existing_Form.sr12_4 = request.POST['sr12_4']
          existing_Form.sr12_5 = request.POST['sr12_5']
          existing_Form.sr12_6 = request.POST['sr12_6']
          existing_Form.sr12_7 = request.POST['sr12_7']
          existing_Form.sr12_8 = request.POST['sr12_8']
          existing_Form.sr12_9 = request.POST['sr12_9']
          existing_Form.sr13_0 = request.POST['sr13_0']
          existing_Form.sr13_1 = request.POST['sr13_1']
          existing_Form.sr13_2 = request.POST['sr13_2']
          existing_Form.sr13_3 = request.POST['sr13_3']
          existing_Form.sr13_4 = request.POST['sr13_4']
          existing_Form.sr13_5 = request.POST['sr13_5']
          existing_Form.sr13_6 = request.POST['sr13_6']
          existing_Form.sr13_7 = request.POST['sr13_7']
          existing_Form.sr13_8 = request.POST['sr13_8']
          existing_Form.sr13_9 = request.POST['sr13_9']
          existing_Form.sr14_0 = request.POST['sr14_0']
          existing_Form.sr14_1 = request.POST['sr14_1']
          existing_Form.sr14_2 = request.POST['sr14_2']
          existing_Form.sr14_3 = request.POST['sr14_3']
          existing_Form.sr14_4 = request.POST['sr14_4']
          existing_Form.sr14_5 = request.POST['sr14_5']
          existing_Form.sr14_6 = request.POST['sr14_6']
          existing_Form.sr14_7 = request.POST['sr14_7']
          existing_Form.sr14_8 = request.POST['sr14_8']
          existing_Form.sr14_9 = request.POST['sr14_9']
          existing_Form.sr15_0 = request.POST['sr15_0']
          existing_Form.sr15_1 = request.POST['sr15_1']
          existing_Form.sr15_2 = request.POST['sr15_2']
          existing_Form.sr15_3 = request.POST['sr15_3']
          existing_Form.sr15_4 = request.POST['sr15_4']
          existing_Form.sr15_5 = request.POST['sr15_5']
          existing_Form.sr15_6 = request.POST['sr15_6']
          existing_Form.sr15_7 = request.POST['sr15_7']
          existing_Form.sr15_8 = request.POST['sr15_8']
          existing_Form.sr15_9 = request.POST['sr15_9']
          existing_Form.sr16_0 = request.POST['sr16_0']
          existing_Form.sr16_1 = request.POST['sr16_1']
          existing_Form.sr16_2 = request.POST['sr16_2']
          existing_Form.sr16_3 = request.POST['sr16_3']
          existing_Form.sr16_4 = request.POST['sr16_4']
          existing_Form.sr16_5 = request.POST['sr16_5']
          existing_Form.sr16_6 = request.POST['sr16_6']
          existing_Form.sr16_7 = request.POST['sr16_7']
          existing_Form.sr16_8 = request.POST['sr16_8']
          existing_Form.sr16_9 = request.POST['sr16_9']
          existing_Form.sr17_0 = request.POST['sr17_0']
          existing_Form.sr17_1 = request.POST['sr17_1']
          existing_Form.sr17_2 = request.POST['sr17_2']
          existing_Form.sr17_3 = request.POST['sr17_3']
          existing_Form.sr17_4 = request.POST['sr17_4']
          existing_Form.sr17_5 = request.POST['sr17_5']
          existing_Form.sr17_6 = request.POST['sr17_6']
          existing_Form.sr17_7 = request.POST['sr17_7']
          existing_Form.sr17_8 = request.POST['sr17_8']
          existing_Form.sr17_9 = request.POST['sr17_9']
          existing_Form.sr18_0 = request.POST['sr18_0']
          existing_Form.sr18_1 = request.POST['sr18_1']
          existing_Form.sr18_2 = request.POST['sr18_2']
          existing_Form.sr18_3 = request.POST['sr18_3']
          existing_Form.sr18_4 = request.POST['sr18_4']
          existing_Form.sr18_5 = request.POST['sr18_5']
          existing_Form.sr18_6 = request.POST['sr18_6']
          existing_Form.sr18_7 = request.POST['sr18_7']
          existing_Form.sr18_8 = request.POST['sr18_8']
          existing_Form.sr18_9 = request.POST['sr18_9']
          existing_Form.sr19_0 = request.POST['sr19_0']
          existing_Form.sr19_1 = request.POST['sr19_1']
          existing_Form.sr19_2 = request.POST['sr19_2']
          existing_Form.sr19_3 = request.POST['sr19_3']
          existing_Form.sr19_4 = request.POST['sr19_4']
          existing_Form.sr19_5 = request.POST['sr19_5']
          existing_Form.sr19_6 = request.POST['sr19_6']
          existing_Form.sr19_7 = request.POST['sr19_7']
          existing_Form.sr19_8 = request.POST['sr19_8']
          existing_Form.sr19_9 = request.POST['sr19_9']
          existing_Form.sr20_0 = request.POST['sr20_0']
          existing_Form.sr20_1 = request.POST['sr20_1']
          existing_Form.sr20_2 = request.POST['sr20_2']
          existing_Form.sr20_3 = request.POST['sr20_3']
          existing_Form.sr20_4 = request.POST['sr20_4']
          existing_Form.sr20_5 = request.POST['sr20_5']
          existing_Form.sr20_6 = request.POST['sr20_6']
          existing_Form.sr20_7 = request.POST['sr20_7']
          existing_Form.sr20_8 = request.POST['sr20_8']
          existing_Form.sr20_9 = request.POST['sr20_9']
          existing_Form.sr21_0 = request.POST['sr21_0']
          existing_Form.sr21_1 = request.POST['sr21_1']
          existing_Form.sr21_2 = request.POST['sr21_2']
          existing_Form.sr21_3 = request.POST['sr21_3']
          existing_Form.sr21_4 = request.POST['sr21_4']
          existing_Form.sr21_5 = request.POST['sr21_5']
          existing_Form.sr21_6 = request.POST['sr21_6']
          existing_Form.sr21_7 = request.POST['sr21_7']
          existing_Form.sr21_8 = request.POST['sr21_8']
          existing_Form.sr21_9 = request.POST['sr21_9']
          existing_Form.sr22_0 = request.POST['sr22_0']
          existing_Form.sr22_1 = request.POST['sr22_1']
          existing_Form.sr21_2 = request.POST['sr21_2']
          existing_Form.sr21_3 = request.POST['sr21_3']
          existing_Form.sr21_4 = request.POST['sr21_4']
          existing_Form.sr21_5 = request.POST['sr21_5']
          existing_Form.sr21_6 = request.POST['sr21_6']
          existing_Form.sr21_7 = request.POST['sr21_7']
          existing_Form.sr21_8 = request.POST['sr21_8']
          existing_Form.sr21_9 = request.POST['sr21_9']
          existing_Form.sr22_0 = request.POST['sr22_0']
          existing_Form.sr22_1 = request.POST['sr22_1']
          existing_Form.sr22_2 = request.POST['sr22_2']
          existing_Form.sr22_3 = request.POST['sr22_3']
          existing_Form.sr22_4 = request.POST['sr22_4']
          existing_Form.sr22_5 = request.POST['sr22_5']
          existing_Form.sr22_6 = request.POST['sr22_6']
          existing_Form.sr22_7 = request.POST['sr22_7']
          existing_Form.sr22_8 = request.POST['sr22_8']
          existing_Form.sr22_9 = request.POST['sr22_9']
          existing_Form.sr23_0 = request.POST['sr23_0']
          existing_Form.sr23_1 = request.POST['sr23_1']
          existing_Form.sr23_2 = request.POST['sr23_2']
          existing_Form.sr23_3 = request.POST['sr23_3']
          existing_Form.sr23_4 = request.POST['sr23_4']
          existing_Form.sr23_5 = request.POST['sr23_5']
          existing_Form.sr23_6 = request.POST['sr23_6']
          existing_Form.sr23_7 = request.POST['sr23_7']
          existing_Form.sr23_8 = request.POST['sr23_8']
          existing_Form.sr23_9 = request.POST['sr23_9']
          existing_Form.sr24_0 = request.POST['sr24_0']
          existing_Form.sr24_1 = request.POST['sr24_1']
          existing_Form.sr24_2 = request.POST['sr24_2']
          existing_Form.sr24_3 = request.POST['sr24_3']
          existing_Form.sr24_4 = request.POST['sr24_4']
          existing_Form.sr24_5 = request.POST['sr24_5']
          existing_Form.sr24_6 = request.POST['sr24_6']
          existing_Form.sr24_7 = request.POST['sr24_7']
          existing_Form.sr24_8 = request.POST['sr24_8']
          existing_Form.sr24_9 = request.POST['sr24_9']
          existing_Form.sr25_0 = request.POST['sr25_0']
          existing_Form.sr25_1 = request.POST['sr25_1']
          existing_Form.sr25_2 = request.POST['sr25_2']
          existing_Form.sr25_3 = request.POST['sr25_3']
          existing_Form.sr25_4 = request.POST['sr25_4']
          existing_Form.sr25_5 = request.POST['sr25_5']
          existing_Form.sr25_6 = request.POST['sr25_6']
          existing_Form.sr25_7 = request.POST['sr25_7']
          existing_Form.sr25_8 = request.POST['sr25_8']
          existing_Form.seqs_lim_1 = request.POST.get('seqs_lim_1')
          existing_Form.seqs_lim_2 = request.POST.get('seqs_lim_2')
          existing_Form.seqs_lim_3 = request.POST.get('seqs_lim_3')
          existing_Form.seqs_lim_4 = request.POST.get('seqs_lim_4')
          existing_Form.seqs_lim_5 = request.POST.get('seqs_lim_5')
          existing_Form.seqs_lim_6 = request.POST.get('seqs_lim_6')
          existing_Form.seqs_lim_7 = request.POST.get('seqs_lim_7')
          existing_Form.seqs_lim_8 = request.POST.get('seqs_lim_8')
          existing_Form.seqs_lim_9 = request.POST.get('seqs_lim_9')
          existing_Form.peqs_lim_1 = request.POST.get('peqs_lim_1')
          existing_Form.peqs_lim_2 = request.POST.get('peqs_lim_2')
          existing_Form.peqs_lim_3 = request.POST.get('peqs_lim_3')
          existing_Form.peqs_lim_4 = request.POST.get('peqs_lim_4')
          existing_Form.peqs_lim_5 = request.POST.get('peqs_lim_5')
          existing_Form.peqs_lim_6 = request.POST.get('peqs_lim_6')
          existing_Form.peqs_lim_7 = request.POST.get('peqs_lim_7')
          existing_Form.peqs_lim_8 = request.POST.get('peqs_lim_8')
          existing_Form.peqs_lim_9 = request.POST.get('peqs_lim_9')
          existing_Form.neqs_lim_1 = request.POST.get('neqs_lim_1')
          existing_Form.neqs_lim_2 = request.POST.get('neqs_lim_2')
          existing_Form.neqs_lim_3 = request.POST.get('neqs_lim_3')
          existing_Form.neqs_lim_4 = request.POST.get('neqs_lim_4')
          existing_Form.neqs_lim_5 = request.POST.get('neqs_lim_5')
          existing_Form.neqs_lim_6 = request.POST.get('neqs_lim_6')
          existing_Form.neqs_lim_7 = request.POST.get('neqs_lim_7')
          existing_Form.neqs_lim_8 = request.POST.get('neqs_lim_8')
          existing_Form.neqs_lim_9 = request.POST.get('neqs_lim_9')
          existing_Form.select = request.POST.get('select')
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
          existing_Form.edit_note = request.POST['edit_note']
          existing_Form.custom_legend = request.POST['custom_legend']
          existing_Form.doc1 = request.POST['doc1']
          existing_Form.doc2 = request.POST['doc2']
          existing_Form.doc3 = request.POST['doc3']
          existing_Form.created_by = request.user
          # existing_Form.analyzedby = request.FILES['analyzedby']
          # existing_Form.reviewedby = request.FILES['reviewedby']
          # existing_Form.approvedby = request.FILES['approvedby']
          # existing_Form.approvedby1 = request.FILES['approvedby1']
          existing_Form.city_location = request.POST['city_location']
          
          
          existing_Form.pdf_heading=request.POST.get('pdf_heading')
          existing_Form.col_head_1=request.POST.get('col_head_1')
          existing_Form.col_head_2=request.POST.get('col_head_2')
          existing_Form.col_head_3=request.POST.get('col_head_3')
          existing_Form.col_head_4=request.POST.get('col_head_4')
          existing_Form.col_head_5=request.POST.get('col_head_5')
          existing_Form.col_head_6=request.POST.get('col_head_6')
          existing_Form.col_head_7=request.POST.get('col_head_7')
          existing_Form.col_head_8=request.POST.get('col_head_8')
          existing_Form.col_head_9=request.POST.get('col_head_9')
          
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
          
          existing_Form.id = None
          existing_Form.save()
          user = request.user
          action = f'Ambient Air 2 Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id

          if "submit_and_view" in request.POST:
            url = f"/ambientAir2-view/{str(id)}/"
            return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
               return redirect(to='ambientAir2List')
          else:
               return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "ambientAir2Clone.html")

def ambientAirClone(request,pk):
     existing_form = AmbientAirForm.objects.get(id=pk)
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
     return render(request,"ambientAirClone.html",context)
def ambientAircloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = AmbientAirForm.objects.get(id=pk)
     except AmbientAirForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
            existing_Form.location = request.POST['location']
            industry_id = request.POST.get('industry')
            existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
            existing_Form.lab_report_no = request.POST['ambient_Air_lab_report_no']
            existing_Form.invoice_bill_no = request.POST['ambientAir_invoice_no']
            existing_Form.reporting_date = request.POST['ambientAir_rep_date']
            existing_Form.report_to = request.POST['ambientAir_rep_to']
            existing_Form.address = request.POST['ambientAir_address']
            existing_Form.attention = request.POST['ambientAir_attention']
            existing_Form.email = request.POST['ambientAir_email']
            existing_Form.sample_id = request.POST['ambientAir_testid']
            existing_Form.ambientAir_test_perf_date = request.POST['ambientAir_test_perf_date']
            existing_Form.ambientAir_test_type_location = request.POST['ambientAir_testtype_location']
            existing_Form.ambientAir_test_perf_by = request.POST['ambientAir_test_perf_by']
            existing_Form.ambienAir_test_desc = request.POST['ambientAir_test_desc']
            existing_Form.ambienAir_select = request.POST['select']
            existing_Form.ambientAir_sr1 = request.POST['ambientAir_sr1']
            existing_Form.ambientAir_sr2 = request.POST['ambientAir_sr2']
            existing_Form.ambientAir_sr3 = request.POST['ambientAir_sr3']
            existing_Form.ambientAir_sr4 = request.POST['ambientAir_sr4']
            existing_Form.ambientAir_sr5 = request.POST['ambientAir_sr5']
            existing_Form.ambientAir_sr6 = request.POST['ambientAir_sr6']
            existing_Form.ambientAir_sr7 = request.POST['ambientAir_sr7']
            existing_Form.ambientAir_sr8 = request.POST['ambientAir_sr8']
            existing_Form.ambientAir_sr9 = request.POST['ambientAir_sr9']
            existing_Form.ambientAir_sr10 = request.POST['ambientAir_sr10']
            existing_Form.ambientAir_sr11 = request.POST['ambientAir_sr11']
            existing_Form.ambientAir_sr12 = request.POST['ambientAir_sr12']
            existing_Form.ambientAir_sr13 = request.POST['ambientAir_sr13']
            existing_Form.ambientAir_sr14 = request.POST['ambientAir_sr14']
            existing_Form.ambientAir_legend_1 = request.POST['ambientAir-legend-1']
            existing_Form.ambientAir_legend_2 = request.POST['ambientAir-legend-2']
            existing_Form.ambientAir_legend_3 = request.POST['ambientAir-legend-3']
            existing_Form.ambientAir_legend_4 = request.POST['ambientAir-legend-4']
            existing_Form.ambientAir_legend_5 = request.POST['ambientAir-legend-5']
            existing_Form.ambientAir_legend_6 = request.POST['ambientAir-legend-6']
            existing_Form.ambientAir_edit_note = request.POST['ambientAir_editNote']
            existing_Form.ambientAir_custom_legend = request.POST['ambientAir_customlegend']
            existing_Form.ambientAir_doc_con_1 = request.POST['ambientAir_doc1']
            existing_Form.ambientAir_doc_con_2 = request.POST['ambientAir_doc2']
            existing_Form.ambientAir_doc_con_3 = request.POST['ambientAir_doc3']
            existing_Form.created_by = request.user
          #   existing_Form.ambientAir_analyzed_by = request.FILES["ambientAir_analyzedby" ]
          #   existing_Form.ambientAir_reviewd_by = request.FILES["ambientAir_reviewedby" ]
          #   existing_Form.ambientAir_approved_by = request.FILES["ambientAir_approvedby" ]
          #   existing_Form.ambientAir_approved_by1 = request.FILES["ambientAir_approvedby1" ]
            existing_Form.city_location = request.POST['city_location']
            existing_Form.extra_field = json.loads(request.POST['extra_field'])
            for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameters = request.POST.getlist('parameters[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               existing_Form.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        


            existing_Form.extra_field = json.dumps(existing_Form.extra_field)
            
            
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
            existing_Form.col_head_1=request.POST.get('col_head_1')
            existing_Form.col_head_2=request.POST.get('col_head_2')
            existing_Form.col_head_3=request.POST.get('col_head_3')
            existing_Form.col_head_4=request.POST.get('col_head_4')
            existing_Form.col_head_5=request.POST.get('col_head_5')
            existing_Form.col_head_6=request.POST.get('col_head_6')
            existing_Form.col_head_7=request.POST.get('col_head_7')
            existing_Form.col_head_8=request.POST.get('col_head_8')
            existing_Form.col_head_9=request.POST.get('col_head_9')
          
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
            action = f'Ambient Air Form {existing_Form.lab_report_no} cloned by {user.username}'
            AuditLog.objects.create(user=user, action=action, timestamp=local_date)
            messages.success(request, 'Operation was successful!')
            id = existing_Form.id
            if "update_and_view" in request.POST:
               url = f"/ambientAir-view/{str(id)}/"
               return redirect(to=url)
          
            if "submit" in request.POST:
               # context = {'list': new_dw}
                 return redirect(to='ambientAirList')
            else:
                 return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "ambientAirClone.html")

__all__ = [
    'ambientAirForm',
    'ambientAirQuality2',
    'ambientAirList',
    'ambientAirDelete',
    'ambientAirEdit',
    'ambientAirUpdateRecord',
    'ambientAirview',
    'ambientAirGeneratePDF',
    'ambientAirGeneratePDF1',
    'ambientAir2List',
    'ambientAir2Delete',
    'ambientAir2Edit',
    'ambientAir2Update',
    'ambientAir2View',
    'ambientAir2Pdf',
    'ambientAir2Pdf1',
    'ambientAir2Clone',
    'ambientAir2cloneSave',
    'ambientAirClone',
    'ambientAircloneSave',
]
