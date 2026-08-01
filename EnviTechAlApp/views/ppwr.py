# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403

def _safe_json_list(_v):
    import json as _json, ast as _ast
    if isinstance(_v, (list, dict)): return _v
    if not _v: return []
    try: return _json.loads(_v)
    except Exception:
        try: return _ast.literal_eval(_v)
        except Exception:
            try: return _json.loads(_v.replace("'", '"'))
            except Exception: return []




@login_required(login_url="/login")
def ppwrAnalysis(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['ppwr_lab_report_no']
          invoice_bill_no = request.POST['ppwr_invoice_bill']
          reporting_date = request.POST['ppwr_rep_date']
          report_to = request.POST['ppwr_rep_to']
          address = request.POST['ppwr_address']
          attention = request.POST['ppwr_attention']
          email = request.POST['ppwr_email']
          sample_id = request.POST['ppwr_sampleId']
          ppwr_sample_col_date = request.POST['ppwr_sample_col_date']
          ppwr_sample_desc = request.POST['ppwr_sample_desc']
          ppwr_sample_type = request.POST['ppwr_sample_type']
          ppwr_sample_col_by = request.POST['ppwr_sample_col_by']
          ppwr_date_analysis_to = request.POST['ppwr_date_analysis_to']
          ppwr_date_analysis_from = request.POST['ppwr_date_analysis_from']
          ppwr_test_desc = request.POST['ppwr_test_desc']
          ppwr_sr1 = request.POST['ppwr_sr1']
          ppwr_sr2 = request.POST['ppwr_sr2']
          ppwr_sr3 = request.POST['ppwr_sr3']
          ppwr_sr4 = request.POST['ppwr_sr4']
          ppwr_sr5 = request.POST['ppwr_sr5']
          ppwr_sr6 = request.POST['ppwr_sr6']
          ppwr_ex_1_1 = request.POST['ex_1_1']
          ppwr_ex_1_2 = request.POST['ex_1_2']
          ppwr_ex_1_3 = request.POST['ex_1_3']
          ppwr_ex_1_4 = request.POST['ex_1_4']
          ppwr_ex_1_5 = request.POST['ex_1_5']
          ppwr_ex_1_6 = request.POST['ex_1_6']
          ppwr_ex_1_7 = request.POST['ex_1_7']
          ppwr_ex_2_1 = request.POST['ex_2_1']
          ppwr_ex_2_2 = request.POST['ex_2_2']
          ppwr_ex_2_3 = request.POST['ex_2_3']
          ppwr_ex_2_4 = request.POST['ex_2_4']
          ppwr_ex_2_5 = request.POST['ex_2_5']
          ppwr_ex_2_6 = request.POST['ex_2_6']
          ppwr_ex_2_7 = request.POST['ex_2_7']
          ppwr_p1 = request.POST['p1']
          ppwr_p2 = request.POST['p2']
          ppwr_p3 = request.POST['p3']
          ppwr_p4 = request.POST['p4']
          ppwr_p5 = request.POST['p5']
          ppwr_p6 = request.POST['p6']
          ppwr_legend_1 = request.POST['ppwr_legend_1']
          ppwr_legend_2 = request.POST['ppwr_legend_2']
          ppwr_editnote = request.POST['ppwr_editnote']
          ppwr_custom_legend = request.POST['ppwr_custom_legend']
          ppwr_doc1 = request.POST['ppwr_doc1']
          ppwr_doc2 = request.POST['ppwr_doc2']
          ppwr_doc3 = request.POST['ppwr_doc3']
          unit_head = request.POST.get('unit_head')
          unit_1 = request.POST.get('unit_1')
          unit_2 = request.POST.get('unit_2')
          unit_3 = request.POST.get('unit_3')
          unit_4 = request.POST.get('unit_4')
          unit_5 = request.POST.get('unit_5')
          unit_6 = request.POST.get('unit_6')
          extra_field = request.POST['extra_field'] 
          # ppwr_analyzedby = request.FILES['ppwr_analyzedby']
          # ppwr_reviewedby = request.FILES['ppwr_reviewedby']
          # ppwr_approvedby = request.FILES['ppwr_approvedby']
          # ppwr_approvedby1 = request.FILES['ppwr_approvedby1']
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
          
          ppwrForm = PPWRAnalysis(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,
                                            report_to=report_to,address=address,attention=attention,email=email,
                                            sample_id=sample_id,ppwr_sample_col_date=ppwr_sample_col_date,ppwr_sample_desc=ppwr_sample_desc,
                                            ppwr_sample_type=ppwr_sample_type,ppwr_sample_col_by=ppwr_sample_col_by,ppwr_date_analysis_to=ppwr_date_analysis_to,
                                            ppwr_date_analysis_from=ppwr_date_analysis_from,ppwr_test_desc=ppwr_test_desc,ppwr_sr1=ppwr_sr1,ppwr_sr2=ppwr_sr2,ppwr_sr3=ppwr_sr3,ppwr_sr4=ppwr_sr4,
                                            ppwr_sr5=ppwr_sr5,ppwr_sr6=ppwr_sr6,ppwr_legend_1=ppwr_legend_1,ppwr_legend_2=ppwr_legend_2,location=location,
                                            ppwr_editnote=ppwr_editnote,ppwr_custom_legend=ppwr_custom_legend,ppwr_doc1=ppwr_doc1,ppwr_doc2=ppwr_doc2,ppwr_doc3=ppwr_doc3,
                                            
                                            ppwr_ex_1_1=ppwr_ex_1_1,ppwr_ex_1_2=ppwr_ex_1_2,ppwr_ex_1_3=ppwr_ex_1_3,ppwr_ex_1_4=ppwr_ex_1_4,ppwr_ex_1_5=ppwr_ex_1_5,ppwr_ex_1_6=ppwr_ex_1_6,ppwr_ex_1_7=ppwr_ex_1_7,
                                            ppwr_ex_2_1=ppwr_ex_2_1,ppwr_ex_2_2=ppwr_ex_2_2,ppwr_ex_2_3=ppwr_ex_2_3,ppwr_ex_2_4=ppwr_ex_2_4,ppwr_ex_2_5=ppwr_ex_2_5,ppwr_ex_2_6=ppwr_ex_2_6,ppwr_ex_2_7=ppwr_ex_2_7,
                                            ppwr_p1=ppwr_p1,ppwr_p2=ppwr_p2,ppwr_p3=ppwr_p3,ppwr_p4=ppwr_p4,ppwr_p5=ppwr_p5,ppwr_p6=ppwr_p6,
                                            city_location=city_location,customer_id=customer_id,analyst_signature=analyst_sign,assistant_manager_signature=review_sign,
                                            lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry,unit_head=unit_head,unit_1=unit_1,unit_2=unit_2,unit_3=unit_3,unit_4=unit_4,unit_5=unit_5,unit_6=unit_6,extra_field=extra_field)
          ppwrForm.ppwr_legend_3 = request.POST.get('ppwr_legend_3')
          ppwrForm.ppwr_legend_4 = request.POST.get('ppwr_legend_4')
          ppwrForm.ppwr_legend_5 = request.POST.get('ppwr_legend_5')
          ppwrForm.save()
          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'PPWR Form {ppwrForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=now_pk_str())
          messages.success(request, 'Operation was successful!')
          id = (PPWRAnalysis.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/ppwr-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="ppwrAnalysis")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
     return render(request,"ppwrAnalysis.html",context)


@login_required(login_url="/login")
def ppwrList(request):
     mba, _srch = _list_filter(request, PPWRAnalysis)
     context ={'searched':_srch, "data":mba}
     return render(request,"ppwrAnalysisList.html",context)

@login_required(login_url="/login")
def ppwrDelete(request,pk):
     mba = PPWRAnalysis.objects.get(id=pk)
     mba.delete()
     user = request.user
     action = f'PPWR Form {mba.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=now_pk_str())
     messages.success(request, 'Operation was successful!')
     return redirect("ppwrList")

@login_required(login_url="/login")
def ppwrEdit(request,pk):
     mba = PPWRAnalysis.objects.get(id=pk)
     mba.extra_field = _safe_json_list(mba.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(mba, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     
     context ={"data":mba,'log':log,'signs':signs,
               'pdf_image_1': image_previews.get('pdf_image_1'),
               'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"ppwrEdit.html",context)

@login_required(login_url="/login")
def ppwrUpdate(request,pk):
     mba = PPWRAnalysis.objects.get(id=pk)
     if request.method == 'POST':
          mba.location = request.POST['location']
          industry_id = request.POST.get('industry')
          if industry_id:
               mba.industry = Industry_sector.objects.get(id=industry_id)
          mba.lab_report_no = request.POST['ppwr_lab_report_no']
          mba.invoice_bill_no = request.POST['ppwr_invoice_bill']
          mba.reporting_date = request.POST['ppwr_rep_date']
          mba.report_to = request.POST['ppwr_rep_to']
          mba.address = request.POST['ppwr_address']
          mba.attention = request.POST['ppwr_attention']
          mba.email = request.POST['ppwr_email']
          mba.sample_id = request.POST['ppwr_sampleId']
          mba.ppwr_sample_col_date = request.POST['ppwr_sample_col_date']
          mba.ppwr_sample_desc = request.POST['ppwr_sample_desc']
          mba.ppwr_sample_type = request.POST['ppwr_sample_type']
          mba.ppwr_sample_col_by = request.POST['ppwr_sample_col_by']
          mba.ppwr_date_analysis_to = request.POST['ppwr_date_analysis_to']
          mba.ppwr_date_analysis_from = request.POST['ppwr_date_analysis_from']          
          mba.ppwr_test_desc = request.POST['ppwr_test_desc']
          mba.ppwr_sr1 = request.POST.get('ppwr_sr1')
          mba.ppwr_sr2 = request.POST.get('ppwr_sr2')
          mba.ppwr_sr3 = request.POST.get('ppwr_sr3')
          mba.ppwr_sr4 = request.POST.get('ppwr_sr4')
          mba.ppwr_sr5 = request.POST.get('ppwr_sr5')
          mba.ppwr_sr6 = request.POST.get('ppwr_sr6')
          mba.ppwr_ex_1_1 = request.POST.get('ex_1_1')
          mba.ppwr_ex_1_2 = request.POST.get('ex_1_2')
          mba.ppwr_ex_1_3 = request.POST.get('ex_1_3')
          mba.ppwr_ex_1_4 = request.POST.get('ex_1_4')
          mba.ppwr_ex_1_5 = request.POST.get('ex_1_5')
          mba.ppwr_ex_1_6 = request.POST.get('ex_1_6')
          mba.ppwr_ex_1_7 = request.POST.get('ex_1_7')
          mba.ppwr_ex_2_1 = request.POST.get('ex_2_1')
          mba.ppwr_ex_2_2 = request.POST.get('ex_2_2')
          mba.ppwr_ex_2_3 = request.POST.get('ex_2_3')
          mba.ppwr_ex_2_4 = request.POST.get('ex_2_4')
          mba.ppwr_ex_2_5 = request.POST.get('ex_2_5')
          mba.ppwr_ex_2_6 = request.POST.get('ex_2_6')
          mba.ppwr_ex_2_7 = request.POST.get('ex_2_7')
          mba.ppwr_p1 = request.POST.get('p1')
          mba.ppwr_p2 = request.POST.get('p2')
          mba.ppwr_p3 = request.POST.get('p3')
          mba.ppwr_p4 = request.POST.get('p4')
          mba.ppwr_p5 = request.POST.get('p5')
          mba.ppwr_p6 = request.POST.get('p6')
          mba.ppwr_legend_1 = request.POST.get('ppwr_legend_1')
          mba.ppwr_legend_2 = request.POST.get('ppwr_legend_2')
          mba.ppwr_legend_3 = request.POST.get('ppwr_legend_3')
          mba.ppwr_legend_4 = request.POST.get('ppwr_legend_4')
          mba.ppwr_legend_5 = request.POST.get('ppwr_legend_5')
          mba.ppwr_editnote = request.POST.get('ppwr_editnote')
          mba.ppwr_custom_legend = request.POST.get('ppwr_custom_legend')
          mba.ppwr_doc1 = request.POST.get('ppwr_doc1')
          mba.ppwr_doc2 = request.POST.get('ppwr_doc2')
          mba.ppwr_doc3 = request.POST.get('ppwr_doc3')
          mba.created_by = request.user
          mba.unit_head = request.POST.get('unit_head')
          mba.unit_1 = request.POST.get('unit_1')
          mba.unit_2 = request.POST.get('unit_2')
          mba.unit_3 = request.POST.get('unit_3')
          mba.unit_4 = request.POST.get('unit_4')
          mba.unit_5 = request.POST.get('unit_5')
          mba.unit_6 = request.POST.get('unit_6')
          # extra (dynamic) result rows — rebuilt from the edit form's array inputs
          _sr  = request.POST.getlist('sr[]')
          _par = request.POST.getlist('parameters[]')
          _un  = request.POST.getlist('units[]')
          _e1  = request.POST.getlist('ex_1[]')
          _res = request.POST.getlist('result[]')
          _e2  = request.POST.getlist('ex_2[]')
          _rows = []
          for _i in range(len(_sr)):
               _rows.append({
                    "sr": _sr[_i],
                    "parameters": _par[_i] if _i < len(_par) else "",
                    "units": _un[_i] if _i < len(_un) else "",
                    "ex_1": _e1[_i] if _i < len(_e1) else "",
                    "result": _res[_i] if _i < len(_res) else "",
                    "ex_2": _e2[_i] if _i < len(_e2) else "",
               })
          mba.extra_field = json.dumps(_rows)
          # mba.ppwr_analyzedby = request.FILES['ppwr_analyzedby']
          # mba.ppwr_reviewedby = request.FILES['ppwr_reviewedby']
          # mba.ppwr_approvedby = request.FILES['ppwr_approvedby']
          # mba.ppwr_approvedby1 = request.FILES['ppwr_approvedby1']
          mba.city_location = request.POST['city_location']
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          if analyst_sign:
               mba.analyst_signature = analyst_sign
          if review_sign:
               mba.assistant_manager_signature = review_sign
          if approved_sign:
               mba.lab_manager_signature = approved_sign
          
          mba.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(mba, image_key, '')
                    setattr(mba, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(mba, image_key, base64_encoded)
                         setattr(mba, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(mba, desc_key, description)

          mba.save()
          user = request.user
          action = f'PPWR Form {mba.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=now_pk_str())
          messages.success(request, 'Operation was successful!')
          id = mba.id
          if "submit_and_view" in request.POST:
               url = f"/ppwr-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="ppwrList")
     return render(request,"ppwrAnalysisList.html")



def ppwrView(request,pk):
     mba = PPWRAnalysis.objects.get(id=pk)
     mba.extra_field = _safe_json_list(mba.extra_field)
     current_url = public_verify_url(request, 'ppwr', pk)
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{mba.lab_report_no}.png"
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
     context = {'data': mba,'qr':qr_relative_path,'logo':logo}

     return render(request,'ppwrReport.html',context)



def ppwrAnalysisPdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ppwrAnalysisPdf as PDFWithPageNumbers




     ppwr = PPWRAnalysis.objects.get(id=pk)
     ppwr.extra_field = _safe_json_list(ppwr.extra_field)

     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description",ppwr.unit_head,ppwr.ppwr_ex_1_1,"Result",ppwr.ppwr_ex_2_1],
     ]
     sr_no = 1
     if ppwr.ppwr_sr1:
          a = [str(sr_no),ppwr.ppwr_p1,ppwr.unit_1,ppwr.ppwr_ex_1_2,ppwr.ppwr_sr1,ppwr.ppwr_ex_2_2]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr2:
          a = [str(sr_no),ppwr.ppwr_p2,ppwr.unit_2,ppwr.ppwr_ex_1_3,ppwr.ppwr_sr2,ppwr.ppwr_ex_2_3]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr3:
          a = [str(sr_no),ppwr.ppwr_p3,ppwr.unit_3,ppwr.ppwr_ex_1_4,ppwr.ppwr_sr3,ppwr.ppwr_ex_2_4]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr4:
          a = [str(sr_no),ppwr.ppwr_p4,ppwr.unit_4,ppwr.ppwr_ex_1_5,ppwr.ppwr_sr4,ppwr.ppwr_ex_2_5]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr5:
          a = [str(sr_no),ppwr.ppwr_p5,ppwr.unit_5,ppwr.ppwr_ex_1_6,ppwr.ppwr_sr5,ppwr.ppwr_ex_2_6]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr6:
          a = [str(sr_no),ppwr.ppwr_p6,ppwr.unit_6,ppwr.ppwr_ex_1_7,ppwr.ppwr_sr6,ppwr.ppwr_ex_2_7]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     for extra_field in ppwr.extra_field:
          parameters = extra_field.get("parameters")
          units = extra_field.get("units")
          ex_1 = extra_field.get("ex_1")
          result = extra_field.get("result")
          ex_2 = extra_field.get("ex_2")
          if parameters:
               a = [str(sr_no), parameters, units, ex_1, result, ex_2]
               sr_no += 1
               TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=ppwr.lab_report_no,invoice_bill_no=ppwr.invoice_bill_no,reporting_date=ppwr.reporting_date,report_to=ppwr.report_to,
                              address=ppwr.address,attention=ppwr.attention,email=ppwr.email,sample_id=ppwr.sample_id,ppwr_sample_col_date=ppwr.ppwr_sample_col_date,
                              ppwr_sample_desc=ppwr.ppwr_sample_desc,ppwr_sample_type=ppwr.ppwr_sample_type,ppwr_sample_col_by=ppwr.ppwr_sample_col_by,ppwr_test_desc = ppwr.ppwr_test_desc,ppwr_date_analysis_from=ppwr.ppwr_date_analysis_from,ppwr_date_analysis_to = ppwr.ppwr_date_analysis_to

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
     with pdf.table(col_widths=(10, 50, 30,30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER','CENTER')) as table:




          _mgspan = 0
          if ppwr.ppwr_sr1 and ppwr.ppwr_sr2 and ppwr.ppwr_sr3 and ppwr.ppwr_sr4:
              if ppwr.ppwr_ex_2_2 and ppwr.ppwr_ex_2_2 == ppwr.ppwr_ex_2_3 == ppwr.ppwr_ex_2_4 == ppwr.ppwr_ex_2_5:
                  _mgspan = 4
          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = ppwr.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    if _mgspan and i == 5 and k >= 1 and k <= 4:
                        if k == 1:
                            row.cell(datum, rowspan=4)
                    else:
                        row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if ppwr.ppwr_editnote:
          a=["Note: "+ppwr.ppwr_editnote] 
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
     if ppwr.ppwr_legend_1:
          a = [ppwr.ppwr_legend_1]
          Table_data_legend.append(a)
          
     if ppwr.ppwr_legend_2:
          a = [ppwr.ppwr_legend_2]
          Table_data_legend.append(a)
     if ppwr.ppwr_legend_3:
          a = [ppwr.ppwr_legend_3]
          Table_data_legend.append(a)

     # Custom Legend comes before the Additional Custom Legends: the analyst found
     # them printing the other way round (01-08-2026).
     if ppwr.ppwr_custom_legend:
          a = [ppwr.ppwr_custom_legend]
          Table_data_legend.append(a)

     if ppwr.ppwr_legend_4:
          a = [ppwr.ppwr_legend_4]
          Table_data_legend.append(a)
     if ppwr.ppwr_legend_5:
          a = [ppwr.ppwr_legend_5]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    # multi_cell wraps within the 190mm text width; cell() would
                    # print one long line straight past the right margin.
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     # if ppwr.ppwr_editnote:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,170,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(167.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=ppwr.ppwr_editnote)
     # line_height = 4
     # y = 180
     # if ppwr.ppwr_legend_1:
     #      pdf.text(10,y,txt=ppwr.ppwr_legend_1)
     #      y = y+line_height
     # if ppwr.ppwr_legend_2:
     #      pdf.text(10,y,txt=ppwr.ppwr_legend_2)
     #      y = y+line_height

     # if ppwr.ppwr_custom_legend:
     #      pdf.text(10,y,txt=ppwr.ppwr_custom_legend)
     #      y = y+line_height


     # pdf.image(ppwr.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(ppwr.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,235,22,22)
     # pdf.image(ppwr.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")


     if ppwr.analyst_signature:
         pdf.image(ppwr.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(ppwr.analyst_signature.role if ppwr.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(ppwr.analyst_signature.role if ppwr.analyst_signature else '')})")
     if ppwr.assistant_manager_signature:
         pdf.image(ppwr.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(ppwr.assistant_manager_signature.role if ppwr.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(ppwr.assistant_manager_signature.role if ppwr.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,235,22,22)
     if ppwr.lab_manager_signature:
         pdf.image(ppwr.lab_manager_signature.signature,178,235,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(ppwr.lab_manager_signature.role if ppwr.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(ppwr.lab_manager_signature.role if ppwr.lab_manager_signature else '')})")

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
     # if ppwr.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if ppwr.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if ppwr.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if ppwr.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     
     _std = ppwr.etal_standard
     _city = (ppwr.city_location or '').strip().lower()

     if _std == "NEQS" and _city == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif _std == "NEQS" and _city == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif _std == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif _std == "PEQS":
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
     pdf.text(128,285,txt=ppwr.ppwr_doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=ppwr.ppwr_doc2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=ppwr.ppwr_doc3)
     
     if ppwr.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ppwr, f'pdf_image_{i}')
               desc = getattr(ppwr, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=ppwr.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/ppwr/'
     # pdf.output(file_path + ppwr.lab_report_no +'.pdf')
     # pdf = open(file_path + ppwr.lab_report_no +'.pdf', 'rb')

     
     # response = FileResponse(pdf)
     # return response
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ppwr.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def ppwrAnalysisPdf1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_ppwrAnalysisPdf1 as PDFWithPageNumbers




     ppwr = PPWRAnalysis.objects.get(id=pk)
     ppwr.extra_field = _safe_json_list(ppwr.extra_field)


     TABLE_DATA = [
           ["Sr.#","Parameter/Analytes Description",ppwr.unit_head,ppwr.ppwr_ex_1_1,"Result",ppwr.ppwr_ex_2_1],
     ]
     sr_no = 1
     if ppwr.ppwr_sr1:
          a = [str(sr_no),ppwr.ppwr_p1,ppwr.unit_1,ppwr.ppwr_ex_1_2,ppwr.ppwr_sr1,ppwr.ppwr_ex_2_2]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr2:
          a = [str(sr_no),ppwr.ppwr_p2,ppwr.unit_2,ppwr.ppwr_ex_1_3,ppwr.ppwr_sr2,ppwr.ppwr_ex_2_3]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr3:
          a = [str(sr_no),ppwr.ppwr_p3,ppwr.unit_3,ppwr.ppwr_ex_1_4,ppwr.ppwr_sr3,ppwr.ppwr_ex_2_4]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr4:
          a = [str(sr_no),ppwr.ppwr_p4,ppwr.unit_4,ppwr.ppwr_ex_1_5,ppwr.ppwr_sr4,ppwr.ppwr_ex_2_5]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr5:
          a = [str(sr_no),ppwr.ppwr_p5,ppwr.unit_5,ppwr.ppwr_ex_1_6,ppwr.ppwr_sr5,ppwr.ppwr_ex_2_6]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if ppwr.ppwr_sr6:
          a = [str(sr_no),ppwr.ppwr_p6,ppwr.unit_6,ppwr.ppwr_ex_1_7,ppwr.ppwr_sr6,ppwr.ppwr_ex_2_7]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     for extra_field in ppwr.extra_field:
          parameters = extra_field.get("parameters")
          units = extra_field.get("units")
          ex_1 = extra_field.get("ex_1")
          result = extra_field.get("result")
          ex_2 = extra_field.get("ex_2")
          if parameters:
               a = [str(sr_no), parameters, units, ex_1, result, ex_2]
               sr_no += 1
               TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=ppwr.lab_report_no,invoice_bill_no=ppwr.invoice_bill_no,reporting_date=ppwr.reporting_date,report_to=ppwr.report_to,
                              address=ppwr.address,attention=ppwr.attention,email=ppwr.email,sample_id=ppwr.sample_id,ppwr_sample_col_date=ppwr.ppwr_sample_col_date,
                              ppwr_sample_desc=ppwr.ppwr_sample_desc,ppwr_sample_type=ppwr.ppwr_sample_type,ppwr_sample_col_by=ppwr.ppwr_sample_col_by,ppwr_test_desc = ppwr.ppwr_test_desc,ppwr_date_analysis_from=ppwr.ppwr_date_analysis_from,ppwr_date_analysis_to = ppwr.ppwr_date_analysis_to

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
     with pdf.table(col_widths=(10, 50, 30,30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER','CENTER')) as table:




          _mgspan = 0
          if ppwr.ppwr_sr1 and ppwr.ppwr_sr2 and ppwr.ppwr_sr3 and ppwr.ppwr_sr4:
              if ppwr.ppwr_ex_2_2 and ppwr.ppwr_ex_2_2 == ppwr.ppwr_ex_2_3 == ppwr.ppwr_ex_2_4 == ppwr.ppwr_ex_2_5:
                  _mgspan = 4
          for k in range(0,len(TABLE_DATA)):
               data_row = TABLE_DATA[k]
               # if k == 0:
               #      data_row[4] = ppwr.select

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    if _mgspan and i == 5 and k >= 1 and k <= 4:
                        if k == 1:
                            row.cell(datum, rowspan=4)
                    else:
                        row.cell(datum)

     # data after Table

     Table_Data1 = [
          
     ]
     if ppwr.ppwr_editnote:
          a=["Note: "+ppwr.ppwr_editnote] 
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
     if ppwr.ppwr_legend_1:
          a = [ppwr.ppwr_legend_1]
          Table_data_legend.append(a)
          
     if ppwr.ppwr_legend_2:
          a = [ppwr.ppwr_legend_2]
          Table_data_legend.append(a)
     if ppwr.ppwr_legend_3:
          a = [ppwr.ppwr_legend_3]
          Table_data_legend.append(a)

     # Custom Legend comes before the Additional Custom Legends: the analyst found
     # them printing the other way round (01-08-2026).
     if ppwr.ppwr_custom_legend:
          a = [ppwr.ppwr_custom_legend]
          Table_data_legend.append(a)

     if ppwr.ppwr_legend_4:
          a = [ppwr.ppwr_legend_4]
          Table_data_legend.append(a)
     if ppwr.ppwr_legend_5:
          a = [ppwr.ppwr_legend_5]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    # multi_cell wraps within the 190mm text width; cell() would
                    # print one long line straight past the right margin.
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     # if ppwr.ppwr_editnote:
     #      pdf.set_font("Calibri","B", 10)
     #      pdf.text(10,170,txt="Note:")
     #      pdf.set_font("Calibri","", 8)
     #      pdf.set_y(167.5)
     #      pdf.set_x(20)
     #      pdf.multi_cell(182,txt=ppwr.ppwr_editnote)
     # line_height = 4
     # y = 180
     # if ppwr.ppwr_legend_1:
     #      pdf.text(10,y,txt=ppwr.ppwr_legend_1)
     #      y = y+line_height
     # if ppwr.ppwr_legend_2:
     #      pdf.text(10,y,txt=ppwr.ppwr_legend_2)
     #      y = y+line_height

     # if ppwr.ppwr_custom_legend:
     #      pdf.text(10,y,txt=ppwr.ppwr_custom_legend)
     #      y = y+line_height


     # pdf.image(ppwr.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(ppwr.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,230,22,22)
     # pdf.image(ppwr.lab_manager_signature.signature,178,234,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     
     if ppwr.analyst_signature:
         pdf.image(ppwr.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(ppwr.analyst_signature.role if ppwr.analyst_signature else '')})"),252)
     pdf.text(26,254.5,f"Analyzed By ({(ppwr.analyst_signature.role if ppwr.analyst_signature else '')})")
     if ppwr.assistant_manager_signature:
         pdf.image(ppwr.assistant_manager_signature.signature,100,234,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(ppwr.assistant_manager_signature.role if ppwr.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,254.5,f"Reviewed By ({(ppwr.assistant_manager_signature.role if ppwr.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,230,22,22)
     if ppwr.lab_manager_signature:
         pdf.image(ppwr.lab_manager_signature.signature,178,230,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(ppwr.lab_manager_signature.role if ppwr.lab_manager_signature else '')})"),252)
     pdf.text(160,254.5,f"Approved By ({(ppwr.lab_manager_signature.role if ppwr.lab_manager_signature else '')})")


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
     pdf.set_y(276)
     pdf.set_x(9)
     pdf.multi_cell(110,3,txt="• Our test reports can be verified by scanning System-generated QR Code.")

     pdf.set_font("Calibri","B", 5)

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',128,259,19,15)
     # if ppwr.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if ppwr.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if ppwr.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if ppwr.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(151,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     
     
     _std = ppwr.etal_standard
     _city = (ppwr.city_location or '').strip().lower()

     if _std == "NEQS" and _city == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif _std == "NEQS" and _city == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif _std == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif _std == "PEQS":
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
     pdf.text(128,280,txt=ppwr.ppwr_doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=ppwr.ppwr_doc2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=ppwr.ppwr_doc3)
     
     if ppwr.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(ppwr, f'pdf_image_{i}')
               desc = getattr(ppwr, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=ppwr.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/mba_pdf/'
     # pdf.output(file_path + ppwr.lab_report_no +'.pdf')

     # pdf = open(file_path + ppwr.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={ppwr.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response


def ppwrclone(request,pk):
     existing_form = PPWRAnalysis.objects.get(id=pk)
     existing_form.extra_field = _safe_json_list(existing_form.extra_field)
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
     return render(request,"ppwrClone.html",context)

def ppwrcloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = PPWRAnalysis.objects.get(id=pk)
     except PPWRAnalysis.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          if industry_id:
               existing_Form.industry = Industry_sector.objects.get(id=industry_id)
          existing_Form.lab_report_no = request.POST['ppwr_lab_report_no']
          existing_Form.invoice_bill_no = request.POST['ppwr_invoice_bill']
          existing_Form.reporting_date = request.POST['ppwr_rep_date']
          existing_Form.report_to = request.POST['ppwr_rep_to']
          existing_Form.address = request.POST['ppwr_address']
          existing_Form.attention = request.POST['ppwr_attention']
          existing_Form.email = request.POST['ppwr_email']
          existing_Form.sample_id = request.POST['ppwr_sampleId']
          existing_Form.ppwr_sample_col_date = request.POST['ppwr_sample_col_date']
          existing_Form.ppwr_sample_desc = request.POST['ppwr_sample_desc']
          existing_Form.ppwr_sample_type = request.POST['ppwr_sample_type']
          existing_Form.ppwr_sample_col_by = request.POST['ppwr_sample_col_by']
          existing_Form.ppwr_date_analysis_to = request.POST['ppwr_date_analysis_to']
          existing_Form.ppwr_date_analysis_from = request.POST['ppwr_date_analysis_from']
          existing_Form.ppwr_test_desc = request.POST['ppwr_test_desc']
          existing_Form.ppwr_sr1 = request.POST.get('ppwr_sr1')
          existing_Form.ppwr_sr2 = request.POST.get('ppwr_sr2')
          existing_Form.ppwr_sr3 = request.POST.get('ppwr_sr3')
          existing_Form.ppwr_sr4 = request.POST.get('ppwr_sr4')
          existing_Form.ppwr_sr5 = request.POST.get('ppwr_sr5')
          existing_Form.ppwr_sr6 = request.POST.get('ppwr_sr6')
          existing_Form.ppwr_ex_1_1 = request.POST.get('ex_1_1')
          existing_Form.ppwr_ex_1_2 = request.POST.get('ex_1_2')
          existing_Form.ppwr_ex_1_3 = request.POST.get('ex_1_3')
          existing_Form.ppwr_ex_1_4 = request.POST.get('ex_1_4')
          existing_Form.ppwr_ex_1_5 = request.POST.get('ex_1_5')
          existing_Form.ppwr_ex_1_6 = request.POST.get('ex_1_6')
          existing_Form.ppwr_ex_1_7 = request.POST.get('ex_1_7')
          existing_Form.ppwr_ex_2_1 = request.POST.get('ex_2_1')
          existing_Form.ppwr_ex_2_2 = request.POST.get('ex_2_2')
          existing_Form.ppwr_ex_2_3 = request.POST.get('ex_2_3')
          existing_Form.ppwr_ex_2_4 = request.POST.get('ex_2_4')
          existing_Form.ppwr_ex_2_5 = request.POST.get('ex_2_5')
          existing_Form.ppwr_ex_2_6 = request.POST.get('ex_2_6')
          existing_Form.ppwr_ex_2_7 = request.POST.get('ex_2_7')
          existing_Form.ppwr_p1 = request.POST.get('p1')
          existing_Form.ppwr_p2 = request.POST.get('p2')
          existing_Form.ppwr_p3 = request.POST.get('p3')
          existing_Form.ppwr_p4 = request.POST.get('p4')
          existing_Form.ppwr_p5 = request.POST.get('p5')
          existing_Form.ppwr_p6 = request.POST.get('p6')
          existing_Form.ppwr_legend_1 = request.POST.get('ppwr_legend_1')
          existing_Form.ppwr_legend_2 = request.POST.get('ppwr_legend_2')
          existing_Form.ppwr_legend_3 = request.POST.get('ppwr_legend_3')
          existing_Form.ppwr_legend_4 = request.POST.get('ppwr_legend_4')
          existing_Form.ppwr_legend_5 = request.POST.get('ppwr_legend_5')
          existing_Form.ppwr_editnote = request.POST.get('ppwr_editnote')
          existing_Form.ppwr_custom_legend = request.POST.get('ppwr_custom_legend')
          existing_Form.ppwr_doc1 = request.POST.get('ppwr_doc1')
          existing_Form.ppwr_doc2 = request.POST.get('ppwr_doc2')
          existing_Form.ppwr_doc3 = request.POST.get('ppwr_doc3')
          existing_Form.city_location = request.POST.get('city_location')
          existing_Form.created_by = request.user
          existing_Form.unit_head = request.POST.get('unit_head')
          existing_Form.unit_1 = request.POST.get('unit_1')
          existing_Form.unit_2 = request.POST.get('unit_2')
          existing_Form.unit_3 = request.POST.get('unit_3')
          existing_Form.unit_4 = request.POST.get('unit_4')
          existing_Form.unit_5 = request.POST.get('unit_5')
          existing_Form.unit_6 = request.POST.get('unit_6')
          # extra (dynamic) result rows — rebuilt from the clone form's array inputs
          _sr  = request.POST.getlist('sr[]')
          _par = request.POST.getlist('parameters[]')
          _un  = request.POST.getlist('units[]')
          _e1  = request.POST.getlist('ex_1[]')
          _res = request.POST.getlist('result[]')
          _e2  = request.POST.getlist('ex_2[]')
          _rows = []
          for _i in range(len(_sr)):
               _rows.append({
                    "sr": _sr[_i],
                    "parameters": _par[_i] if _i < len(_par) else "",
                    "units": _un[_i] if _i < len(_un) else "",
                    "ex_1": _e1[_i] if _i < len(_e1) else "",
                    "result": _res[_i] if _i < len(_res) else "",
                    "ex_2": _e2[_i] if _i < len(_e2) else "",
               })
          existing_Form.extra_field = json.dumps(_rows)
          # existing_Form.ppwr_analyzedby = request.FILES['ppwr_analyzedby']
          # existing_Form.ppwr_reviewedby = request.FILES['ppwr_reviewedby']
          # existing_Form.ppwr_approvedby = request.FILES['ppwr_approvedby']
          # existing_Form.ppwr_approvedby1 = request.FILES['ppwr_approvedby1']
          
          
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')
  
          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None
  
          # Assign to ambientUpdate if needed
          if analyst_sign:
               existing_Form.analyst_signature = analyst_sign
          if review_sign:
               existing_Form.assistant_manager_signature = review_sign
          if approved_sign:
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
          action = f'PPWR Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=now_pk_str())
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/ppwr-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='ppwrList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "ppwrClone.html")

__all__ = [
    'ppwrAnalysis',
    'ppwrList',
    'ppwrDelete',
    'ppwrEdit',
    'ppwrUpdate',
    'ppwrView',
    'ppwrAnalysisPdf',
    'ppwrAnalysisPdf1',
    'ppwrclone',
    'ppwrcloneSave',
]
