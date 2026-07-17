# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def packingPoly(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['pack_lab_rep_no']
          invoice_bill_no = request.POST['pack_invoice']
          reporting_date = request.POST['pack_rep_date']
          report_to = request.POST['pack_rep_to']
          address = request.POST['pack_address']
          attention = request.POST['pack_attention']
          email = request.POST['pack_email']
          sample_id = request.POST['pack_sampleId']
          pack_sample_colc_date = request.POST['pack_sample_colc_date']
          pack_sample_desc = request.POST['pack_sample_desc']
          pack_sample_type = request.POST['pack_sample_type']
          pack_sample_colc_by = request.POST['pack_sample_colc_by']
          pack_test_desc = request.POST['pack_test_desc']
          pack_sr1 = request.POST['pack_sr1']
          pack_legend_1 = request.POST['pack-legend-1']
          pack_edit_note = request.POST['pack_edit_note']
          pack_custom_legend = request.POST['pack_custom_legend']
          doc_con1 = request.POST['doc_con1']
          doc_con2 = request.POST['doc_con2']
          doc_con3 = request.POST['doc_con3']
          # pack_analyzed_by = request.FILES['pack-analyzedby']
          # pack_reviewed_by = request.FILES['pack-reviewedby']
          # pack_approved_by = request.FILES['pack-approvedby']
          # pack_approved_by1 = request.FILES['pack-approvedby1']
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

          packingForm = PackingPolyBagForm(lab_report_no = lab_report_no ,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,
                                        report_to=report_to,address=address,attention=attention,email=email,
                                        sample_id=sample_id,pack_sample_colc_date=pack_sample_colc_date,pack_sample_desc=pack_sample_desc,location=location,
                                        pack_sample_type=pack_sample_type,pack_sample_colc_by=pack_sample_colc_by,pack_test_desc=
                                        pack_test_desc,pack_sr1=pack_sr1,pack_legend_1=pack_legend_1,pack_edit_note=pack_edit_note,pack_custom_legend=pack_custom_legend,doc_con1=doc_con1,doc_con2=doc_con2,doc_con3=doc_con3,
                                        city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                        lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          packingForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Packing Poly Bag Form {packingForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (PackingPolyBagForm.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/packingpolybag-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="packingPolyBag")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"packingPolyBag.html",context)

@login_required(login_url="/login")
def packingPolyBagList(request):
     ppb, _srch = _list_filter(request, PackingPolyBagForm)
     context ={'searched':_srch, 'data':ppb}
     return render(request,"packingPolyBagList.html",context)

@login_required(login_url="/login")
def  packingPolyBagDelete(request,pk):
     ppb = PackingPolyBagForm.objects.get(id=pk)
     ppb.delete()
     user = request.user
     action = f'Packing Poly Bag Form {ppb.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect(to="packingPolyBagList")

@login_required(login_url="/login")
def packingPolyBagEdit(request,pk):
     ppb = PackingPolyBagForm.objects.get(id=pk)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(ppb, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {"data":ppb,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"packingPolyBagEdit.html",context)

@login_required(login_url="/login")
def packingPolyBagUpdate(request,pk):
     ppb = PackingPolyBagForm.objects.get(id=pk)
     if request.method == 'POST':
          ppb.location = request.POST['location']
          industry_id = request.POST.get('industry')
          ppb.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          ppb.lab_report_no = request.POST['pack_lab_rep_no']
          ppb.invoice_bill_no = request.POST['pack_invoice']
          ppb.reporting_date = request.POST['pack_rep_date']
          ppb.report_to = request.POST['pack_rep_to']
          ppb.address = request.POST['pack_address']
          ppb.attention = request.POST['pack_attention']
          ppb.email = request.POST['pack_email']
          ppb.sample_id = request.POST['pack_sampleId']
          ppb.pack_sample_colc_date = request.POST['pack_sample_colc_date']
          ppb.pack_sample_desc = request.POST['pack_sample_desc']
          ppb.pack_sample_type = request.POST['pack_sample_type']
          ppb.pack_sample_colc_by = request.POST['pack_sample_colc_by']
          ppb.pack_test_desc = request.POST['pack_test_desc']
          ppb.pack_sr1 = request.POST['pack_sr1']
          ppb.pack_legend_1 = request.POST['pack-legend-1']
          ppb.pack_edit_note = request.POST['pack_edit_note']
          ppb.pack_custom_legend = request.POST['pack_custom_legend']
          ppb.doc_con1 = request.POST['doc_con1']
          ppb.doc_con2 = request.POST['doc_con2']
          ppb.doc_con3 = request.POST['doc_con3']
          ppb.created_by = request.user
          # ppb.pack_analyzed_by = request.FILES['pack-analyzedby']
          # ppb.pack_reviewed_by = request.FILES['pack-reviewedby']
          # ppb.pack_approved_by = request.FILES['pack-approvedby']
          # ppb.pack_approved_by1 = request.FILES['pack-approvedby1']
          ppb.city_location = request.POST['city_location']
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          ppb.analyst_signature = analyst_sign
          ppb.assistant_manager_signature = review_sign
          ppb.lab_manager_signature = approved_sign
          
          ppb.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(ppb, image_key, '')
                    setattr(ppb, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(ppb, image_key, base64_encoded)
                         setattr(ppb, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(ppb, desc_key, description)
          
          
          ppb.save()
          user = request.user
          action = f'Packing Poly Bag Form {ppb.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = ppb.id
          if "submit_and_view" in request.POST:
               url = f'/packingpolybag-view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('packingPolyBagList')
     return render(request,"packingPolyBagList.html")
     



def packingPolyBagView(request,pk):
     ppb = PackingPolyBagForm.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{ppb.lab_report_no}.png"
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
     context = {'data':ppb,'qr':qr_relative_path,'logo':logo}

     return render(request,'packingPolyBagReport.html',context)



def packingPolyBagReport(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_packingPolyBagReport as PDFWithPageNumbers




     pack = PackingPolyBagForm.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Units","Methods","Results"],
     ]
     sr_no = 1
     if pack.pack_sr1:
          a = [str(sr_no),"PVC Content","-","Beilstein",pack.pack_sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)



     pdf = PDFWithPageNumbers(lab_report_no=pack.lab_report_no,invoice_bill_no=pack.invoice_bill_no,reporting_date=pack.reporting_date,report_to=pack.report_to,
                              address=pack.address,attention=pack.attention,email=pack.email,sample_id=pack.sample_id,pack_sample_colc_date=pack.pack_sample_colc_date,
                              pack_test_desc=pack.pack_test_desc,pack_sample_type=pack.pack_sample_type,pack_sample_colc_by=pack.pack_sample_colc_by,pack_sample_desc=pack.pack_sample_desc

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
               #      data_row[4] = pack.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     if pack.pack_edit_note:
          pdf.set_font("Calibri","B", 10)
          pdf.text(10,145,txt="Conclusion:")
          pdf.set_font("Calibri","", 8)
          pdf.set_y(142.5)
          pdf.set_x(27)
          pdf.multi_cell(182,txt=pack.pack_edit_note)
     line_height = 4
     y = 150
     if pack.pack_legend_1:
          pdf.text(10,y,txt=pack.pack_legend_1)
          y = y+line_height
     if pack.pack_custom_legend:
          pdf.text(10,y,txt=pack.pack_custom_legend)
          y = y+line_height


     # pdf.image(pack.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(pack.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(pack.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     if pack.analyst_signature:
         pdf.image(pack.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(pack.analyst_signature.role if pack.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(pack.analyst_signature.role if pack.analyst_signature else '')})")
     if pack.assistant_manager_signature:
         pdf.image(pack.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(pack.assistant_manager_signature.role if pack.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(pack.assistant_manager_signature.role if pack.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if pack.lab_manager_signature:
         pdf.image(pack.lab_manager_signature.signature,178,239,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(pack.lab_manager_signature.role if pack.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(pack.lab_manager_signature.role if pack.lab_manager_signature else '')})")
     


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
     # if pack.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if pack.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if pack.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if pack.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     
     if pack.location == "NEQS" and pack.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif pack.location == "NEQS" and pack.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif pack.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif pack.location == "PEQS":
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
     pdf.text(128,285,txt=pack.doc_con1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=pack.doc_con2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=pack.doc_con3)

     
     if pack.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(pack, f'pdf_image_{i}')
               desc = getattr(pack, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=pack.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/polyBag/'
     # pdf.output(file_path + pack.lab_report_no +'.pdf')
     # pdf = open(file_path + pack.lab_report_no +'.pdf', 'rb')

     # # pdf.output(pack.lab_report_no +'.pdf')

     # # pdf = open(pack.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response   
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={pack.lab_report_no}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response


def packingPolyBagReport1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_packingPolyBagReport1 as PDFWithPageNumbers




     pack = PackingPolyBagForm.objects.get(id=pk)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Units","Methods","Results"],
     ]
     sr_no = 1
     if pack.pack_sr1:
          a = [str(sr_no),"PVC Content","-","Beilstein",pack.pack_sr1]
          sr_no = sr_no+1
          TABLE_DATA.append(a)



     pdf = PDFWithPageNumbers(lab_report_no=pack.lab_report_no,invoice_bill_no=pack.invoice_bill_no,reporting_date=pack.reporting_date,report_to=pack.report_to,
                              address=pack.address,attention=pack.attention,email=pack.email,sample_id=pack.sample_id,pack_sample_colc_date=pack.pack_sample_colc_date,
                              pack_test_desc=pack.pack_test_desc,pack_sample_type=pack.pack_sample_type,pack_sample_colc_by=pack.pack_sample_colc_by,pack_sample_desc=pack.pack_sample_desc

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
               #      data_row[4] = pack.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table

     if pack.pack_edit_note:
          pdf.set_font("Calibri","B", 10)
          pdf.text(10,150,txt="Conclusion:")
          pdf.set_font("Calibri","", 8)
          pdf.set_y(147.5)
          pdf.set_x(27)
          pdf.multi_cell(182,txt=pack.pack_edit_note)
     line_height = 4
     y = 155
     if pack.pack_legend_1:
          pdf.text(10,y,txt=pack.pack_legend_1)
          y = y+line_height
     if pack.pack_custom_legend:
          pdf.text(10,y,txt=pack.pack_custom_legend)
          y = y+line_height


     # pdf.image(pack.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(pack.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,229,22,22)
     # pdf.image(pack.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if pack.analyst_signature:
         pdf.image(pack.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(pack.analyst_signature.role if pack.analyst_signature else '')})"),252)
     pdf.text(26,254.5,f"Analyzed By ({(pack.analyst_signature.role if pack.analyst_signature else '')})")
     if pack.assistant_manager_signature:
         pdf.image(pack.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(pack.assistant_manager_signature.role if pack.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,254.5,f"Reviewed By ({(pack.assistant_manager_signature.role if pack.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,229,22,22)
     if pack.lab_manager_signature:
         pdf.image(pack.lab_manager_signature.signature,178,234,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(pack.lab_manager_signature.role if pack.lab_manager_signature else '')})"),252)
     pdf.text(160,254.5,f"Approved By ({(pack.lab_manager_signature.role if pack.lab_manager_signature else '')})")


     
     pdf.line(10,256,-10+pdf.w,256)
     pdf.set_font("Calibri","", 8)
     pdf.text(10,265,txt="• Report is valid for current batch (sample).")
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

     # pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,259,19,15)
     # if pack.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if pack.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if pack.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if pack.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,259,19,15)
     if pack.location == "NEQS" and pack.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif pack.location == "NEQS" and pack.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif pack.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif pack.location == "PEQS":
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
     pdf.text(128,280,txt=pack.doc_con1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=pack.doc_con2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=pack.doc_con3)

     
     if pack.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(pack, f'pdf_image_{i}')
               desc = getattr(pack, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=pack.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/pp_pdf/'
     # pdf.output(file_path + pack.lab_report_no +'.pdf')

     # pdf = open(file_path + pack.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={pack.lab_report_no}.pdf'
     response.write(pdf_output.getvalue())
     return response
          

def packingPolyclone(request,pk):
     existing_form = PackingPolyBagForm.objects.get(id=pk)
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
     return render(request,"packingPolyClone.html",context)

def packingPolycloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = PackingPolyBagForm.objects.get(id=pk)
     except PackingPolyBagForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['pack_lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['pack_invoice']
          existing_Form.reporting_date = request.POST['pack_rep_date']
          existing_Form.report_to = request.POST['pack_rep_to']
          existing_Form.address = request.POST['pack_address']
          existing_Form.attention = request.POST['pack_attention']
          existing_Form.email = request.POST['pack_email']
          existing_Form.sample_id = request.POST['pack_sampleId']
          existing_Form.pack_sample_colc_date = request.POST['pack_sample_colc_date']
          existing_Form.pack_sample_desc = request.POST['pack_sample_desc']
          existing_Form.pack_sample_type = request.POST['pack_sample_type']
          existing_Form.pack_sample_colc_by = request.POST['pack_sample_colc_by']
          existing_Form.pack_test_desc = request.POST['pack_test_desc']
          existing_Form.pack_sr1 = request.POST['pack_sr1']
          existing_Form.pack_legend_1 = request.POST['pack-legend-1']
          existing_Form.pack_edit_note = request.POST['pack_edit_note']
          existing_Form.pack_custom_legend = request.POST['pack_custom_legend']
          existing_Form.doc_con1 = request.POST['doc_con1']
          existing_Form.doc_con2 = request.POST['doc_con2']
          existing_Form.doc_con3 = request.POST['doc_con3']
          existing_Form.created_by = request.user
          # existing_Form.pack_analyzed_by = request.FILES['pack-analyzedby']
          # existing_Form.pack_reviewed_by = request.FILES['pack-reviewedby']
          # existing_Form.pack_approved_by = request.FILES['pack-approvedby']
          # existing_Form.pack_approved_by1 = request.FILES['pack-approvedby1']
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
          action = f'Packing Poly Bag Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/packingpolybag-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='packingPolyBagList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "packingPolyClone.html")

__all__ = [
    'packingPoly',
    'packingPolyBagList',
    'packingPolyBagDelete',
    'packingPolyBagEdit',
    'packingPolyBagUpdate',
    'packingPolyBagView',
    'packingPolyBagReport',
    'packingPolyBagReport1',
    'packingPolyclone',
    'packingPolycloneSave',
]
