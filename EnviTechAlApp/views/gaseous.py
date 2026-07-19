# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def gaseousEmission(request):
    if request.method == 'POST':
        location = request.POST['location']
        industry_id = request.POST.get('industry')
        industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
        city_location = request.POST['city_location']
        lab_report_no = request.POST['GasEm-lab_report_no']
        invoice_bill_no = request.POST['GasEm-invoice-bill-no']
        reporting_date = request.POST['GasEm-reporting-date']
        report_to = request.POST['GasEm-report-to']
        address = request.POST['GasEm-address']
        attention = request.POST['GasEm-attention']
        email = request.POST['GasEm-email']
        sample_id = request.POST['GasEm-test-id']
        GaseEm_test_perf_date = request.POST['GasEm-test-perf-date']
        GaseEm_test_type = request.POST['GasEm-test-type']
        GasEm_test_type_extra = request.POST['GasEm-test-type-extra']
        GaseEm_test_perf_by = request.POST['GasEm-test-perf-by']
        GasEm_test_desc = request.POST['GasEm-test-desc']
        GaseEm_types = request.POST.get('GasEm-type')
        GaseEm_select = request.POST.get('select')
        GaseEm_sr1 = request.POST['GasEm-sr1']
        GaseEm_sr2 = request.POST['GasEm-sr2']
        GaseEm_sr3 = request.POST['GasEm-sr3']
        GaseEm_sr4 = request.POST['GasEm-sr4']
        GaseEm_sr5 = request.POST['GasEm-sr5']
        GaseEm_sr6 = request.POST['GasEm-sr6']
        GaseEm_sr7 = request.POST['GasEm-sr7']
        GaseEm_sr8 = request.POST['GasEm-sr8']
        GaseEm_sr9 = request.POST['GasEm-sr9']
        GaseEm_sr10 = request.POST['GasEm-sr10']
        GaseEm_sr11 = request.POST['GasEm-sr11']
        GaseEm_sr12 = request.POST['GasEm-sr12']
        GaseEm_sr13 = request.POST['GasEm-sr13']
        GaseEm_sr14 = request.POST['GasEm-sr14']
        GaseEm_sr15 = request.POST['GasEm-sr15']
        GaseEm_sr16 = request.POST['GasEm-sr16']
        GaseEm_sr17 = request.POST['GasEm-sr17']
        GaseEm_sr18 = request.POST['GasEm-sr18']
        GaseEm_sr19 = request.POST['GasEm-sr19']
        GaseEm_sr20 = request.POST['GasEm-sr20']
        GaseEm_sr21 = request.POST['GasEm-sr21']
        GaseEm_sr22 = request.POST['GasEm-sr22']
        GaseEm_legend_1 = request.POST['GasEm-legend-1']
        GaseEm_legend_2 = request.POST['GasEm-legend-2']
        GaseEm_legend_3 = request.POST['GasEm-legend-3']
        GaseEm_legend_4 = request.POST['GasEm-legend-4']
        GaseEm_legend_5 = request.POST['GasEm-legend-5']
        GaseEm_legend_6 = request.POST['GasEm-legend-6']
        GaseEm_legend_7 = request.POST['GasEm-legend-7']
        GaseEm_legend_8 = request.POST['GasEm-legend-8']
        GaseEm_legend_9 = request.POST['GasEm-legend-9']
        GaseEm_legend_10 = request.POST['GasEm-legend-10']
        GaseEm_legend_11 = request.POST['GasEm-legend-11']
        GaseEm_edit_note = request.POST['GasEm-editnote']
        GaseEm_custom_legend = request.POST['GasEm-custom-legend']
        GaseEm_doc_con_1 = request.POST['GasEm-doc1']
        GaseEm_doc_con_2 = request.POST['GasEm-doc2']
        GaseEm_doc_con_3 = request.POST['GasEm-doc3']
     #    GaseEm_analyzed_by = request.FILES["GasEm-analyzedby" ]
     #    GaseEm_reviewd_by = request.FILES["GasEm-reviewedby" ]
     #    GaseEm_approved_by = request.FILES["GasEm-approvedby" ]
     #    GaseEm_approved_by1 = request.FILES["GasEm-approvedby1" ]
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

        gaseousForm = GaseousEmissionForm(lab_report_no = lab_report_no,invoice_bill_no = invoice_bill_no,
                                          reporting_date=reporting_date,report_to=report_to,
                                          address=address,attention=attention,email=email,GasEm_test_type_extra=GasEm_test_type_extra,
                                          sample_id=sample_id,GaseEm_test_perf_date =GaseEm_test_perf_date,GaseEm_test_type=GaseEm_test_type,GaseEm_test_perf_by=GaseEm_test_perf_by,
                                          GasEm_test_desc = GasEm_test_desc,GaseEm_types=GaseEm_types,GaseEm_select=GaseEm_select,GaseEm_sr1=GaseEm_sr1,
                                          GaseEm_sr2=GaseEm_sr2,GaseEm_sr3=GaseEm_sr3,GaseEm_sr4=GaseEm_sr4,GaseEm_sr5=GaseEm_sr5,GaseEm_sr6=GaseEm_sr6,
                                          GaseEm_sr7=GaseEm_sr7,GaseEm_sr8=GaseEm_sr8,GaseEm_sr9=GaseEm_sr9,GaseEm_sr10=GaseEm_sr10,GaseEm_sr11=GaseEm_sr11,
                                          GaseEm_sr12=GaseEm_sr12,GaseEm_sr13=GaseEm_sr13,GaseEm_sr14=GaseEm_sr14,GaseEm_sr15=GaseEm_sr15,GaseEm_sr16=GaseEm_sr16,
                                          GaseEm_sr17=GaseEm_sr17,GaseEm_sr18=GaseEm_sr18,GaseEm_sr19=GaseEm_sr19,GaseEm_sr20=GaseEm_sr20,
                                          GaseEm_sr21=GaseEm_sr21,GaseEm_sr22=GaseEm_sr22,GaseEm_legend_1=GaseEm_legend_1,GaseEm_legend_2=GaseEm_legend_2,
                                          GaseEm_legend_3=GaseEm_legend_3,GaseEm_legend_4=GaseEm_legend_4,GaseEm_legend_5=GaseEm_legend_5,
                                          GaseEm_legend_6=GaseEm_legend_6,GaseEm_legend_7=GaseEm_legend_7,GaseEm_legend_8=GaseEm_legend_8,
                                          GaseEm_legend_9=GaseEm_legend_9,GaseEm_legend_10=GaseEm_legend_10,GaseEm_legend_11=GaseEm_legend_11,
                                          GaseEm_edit_note=GaseEm_edit_note,location=location,extra_field=extra_field,
                                          GaseEm_custom_legend=GaseEm_custom_legend,GaseEm_doc_con_1=GaseEm_doc_con_1,GaseEm_doc_con_2=GaseEm_doc_con_2,
                                          GaseEm_doc_con_3=GaseEm_doc_con_3,city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,
                                          **image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
        gaseousForm.save()
        
        if customer_id:
             LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)
        user = request.user
        action = f'Gaseous Emission Form {gaseousForm.lab_report_no} created by {user.username}'
        AuditLog.objects.create(user=user, action=action, timestamp=local_date)
        messages.success(request, 'Operation was successful!')
        id = (GaseousEmissionForm.objects.last()).id
        if "submit_and_view" in request.POST:
               url = f"/GaseousForm-view-form/{str(id)}/"
               return redirect(to=url)
        if "submit_and_new" in request.POST:
               return render(request, "gaseousEmission.html")

    else:
         log = LoggingSheet.objects.all()
         log = serializers.serialize('json',log)
         context = {'log':log,'signs':signs,'industry':industries}
         return render(request,"gaseousEmission.html",context)


