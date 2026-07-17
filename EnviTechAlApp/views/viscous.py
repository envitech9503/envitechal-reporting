# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def viscousLiquid(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['lab_rep_no']
          invoice_bill_no = request.POST['invoice_no']
          reporting_date = request.POST['report_date']
          report_to = request.POST['report_to']
          address = request.POST['address']
          attention = request.POST['Attention']
          email = request.POST['Email']
          sample_id = request.POST['sampleId']
          sample_Col_date = request.POST['sample_Col_date']
          sample_Desc = request.POST['sample_Desc']
          sample_type = request.POST['sample_type']
          sample_col_by = request.POST['sample_col_by']
          date_of_analysis_from = request.POST['date_of_analysis_from']
          date_of_analysis_to = request.POST['date_of_analysis_To']
          test_desc = request.POST['test_desc']
          viscous_select = request.POST.get('select')
          sr1 = request.POST['sr1']
          legend_1 = request.POST['legend_1']
          legend_2 = request.POST['legend_2']
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
          
          viscousForm = ViscousLiquid(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,report_to=report_to,
                                      address=address,attention=attention,email=email,sample_id=sample_id,sample_Col_date=sample_Col_date,
                                      sample_Desc=sample_Desc,sample_type=sample_type,sample_col_by=sample_col_by,date_of_analysis_from=date_of_analysis_from,
                                      date_of_analysis_to=date_of_analysis_to,test_desc=test_desc,viscous_select=viscous_select,sr1=sr1,legend_1=legend_1,legend_2=legend_2,
                                      edit_note=edit_note,custom_legend=custom_legend,doc1=doc1,location=location,city_location=city_location,
                                      doc2=doc2,doc3=doc3,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                      lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          
          viscousForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Viscous Liquid Form {viscousForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (ViscousLiquid.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/viscousLiquid-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="viscousLiquid")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
     return render(request,"viscousLiquid.html",context)


@login_required(login_url="/login")
def viscousLiquidList(request):
     vL, _srch = _list_filter(request, ViscousLiquid)
     context = {'searched':_srch, 'data':vL}
     return render(request,"viscousLiquidList.html",context)


@login_required(login_url="/login")
def viscousLiquidDelete(request,pk):
     vl = ViscousLiquid.objects.get(id=pk)
     vl.delete()
     user = request.user
     action = f'Viscous Liquid Form {vl.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("viscousLiquidList")


@login_required(login_url="/login")
def viscousLiquidEdit(request,pk):
     vL = ViscousLiquid.objects.get(id=pk)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(vL, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     context = {'data':vL,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"viscousLiquidEdit.html",context)


@login_required(login_url="/login")
def viscousLiquidUpdate(request,pk):
     vL = ViscousLiquid.objects.get(id=pk)
     if request.method == 'POST':
          vL.location = request.POST['location']
          industry_id = request.POST.get('industry')
          vL.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          vL.lab_report_no = request.POST['lab_rep_no']
          vL.invoice_bill_no = request.POST['invoice_no']
          vL.reporting_date = request.POST['report_date']
          vL.report_to = request.POST['report_to']
          vL.address = request.POST['address']
          vL.attention = request.POST['Attention']
          vL.email = request.POST['Email']
          vL.sample_id = request.POST['sampleId']
          vL.sample_Col_date = request.POST['sample_Col_date']
          vL.sample_Desc = request.POST['sample_Desc']
          vL.sample_type = request.POST['sample_type']
          vL.sample_col_by = request.POST['sample_col_by']
          vL.date_of_analysis_from = request.POST['date_of_analysis_from']
          vL.date_of_analysis_to = request.POST['date_of_analysis_To']
          vL.test_desc = request.POST['test_desc']
          vL.viscous_select = request.POST.get('select')
          vL.sr1 = request.POST['sr1']
          vL.legend_1 = request.POST['legend_1']
          vL.legend_2 = request.POST['legend_2']
          vL.edit_note = request.POST['edit_note']
          vL.custom_legend = request.POST['custom_legend']
          vL.doc1 = request.POST['doc1']
          vL.doc2 = request.POST['doc2']
          vL.doc3 = request.POST['doc3']
          vL.created_by = request.user
          # vL.analyzedby = request.FILES['analyzedby']
          # vL.reviewedby = request.FILES['reviewedby']
          # vL.approvedby = request.FILES['approvedby']
          # vL.approvedby1 = request.FILES['approvedby1']
          vL.city_location = request.POST['city_location']
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          vL.analyst_signature = analyst_sign
          vL.assistant_manager_signature = review_sign
          vL.lab_manager_signature = approved_sign
          
          vL.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(vL, image_key, '')
                    setattr(vL, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(vL, image_key, base64_encoded)
                         setattr(vL, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(vL, desc_key, description)

          vL.save()
          user = request.user
          action = f'Viscous Liquid Form {vL.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = vL.id
          if "submit_and_view" in request.POST:
               url = f"/viscousLiquid-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="viscousLiquidList")
     return render(request,"viscousLiquidList.html")



def viscousLiquidview(request,pk):
     vL =ViscousLiquid.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{vL.lab_report_no}.png"
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
     context = {'data':vL,'qr':qr_relative_path,'logo':logo}

     return render(request,'viscousLiquidView.html',context)



def viscousLiquidPdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_viscousLiquidPdf as PDFWithPageNumbers




     vL = ViscousLiquid.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result"],
     ]
     sr_no = 1
     if vL.sr1 and vL.viscous_select =="ASTM":
          a = [str(sr_no),"Oil & Grease","ASTM D-3921","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif vL.sr1 and vL.viscous_select =="USEPA":
          a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif vL.sr1 and vL.viscous_select =="APHA":
          a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)








     pdf = PDFWithPageNumbers(lab_report_no=vL.lab_report_no,invoice_bill_no=vL.invoice_bill_no,reporting_date=vL.reporting_date,report_to=vL.report_to,
                              address=vL.address,attention=vL.attention,email=vL.email,sample_id=vL.sample_id,sample_Col_date=vL.sample_Col_date,
                              sample_Desc=vL.sample_Desc,sample_type=vL.sample_type,sample_col_by=vL.sample_col_by,test_desc = vL.test_desc,
                              date_of_analysis_from=vL.date_of_analysis_from,date_of_analysis_to=vL.date_of_analysis_to

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
     with pdf.table(col_widths=(10, 50, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = vL.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if vL.edit_note:
          a=["Note: "+vL.edit_note] 
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
     if vL.legend_1:
          a = [vL.legend_1]
          Table_data_legend.append(a)
          
     if vL.legend_2:
          a = [vL.legend_2]
          Table_data_legend.append(a)

     if vL.custom_legend:
          a = [vL.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     # if vL.edit_note:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,140,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(137.8)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=vL.edit_note)
     # line_height = 4
     # y = 150
     # if vL.legend_1:
     #      pdf.text(10,y,txt=vL.legend_1)
     #      y = y+line_height
     # if vL.legend_2:
     #      pdf.text(10,y,txt=vL.legend_2)
     #      y = y+line_height

     # if vL.custom_legend:
     #      pdf.text(10,y,txt=vL.custom_legend)
     #      y = y+line_height


     # pdf.image(vL.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(vL.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(vL.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     
     if vL.analyst_signature:
         pdf.image(vL.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(vL.analyst_signature.role if vL.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(vL.analyst_signature.role if vL.analyst_signature else '')})")
     if vL.assistant_manager_signature:
         pdf.image(vL.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(vL.assistant_manager_signature.role if vL.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(vL.assistant_manager_signature.role if vL.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if vL.lab_manager_signature:
         pdf.image(vL.lab_manager_signature.signature,178,239,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(vL.lab_manager_signature.role if vL.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(vL.lab_manager_signature.role if vL.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,261,-10+pdf.w,261)
     pdf.set_font("Calibri","", 8)
     pdf.text(10,270,txt="• Report is valid for current batch (sample).")
     pdf.text(10,273.5,txt="• This report is not valid for any publication or judical purpose.")
     pdf.set_y(274.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(278)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,264,19,15)
     # if vL.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if vL.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if vL.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if vL.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(183,281,txt="(Certificate # 080177424-EMS)")
     
     
     if vL.location == "NEQS" and vL.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vL.location == "NEQS" and vL.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif vL.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vL.location == "PEQS":
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
     pdf.text(128,285,txt=vL.doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=vL.doc2)
     pdf.rect(180,282,25,5)
     pdf.text(183.5,285,txt=vL.doc3)
     
     if vL.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(vL, f'pdf_image_{i}')
               desc = getattr(vL, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=vL.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/viscousLiquid/'
     # pdf.output(file_path + vL.lab_report_no +'.pdf')
     # pdf = open(file_path + vL.lab_report_no +'.pdf', 'rb')

     # response = FileResponse(pdf)
     # return response
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={vL.lab_report_no}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response


def viscousLiquidPdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_viscousLiquidPdf1 as PDFWithPageNumbers




     vL = ViscousLiquid.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Methods","Unit","Result"],
     ]
     sr_no = 1
     if vL.sr1 and vL.viscous_select =="ASTM":
          a = [str(sr_no),"Oil & Grease","ASTM D-3921","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif vL.sr1 and vL.viscous_select =="USEPA":
          a = [str(sr_no),"Oil & Grease","USEPA 1664","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif vL.sr1 and vL.viscous_select =="APHA":
          a = [str(sr_no),"Oil & Grease","APHA 5220-B","mg/L",vL.sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)








     pdf = PDFWithPageNumbers(lab_report_no=vL.lab_report_no,invoice_bill_no=vL.invoice_bill_no,reporting_date=vL.reporting_date,report_to=vL.report_to,
                              address=vL.address,attention=vL.attention,email=vL.email,sample_id=vL.sample_id,sample_Col_date=vL.sample_Col_date,
                              sample_Desc=vL.sample_Desc,sample_type=vL.sample_type,sample_col_by=vL.sample_col_by,test_desc = vL.test_desc,
                              date_of_analysis_from=vL.date_of_analysis_from,date_of_analysis_to=vL.date_of_analysis_to

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
     with pdf.table(col_widths=(10, 50, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = vL.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if vL.edit_note:
          a=["Note: "+vL.edit_note] 
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
     if vL.legend_1:
          a = [vL.legend_1]
          Table_data_legend.append(a)
          
     if vL.legend_2:
          a = [vL.legend_2]
          Table_data_legend.append(a)

     if vL.custom_legend:
          a = [vL.custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     # if vL.edit_note:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,140,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(137.8)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=vL.edit_note)
     # line_height = 4
     # y = 150
     # if vL.legend_1:
     #      pdf.text(10,y,txt=vL.legend_1)
     #      y = y+line_height
     # if vL.legend_2:
     #      pdf.text(10,y,txt=vL.legend_2)
     #      y = y+line_height

     # if vL.custom_legend:
     #      pdf.text(10,y,txt=vL.custom_legend)
     #      y = y+line_height


     # pdf.image(vL.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(vL.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(vL.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     
     if vL.analyst_signature:
         pdf.image(vL.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(vL.analyst_signature.role if vL.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(vL.analyst_signature.role if vL.analyst_signature else '')})")
     if vL.assistant_manager_signature:
         pdf.image(vL.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(vL.assistant_manager_signature.role if vL.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(vL.assistant_manager_signature.role if vL.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if vL.lab_manager_signature:
         pdf.image(vL.lab_manager_signature.signature,178,239,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(vL.lab_manager_signature.role if vL.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(vL.lab_manager_signature.role if vL.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,261,-10+pdf.w,261)
     pdf.set_font("Calibri","", 8)
     pdf.text(10,270,txt="• Report is valid for current batch (sample).")
     pdf.text(10,273.5,txt="• This report is not valid for any publication or judical purpose.")
     pdf.set_y(274.4)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Envi Tech AL is not responsible for the sample identification and data shared by the client.")
     pdf.set_y(278)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• The sample shall be discarded after five working days unless otherwise instructed.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,264,19,15)
     # if vL.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if vL.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if vL.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if vL.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(183,281,txt="(Certificate # 080177424-EMS)")
     
     
     if vL.location == "NEQS" and vL.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vL.location == "NEQS" and vL.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif vL.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif vL.location == "PEQS":
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
     pdf.text(128,285,txt=vL.doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=vL.doc2)
     pdf.rect(180,282,25,5)
     pdf.text(183.5,285,txt=vL.doc3)
     
     if vL.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(vL, f'pdf_image_{i}')
               desc = getattr(vL, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=vL.pdf_heading,align="C")
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


     # file_path = '/home/django/EnviTechAlApp/vl_pdf/'
     # pdf.output(file_path + vL.lab_report_no +'.pdf')

     # pdf = open(file_path + vL.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={vL.lab_report_no}.pdf'
     response.write(pdf_output.getvalue())
     return response


def viscousLiquidclone(request,pk):
     existing_form = ViscousLiquid.objects.get(id=pk)
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
     return render(request,"viscousLiquidClone.html",context)

def viscousLiquidcloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = ViscousLiquid.objects.get(id=pk)
     except ViscousLiquid.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['invoice_no']
          existing_Form.reporting_date = request.POST['report_date']
          existing_Form.report_to = request.POST['report_to']
          existing_Form.address = request.POST['address']
          existing_Form.attention = request.POST['Attention']
          existing_Form.email = request.POST['Email']
          existing_Form.sample_id = request.POST['sampleId']
          existing_Form.sample_Col_date = request.POST['sample_Col_date']
          existing_Form.sample_Desc = request.POST['sample_Desc']
          existing_Form.sample_type = request.POST['sample_type']
          existing_Form.sample_col_by = request.POST['sample_col_by']
          existing_Form.date_of_analysis_from = request.POST['date_of_analysis_from']
          existing_Form.date_of_analysis_to = request.POST['date_of_analysis_To']
          existing_Form.test_desc = request.POST['test_desc']
          existing_Form.viscous_select = request.POST.get('select')
          existing_Form.sr1 = request.POST['sr1']
          existing_Form.legend_1 = request.POST['legend_1']
          existing_Form.legend_2 = request.POST['legend_2']
          existing_Form.edit_note = request.POST['edit_note']
          existing_Form.custom_legend = request.POST['custom_legend']
          existing_Form.doc1 = request.POST['doc1']
          existing_Form.doc2 = request.POST['doc2']
          existing_Form.created_by = request.user
          # existing_Form.analyzedby = request.FILES['analyzedby']
          # existing_Form.reviewedby = request.FILES['reviewedby']
          # existing_Form.approvedby = request.FILES['approvedby']
          # existing_Form.approvedby1 = request.FILES['approvedby1']
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
          action = f'Viscous Liquid Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/viscousLiquid-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='viscousLiquidList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "viscousLiquidClone.html")

__all__ = [
    'viscousLiquid',
    'viscousLiquidList',
    'viscousLiquidDelete',
    'viscousLiquidEdit',
    'viscousLiquidUpdate',
    'viscousLiquidview',
    'viscousLiquidPdf',
    'viscousLiquidPdf1',
    'viscousLiquidclone',
    'viscousLiquidcloneSave',
]
