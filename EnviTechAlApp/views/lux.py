# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def luxAnalysis(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['lux_lab_rep_no']
          invoice_bill_no = request.POST['lux_invoice_no']
          reporting_date = request.POST['lux_report_date']
          report_to = request.POST['lux_report_to']
          address = request.POST['lux-address']
          attention = request.POST['lux_attention']
          email = request.POST['lux_email']
          sample_id = request.POST['lux_testId']
          lux_test_perf_date = request.POST['lux_test_perf_date']
          lux_test_type = request.POST['lux_test_type']
          lux_test_perfBy = request.POST['lux_test_perf_by']
          lux_test_desc = request.POST['lux_test_desc']
          lux_parameters_1 = request.POST['lux_parameters_1']
          lux_result_1 = request.POST['lux_result_1']
          lux_parameters_2 = request.POST['lux_parameters_2']
          lux_result_2 = request.POST['lux_result_2']
          lux_parameters_3 = request.POST['lux_parameters_3']
          lux_result_3 = request.POST['lux_result_3']
          lux_parameters_4 = request.POST['lux_parameters_4']
          lux_result_4 = request.POST['lux_result_4']
          lux_parameters_5 = request.POST['lux_parameters_5']
          lux_result_5 = request.POST['lux_result_5']
          lux_parameters_6 = request.POST['lux_parameters_6']
          lux_result_6 = request.POST['lux_result_6']
          lux_parameters_7 = request.POST['lux_parameters_7']
          lux_result_7 = request.POST['lux_result_7']
          lux_parameters_8 = request.POST['lux_parameters_8']
          lux_result_8 = request.POST['lux_result_8']
          lux_parameters_9 = request.POST['lux_parameters_9']
          lux_result_9 = request.POST['lux_result_9']
          lux_parameters_10 = request.POST['lux_parameters_10']
          lux_result_10 = request.POST['lux_result_10']
          lux_parameters_11 = request.POST['lux_parameters_11']
          lux_result_11 = request.POST['lux_result_11']
          lux_parameters_12 = request.POST['lux_parameters_12']
          lux_result_12 = request.POST['lux_result_12']
          lux_parameters_13 = request.POST['lux_parameters_13']
          lux_result_13 = request.POST['lux_result_13']
          lux_legend_1 = request.POST['lux-legend-1']
          lux_legend_2 = request.POST['lux-legend-2']
          lux_legend_3 = request.POST['lux-legend-3']
          lux_legend_4 = request.POST['lux-legend-4']
          lux_legend_5 = request.POST['lux-legend-5']
          lux_legend_6 = request.POST['lux-legend-6']
          lux_legend_7 = request.POST['lux-legend-7']
          lux_legend_8 = request.POST['lux-legend-8']
          lux_legend_9 = request.POST['lux-legend-9']
          lux_legend_10 = request.POST['lux-legend-10']
          lux_legend_11 = request.POST['lux-legend-11']
          lux_edit_note = request.POST['lux_edit_note']
          lux_custom_legend = request.POST['lux_custom_legend']
          lux_doc_con1 = request.POST['lux_doc_con1']
          lux_doc_con2 = request.POST['lux_doc_con2']
          lux_doc_con3 = request.POST['lux_doc_con3']
          # lux_analyzedby = request.FILES['lux-analyzedby']
          # lux_reviewedby = request.FILES['lux-reviewedby']
          # lux_approvedby = request.FILES['lux-approvedby']
          # lux_approvedby1 = request.FILES['lux-approvedby1']
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
          
          luxForm = LuxAnalysisForm(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,
                                    report_to=report_to,address=address,attention=attention,email=email,
                                    sample_id=sample_id,lux_test_perf_date=lux_test_perf_date,lux_test_type=lux_test_type,lux_test_perfBy=lux_test_perfBy,
                                    lux_test_desc=lux_test_desc,lux_parameters_1=lux_parameters_1,lux_result_1=lux_result_1,lux_parameters_2=lux_parameters_2,
                                    lux_result_2=lux_result_2,lux_parameters_3=lux_parameters_3,lux_result_3=lux_result_3,lux_parameters_4=lux_parameters_4,
                                    lux_result_4=lux_result_4,lux_parameters_5=lux_parameters_5,lux_result_5=lux_result_5,lux_parameters_6=lux_parameters_6,
                                    lux_result_6=lux_result_6,lux_parameters_7=lux_parameters_7,lux_result_7=lux_result_7,lux_parameters_8=lux_parameters_8,
                                    lux_result_8=lux_result_8,lux_parameters_9=lux_parameters_9,lux_result_9=lux_result_9,lux_parameters_10=lux_parameters_10,
                                    lux_result_10=lux_result_10,lux_parameters_11=lux_parameters_11,lux_result_11=lux_result_11,lux_parameters_12=lux_parameters_12,
                                    lux_result_12=lux_result_12,lux_parameters_13=lux_parameters_13,lux_result_13=lux_result_13,lux_legend_1=lux_legend_1,
                                    lux_legend_2=lux_legend_2,lux_legend_3=lux_legend_3,lux_legend_4=lux_legend_4,lux_legend_5=lux_legend_5,
                                    lux_legend_6=lux_legend_6,lux_legend_7=lux_legend_7,lux_legend_8=lux_legend_8,lux_legend_9=lux_legend_9,lux_legend_10=lux_legend_10,
                                    lux_legend_11=lux_legend_11,lux_edit_note=lux_edit_note,location=location,
                                    lux_custom_legend=lux_custom_legend,lux_doc_con1=lux_doc_con1,lux_doc_con2=lux_doc_con2,
                                    lux_doc_con3=lux_doc_con3,city_location=city_location,extra_field=extra_field,customer_id=customer_id,
                                    analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                    lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          luxForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Lux Analysis Form {luxForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (LuxAnalysisForm.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f'/luxAnalysisReport/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to='luxAnalysis')
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"luxAnalysis.html",context)


@login_required(login_url="/login")
def luxAnalysisList(request):
     luxAnalysis, _srch = _list_filter(request, LuxAnalysisForm)
     context = {'searched':_srch, 'data':luxAnalysis}
     return render(request,"luxAnalysisList.html",context)

@login_required(login_url="/login")
def luxAnalysisDelete(request,pk):
     luxAnalysis = LuxAnalysisForm.objects.get(id=pk)
     luxAnalysis.delete()
     user = request.user
     action = f'Lux Analysis Form {luxAnalysis.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect('luxAnalysisList')

@login_required(login_url="/login")
def luxAnalysisEdit(request,pk):
     luxAnalysis = LuxAnalysisForm.objects.get(id=pk)
     luxAnalysis.extra_field = luxAnalysis.extra_field.replace("'", "\"")
     luxAnalysis.extra_field = json.loads(luxAnalysis.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(luxAnalysis, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':luxAnalysis,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"luxAnalysisEdit.html",context)

@login_required(login_url="/login")
def luxAnalysisUpdate(request,pk):
     luxAnalysis = LuxAnalysisForm.objects.get(id=pk)
     if request.method == 'POST':
          luxAnalysis.location = request.POST['location']
          industry_id = request.POST.get('industry')
          luxAnalysis.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          luxAnalysis.lab_report_no = request.POST['lux_lab_rep_no']
          luxAnalysis.invoice_bill_no = request.POST['lux_invoice_no']
          luxAnalysis.reporting_date = request.POST['lux_report_date']
          luxAnalysis.report_to = request.POST['lux_report_to']
          luxAnalysis.address = request.POST['lux-address']
          luxAnalysis.attention = request.POST['lux_attention']
          luxAnalysis.email = request.POST['lux_email']
          luxAnalysis.sample_id = request.POST['lux_testId']
          luxAnalysis.lux_test_perf_date = request.POST['lux_test_perf_date']
          luxAnalysis.lux_test_type = request.POST['lux_test_type']
          luxAnalysis.lux_test_perfBy = request.POST['lux_test_perf_by']
          luxAnalysis.lux_test_desc = request.POST['lux_test_desc']
          luxAnalysis.lux_parameters_1 = request.POST['lux_parameters_1']
          luxAnalysis.lux_result_1 = request.POST['lux_result_1']
          luxAnalysis.lux_parameters_2 = request.POST['lux_parameters_2']
          luxAnalysis.lux_result_2 = request.POST['lux_result_2']
          luxAnalysis.lux_parameters_3 = request.POST['lux_parameters_3']
          luxAnalysis.lux_result_3 = request.POST['lux_result_3']
          luxAnalysis.lux_parameters_4 = request.POST['lux_parameters_4']
          luxAnalysis.lux_result_4 = request.POST['lux_result_4']
          luxAnalysis.lux_parameters_5 = request.POST['lux_parameters_5']
          luxAnalysis.lux_result_5 = request.POST['lux_result_5']
          luxAnalysis.lux_parameters_6 = request.POST['lux_parameters_6']
          luxAnalysis.lux_result_6 = request.POST['lux_result_6']
          luxAnalysis.lux_parameters_7 = request.POST['lux_parameters_7']
          luxAnalysis.lux_result_7 = request.POST['lux_result_7']
          luxAnalysis.lux_parameters_8 = request.POST['lux_parameters_8']
          luxAnalysis.lux_result_8 = request.POST['lux_result_8']
          luxAnalysis.lux_parameters_9 = request.POST['lux_parameters_9']
          luxAnalysis.lux_result_9 = request.POST['lux_result_9']
          luxAnalysis.lux_parameters_10 = request.POST['lux_parameters_10']
          luxAnalysis.lux_result_10 = request.POST['lux_result_10']
          luxAnalysis.lux_parameters_11 = request.POST['lux_parameters_11']
          luxAnalysis.lux_result_11 = request.POST['lux_result_11']
          luxAnalysis.lux_parameters_12 = request.POST['lux_parameters_12']
          luxAnalysis.lux_result_12 = request.POST['lux_result_12']
          luxAnalysis.lux_parameters_13 = request.POST['lux_parameters_13']
          luxAnalysis.lux_result_13 = request.POST['lux_result_13']
          luxAnalysis.lux_legend_1 = request.POST['lux-legend-1']
          luxAnalysis.lux_legend_2 = request.POST['lux-legend-2']
          luxAnalysis.lux_legend_3 = request.POST['lux-legend-3']
          luxAnalysis.lux_legend_4 = request.POST['lux-legend-4']
          luxAnalysis.lux_legend_5 = request.POST['lux-legend-5']
          luxAnalysis.lux_legend_6 = request.POST['lux-legend-6']
          luxAnalysis.lux_legend_7 = request.POST['lux-legend-7']
          luxAnalysis.lux_legend_8 = request.POST['lux-legend-8']
          luxAnalysis.lux_legend_9 = request.POST['lux-legend-9']
          luxAnalysis.lux_legend_10 = request.POST['lux-legend-10']
          luxAnalysis.lux_legend_11 = request.POST['lux-legend-11']
          luxAnalysis.lux_edit_note = request.POST['lux_edit_note']
          luxAnalysis.lux_custom_legend = request.POST['lux_custom_legend']
          luxAnalysis.lux_doc_con1 = request.POST['lux_doc_con1']
          luxAnalysis.lux_doc_con2 = request.POST['lux_doc_con2']
          luxAnalysis.lux_doc_con3 = request.POST['lux_doc_con3']
          luxAnalysis.created_by = request.user
          # luxAnalysis.lux_analyzedby = request.FILES['lux-analyzedby']
          # luxAnalysis.lux_reviewedby = request.FILES['lux-reviewedby']
          # luxAnalysis.lux_approvedby = request.FILES['lux-approvedby']
          # luxAnalysis.lux_approvedby1 = request.FILES['lux-approvedby1']
          luxAnalysis.city_location = request.POST['city_location']
          luxAnalysis.extra_field = json.loads(request.POST.get('extra_field'))
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
          

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          luxAnalysis.analyst_signature = analyst_sign
          luxAnalysis.assistant_manager_signature = review_sign
          luxAnalysis.lab_manager_signature = approved_sign
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameter = request.POST.getlist('parameter[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]

               luxAnalysis.extra_field.append({
                         "sr": sr,
                         "parameter": parameter,
                         "unit": unit,
                         "result": result,
                    })        
               
               
          luxAnalysis.pdf_heading=request.POST.get('pdf_heading')
          
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
                    setattr(luxAnalysis, image_key, '')
                    setattr(luxAnalysis, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(luxAnalysis, image_key, base64_encoded)
                         setattr(luxAnalysis, desc_key, description or '')
                         print(f"Updated image {i}")
                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
               else:
                    if description is not None:
                         setattr(luxAnalysis, desc_key, description)
                         print(f"Updated description {i}")

          luxAnalysis.save()
          user = request.user
          action = f'Lux Analysis Form {luxAnalysis.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')


          id = luxAnalysis.id
          if "submit_and_view" in request.POST:
               url = f'/luxAnalysisReport/{str(id)}/'
               return redirect(to=url)
          if "submit" in request.POST:
               return redirect('luxAnalysisList')
     return render(request,"luxAnalysisList.html")



def luxAnalysisView(request,pk):
     luxAnalysis = LuxAnalysisForm.objects.get(id=pk)
     luxAnalysis.extra_field = luxAnalysis.extra_field.replace("'", "\"")
     luxAnalysis.extra_field = json.loads(luxAnalysis.extra_field)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{luxAnalysis.lab_report_no}.png"
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
     context = {'data':luxAnalysis,'qr':qr_relative_path,'logo':logo}

     return render(request,'luxAnalysisReport.html',context)



def luxAnalysisReportPdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_luxAnalysisReportPdf as PDFWithPageNumbers




     lux = LuxAnalysisForm.objects.get(id=pk)
     lux.extra_field = lux.extra_field.replace("'", "\"")
     lux.extra_field = json.loads(lux.extra_field)

     TABLE_DATA = [
           ["Sr.#","Locations","Unit","Result"],
     ]
     sr_no = 1
     if lux.lux_result_1:
          a = [str(sr_no),lux.lux_parameters_1,"Lux(lx)",lux.lux_result_1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_2:
          a = [str(sr_no),lux.lux_parameters_2,"Lux(lx)",lux.lux_result_2]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_3:
          a = [str(sr_no),lux.lux_parameters_3,"Lux(lx)",lux.lux_result_3]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_4:
          a = [str(sr_no),lux.lux_parameters_4,"Lux(lx)",lux.lux_result_4]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_5:
          a = [str(sr_no),lux.lux_parameters_5,"Lux(lx)",lux.lux_result_5]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_6:
          a = [str(sr_no),lux.lux_parameters_6,"Lux(lx)",lux.lux_result_6]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_7:
          a = [str(sr_no),lux.lux_parameters_7,"Lux(lx)",lux.lux_result_7]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_8:
          a = [str(sr_no),lux.lux_parameters_8,"Lux(lx)",lux.lux_result_8]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_9:
          a = [str(sr_no),lux.lux_parameters_9,"Lux(lx)",lux.lux_result_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_10:
          a = [str(sr_no),lux.lux_parameters_10,"Lux(lx)",lux.lux_result_10]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_11:
          a = [str(sr_no),lux.lux_parameters_11,"Lux(lx)",lux.lux_result_11]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_12:
          a = [str(sr_no),lux.lux_parameters_12,"Lux(lx)",lux.lux_result_12]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_13:
          a = [str(sr_no),lux.lux_parameters_13,"Lux(lx)",lux.lux_result_13]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in lux.extra_field:
          parameter = extra_field.get("parameter")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
               # Check if the "parameter" field is not empty before adding the row
          if parameter:
               a = [str(sr_no), parameter, unit, result,]
               sr_no += 1
               TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=lux.lab_report_no,invoice_bill_no=lux.invoice_bill_no,reporting_date=lux.reporting_date,report_to=lux.report_to,
                              address=lux.address,attention=lux.attention,email=lux.email,sample_id=lux.sample_id,lux_test_perf_date=lux.lux_test_perf_date,
                              lux_test_desc=lux.lux_test_desc,lux_test_type=lux.lux_test_type,lux_test_perfBy=lux.lux_test_perfBy,

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
     with pdf.table(col_widths=(10, 50, 30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = lux.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if lux.lux_edit_note:
          a=["Note: "+lux.lux_edit_note] 
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
     if lux.lux_legend_1:
          a = [lux.lux_legend_1]
          Table_data_legend.append(a)
          
     if lux.lux_legend_2:
          a = [lux.lux_legend_2]
          Table_data_legend.append(a)
          
     if lux.lux_legend_3:
          a = [lux.lux_legend_3]
          Table_data_legend.append(a)
          
     if lux.lux_legend_4:
          a = [lux.lux_legend_4]
          Table_data_legend.append(a)
          
     if lux.lux_legend_5:
          a = [lux.lux_legend_5]
          Table_data_legend.append(a)
          
     if lux.lux_legend_6:
          a = [lux.lux_legend_6]
          Table_data_legend.append(a)
          
     if lux.lux_legend_7:
          a = [lux.lux_legend_7]
          Table_data_legend.append(a)
          
     if lux.lux_legend_8:
          a = [lux.lux_legend_8]
          Table_data_legend.append(a)
          
     if lux.lux_legend_9:
          a = [lux.lux_legend_9]
          Table_data_legend.append(a)
          
     if lux.lux_legend_10:
          a = [lux.lux_legend_10]
          Table_data_legend.append(a)
          
     if lux.lux_legend_11:
          a = [lux.lux_legend_11]
          Table_data_legend.append(a)
          

     if lux.lux_custom_legend:
          a = [lux.lux_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')




     # pdf.image(lux.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(lux.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(lux.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     if lux.analyst_signature:
         pdf.image(lux.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(lux.analyst_signature.role if lux.analyst_signature else '')})"),257)
     pdf.text(26,259.3,f"Analyzed By ({(lux.analyst_signature.role if lux.analyst_signature else '')})")
     if lux.assistant_manager_signature:
         pdf.image(lux.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(lux.assistant_manager_signature.role if lux.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.3,f"Reviewed By ({(lux.assistant_manager_signature.role if lux.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if lux.lab_manager_signature:
         pdf.image(lux.lab_manager_signature.signature,178,239,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(lux.lab_manager_signature.role if lux.lab_manager_signature else '')})"),257)
     pdf.text(160,259.3,f"Approved By ({(lux.lab_manager_signature.role if lux.lab_manager_signature else '')})")



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
     # if lux.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if lux.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if lux.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if lux.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     
     
     
     if lux.location == "NEQS" and lux.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif lux.location == "NEQS" and lux.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif lux.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif lux.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     # if lux.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     pdf.set_font("Calibri","B", 5)
               
     pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,281,txt="(Certificate # 080177424-EMS)")


     pdf.set_font("Calibri","", 7)
     pdf.rect(126,282,25,5)
     pdf.text(128,285,txt=lux.lux_doc_con1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=lux.lux_doc_con2)
     pdf.rect(180,282,25,5)
     pdf.text(183.5,285,txt=lux.lux_doc_con3)

     if lux.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(lux, f'pdf_image_{i}')
               desc = getattr(lux, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         print(f"Failed to decode image {i}:", e)

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=lux.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/luxAnalysis/'
     # pdf.output(file_path + lux.lab_report_no +'.pdf')
     # pdf = open(file_path + lux.lab_report_no +'.pdf', 'rb')


     # # pdf.output(lux.lab_report_no +'.pdf')

     # # pdf = open(lux.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={lux.lab_report_no}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def luxAnalysisReportPdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_luxAnalysisReportPdf1 as PDFWithPageNumbers




     lux = LuxAnalysisForm.objects.get(id=pk)
     lux.extra_field = lux.extra_field.replace("'", "\"")
     lux.extra_field = json.loads(lux.extra_field)

     TABLE_DATA = [
           ["Sr.#","Locations","Unit","Result"],
     ]
     sr_no = 1
     if lux.lux_result_1:
          a = [str(sr_no),lux.lux_parameters_1,"Lux(lx)",lux.lux_result_1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_2:
          a = [str(sr_no),lux.lux_parameters_2,"Lux(lx)",lux.lux_result_2]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_3:
          a = [str(sr_no),lux.lux_parameters_3,"Lux(lx)",lux.lux_result_3]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_4:
          a = [str(sr_no),lux.lux_parameters_4,"Lux(lx)",lux.lux_result_4]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_5:
          a = [str(sr_no),lux.lux_parameters_5,"Lux(lx)",lux.lux_result_5]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_6:
          a = [str(sr_no),lux.lux_parameters_6,"Lux(lx)",lux.lux_result_6]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_7:
          a = [str(sr_no),lux.lux_parameters_7,"Lux(lx)",lux.lux_result_7]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_8:
          a = [str(sr_no),lux.lux_parameters_8,"Lux(lx)",lux.lux_result_8]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_9:
          a = [str(sr_no),lux.lux_parameters_9,"Lux(lx)",lux.lux_result_9]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_10:
          a = [str(sr_no),lux.lux_parameters_10,"Lux(lx)",lux.lux_result_10]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_11:
          a = [str(sr_no),lux.lux_parameters_11,"Lux(lx)",lux.lux_result_11]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_12:
          a = [str(sr_no),lux.lux_parameters_12,"Lux(lx)",lux.lux_result_12]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if lux.lux_result_13:
          a = [str(sr_no),lux.lux_parameters_13,"Lux(lx)",lux.lux_result_13]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in lux.extra_field:
          parameter = extra_field.get("parameter")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
               # Check if the "parameter" field is not empty before adding the row
          if parameter:
               a = [str(sr_no), parameter, unit, result,]
               sr_no += 1
               TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=lux.lab_report_no,invoice_bill_no=lux.invoice_bill_no,reporting_date=lux.reporting_date,report_to=lux.report_to,
                              address=lux.address,attention=lux.attention,email=lux.email,sample_id=lux.sample_id,lux_test_perf_date=lux.lux_test_perf_date,
                              lux_test_desc=lux.lux_test_desc,lux_test_type=lux.lux_test_type,lux_test_perfBy=lux.lux_test_perfBy,

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
     with pdf.table(col_widths=(10, 50, 30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = lux.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if lux.lux_edit_note:
          a=["Note: "+lux.lux_edit_note] 
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
     if lux.lux_legend_1:
          a = [lux.lux_legend_1]
          Table_data_legend.append(a)
          
     if lux.lux_legend_2:
          a = [lux.lux_legend_2]
          Table_data_legend.append(a)
          
     if lux.lux_legend_3:
          a = [lux.lux_legend_3]
          Table_data_legend.append(a)
          
     if lux.lux_legend_4:
          a = [lux.lux_legend_4]
          Table_data_legend.append(a)
          
     if lux.lux_legend_5:
          a = [lux.lux_legend_5]
          Table_data_legend.append(a)
          
     if lux.lux_legend_6:
          a = [lux.lux_legend_6]
          Table_data_legend.append(a)
          
     if lux.lux_legend_7:
          a = [lux.lux_legend_7]
          Table_data_legend.append(a)
          
     if lux.lux_legend_8:
          a = [lux.lux_legend_8]
          Table_data_legend.append(a)
          
     if lux.lux_legend_9:
          a = [lux.lux_legend_9]
          Table_data_legend.append(a)
          
     if lux.lux_legend_10:
          a = [lux.lux_legend_10]
          Table_data_legend.append(a)
          
     if lux.lux_legend_11:
          a = [lux.lux_legend_11]
          Table_data_legend.append(a)
          

     if lux.lux_custom_legend:
          a = [lux.lux_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')




     # pdf.image(lux.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(lux.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,229,22,22)
     # pdf.image(lux.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     
     if lux.analyst_signature:
         pdf.image(lux.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(lux.analyst_signature.role if lux.analyst_signature else '')})"),252)
     pdf.text(26,253.9,f"Analyzed By ({(lux.analyst_signature.role if lux.analyst_signature else '')})")
     if lux.assistant_manager_signature:
         pdf.image(lux.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(lux.assistant_manager_signature.role if lux.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,253.9,f"Reviewed By ({(lux.assistant_manager_signature.role if lux.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if lux.lab_manager_signature:
         pdf.image(lux.lab_manager_signature.signature,178,234,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(lux.lab_manager_signature.role if lux.lab_manager_signature else '')})"),252)
     pdf.text(160,253.9,f"Approved By ({(lux.lab_manager_signature.role if lux.lab_manager_signature else '')})")


     
     pdf.line(10,256,-10+pdf.w,256)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,265,txt="• Report is valid for current batch (sample).")
     pdf.text(10,268.5,txt="• This report is not valid for any publication or judicial purpose.")
     pdf.set_y(269.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(274)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")
     pdf.set_y(278)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,259,19,15)
     if lux.location == "NEQS" and lux.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif lux.location == "NEQS" and lux.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif lux.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif lux.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     # if lux.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if lux.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")


     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=lux.lux_doc_con1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=lux.lux_doc_con2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,txt=lux.lux_doc_con3)

     
     if lux.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(lux, f'pdf_image_{i}')
               desc = getattr(lux, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         print(f"Failed to decode image {i}:", e)

          count = len(images)
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=lux.pdf_heading,align="C")
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


     # file_path = '/home/django/EnviTechAlApp/la_pdf/'
     # pdf.output(file_path + lux.lab_report_no +'.pdf')

     # pdf = open(file_path + lux.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={lux.lab_report_no}.pdf'
     response.write(pdf_output.getvalue())
     return response

def luxFormclone(request,pk):
     existing_form = LuxAnalysisForm.objects.get(id=pk)
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
     return render(request,"luxClone.html",context) 

def luxFormcloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = LuxAnalysisForm.objects.get(id=pk)
     except LuxAnalysisForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['lux_lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['lux_invoice_no']
          existing_Form.reporting_date = request.POST['lux_report_date']
          existing_Form.report_to = request.POST['lux_report_to']
          existing_Form.address = request.POST['lux-address']
          existing_Form.attention = request.POST['lux_attention']
          existing_Form.email = request.POST['lux_email']
          existing_Form.sample_id = request.POST['lux_testId']
          existing_Form.lux_test_perf_date = request.POST['lux_test_perf_date']
          existing_Form.lux_test_type = request.POST['lux_test_type']
          existing_Form.lux_test_perfBy = request.POST['lux_test_perf_by']
          existing_Form.lux_test_desc = request.POST['lux_test_desc']
          existing_Form.lux_parameters_1 = request.POST['lux_parameters_1']
          existing_Form.lux_result_1 = request.POST['lux_result_1']
          existing_Form.lux_parameters_2 = request.POST['lux_parameters_2']
          existing_Form.lux_result_2 = request.POST['lux_result_2']
          existing_Form.lux_parameters_3 = request.POST['lux_parameters_3']
          existing_Form.lux_result_3 = request.POST['lux_result_3']
          existing_Form.lux_parameters_4 = request.POST['lux_parameters_4']
          existing_Form.lux_result_4 = request.POST['lux_result_4']
          existing_Form.lux_parameters_5 = request.POST['lux_parameters_5']
          existing_Form.lux_result_5 = request.POST['lux_result_5']
          existing_Form.lux_parameters_6 = request.POST['lux_parameters_6']
          existing_Form.lux_result_6 = request.POST['lux_result_6']
          existing_Form.lux_parameters_7 = request.POST['lux_parameters_7']
          existing_Form.lux_result_7 = request.POST['lux_result_7']
          existing_Form.lux_parameters_8 = request.POST['lux_parameters_8']
          existing_Form.lux_result_8 = request.POST['lux_result_8']
          existing_Form.lux_parameters_9 = request.POST['lux_parameters_9']
          existing_Form.lux_result_9 = request.POST['lux_result_9']
          existing_Form.lux_parameters_10 = request.POST['lux_parameters_10']
          existing_Form.lux_result_10 = request.POST['lux_result_10']
          existing_Form.lux_parameters_11 = request.POST['lux_parameters_11']
          existing_Form.lux_result_11 = request.POST['lux_result_11']
          existing_Form.lux_parameters_12 = request.POST['lux_parameters_12']
          existing_Form.lux_result_12 = request.POST['lux_result_12']
          existing_Form.lux_parameters_13 = request.POST['lux_parameters_13']
          existing_Form.lux_result_13 = request.POST['lux_result_13']
          existing_Form.lux_legend_1 = request.POST['lux-legend-1']
          existing_Form.lux_legend_2 = request.POST['lux-legend-2']
          existing_Form.lux_legend_3 = request.POST['lux-legend-3']
          existing_Form.lux_legend_4 = request.POST['lux-legend-4']
          existing_Form.lux_legend_5 = request.POST['lux-legend-5']
          existing_Form.lux_legend_6 = request.POST['lux-legend-6']
          existing_Form.lux_legend_7 = request.POST['lux-legend-7']
          existing_Form.lux_legend_8 = request.POST['lux-legend-8']
          existing_Form.lux_legend_9 = request.POST['lux-legend-9']
          existing_Form.lux_legend_10 = request.POST['lux-legend-10']
          existing_Form.lux_legend_11 = request.POST['lux-legend-11']
          existing_Form.lux_edit_note = request.POST['lux_edit_note']
          existing_Form.lux_custom_legend = request.POST['lux_custom_legend']
          existing_Form.lux_doc_con1 = request.POST['lux_doc_con1']
          existing_Form.lux_doc_con2 = request.POST['lux_doc_con2']
          existing_Form.lux_doc_con3 = request.POST['lux_doc_con3']
          existing_Form.created_by = request.user
          # existing_Form.lux_analyzedby = request.FILES['lux-analyzedby']
          # existing_Form.lux_reviewedby = request.FILES['lux-reviewedby']
          # existing_Form.lux_approvedby = request.FILES['lux-approvedby']
          # existing_Form.lux_approvedby1 = request.FILES['lux-approvedby1']
          existing_Form.city_location = request.POST['city_location']
          existing_Form.extra_field = json.loads(request.POST['extra_field'])
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameter = request.POST.getlist('parameter[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]

               existing_Form.extra_field.append({
                         "sr": sr,
                         "parameter": parameter,
                         "unit": unit,
                         "result": result,
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
                    setattr(existing_Form, image_key, '')
                    setattr(existing_Form, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(existing_Form, image_key, base64_encoded)
                         setattr(existing_Form, desc_key, description or '')
                         print(f"Updated image {i}")
                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
               else:
                    if description is not None:
                         setattr(existing_Form, desc_key, description)
                         print(f"Updated description {i}")
          existing_Form.id = None
          existing_Form.save()
          user = request.user
          # action = f'Lux Analysis Form {existing_Form.lab_report_no} cloned by {user.username}'
          # AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/luxAnalysisReport/{str(id)}/"
              return redirect(to=url)
          
          if "submit" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='luxAnalysisList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "luxClone.html")

__all__ = [
    'luxAnalysis',
    'luxAnalysisList',
    'luxAnalysisDelete',
    'luxAnalysisEdit',
    'luxAnalysisUpdate',
    'luxAnalysisView',
    'luxAnalysisReportPdf',
    'luxAnalysisReportPdf1',
    'luxFormclone',
    'luxFormcloneSave',
]
