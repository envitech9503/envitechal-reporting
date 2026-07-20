# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403



@login_required(login_url="/login")
def vehicularEmission(request):
     if request.method == "POST":
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['vehEm_lab_report_no']
          invoice_bill_no = request.POST['vehEm_invoice_no']
          reporting_date = request.POST['vehEm_report_date']
          report_to = request.POST['vehEm_report_to']
          address = request.POST['vehEm_address']
          attention = request.POST['vehEm_attention']
          email = request.POST['vehEm_email']
          sample_id = request.POST['vehEm_testId']
          vehEm_test_perf_date = request.POST['vehEm_test_perf_date']
          vehEm_test_type = request.POST['vehEm_test_type']
          vehEm_test_type_extra = request.POST['vehEm_test_type_extra']
          vehEm_test_perfBy = request.POST['vehEm_test_perfBy']
          vehEm_test_desc = request.POST['vehEm_test_desc']
          select = request.POST['select']
          vehEm_sr1 = request.POST['vehEm_sr1']
          vehEm_sr2 = request.POST['vehEm_sr2']
          vehEm_sr3 = request.POST['vehEm_sr3']
          vehEm_legend_1 = request.POST['vehEm-legend-1']
          vehEm_legend_2 = request.POST['vehEm-legend-2']
          vehEm_legend_3 = request.POST['vehEm-legend-3']
          vehEm_legend_4 = request.POST['vehEm-legend-4']
          vehEm_legend_5 = request.POST['vehEm-legend-5']
          vehEm_legend_6 = request.POST['vehEm-legend-6']
          vehEm_legend_7 = request.POST['vehEm-legend-7']
          vehEm_legend_8 = request.POST['vehEm-legend-8']
          vehEm_legend_9 = request.POST['vehEm-legend-9']
          vehEm_legend_10 = request.POST['vehEm-legend-10']
          vehEm_legend_11 = request.POST['vehEm-legend-11']
          vehEm_edit_note = request.POST['vehEm_edit_note']
          vehEm_custom_legend = request.POST['vehEm_custom_legend']
          vehEm_doc_con1 = request.POST['vehEm_doc-con1']
          vehEm_doc_con2 = request.POST['vehEm_doc-con2']
          vehEm_doc_con3 = request.POST['vehEm_doc-con3']
          # vehEm_analyzedby = request.FILES['vehEm-analyzedby']
          # vehEm_reviewedby = request.FILES['vehEm-reviewedby']
          # vehEm_approvedby = request.FILES['vehEm-approvedby']
          # vehEm_approvedby1 = request.FILES['vehEm-approvedby1']
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
     
          vehicularemissionForm = VehiculEmissionForm(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,
                                                      reporting_date=reporting_date,report_to=report_to,address=address,attention=
                                                      attention,email=email,sample_id=sample_id,vehEm_test_perf_date=vehEm_test_perf_date,
                                                      vehEm_test_type=vehEm_test_type,vehEm_test_type_extra=vehEm_test_type_extra,vehEm_test_perfBy=vehEm_test_perfBy,vehEm_test_desc=vehEm_test_desc,location=location,
                                                      select=select,vehEm_sr1=vehEm_sr1,vehEm_sr2=vehEm_sr2,vehEm_sr3=vehEm_sr3,vehEm_legend_1=
                                                      vehEm_legend_1,vehEm_legend_2=vehEm_legend_2,vehEm_legend_3=vehEm_legend_3,vehEm_legend_4=vehEm_legend_4,
                                                      vehEm_legend_5=vehEm_legend_5,vehEm_legend_6=vehEm_legend_6,vehEm_legend_7=vehEm_legend_7,vehEm_legend_8=vehEm_legend_8,
                                                      vehEm_legend_9=vehEm_legend_9,vehEm_legend_10=vehEm_legend_10,vehEm_legend_11=vehEm_legend_11,vehEm_edit_note=vehEm_edit_note,
                                                      vehEm_custom_legend=vehEm_custom_legend,vehEm_doc_con1=vehEm_doc_con1,vehEm_doc_con2=vehEm_doc_con2,vehEm_doc_con3=vehEm_doc_con3,
                                                      extra_field=extra_field,city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,
                                                      assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          vehicularemissionForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Vehicular Emission Form {vehicularemissionForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (VehiculEmissionForm.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/vehicularEmission-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect("vahicularEmission")

     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"vehicularEmission.html",context)


@login_required(login_url="/login")
def vehicularEmissionList(request):
     vel, _srch = _list_filter(request, VehiculEmissionForm)
     context = {'searched':_srch, 'data':vel}
     return render(request,'vehicularEmissionList.html',context)

@login_required(login_url="/login")
def vehicularEmissionDelete(request,pk):
     vem =VehiculEmissionForm.objects.get(id=pk)
     vem.delete()
     user = request.user
     action = f'Vehicular Emission Form {vem.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect(to="vehicularEmissionList")

@login_required(login_url="/login")
def vehicularEmissionEdit(request,pk):
     vem = VehiculEmissionForm.objects.get(id=pk)
     vem.extra_field = vem.extra_field.replace("'", "\"")
     vem.extra_field = json.loads(vem.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(vem, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     context = {'data':vem,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"vehicularEmissionEdit.html",context)

@login_required(login_url="/login")
def vehicularEmissionUpdate(request,pk):
     vem = VehiculEmissionForm.objects.get(id=pk)
     if request.method == "POST":
          vem.location = request.POST['location']
          industry_id = request.POST.get('industry')
          vem.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          vem.lab_report_no = request.POST['vehEm_lab_report_no']
          vem.invoice_bill_no = request.POST['vehEm_invoice_no']
          vem.reporting_date = request.POST['vehEm_report_date']
          vem.report_to = request.POST['vehEm_report_to']
          vem.address = request.POST['vehEm_address']
          vem.attention = request.POST['vehEm_attention']
          vem.email = request.POST['vehEm_email']
          vem.sample_id = request.POST['vehEm_testId']
          vem.vehEm_test_perf_date = request.POST['vehEm_test_perf_date']
          vem.vehEm_test_type = request.POST['vehEm_test_type']
          vem.vehEm_test_type_extra = request.POST['vehEm_test_type_extra']
          vem.vehEm_test_perfBy = request.POST['vehEm_test_perfBy']
          vem.vehEm_test_desc = request.POST['vehEm_test_desc']
          vem.select = request.POST['select']
          vem.vehEm_sr1 = request.POST['vehEm_sr1']
          vem.vehEm_sr2 = request.POST['vehEm_sr2']
          vem.vehEm_sr3 = request.POST['vehEm_sr3']
          vem.vehEm_legend_1 = request.POST['vehEm-legend-1']
          vem.vehEm_legend_2 = request.POST['vehEm-legend-2']
          vem.vehEm_legend_3 = request.POST['vehEm-legend-3']
          vem.vehEm_legend_4 = request.POST['vehEm-legend-4']
          vem.vehEm_legend_5 = request.POST['vehEm-legend-5']
          vem.vehEm_legend_6 = request.POST['vehEm-legend-6']
          vem.vehEm_legend_7 = request.POST['vehEm-legend-7']
          vem.vehEm_legend_8 = request.POST['vehEm-legend-8']
          vem.vehEm_legend_9 = request.POST['vehEm-legend-9']
          vem.vehEm_legend_10 = request.POST['vehEm-legend-10']
          vem.vehEm_legend_11 = request.POST['vehEm-legend-11']
          vem.vehEm_edit_note = request.POST['vehEm_edit_note']
          vem.vehEm_custom_legend = request.POST['vehEm_custom_legend']
          vem.vehEm_doc_con1 = request.POST['vehEm_doc-con1']
          vem.vehEm_doc_con2 = request.POST['vehEm_doc-con2']
          vem.vehEm_doc_con3 = request.POST['vehEm_doc-con3']
          vem.created_by = request.user
          # vem.vehEm_analyzedby = request.FILES['vehEm-analyzedby']
          # vem.vehEm_reviewedby = request.FILES['vehEm-reviewedby']
          # vem.vehEm_approvedby = request.FILES['vehEm-approvedby']
          # vem.vehEm_approvedby1 = request.FILES['vehEm-approvedby1']
          vem.city_location = request.POST['city_location']
          vem.extra_field = json.loads(request.POST['extra_field'])
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          vem.analyst_signature = analyst_sign
          vem.assistant_manager_signature = review_sign
          vem.lab_manager_signature = approved_sign
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               parameters = request.POST.getlist('parameters[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               vem.extra_field.append({
                         "sr": sr,
                         "parameters": parameters,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        

                            
            

          
          vem.extra_field = json.dumps(vem.extra_field)
          
          vem.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(vem, image_key, '')
                    setattr(vem, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(vem, image_key, base64_encoded)
                         setattr(vem, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(vem, desc_key, description)
          vem.save()
          user = request.user
          action = f'Vehicular Emission Form {vem.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = vem.id
          if "update_and_view" in request.POST:
               url = f'/vehicularEmission-view/{str(id)}/'
               return redirect(to=url)
          else:
               return redirect("vehicularEmissionList")
     return render(request,"vehicularEmissionList.html")


def vehicularEmissionView(request,pk):
     vem = VehiculEmissionForm.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     vem.extra_field = vem.extra_field.replace("'", "\"")
     vem.extra_field = json.loads(vem.extra_field)
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{vem.lab_report_no}.png"
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
     context = {'data':vem,'qr':qr_relative_path,'logo':logo}

     return render(request,'vehicularEmissionReport.html',context)


def vehicularEmissionReport(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_vehicularEmissionReport as PDFWithPageNumbers




     vem = VehiculEmissionForm.objects.get(id=pk)
     vem.extra_field = vem.extra_field.replace("'", "\"")
     vem.extra_field = json.loads(vem.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Result",""],
     ]
     sr_no = 1
     if vem.vehEm_sr1:
          a = [str(sr_no),"Carbon Monoxide","%",vem.vehEm_sr1,"6"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if vem.vehEm_sr2:
          a = [str(sr_no),"Smoke Ringlemann Scale","-",vem.vehEm_sr2,"2"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if vem.vehEm_sr3:
          a = [str(sr_no),"	Noise","dB",vem.vehEm_sr3,"85"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     
     for extra_field in vem.extra_field:
               parameters = extra_field.get("parameters")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               if parameters:
                    a = [str(sr_no), parameters, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                              address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,vehEm_test_perf_date=vem.vehEm_test_perf_date,
                              vehEm_test_desc=vem.vehEm_test_desc,vehEm_test_type=vem.vehEm_test_type,vehEm_test_perfBy=vem.vehEm_test_perfBy,vehEm_test_type_extra=vem.vehEm_test_type_extra

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
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               if k == 0:
                    data_row[4] = vem.select + ' Limits'

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table
          Table_Data1 = [
          
     ]
     if vem.vehEm_edit_note:
          a=["Note: "+vem.vehEm_edit_note] 
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
     if vem.vehEm_legend_1:
          a = [vem.vehEm_legend_1]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_2:
          a = [vem.vehEm_legend_2]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_3:
          a = [vem.vehEm_legend_3]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_4:
          a = [vem.vehEm_legend_4]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_5:
          a = [vem.vehEm_legend_5]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_6:
          a = [vem.vehEm_legend_6]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_7:
          a = [vem.vehEm_legend_7]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_8:
          a = [vem.vehEm_legend_8]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_9:
          a = [vem.vehEm_legend_9]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_10:
          a = [vem.vehEm_legend_10]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_11:
          a = [vem.vehEm_legend_11]
          Table_data_legend.append(a)
          

     if vem.vehEm_custom_legend:
          a = [vem.vehEm_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')

     


     if vem.analyst_signature:
         pdf.image(vem.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,251,36+pdf.get_string_width(f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})"),251)
     pdf.text(26,254,f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})")
     if vem.assistant_manager_signature:
         pdf.image(vem.assistant_manager_signature.signature,100,233,20.32,20.32)
     pdf.line(126,251,47.5+pdf.get_string_width(f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})"),251)
     pdf.text(87.5,254,f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if vem.lab_manager_signature:
         pdf.image(vem.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,251,165+pdf.get_string_width(f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})"),251)
     pdf.text(160,254,f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})")



     pdf.line(10,256,-10+pdf.w,256)
     
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
     if vem.location == "NEQS" and (vem.city_location or "").lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif vem.location == "NEQS" and (vem.city_location or "").lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(227/Dir/(ML&I)/EPA/12/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 227/Dir/(ML&I)/EPA/12/2025.")
          
          
     elif vem.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif vem.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(227/Dir/(ML&I)/EPA/12/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 227/Dir/(ML&I)/EPA/12/2025.")
          
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,258,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,275,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=vem.vehEm_doc_con1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=vem.vehEm_doc_con2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,txt=vem.vehEm_doc_con3)

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

     # file_path = '/home/django/EnviTechAlApp/vehicularEmission/'
     # pdf.output(file_path + vem.lab_report_no +'.pdf')
     # pdf = open(file_path + vem.lab_report_no +'.pdf', 'rb')

     # # pdf.output(vem.lab_report_no +'.pdf')

     # # pdf = open(vem.lab_report_no +'.pdf', 'rb')
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
     
     
def vehicularEmissionReport1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_vehicularEmissionReport1 as PDFWithPageNumbers




     vem = VehiculEmissionForm.objects.get(id=pk)
     vem.extra_field = vem.extra_field.replace("'", "\"")
     vem.extra_field = json.loads(vem.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Result",""],
     ]
     sr_no = 1
     if vem.vehEm_sr1:
          a = [str(sr_no),"Carbon Monoxide","%",vem.vehEm_sr1,"6"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if vem.vehEm_sr2:
          a = [str(sr_no),"Smoke Ringlemann Scale","-",vem.vehEm_sr2,"2"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if vem.vehEm_sr3:
          a = [str(sr_no),"	Noise","dB",vem.vehEm_sr3,"85"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in vem.extra_field:
               parameters = extra_field.get("parameters")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               if parameters:
                    a = [str(sr_no), parameters, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=vem.lab_report_no,invoice_bill_no=vem.invoice_bill_no,reporting_date=vem.reporting_date,report_to=vem.report_to,
                              address=vem.address,attention=vem.attention,email=vem.email,sample_id=vem.sample_id,vehEm_test_perf_date=vem.vehEm_test_perf_date,
                              vehEm_test_desc=vem.vehEm_test_desc,vehEm_test_type=vem.vehEm_test_type,vehEm_test_perfBy=vem.vehEm_test_perfBy,

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
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               if k == 0:
                    data_row[4] = vem.select + ' Limits'

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table
          Table_Data1 = [
          
     ]
     if vem.vehEm_edit_note:
          a=["Note: "+vem.vehEm_edit_note] 
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
     if vem.vehEm_legend_1:
          a = [vem.vehEm_legend_1]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_2:
          a = [vem.vehEm_legend_2]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_3:
          a = [vem.vehEm_legend_3]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_4:
          a = [vem.vehEm_legend_4]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_5:
          a = [vem.vehEm_legend_5]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_6:
          a = [vem.vehEm_legend_6]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_7:
          a = [vem.vehEm_legend_7]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_8:
          a = [vem.vehEm_legend_8]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_9:
          a = [vem.vehEm_legend_9]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_10:
          a = [vem.vehEm_legend_10]
          Table_data_legend.append(a)
          
     if vem.vehEm_legend_11:
          a = [vem.vehEm_legend_11]
          Table_data_legend.append(a)
          

     if vem.vehEm_custom_legend:
          a = [vem.vehEm_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')

   

     # pdf.image(vem.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,251,36+pdf.get_string_width("Analyzed By (Analyst)"),251)
     # pdf.text(26,254,"Analyzed By (Analyst)")
     # pdf.image(vem.assistant_manager_signature.signature,100,233,20.32,20.32)
     # pdf.line(126,251,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),251)
     # pdf.text(87.5,254,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,230,22,22)
     # pdf.image(vem.lab_manager_signature.signature,178,233,20.32,20.32)
     # pdf.line(155,251,165+pdf.get_string_width("Approved By (Lab Manager)"),251)
     # pdf.text(160,254,"Approved By (Lab Manager)")
     
     
     if vem.analyst_signature:
         pdf.image(vem.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,251,36+pdf.get_string_width(f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})"),251)
     pdf.text(26,254,f"Analyzed By ({(vem.analyst_signature.role if vem.analyst_signature else '')})")
     if vem.assistant_manager_signature:
         pdf.image(vem.assistant_manager_signature.signature,100,233,20.32,20.32)
     pdf.line(126,251,47.5+pdf.get_string_width(f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})"),251)
     pdf.text(87.5,254,f"Reviewed By ({(vem.assistant_manager_signature.role if vem.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if vem.lab_manager_signature:
         pdf.image(vem.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,251,165+pdf.get_string_width(f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})"),251)
     pdf.text(160,254,f"Approved By ({(vem.lab_manager_signature.role if vem.lab_manager_signature else '')})")



     pdf.line(10,256,-10+pdf.w,256)
     
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
     if vem.location == "NEQS" and (vem.city_location or "").lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif vem.location == "NEQS" and (vem.city_location or "").lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(227/Dir/(ML&I)/EPA/12/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 227/Dir/(ML&I)/EPA/12/2025.")
          
          
     elif vem.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif vem.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(227/Dir/(ML&I)/EPA/12/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 227/Dir/(ML&I)/EPA/12/2025.")
          
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,258,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,275,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=vem.vehEm_doc_con1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=vem.vehEm_doc_con2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,txt=vem.vehEm_doc_con3)
     
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


     # file_path = '/home/django/EnviTechAlApp/vem_pdf/'
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


def vehicularEmissionclone(request,pk):
     existing_form = VehiculEmissionForm.objects.get(id=pk)
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
     return render(request,"vehicularEmissionClone.html",context)

def vehicularEmissioncloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = VehiculEmissionForm.objects.get(id=pk)
     except VehiculEmissionForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == "POST":
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['vehEm_lab_report_no']
          existing_Form.invoice_bill_no = request.POST['vehEm_invoice_no']
          existing_Form.reporting_date = request.POST['vehEm_report_date']
          existing_Form.report_to = request.POST['vehEm_report_to']
          existing_Form.address = request.POST['vehEm_address']
          existing_Form.attention = request.POST['vehEm_attention']
          existing_Form.email = request.POST['vehEm_email']
          existing_Form.sample_id = request.POST['vehEm_testId']
          existing_Form.vehEm_test_perf_date = request.POST['vehEm_test_perf_date']
          existing_Form.vehEm_test_type = request.POST['vehEm_test_type']
          existing_Form.vehEm_test_type_extra = request.POST['vehEm_test_type_extra']
          existing_Form.vehEm_test_perfBy = request.POST['vehEm_test_perfBy']
          existing_Form.vehEm_test_desc = request.POST['vehEm_test_desc']
          existing_Form.select = request.POST['select']
          existing_Form.vehEm_sr1 = request.POST['vehEm_sr1']
          existing_Form.vehEm_sr2 = request.POST['vehEm_sr2']
          existing_Form.vehEm_sr3 = request.POST['vehEm_sr3']
          existing_Form.vehEm_legend_1 = request.POST['vehEm-legend-1']
          existing_Form.vehEm_legend_2 = request.POST['vehEm-legend-2']
          existing_Form.vehEm_legend_3 = request.POST['vehEm-legend-3']
          existing_Form.vehEm_legend_4 = request.POST['vehEm-legend-4']
          existing_Form.vehEm_legend_5 = request.POST['vehEm-legend-5']
          existing_Form.vehEm_legend_6 = request.POST['vehEm-legend-6']
          existing_Form.vehEm_legend_7 = request.POST['vehEm-legend-7']
          existing_Form.vehEm_legend_8 = request.POST['vehEm-legend-8']
          existing_Form.vehEm_legend_9 = request.POST['vehEm-legend-9']
          existing_Form.vehEm_legend_10 = request.POST['vehEm-legend-10']
          existing_Form.vehEm_legend_11 = request.POST['vehEm-legend-11']
          existing_Form.vehEm_edit_note = request.POST['vehEm_edit_note']
          existing_Form.vehEm_custom_legend = request.POST['vehEm_custom_legend']
          existing_Form.vehEm_doc_con1 = request.POST['vehEm_doc-con1']
          existing_Form.vehEm_doc_con2 = request.POST['vehEm_doc-con2']
          existing_Form.vehEm_doc_con3 = request.POST['vehEm_doc-con3']
          existing_Form.created_by = request.user
          # existing_Form.vehEm_analyzedby = request.FILES['vehEm-analyzedby']
          # existing_Form.vehEm_reviewedby = request.FILES['vehEm-reviewedby']
          # existing_Form.vehEm_approvedby = request.FILES['vehEm-approvedby']
          # existing_Form.vehEm_approvedby1 = request.FILES['vehEm-approvedby1']
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
          action = f'Vehicular Analysis Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/vehicularEmission-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='vehicularEmissionList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "vehicularEmissionClone.html")

__all__ = [
    'vehicularEmission',
    'vehicularEmissionList',
    'vehicularEmissionDelete',
    'vehicularEmissionEdit',
    'vehicularEmissionUpdate',
    'vehicularEmissionView',
    'vehicularEmissionReport',
    'vehicularEmissionReport1',
    'vehicularEmissionclone',
    'vehicularEmissioncloneSave',
]
