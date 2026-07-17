# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


#continue from here

@login_required(login_url="/login")
def machineOil(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['machine_lab_rep_no']
          invoice_bill_no = request.POST['machine_invoice_no']
          reporting_date = request.POST['machine_rep_date']
          report_to = request.POST['machine_report_to']
          address = request.POST['machine_address']
          attention = request.POST['machine_attention']
          email = request.POST['machine_email']
          sample_id = request.POST['machine_sampleId']
          machine_sample_col_date = request.POST['machine_sample_col_date']
          machine_sample_desc = request.POST['machine_sample_desc']
          machine_sample_type = request.POST['machine_sample_type']
          machine_sample_col_by = request.POST['machine_sample_col_by']
          machine_test_desc = request.POST['machine_test_desc']
          machine_sr1 = request.POST['machine_sr1']
          machine_sr2 = request.POST['machine_sr2']
          machine_sr3 = request.POST['machine_sr3']
          machine_sr4 = request.POST['machine_sr4']
          machine_sr5 = request.POST['machine_sr5']
          machine_sr6 = request.POST['machine_sr6']
          machine_sr7 = request.POST['machine_sr7']
          machine_sr8 = request.POST['machine_sr8']
          machine_sr9 = request.POST['machine_sr9']
          machine_sr10 = request.POST['machine_sr10']
          machine_sr11 = request.POST['machine_sr11']
          machine_sr12 = request.POST['machine_sr12']
          machine_sr13 = request.POST['machine_sr13']
          machine_sr14 = request.POST['machine_sr14']
          machine_sr15 = request.POST['machine_sr15']
          machine_sr16 = request.POST['machine_sr16']
          machine_legend_1 = request.POST['machine_legend-1']
          machine_legend_2 = request.POST['machine_legend-2']
          custom_legend = request.POST['custom_legend']
          machine_edit_note = request.POST['machine_edit_note']
          machine_custom_legend = request.POST['machine_custom_legend']
          machine_doc1 = request.POST['machine_doc1']
          machine_doc2 = request.POST['machine_doc2']
          machine_doc3 = request.POST['machine_doc3']
          # machine_analyzedby = request.FILES['machine_analyzedby']
          # machine_reviewedby = request.FILES['machine_reviewedby']
          # machine_approvedby = request.FILES['machine_approvedby']
          # machine_approvedby1 = request.FILES['machine_approvedby1']
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

          machineOil = MachineOilForm(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,
                                      reporting_date=reporting_date,report_to=report_to,
                                      address=address,attention=attention,
                                      email=email,sample_id=sample_id,
                                      machine_sample_col_date=machine_sample_col_date,machine_sample_desc=machine_sample_desc,
                                      machine_sample_type=machine_sample_type,machine_sample_col_by=machine_sample_col_by,
                                      machine_test_desc=machine_test_desc,machine_sr1=machine_sr1,machine_sr2=machine_sr2,
                                      machine_sr3=machine_sr3,machine_sr4=machine_sr4,machine_sr5=machine_sr5,
                                      machine_sr6=machine_sr6,machine_sr7=machine_sr7,machine_sr8=machine_sr8,location=location,
                                      machine_sr9=machine_sr9,machine_sr10=machine_sr10,machine_sr11=machine_sr11,machine_sr12=machine_sr12,
                                      machine_sr13=machine_sr13,machine_sr14=machine_sr14,machine_sr15=machine_sr15,machine_sr16=
                                      machine_sr16,machine_legend_1=machine_legend_1,machine_legend_2=machine_legend_2,custom_legend=custom_legend,
                                      machine_edit_note=machine_edit_note,machine_custom_legend=machine_custom_legend,machine_doc1=machine_doc1,machine_doc2=machine_doc2,machine_doc3=machine_doc3,
                                     city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                     lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          machineOil.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Machine Oil Form {machineOil.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (MachineOilForm.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/machineOil-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="machineOil")

     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"machineOil.html",context)



@login_required(login_url="/login")
def machineOilList(request):
     machineOil, _srch = _list_filter(request, MachineOilForm)
     context = {'searched':_srch, 'data':machineOil}
     return render(request,"machineOilList.html",context)

@login_required(login_url="/login")
def machineOilDelete(request,pk):
     machineOil= MachineOilForm.objects.get(id=pk)
     machineOil.delete()
     user = request.user
     action = f'Machine Oil Form {machineOil.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("machineOilList")

@login_required(login_url="/login")
def machineOilEdit(request,pk):
     machineOil =  MachineOilForm.objects.get(id=pk)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(machineOil, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':machineOil,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"machineOilEdit.html",context)

@login_required(login_url="/login")
def machineOilUpdate(request,pk):
     machineOil = MachineOilForm.objects.get(id=pk)
     if request.method == 'POST':
          machineOil.location = request.POST['location']
          industry_id = request.POST.get('industry')
          machineOil.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          machineOil.lab_report_no = request.POST['machine_lab_rep_no']
          machineOil.invoice_bill_no = request.POST['machine_invoice_no']
          machineOil.reporting_date = request.POST['machine_rep_date']
          machineOil.report_to = request.POST['machine_report_to']
          machineOil.address = request.POST['machine_address']
          machineOil.attention = request.POST['machine_attention']
          machineOil.email = request.POST['machine_email']
          machineOil.sample_id = request.POST['machine_sampleId']
          machineOil.machine_sample_col_date = request.POST['machine_sample_col_date']
          machineOil.machine_sample_desc = request.POST['machine_sample_desc']
          machineOil.machine_sample_type = request.POST['machine_sample_type']
          machineOil.machine_sample_col_by = request.POST['machine_sample_col_by']
          machineOil.machine_test_desc = request.POST['machine_test_desc']
          machineOil.machine_sr1 = request.POST['machine_sr1']
          machineOil.machine_sr2 = request.POST['machine_sr2']
          machineOil.machine_sr3 = request.POST['machine_sr3']
          machineOil.machine_sr4 = request.POST['machine_sr4']
          machineOil.machine_sr5 = request.POST['machine_sr5']
          machineOil.machine_sr6 = request.POST['machine_sr6']
          machineOil.machine_sr7 = request.POST['machine_sr7']
          machineOil.machine_sr8 = request.POST['machine_sr8']
          machineOil.machine_sr9 = request.POST['machine_sr9']
          machineOil.machine_sr10 = request.POST['machine_sr10']
          machineOil.machine_sr11 = request.POST['machine_sr11']
          machineOil.machine_sr12 = request.POST['machine_sr12']
          machineOil.machine_sr13 = request.POST['machine_sr13']
          machineOil.machine_sr14 = request.POST['machine_sr14']
          machineOil.machine_sr15 = request.POST['machine_sr15']
          machineOil.machine_sr16 = request.POST['machine_sr16']
          machineOil.machine_legend_1 = request.POST['machine_legend-1']
          machineOil.machine_legend_2 = request.POST['machine_legend-2']
          machineOil.custom_legend = request.POST['custom_legend']
          machineOil.machine_edit_note = request.POST['machine_edit_note']
          machineOil.machine_custom_legend = request.POST['machine_custom_legend']
          machineOil.machine_doc1 = request.POST['machine_doc1']
          machineOil.machine_doc2 = request.POST['machine_doc2']
          machineOil.machine_doc3 = request.POST['machine_doc3']
          machineOil.created_by = request.user
          # machineOil.machine_analyzedby = request.FILES['machine_analyzedby']
          # machineOil.machine_reviewedby = request.FILES['machine_reviewedby']
          # machineOil.machine_approvedby = request.FILES['machine_approvedby']
          # machineOil.machine_approvedby1 = request.FILES['machine_approvedby1']
          machineOil.city_location = request.POST['city_location']
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          machineOil.analyst_signature = analyst_sign
          machineOil.assistant_manager_signature = review_sign
          machineOil.lab_manager_signature = approved_sign

          machineOil.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(machineOil, image_key, '')
                    setattr(machineOil, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(machineOil, image_key, base64_encoded)
                         setattr(machineOil, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(machineOil, desc_key, description)
          

          machineOil.save()
          user = request.user
          action = f'Machine Oil Form {machineOil.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = machineOil.id
          if "submit_and_view" in request.POST:
               url = f"/machineOil-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="machineOilList")


     return render(request,"machineOil.html")


def machineOilView(request,pk):
     machineOil = MachineOilForm.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{machineOil.lab_report_no}.png"
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
     context = {'data':machineOil,'qr':qr_relative_path,'logo':logo}

     return render(request,'machineOilReport.html',context)

def machineOilReportPdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_machineOilReportPdf as PDFWithPageNumbers




     machine = MachineOilForm.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result","*GOTS Limits"],
     ]
     sr_no = 1
     if machine.machine_sr1:
          a = [str(sr_no),"Antimony (Sb)","ASTM D-5185","mg/kg",machine.machine_sr1,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr2:
          a = [str(sr_no),"Arsenic (As)","ASTM D-5185","mg/kg",machine.machine_sr2,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr3:
          a = [str(sr_no),"Barium (Ba)","ASTM D-5185","mg/kg",machine.machine_sr3,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr4:
          a = [str(sr_no),"Cadmium (Cd)","ASTM D-5185","mg/kg",machine.machine_sr4,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr5:
          a = [str(sr_no),"Cobalt (Co)","ASTM D-5185","mg/kg",machine.machine_sr5,"500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr6:
          a = [str(sr_no),"Copper (Cu)","ASTM D-5185","mg/kg",machine.machine_sr6,"250"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr7:
          a = [str(sr_no),"Chromium (Cr)","ASTM D-5185","mg/kg",machine.machine_sr7,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr8:
          a = [str(sr_no),"Iron (Fe)","ASTM D-5185","mg/kg",machine.machine_sr8,"2500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr9:
          a = [str(sr_no),"Lead (Pb)","ASTM D-5185","mg/kg",machine.machine_sr9,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr10:
          a = [str(sr_no),"Manganese (Mn)","ASTM D-5185","mg/kg",machine.machine_sr10,"1000"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr11:
          a = [str(sr_no),"Nickel (Ni)","ASTM D-5185","mg/kg",machine.machine_sr11,"200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr12:
          a = [str(sr_no),"Mercury (Hg)","ASTM D7622","mg/kg",machine.machine_sr12,"04"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr13:
          a = [str(sr_no),"Selenium (Se)","ASTM D-5185","mg/kg",machine.machine_sr13,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr14:
          a = [str(sr_no),"Silver (Ag)","ASTM D-5185","mg/kg",machine.machine_sr14,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr15:
          a = [str(sr_no),"Zinc (Zn)","ASTM D-5185","mg/kg",machine.machine_sr15,"1500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr16:
          a = [str(sr_no),"Tin (Sn)","ASTM D-5185","mg/kg",machine.machine_sr16,"250"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)          






     pdf = PDFWithPageNumbers(lab_report_no=machine.lab_report_no,invoice_bill_no=machine.invoice_bill_no,reporting_date=machine.reporting_date,report_to=machine.report_to,
                              address=machine.address,attention=machine.attention,email=machine.email,sample_id=machine.sample_id,machine_sample_col_date=machine.machine_sample_col_date,
                              machine_sample_desc=machine.machine_sample_desc,machine_sample_type=machine.machine_sample_type,machine_sample_col_by=machine.machine_sample_col_by,machine_test_desc = machine.machine_test_desc

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
     with pdf.table(col_widths=(10, 50, 30,30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = machine.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               _exc = False
               if k > 0 and len(data_row) >= 6:
                   _exc = _etal_mo_exceeds(data_row[4], data_row[5])
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    if _exc and i == 4:
                        row.cell(datum, style=_etal_red_style())
                    else:
                        row.cell(datum)

     # data after Table


     Table_Data1 = [
          
     ]
     if machine.machine_edit_note:
          a=["Note: "+machine.machine_edit_note] 
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
     if machine.machine_legend_1:
          a = [machine.machine_legend_1]
          Table_data_legend.append(a)
          
     if machine.machine_legend_2:
          a = [machine.machine_legend_2]
          Table_data_legend.append(a)

     if machine.custom_legend:
          a = [machine.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     # if machine.machine_edit_note:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,217,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(214.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=machine.machine_edit_note)
     # line_height = 4
     # y = 224
     # if machine.machine_legend_1:
     #      pdf.text(10,y,txt=machine.machine_legend_1)
     #      y = y+line_height
     # if machine.machine_legend_2:
     #      pdf.text(10,y,txt=machine.machine_legend_2)
     #      y = y+line_height

     # if machine.machine_custom_legend:
     #      pdf.text(10,y,txt=machine.machine_custom_legend)
     #      y = y+line_height


     # pdf.image(machine.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(machine.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(machine.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     if machine.analyst_signature:
         pdf.image(machine.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(machine.analyst_signature.role if machine.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(machine.analyst_signature.role if machine.analyst_signature else '')})")
     if machine.assistant_manager_signature:
         pdf.image(machine.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(machine.assistant_manager_signature.role if machine.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(machine.assistant_manager_signature.role if machine.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if machine.lab_manager_signature:
         pdf.image(machine.lab_manager_signature.signature,178,239,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(machine.lab_manager_signature.role if machine.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(machine.lab_manager_signature.role if machine.lab_manager_signature else '')})")


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
     # if machine.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if machine.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if machine.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if machine.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     
     if machine.location == "NEQS" and machine.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif machine.location == "NEQS" and machine.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif machine.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif machine.location == "PEQS":
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
     pdf.text(128,285,txt=machine.machine_doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=machine.machine_doc2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=machine.machine_doc3)
     
     if machine.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(machine, f'pdf_image_{i}')
               desc = getattr(machine, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=machine.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/machineOil/'
     # pdf.output(file_path + machine.lab_report_no +'.pdf')
     # pdf = open(file_path + machine.lab_report_no +'.pdf', 'rb')


     # response = FileResponse(pdf)
     # return response
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={machine.lab_report_no}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def machineOilReportPdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_machineOilReportPdf1 as PDFWithPageNumbers




     machine = MachineOilForm.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result","*GOTS Limits"],
     ]
     sr_no = 1
     if machine.machine_sr1:
          a = [str(sr_no),"Antimony (Sb)","ASTM D-5185","mg/kg",machine.machine_sr1,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr2:
          a = [str(sr_no),"Arsenic (As)","ASTM D-5185","mg/kg",machine.machine_sr2,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr3:
          a = [str(sr_no),"Barium (Ba)","ASTM D-5185","mg/kg",machine.machine_sr3,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr4:
          a = [str(sr_no),"Cadmium (Cd)","ASTM D-5185","mg/kg",machine.machine_sr4,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr5:
          a = [str(sr_no),"Cobalt (Co)","ASTM D-5185","mg/kg",machine.machine_sr5,"500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr6:
          a = [str(sr_no),"Copper (Cu)","ASTM D-5185","mg/kg",machine.machine_sr6,"250"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr7:
          a = [str(sr_no),"Chromium (Cr)","ASTM D-5185","mg/kg",machine.machine_sr7,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr8:
          a = [str(sr_no),"Iron (Fe)","ASTM D-5185","mg/kg",machine.machine_sr8,"2500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr9:
          a = [str(sr_no),"Lead (Pb)","ASTM D-5185","mg/kg",machine.machine_sr9,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr10:
          a = [str(sr_no),"Manganese (Mn)","ASTM D-5185","mg/kg",machine.machine_sr10,"1000"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr11:
          a = [str(sr_no),"Nickel (Ni)","ASTM D-5185","mg/kg",machine.machine_sr11,"200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr12:
          a = [str(sr_no),"Mercury (Hg)","ASTM D7622","mg/kg",machine.machine_sr12,"04"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr13:
          a = [str(sr_no),"Selenium (Se)","ASTM D-5185","mg/kg",machine.machine_sr13,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr14:
          a = [str(sr_no),"Silver (Ag)","ASTM D-5185","mg/kg",machine.machine_sr14,"100"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr15:
          a = [str(sr_no),"Zinc (Zn)","ASTM D-5185","mg/kg",machine.machine_sr15,"1500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if machine.machine_sr16:
          a = [str(sr_no),"Tin (Sn)","ASTM D-5185","mg/kg",machine.machine_sr16,"250"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)          






     pdf = PDFWithPageNumbers(lab_report_no=machine.lab_report_no,invoice_bill_no=machine.invoice_bill_no,reporting_date=machine.reporting_date,report_to=machine.report_to,
                              address=machine.address,attention=machine.attention,email=machine.email,sample_id=machine.sample_id,machine_sample_col_date=machine.machine_sample_col_date,
                              machine_sample_desc=machine.machine_sample_desc,machine_sample_type=machine.machine_sample_type,machine_sample_col_by=machine.machine_sample_col_by,machine_test_desc = machine.machine_test_desc

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
     with pdf.table(col_widths=(10, 50, 30,30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = machine.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               _exc = False
               if k > 0 and len(data_row) >= 6:
                   _exc = _etal_mo_exceeds(data_row[4], data_row[5])
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    if _exc and i == 4:
                        row.cell(datum, style=_etal_red_style())
                    else:
                        row.cell(datum)

     # data after Table

     number_of_rows = len(TABLE_DATA)  # Replace with the actual number of rows
     row_height = 4  # Replace with the actual row height in your table
     table_height = (number_of_rows) * row_height  
     
     if pdf.y + number_of_rows * row_height >= pdf.h:
          pdf.add_page()
     Table_Data1 = [
          
     ]
     if machine.machine_edit_note:
          a=["Note: "+machine.machine_edit_note] 
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
     if machine.machine_legend_1:
          a = [machine.machine_legend_1]
          Table_data_legend.append(a)
          
     if machine.machine_legend_2:
          a = [machine.machine_legend_2]
          Table_data_legend.append(a)

     if machine.custom_legend:
          a = [machine.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     # if machine.machine_edit_note:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,217,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(214.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=machine.machine_edit_note)
     # line_height = 4
     # y = 224
     # if machine.machine_legend_1:
     #      pdf.text(10,y,txt=machine.machine_legend_1)
     #      y = y+line_height
     # if machine.machine_legend_2:
     #      pdf.text(10,y,txt=machine.machine_legend_2)
     #      y = y+line_height

     # if machine.machine_custom_legend:
     #      pdf.text(10,y,txt=machine.machine_custom_legend)
     #      y = y+line_height


     # pdf.image(machine.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(machine.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,230,22,22)
     # pdf.image(machine.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if machine.analyst_signature:
         pdf.image(machine.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(machine.analyst_signature.role if machine.analyst_signature else '')})"),252)
     pdf.text(26,254.5,f"Analyzed By ({(machine.analyst_signature.role if machine.analyst_signature else '')})")
     if machine.assistant_manager_signature:
         pdf.image(machine.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(machine.assistant_manager_signature.role if machine.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,254.5,f"Reviewed By ({(machine.assistant_manager_signature.role if machine.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,230,22,22)
     if machine.lab_manager_signature:
         pdf.image(machine.lab_manager_signature.signature,178,234,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(machine.lab_manager_signature.role if machine.lab_manager_signature else '')})"),252)
     pdf.text(160,254.5,f"Approved By ({(machine.lab_manager_signature.role if machine.lab_manager_signature else '')})")


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
     # if machine.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if machine.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if machine.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if machine.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     
     
     
     if machine.location == "NEQS" and machine.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif machine.location == "NEQS" and machine.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif machine.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif machine.location == "PEQS":
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
     pdf.text(128,280,txt=machine.machine_doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=machine.machine_doc2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=machine.machine_doc3)
     
     if machine.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(waterForm, f'pdf_image_{i}')
               desc = getattr(waterForm, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=waterForm.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/mo_pdf/'
     # pdf.output(file_path + machine.lab_report_no +'.pdf')

     # pdf = open(file_path + machine.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={machine.lab_report_no}.pdf'
     response.write(pdf_output.getvalue())
     return response
          

def machineOilclone(request,pk):
     existing_form = MachineOilForm.objects.get(id=pk)
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
     return render(request,"machineOilClone.html",context)

def machineOilcloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = MachineOilForm.objects.get(id=pk)
     except MachineOilForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['machine_lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['machine_invoice_no']
          existing_Form.reporting_date = request.POST['machine_rep_date']
          existing_Form.report_to = request.POST['machine_report_to']
          existing_Form.address = request.POST['machine_address']
          existing_Form.attention = request.POST['machine_attention']
          existing_Form.email = request.POST['machine_email']
          existing_Form.sample_id = request.POST['machine_sampleId']
          existing_Form.machine_sample_col_date = request.POST['machine_sample_col_date']
          existing_Form.machine_sample_desc = request.POST['machine_sample_desc']
          existing_Form.machine_sample_type = request.POST['machine_sample_type']
          existing_Form.machine_sample_col_by = request.POST['machine_sample_col_by']
          existing_Form.machine_test_desc = request.POST['machine_test_desc']
          existing_Form.machine_sr1 = request.POST['machine_sr1']
          existing_Form.machine_sr2 = request.POST['machine_sr2']
          existing_Form.machine_sr3 = request.POST['machine_sr3']
          existing_Form.machine_sr4 = request.POST['machine_sr4']
          existing_Form.machine_sr5 = request.POST['machine_sr5']
          existing_Form.machine_sr6 = request.POST['machine_sr6']
          existing_Form.machine_sr7 = request.POST['machine_sr7']
          existing_Form.machine_sr8 = request.POST['machine_sr8']
          existing_Form.machine_sr9 = request.POST['machine_sr9']
          existing_Form.machine_sr10 = request.POST['machine_sr10']
          existing_Form.machine_sr11 = request.POST['machine_sr11']
          existing_Form.machine_sr12 = request.POST['machine_sr12']
          existing_Form.machine_sr13 = request.POST['machine_sr13']
          existing_Form.machine_sr14 = request.POST['machine_sr14']
          existing_Form.machine_sr15 = request.POST['machine_sr15']
          existing_Form.machine_sr16 = request.POST['machine_sr16']
          existing_Form.machine_legend_1 = request.POST['machine_legend-1']
          existing_Form.machine_legend_2 = request.POST['machine_legend-2']
          existing_Form.custom_legend = request.POST['custom_legend']
          existing_Form.machine_edit_note = request.POST['machine_edit_note']
          existing_Form.machine_custom_legend = request.POST['machine_custom_legend']
          existing_Form.machine_doc1 = request.POST['machine_doc1']
          existing_Form.machine_doc2 = request.POST['machine_doc2']
          existing_Form.machine_doc3 = request.POST['machine_doc3']
          existing_Form.city_location = request.POST['city_location']
          existing_Form.created_by = request.user
          # existing_Form.machine_analyzedby = request.FILES['machine_analyzedby']
          # existing_Form.machine_reviewedby = request.FILES['machine_reviewedby']
          # existing_Form.machine_approvedby = request.FILES['machine_approvedby']
          # existing_Form.machine_approvedby1 = request.FILES['machine_approvedby1']
          
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
          action = f'Machine Oil Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/machineOil-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='machineOilList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "machineOilClone.html")

__all__ = [
    'machineOil',
    'machineOilList',
    'machineOilDelete',
    'machineOilEdit',
    'machineOilUpdate',
    'machineOilView',
    'machineOilReportPdf',
    'machineOilReportPdf1',
    'machineOilclone',
    'machineOilcloneSave',
]