@login_required(login_url="/login")
def gaseousEmissionList(request):
     gaseous_Emission, _srch = _list_filter(request, GaseousEmissionForm)
     context = {'searched':_srch, 'data' : gaseous_Emission}

     return render(request,"gaseousEmissionList.html",context)




def gaseousEmissionReport(request,pk):
     try:
          gaseousReport = GaseousEmissionForm.objects.get(id=pk)
     except GaseousEmissionForm.DoesNotExist:
          raise Http404("Gaseous Emission report not found.")
          
     current_url = request.build_absolute_uri()
     
     try:
          gaseousReport.extra_field = gaseousReport.extra_field.replace("'", "\"")
          gaseousReport.extra_field = json.loads(gaseousReport.extra_field)
     except (ValueError, AttributeError):
        gaseousReport.extra_field = {}     


          # Generate a unique file name for the QR code
     qr_filename = f"qr_{gaseousReport.lab_report_no}.png"
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
          'list': gaseousReport,
          'qr': qr_relative_path,
          'logo':logo
     }

     return render(request,"gaseousEmissionReport.html",context)



def gaseousReportgeneratePDF(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_gaseousReportgeneratePDF as PDFWithPageNumbers





     gaseousForm = GaseousEmissionForm.objects.get(id=pk)
     gaseousForm.extra_field = gaseousForm.extra_field.replace("'", "\"")
     gaseousForm.extra_field = json.loads(gaseousForm.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Test Result",""],
     ]
     sr_no = 1
     if gaseousForm.GaseEm_sr1:
          a = [str(sr_no),"Smoke, Ringlemann Scale","-",gaseousForm.GaseEm_sr1,"2"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr2 and gaseousForm.GaseEm_types == 'gas_fired':
          a = [str(sr_no),"Particulate matter","mg/Nm³",gaseousForm.GaseEm_sr2,"300"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif gaseousForm.GaseEm_sr2 and gaseousForm.GaseEm_types == 'oil_fired':
          a = [str(sr_no),"Particulate matter","mg/Nm³",gaseousForm.GaseEm_sr2,"300"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif gaseousForm.GaseEm_sr2 and gaseousForm.GaseEm_types == 'coal_fired':
          a = [str(sr_no),"Particulate matter","mg/Nm³",gaseousForm.GaseEm_sr2,"500"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr3:
          a = [str(sr_no),"Carbon Monoxide (CO)","mg/Nm³",gaseousForm.GaseEm_sr3,"800"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr4:
          a = [str(sr_no),"Nitrogen Dioxide (NO₂)","mg/Nm³",gaseousForm.GaseEm_sr4,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr5:
          a = [str(sr_no),"Nitrogen Oxide (NO)","mg/Nm³",gaseousForm.GaseEm_sr5,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == 'gas_fired':
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"400"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == "oil_fired":
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"600"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     elif gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == "coal_fired":
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"1200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     if gaseousForm.GaseEm_sr7:
          a = [str(sr_no),"Oxygen (O₂)","%",gaseousForm.GaseEm_sr7,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr8:
          a = [str(sr_no),"Hydrogen Sulfide(H₂S)","mg/Nm³",gaseousForm.GaseEm_sr8,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr9:
          a = [str(sr_no),"Hydrogen Chloride","mg/Nm³",gaseousForm.GaseEm_sr9,"400"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr10:
          a = [str(sr_no),"Chlorine","mg/Nm³",gaseousForm.GaseEm_sr10,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr11:
          a = [str(sr_no),"Hydrogen Fluoride","mg/Nm³",gaseousForm.GaseEm_sr11,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr12:
          a = [str(sr_no),"Sulphur Dioxide (SO₂)","mg/Nm³",gaseousForm.GaseEm_sr12,"1700"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr13:
          a = [str(sr_no),"Mercury","mg/Nm³",gaseousForm.GaseEm_sr13,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr14:
          a = [str(sr_no),"Cadmium","mg/Nm³",gaseousForm.GaseEm_sr14,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr15:
          a = [str(sr_no),"Arsenic","mg/Nm³",gaseousForm.GaseEm_sr15,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr16:
          a = [str(sr_no),"Copper","mg/Nm³",gaseousForm.GaseEm_sr16,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr17:
          a = [str(sr_no),"Antimony","mg/Nm³",gaseousForm.GaseEm_sr17,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr18:
          a = [str(sr_no),"Zinc","mg/Nm³",gaseousForm.GaseEm_sr18,"200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr19:
          a = [str(sr_no),"Lead","mg/Nm³",gaseousForm.GaseEm_sr19,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr20:
          a = [str(sr_no),"Carbon dioxide (CO₂)","%",gaseousForm.GaseEm_sr20,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr21:
          a = [str(sr_no),"Hydrocarbon","%",gaseousForm.GaseEm_sr21,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr22:
          a = [str(sr_no),"Noise","dB",gaseousForm.GaseEm_sr22,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in gaseousForm.extra_field:
          parameters = extra_field.get("parameters")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")
               # Check if the "parameters" field is not empty before adding the row
          if parameters:
               a = [str(sr_no), parameters, unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)     


     pdf = PDFWithPageNumbers(lab_report_no=gaseousForm.lab_report_no,invoice_bill_no=gaseousForm.invoice_bill_no,reporting_date=gaseousForm.reporting_date,report_to=gaseousForm.report_to,
                              address=gaseousForm.address,attention=gaseousForm.attention,email=gaseousForm.email,sample_id=gaseousForm.sample_id,GaseEm_test_perf_date=gaseousForm.GaseEm_test_perf_date,
                              GasEm_test_desc=gaseousForm.GasEm_test_desc,GaseEm_test_type=gaseousForm.GaseEm_test_type,GaseEm_test_perf_by=gaseousForm.GaseEm_test_perf_by,
                              GaseEm_types=gaseousForm.GaseEm_types,GasEm_test_type_extra=gaseousForm.GasEm_test_type_extra,
                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True,margin=15)











     #report data table
     num_rows = 0
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows = num_rows+1
               if k == 0:
                    data_row[4] = gaseousForm.GaseEm_select + " Limits"

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)

     
     if num_rows >=18 and num_rows <=23:
          pdf.add_page()
     Table_Data1 = [
          
     ]
     if gaseousForm.GaseEm_edit_note:
          a=["Note: "+gaseousForm.GaseEm_edit_note] 
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
     if gaseousForm.GaseEm_legend_1:
          a = [gaseousForm.GaseEm_legend_1]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_2:
          a = [gaseousForm.GaseEm_legend_2]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_3:
          a = [gaseousForm.GaseEm_legend_3]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_4:
          a = [gaseousForm.GaseEm_legend_4]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_5:
          a = [gaseousForm.GaseEm_legend_5]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_6:
          a = [gaseousForm.GaseEm_legend_6]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_7:
          a = [gaseousForm.GaseEm_legend_7]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_8:
          a = [gaseousForm.GaseEm_legend_8]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_9:
          a = [gaseousForm.GaseEm_legend_9]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_10:
          a = [gaseousForm.GaseEm_legend_10]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_11:
          a = [gaseousForm.GaseEm_legend_11]
          Table_data_legend.append(a)
          

     if gaseousForm.GaseEm_custom_legend:
          a = [gaseousForm.GaseEm_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')


     if gaseousForm.analyst_signature:
         pdf.image(gaseousForm.analyst_signature.signature,30,231,20.32,20.32)
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(gaseousForm.analyst_signature.role if gaseousForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(gaseousForm.analyst_signature.role if gaseousForm.analyst_signature else '')})")
     if gaseousForm.assistant_manager_signature:
         pdf.image(gaseousForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({(gaseousForm.assistant_manager_signature.role if gaseousForm.assistant_manager_signature else '')})"),250)
     pdf.text(87.5,253,f"Reviewed By ({(gaseousForm.assistant_manager_signature.role if gaseousForm.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if gaseousForm.lab_manager_signature:
         pdf.image(gaseousForm.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(gaseousForm.lab_manager_signature.role if gaseousForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(gaseousForm.lab_manager_signature.role if gaseousForm.lab_manager_signature else '')})")


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
     
     if gaseousForm.location == "NEQS" and gaseousForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif gaseousForm.location == "NEQS" and gaseousForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 258.9, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif gaseousForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif gaseousForm.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 258.9, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
     # if gaseousForm.location == "NEQS":
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
     pdf.text(128,280,txt=gaseousForm.GaseEm_doc_con_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=gaseousForm.GaseEm_doc_con_2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,txt=gaseousForm.GaseEm_doc_con_3)

     if gaseousForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(gaseousForm, f'pdf_image_{i}')
               desc = getattr(gaseousForm, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=gaseousForm.pdf_heading,align="C")
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


     # file_path = '/home/django/EnviTechAlApp/gaseousEmission/'
     # pdf.output(file_path + gaseousForm.lab_report_no +'.pdf')
     # pdf = open(file_path + gaseousForm.lab_report_no +'.pdf', 'rb')

     # # pdf.output(gaseousForm.lab_report_no +'.pdf')

     # # pdf = open(gaseousForm.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={gaseousForm.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response
     
     
def gaseousReportgeneratePDF1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_gaseousReportgeneratePDF1 as PDFWithPageNumbers





     gaseousForm = GaseousEmissionForm.objects.get(id=pk)
     gaseousForm.extra_field = gaseousForm.extra_field.replace("'", "\"")
     gaseousForm.extra_field = json.loads(gaseousForm.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description","Unit","Test Result",""],
     ]
     sr_no = 1
     if gaseousForm.GaseEm_sr1:
          a = [str(sr_no),"Smoke, Ringlemann Scale","-",gaseousForm.GaseEm_sr1,"2"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr2:
          a = [str(sr_no),"Particulate matter","mg/Nm³",gaseousForm.GaseEm_sr2,"300"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr3:
          a = [str(sr_no),"Carbon Monoxide (CO)","mg/Nm³",gaseousForm.GaseEm_sr3,"800"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr4:
          a = [str(sr_no),"Nitrogen Dioxide (NO₂)","mg/Nm³",gaseousForm.GaseEm_sr4,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr5:
          a = [str(sr_no),"Nitrogen Oxide (NO)","mg/Nm³",gaseousForm.GaseEm_sr5,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == 'gas_fired':
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"400"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == "oil_fired":
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"600"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     elif gaseousForm.GaseEm_sr6 and gaseousForm.GaseEm_types == "coal_fired":
          a = [str(sr_no),"NOx","mg/Nm³",gaseousForm.GaseEm_sr6,"1200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     if gaseousForm.GaseEm_sr7:
          a = [str(sr_no),"Oxygen (O₂)","%",gaseousForm.GaseEm_sr7,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr8:
          a = [str(sr_no),"Hydrogen Sulfide(H₂S)","mg/Nm³",gaseousForm.GaseEm_sr8,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr9:
          a = [str(sr_no),"Hydrogen Chloride","mg/Nm³",gaseousForm.GaseEm_sr9,"400"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr10:
          a = [str(sr_no),"Chlorine","mg/Nm³",gaseousForm.GaseEm_sr10,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr11:
          a = [str(sr_no),"Hydrogen Fluoride","mg/Nm³",gaseousForm.GaseEm_sr11,"150"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr12:
          a = [str(sr_no),"Sulphur Dioxide (SO₂)","mg/Nm³",gaseousForm.GaseEm_sr12,"1700"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr13:
          a = [str(sr_no),"Mercury","mg/Nm³",gaseousForm.GaseEm_sr13,"10"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr14:
          a = [str(sr_no),"Cadmium","mg/Nm³",gaseousForm.GaseEm_sr14,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr15:
          a = [str(sr_no),"Arsenic","mg/Nm³",gaseousForm.GaseEm_sr15,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr16:
          a = [str(sr_no),"Copper","mg/Nm³",gaseousForm.GaseEm_sr16,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr17:
          a = [str(sr_no),"Antimony","mg/Nm³",gaseousForm.GaseEm_sr17,"20"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr18:
          a = [str(sr_no),"Zinc","mg/Nm³",gaseousForm.GaseEm_sr18,"200"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr19:
          a = [str(sr_no),"Lead","mg/Nm³",gaseousForm.GaseEm_sr19,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr20:
          a = [str(sr_no),"Carbon dioxide (CO₂)","%",gaseousForm.GaseEm_sr20,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr21:
          a = [str(sr_no),"Hydrocarbon","%",gaseousForm.GaseEm_sr21,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if gaseousForm.GaseEm_sr22:
          a = [str(sr_no),"Noise","dB",gaseousForm.GaseEm_sr22,"-"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in gaseousForm.extra_field:
          parameters = extra_field.get("parameters")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")
               # Check if the "parameters" field is not empty before adding the row
          if parameters:
               a = [str(sr_no), parameters, unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)     


     pdf = PDFWithPageNumbers(lab_report_no=gaseousForm.lab_report_no,invoice_bill_no=gaseousForm.invoice_bill_no,reporting_date=gaseousForm.reporting_date,report_to=gaseousForm.report_to,
                              address=gaseousForm.address,attention=gaseousForm.attention,email=gaseousForm.email,sample_id=gaseousForm.sample_id,GaseEm_test_perf_date=gaseousForm.GaseEm_test_perf_date,
                              GasEm_test_desc=gaseousForm.GasEm_test_desc,GaseEm_test_type=gaseousForm.GaseEm_test_type,GaseEm_test_perf_by=gaseousForm.GaseEm_test_perf_by,
                              GaseEm_types=gaseousForm.GaseEm_types,GasEm_test_type_extra=gaseousForm.GasEm_test_type_extra,
                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True,margin=15)











     #report data table
     num_rows = 0
     with pdf.table(col_widths=(6, 45, 30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               num_rows = num_rows+1
               if k == 0:
                    data_row[4] = gaseousForm.GaseEm_select + " Limits"

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)

     
     if num_rows >=18 and num_rows <=23:
          pdf.add_page()
     Table_Data1 = [
          
     ]
     if gaseousForm.GaseEm_edit_note:
          a=["Note: "+gaseousForm.GaseEm_edit_note] 
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
     if gaseousForm.GaseEm_legend_1:
          a = [gaseousForm.GaseEm_legend_1]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_2:
          a = [gaseousForm.GaseEm_legend_2]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_3:
          a = [gaseousForm.GaseEm_legend_3]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_4:
          a = [gaseousForm.GaseEm_legend_4]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_5:
          a = [gaseousForm.GaseEm_legend_5]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_6:
          a = [gaseousForm.GaseEm_legend_6]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_7:
          a = [gaseousForm.GaseEm_legend_7]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_8:
          a = [gaseousForm.GaseEm_legend_8]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_9:
          a = [gaseousForm.GaseEm_legend_9]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_10:
          a = [gaseousForm.GaseEm_legend_10]
          Table_data_legend.append(a)
          
     if gaseousForm.GaseEm_legend_11:
          a = [gaseousForm.GaseEm_legend_11]
          Table_data_legend.append(a)
          

     if gaseousForm.GaseEm_custom_legend:
          a = [gaseousForm.GaseEm_custom_legend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')


    


     if gaseousForm.analyst_signature:
         pdf.image(gaseousForm.analyst_signature.signature,30,231,20.32,20.32)
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(gaseousForm.analyst_signature.role if gaseousForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(gaseousForm.analyst_signature.role if gaseousForm.analyst_signature else '')})")
     if gaseousForm.assistant_manager_signature:
         pdf.image(gaseousForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({(gaseousForm.assistant_manager_signature.role if gaseousForm.assistant_manager_signature else '')})"),250)
     pdf.text(87.5,253,f"Reviewed By ({(gaseousForm.assistant_manager_signature.role if gaseousForm.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if gaseousForm.lab_manager_signature:
         pdf.image(gaseousForm.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(gaseousForm.lab_manager_signature.role if gaseousForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(gaseousForm.lab_manager_signature.role if gaseousForm.lab_manager_signature else '')})")



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
     if gaseousForm.location == "NEQS" and gaseousForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif gaseousForm.location == "NEQS" and gaseousForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
          
     elif gaseousForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif gaseousForm.location == "PEQS":
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

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=gaseousForm.GaseEm_doc_con_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=gaseousForm.GaseEm_doc_con_2)
     pdf.rect(180,277,25,5)
     pdf.text(183.5,280,txt=gaseousForm.GaseEm_doc_con_3)


     if gaseousForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(gaseousForm, f'pdf_image_{i}')
               desc = getattr(gaseousForm, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=gaseousForm.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/gae_pdf/'
     # pdf.output(file_path + gaseousForm.lab_report_no +'.pdf')

     # pdf = open(file_path + gaseousForm.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={gaseousForm.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response

def GaseousFormclone(request,pk):
     existing_form = GaseousEmissionForm.objects.get(id=pk)
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
     return render(request,"gaseousEmissionClone.html",context) 

def GaseousFormcloneSave(request,pk):         
     try:
        # Fetch the existing form instance by ID
         existing_Form = GaseousEmissionForm.objects.get(id=pk)
     except GaseousEmissionForm.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
        existing_Form.location = request.POST['location']
        industry_id = request.POST.get('industry')
        existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
        existing_Form.lab_report_no = request.POST['GasEm-lab_report_no']
        existing_Form.invoice_bill_no = request.POST['GasEm-invoice-bill-no']
        existing_Form.reporting_date = request.POST['GasEm-reporting-date']
        existing_Form.report_to = request.POST['GasEm-report-to']
        existing_Form.address = request.POST['GasEm-address']
        existing_Form.attention = request.POST['GasEm-attention']
        existing_Form.email = request.POST['GasEm-email']
        existing_Form.sample_id = request.POST['GasEm-test-id']
        existing_Form.GaseEm_test_perf_date = request.POST['GasEm-test-perf-date']
        existing_Form.GaseEm_test_type = request.POST['GasEm-test-type']
        existing_Form.GasEm_test_type_extra = request.POST['GasEm-test-type-extra']
        existing_Form.GaseEm_test_perf_by = request.POST['GasEm-test-perf-by']
        existing_Form.GasEm_test_desc = request.POST['GasEm-test-desc']
        existing_Form.GaseEm_types = request.POST.get('GasEm-type')
        existing_Form.GaseEm_select = request.POST.get('select')
        existing_Form.GaseEm_sr1 = request.POST['GasEm-sr1']
        existing_Form.GaseEm_sr2 = request.POST['GasEm-sr2']
        existing_Form.GaseEm_sr3 = request.POST['GasEm-sr3']
        existing_Form.GaseEm_sr4 = request.POST['GasEm-sr4']
        existing_Form.GaseEm_sr5 = request.POST['GasEm-sr5']
        existing_Form.GaseEm_sr6 = request.POST['GasEm-sr6']
        existing_Form.GaseEm_sr7 = request.POST['GasEm-sr7']
        existing_Form.GaseEm_sr8 = request.POST['GasEm-sr8']
        existing_Form.GaseEm_sr9 = request.POST['GasEm-sr9']
        existing_Form.GaseEm_sr10 = request.POST['GasEm-sr10']
        existing_Form.GaseEm_sr11 = request.POST['GasEm-sr11']
        existing_Form.GaseEm_sr12 = request.POST['GasEm-sr12']
        existing_Form.GaseEm_sr13 = request.POST['GasEm-sr13']
        existing_Form.GaseEm_sr14 = request.POST['GasEm-sr14']
        existing_Form.GaseEm_sr15 = request.POST['GasEm-sr15']
        existing_Form.GaseEm_sr16 = request.POST['GasEm-sr16']
        existing_Form.GaseEm_sr17 = request.POST['GasEm-sr17']
        existing_Form.GaseEm_sr18 = request.POST['GasEm-sr18']
        existing_Form.GaseEm_sr19 = request.POST['GasEm-sr19']
        existing_Form.GaseEm_sr20 = request.POST['GasEm-sr20']
        existing_Form.GaseEm_sr21 = request.POST['GasEm-sr21']
        existing_Form.GaseEm_sr22 = request.POST['GasEm-sr22']
        existing_Form.GaseEm_legend_1 = request.POST['GasEm-legend-1']
        existing_Form.GaseEm_legend_2 = request.POST['GasEm-legend-2']
        existing_Form.GaseEm_legend_3 = request.POST['GasEm-legend-3']
        existing_Form.GaseEm_legend_4 = request.POST['GasEm-legend-4']
        existing_Form.GaseEm_legend_5 = request.POST['GasEm-legend-5']
        existing_Form.GaseEm_legend_6 = request.POST['GasEm-legend-6']
        existing_Form.GaseEm_legend_7 = request.POST['GasEm-legend-7']
        existing_Form.GaseEm_legend_8 = request.POST['GasEm-legend-8']
        existing_Form.GaseEm_legend_9 = request.POST['GasEm-legend-9']
        existing_Form.GaseEm_legend_10 = request.POST['GasEm-legend-10']
        existing_Form.GaseEm_legend_11 = request.POST['GasEm-legend-11']
        existing_Form.GaseEm_edit_note = request.POST['GasEm-editnote']
        existing_Form.GaseEm_custom_legend = request.POST['GasEm-custom-legend']
        existing_Form.GaseEm_doc_con_1 = request.POST['GasEm-doc1']
        existing_Form.GaseEm_doc_con_2 = request.POST['GasEm-doc2']
        existing_Form.GaseEm_doc_con_3 = request.POST['GasEm-doc3']
        existing_Form.created_by = request.user
     #    existing_Form.GaseEm_analyzed_by = request.FILES["GasEm-analyzedby" ]
     #    existing_Form.GaseEm_reviewd_by = request.FILES["GasEm-reviewedby" ]
     #    existing_Form.GaseEm_approved_by = request.FILES["GasEm-approvedby" ]
     #    existing_Form.GaseEm_approved_by1 = request.FILES["GasEm-approvedby1"]
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
          
        existing_Form.extra_field = json.dumps(existing_Form.extra_field)
        
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
        action = f'Gaseous Emission Form {existing_Form.lab_report_no} cloned by {user.username}'
        AuditLog.objects.create(user=user, action=action, timestamp=local_date)
        messages.success(request, 'Operation was successful!')
        id = existing_Form.id
        if "submit_and_view" in request.POST:
            url = f"/GaseousForm-view-form/{str(id)}/"
            return redirect(to=url)
          
        if "submit" in request.POST:
               # context = {'list': new_dw}
            return redirect(to='gaseousEmissionList')
        else:
            return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "gaseousEmissionClone.html")

__all__ = [
    'gaseousEmission',
    'gaseousEmissionList',
    'gaseousEmissionReport',
    'gaseousReportgeneratePDF',
    'gaseousReportgeneratePDF1',
    'GaseousFormclone',
    'GaseousFormcloneSave',
]
