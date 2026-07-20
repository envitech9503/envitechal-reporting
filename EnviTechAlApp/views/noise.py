# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403

def noise_distance_legend(location):
    _m = {'PEQS': 'Punjab', 'SEQS': 'Sindh', 'NEQS': 'National'}
    _std = (location or '').strip().upper()
    _name = _m.get(_std)
    if not _name:
        return None
    return ('Noise measurements were conducted at a distance of 7.5 metres from the source, '
            'in accordance with the %s Environmental Quality Standards (%s).' % (_name, _std))




@login_required(login_url="/login")
def noiseAnalysis(request):
     if request.method == 'POST':
          location = request.POST['location']
          industry_id = request.POST.get('industry')
          industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          city_location = request.POST['city_location']
          lab_report_no = request.POST['lab_rep_no']
          invoice_bill_no = request.POST['invoice_no']
          reporting_date = request.POST['rep_date']
          report_to = request.POST['report_to']
          address = request.POST['address']
          attention = request.POST['attention']
          email = request.POST['email']
          sample_id = request.POST['testId']
          test_perf_date = request.POST['test_perf_date']
          test_type = request.POST['test_type']
          test_perf_by = request.POST['test_perf_by']
          test_desc = request.POST['test_desc']
          select = request.POST.get('select')
          select1 = request.POST.get('select1')
          custom_limit = request.POST.get('custom_limit')
          r1 = request.POST['r1']
          r1_1 = request.POST['r1_1']
          r2 = request.POST['r2']
          r2_2 = request.POST['r2_2']
          r3 = request.POST['r3']
          r3_3 = request.POST['r3_3']
          r4 = request.POST['r4']
          r4_4 = request.POST['r4_4']
          r5 = request.POST['r5']
          r5_5 = request.POST['r5_5']
          r6 = request.POST['r6']
          r6_6 = request.POST['r6_6']
          r7 = request.POST['r7']
          r7_7 = request.POST['r7_7']
          r8 = request.POST['r8']
          r8_8 = request.POST['r8_8']
          r9 = request.POST['r9']
          r9_9 = request.POST['r9_9']
          r10 = request.POST['r10']
          r10_10 = request.POST['r10_10']
          r11 = request.POST['r11']
          r11_11 = request.POST['r11_11']
          r12 = request.POST['r12']
          r12_12 = request.POST['r12_12']
          r13 = request.POST['r13']
          r13_13 = request.POST['r13_13']
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
          noiseForm = NoiseAnalysis(lab_report_no=lab_report_no,invoice_bill_no=invoice_bill_no,reporting_date=reporting_date,report_to=report_to,
                                    address=address,attention=attention,email=email,sample_id=sample_id,test_perf_date=test_perf_date,
                                    test_type=test_type,test_perf_by=test_perf_by,test_desc=test_desc,select=select,select1=select1,custom_limit=custom_limit,r1=r1,r1_1=r1_1,
                                    r2=r2,r2_2=r2_2,r3=r3,r3_3=r3_3,r4=r4,r4_4=r4_4,r5=r5,r5_5=r5_5,r6=r6,r6_6=r6_6,r7=r7,r7_7=r7_7,
                                    r8=r8,r8_8=r8_8,r9=r9,r9_9=r9_9,r10=r10,r10_10=r10_10,r11=r11,r11_11=r11_11,r12=r12,r12_12=r12_12,
                                    r13=r13,r13_13=r13_13,legend_1=legend_1,legend_2=legend_2,legend_3=legend_3,legend_4=legend_4,
                                    legend_5=legend_5,legend_6=legend_6,legend_7=legend_7,legend_8=legend_8,legend_9=legend_9,legend_10=legend_10,
                                    legend_11=legend_11,editNote=editNote,customlegend=customlegend,location=location,
                                    doc1=doc1,doc2=doc2,doc3=doc3,city_location=city_location,extra_field=extra_field,customer_id=customer_id,
                                    analyst_signature=analyst_sign,assistant_manager_signature=review_sign,lab_manager_signature=approved_sign,**image_data,pdf_heading=pdf_heading,created_by = request.user,industry=industry)
          noiseForm.save()

          
          
          if customer_id:
               LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

          user = request.user
          action = f'Noise Analysis Form {noiseForm.lab_report_no} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = (NoiseAnalysis.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/noiseAnalysis-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="noiseAnalysis")
     else:
          log = LoggingSheet.objects.all()
          log = serializers.serialize('json',log)
          context = {'log':log,'signs':signs,'industry':industries}
          return render(request,"noiseAnalysis.html",context)


@login_required(login_url="/login")
def noiseAnalysisList(request):
     nA, _srch = _list_filter(request, NoiseAnalysis)
     context = {'searched':_srch, 'data':nA}
     return render(request,"noiseAnalysisList.html",context)


@login_required(login_url="/login")
def noiseAnalysisDelete(request,pk):
     nA = NoiseAnalysis.objects.get(id=pk)
     nA.delete()
     user = request.user
     action = f'Noise Analysis Form {nA.lab_report_no} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Operation was successful!')
     return redirect("noiseAnalysisList")


@login_required(login_url="/login")
def noiseAnalysisEdit(request,pk):
     nA = NoiseAnalysis.objects.get(id=pk)
     nA.extra_field = nA.extra_field.replace("'", "\"")
     nA.extra_field = json.loads(nA.extra_field)
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(nA, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':nA,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),}
     return render(request,"noiseAnalysisEdit.html",context)


@login_required(login_url="/login")
def noiseAnalysisUpdate(request,pk):
     nA = NoiseAnalysis.objects.get(id=pk)
     if request.method == 'POST':
          nA.location = request.POST['location']
          industry_id = request.POST.get('industry')
          nA.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          nA.lab_report_no = request.POST['lab_rep_no']
          nA.invoice_bill_no = request.POST['invoice_no']
          nA.reporting_date = request.POST['rep_date']
          nA.report_to = request.POST['report_to']
          nA.address = request.POST['address']
          nA.attention = request.POST['attention']
          nA.email = request.POST['email']
          nA.sample_id = request.POST['testId']
          nA.test_perf_date = request.POST['test_perf_date']
          nA.test_type = request.POST['test_type']
          nA.test_perf_by = request.POST['test_perf_by']
          nA.test_desc = request.POST['test_desc']
          nA.select = request.POST.get('select')
          nA.select1 = request.POST.get('select1')
          nA.custom_limit = request.POST.get('custom_limit')
          nA.r1 = request.POST['r1']
          nA.r1_1 = request.POST['r1_1']
          nA.r2 = request.POST['r2']
          nA.r2_2 = request.POST['r2_2']
          nA.r3 = request.POST['r3']
          nA.r3_3 = request.POST['r3_3']
          nA.r4 = request.POST['r4']
          nA.r4_4 = request.POST['r4_4']
          nA.r5 = request.POST['r5']
          nA.r5_5 = request.POST['r5_5']
          nA.r6 = request.POST['r6']
          nA.r6_6 = request.POST['r6_6']
          nA.r7 = request.POST['r7']
          nA.r7_7 = request.POST['r7_7']
          nA.r8 = request.POST['r8']
          nA.r8_8 = request.POST['r8_8']
          nA.r9 = request.POST['r9']
          nA.r9_9 = request.POST['r9_9']
          nA.r10 = request.POST['r10']
          nA.r10_10 = request.POST['r10_10']
          nA.r11 = request.POST['r11']
          nA.r11_11 = request.POST['r11_11']
          nA.r12 = request.POST['r12']
          nA.r12_12 = request.POST['r12_12']
          nA.r13 = request.POST['r13']
          nA.r13_13 = request.POST['r13_13']
          nA.legend_1 = request.POST['legend_1']
          nA.legend_2 = request.POST['legend_2']
          nA.legend_3 = request.POST['legend_3']
          nA.legend_4 = request.POST['legend_4']
          nA.legend_5 = request.POST['legend_5']
          nA.legend_6 = request.POST['legend_6']
          nA.legend_7 = request.POST['legend_7']
          nA.legend_8 = request.POST['legend_8']
          nA.legend_9 = request.POST['legend_9']
          nA.legend_10 = request.POST['legend_10']
          nA.legend_11 = request.POST['legend_11']
          nA.editNote = request.POST['editNote']
          nA.customlegend = request.POST['customlegend']
          nA.doc1 = request.POST['doc1']
          nA.doc2 = request.POST['doc2']
          nA.doc3 = request.POST['doc3']
          nA.created_by = request.user
          # nA.analyzedby = request.FILES['analyzedby']
          # nA.reviewedby = request.FILES['reviewedby']
          # nA.approvedby = request.FILES['approvedby']
          # nA.approvedby1 = request.FILES['approvedby1']
          nA.city_location = request.POST['city_location']
          nA.extra_field = json.loads(request.POST['extra_field'])
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          nA.analyst_signature = analyst_sign
          nA.assistant_manager_signature = review_sign
          nA.lab_manager_signature = approved_sign
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               areas = request.POST.getlist('areas[]')[i]
               methods = request.POST.getlist('methods[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               nA.extra_field.append({
                         "sr": sr,
                         "areas": areas,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        

          nA.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(nA, image_key, '')
                    setattr(nA, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(nA, image_key, base64_encoded)
                         setattr(nA, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(nA, desc_key, description)


          nA.save()
          user = request.user
          action = f'Noise Analysis Form {nA.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = nA.id
          if "submit_and_view" in request.POST:
               url = f"/noiseAnalysis-view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="noiseAnalysisList")
     return render(request,"noiseAnalysisList.html")



def noiseAnalysisView(request,pk):
     nA = NoiseAnalysis.objects.get(id=pk)
     nA.extra_field = nA.extra_field.replace("'", "\"")
     nA.extra_field = json.loads(nA.extra_field)
     current_url = request.build_absolute_uri()
     # Generate a unique file name for the QR code
     qr_filename = f"qr_{nA.lab_report_no}.png"
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
     context = {'data':nA,'qr':qr_relative_path,'logo':logo}

     return render(request,'noiseAnalysisReport.html',context)



def noiseAnalysisReport(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_noiseAnalysisReport as PDFWithPageNumbers




     nA= NoiseAnalysis.objects.get(id=pk)
     nA.extra_field = nA.extra_field.replace("'", "\"")
     nA.extra_field = json.loads(nA.extra_field)

     TABLE_DATA = [
           ["Sr.#","Locations","Methods","Unit","Result",""],
     ]
     sr_no = 1
     if nA.r1 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     if nA.r2 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r3 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r4 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r5 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r6 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r7 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r8 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r9 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r10 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r11 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r12 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r13 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     if nA.select1 == "Custom":
          _na_pairs = [(nA.r1,nA.r1_1),(nA.r2,nA.r2_2),(nA.r3,nA.r3_3),(nA.r4,nA.r4_4),(nA.r5,nA.r5_5),(nA.r6,nA.r6_6),(nA.r7,nA.r7_7),(nA.r8,nA.r8_8),(nA.r9,nA.r9_9),(nA.r10,nA.r10_10),(nA.r11,nA.r11_11),(nA.r12,nA.r12_12),(nA.r13,nA.r13_13)]
          for _loc,_res in _na_pairs:
               if _loc:
                    TABLE_DATA.append([str(sr_no),_loc,"ASTM E1686-16","dB",_res,(nA.custom_limit or "-")])
                    sr_no = sr_no+1
     for extra_field in nA.extra_field:
          areas = extra_field.get("areas")
          methods = extra_field.get("methods")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")
               # Check if the "areas" field is not empty before adding the row
          if areas:
               a = [str(sr_no),areas,methods,unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)






     pdf = PDFWithPageNumbers(lab_report_no=nA.lab_report_no,invoice_bill_no=nA.invoice_bill_no,reporting_date=nA.reporting_date,report_to=nA.report_to,
                              address=nA.address,attention=nA.attention,email=nA.email,sample_id=nA.sample_id,test_perf_date=nA.test_perf_date,
                              test_desc=nA.test_desc,test_type=nA.test_type,test_perf_by=nA.test_perf_by,select1=nA.select1

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
               if k == 0:
                    data_row[5] = nA.select + ' Limits'

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table
     Table_Data1 = [
          
     ]
     if nA.editNote:
          a=["Note: "+nA.editNote] 
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
     if nA.legend_1:
          a = [nA.legend_1]
          Table_data_legend.append(a)
          
     if nA.legend_2:
          a = [nA.legend_2]
          Table_data_legend.append(a)
          
     if nA.legend_3:
          a = [nA.legend_3]
          Table_data_legend.append(a)
          
     if nA.legend_4:
          a = [nA.legend_4]
          Table_data_legend.append(a)
          
     if nA.legend_5:
          a = [nA.legend_5]
          Table_data_legend.append(a)
          
     if nA.legend_6:
          a = [nA.legend_6]
          Table_data_legend.append(a)
          
     if nA.legend_7:
          a = [nA.legend_7]
          Table_data_legend.append(a)
          
     if nA.legend_8:
          a = [nA.legend_8]
          Table_data_legend.append(a)
          
     if nA.legend_9:
          a = [nA.legend_9]
          Table_data_legend.append(a)
          
     if nA.legend_10:
          a = [nA.legend_10]
          Table_data_legend.append(a)
          
     if nA.legend_11:
          a = [nA.legend_11]
          Table_data_legend.append(a)
          

     if nA.customlegend:
          a = [nA.customlegend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')


     


     # pdf.image(nA.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(nA.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,233,22,22)
     # pdf.image(nA.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     
     if nA.analyst_signature:
         pdf.image(nA.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})"),257)
     pdf.text(26,259.5,f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})")
     if nA.assistant_manager_signature:
         pdf.image(nA.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,259.5,f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,233,22,22)
     if nA.lab_manager_signature:
         pdf.image(nA.lab_manager_signature.signature,178,233,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})"),257)
     pdf.text(160,259.5,f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})")


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
     # if nA.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if nA.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if nA.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if nA.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     if nA.location == "NEQS" and nA.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif nA.location == "NEQS" and nA.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 264, 25, 16)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,263.5,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,267,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif nA.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 263, 19, 15)
          pdf.text(152,280,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,266,txt="Disclaimer:")

     elif nA.location == "PEQS":
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
     pdf.text(128,285,txt=nA.doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=nA.doc2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=nA.doc3)
     
     if nA.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(nA, f'pdf_image_{i}')
               desc = getattr(nA, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=nA.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/noiseAnalysis/'
     # pdf.output(file_path + nA.lab_report_no +'.pdf')
     # pdf = open(file_path + nA.lab_report_no +'.pdf', 'rb')

     # # pdf.output(nA.lab_report_no +'.pdf')

     # # pdf = open(nA.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={nA.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def noiseAnalysisReport1(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_noiseAnalysisReport1 as PDFWithPageNumbers




     nA= NoiseAnalysis.objects.get(id=pk)
     nA.extra_field = nA.extra_field.replace("'", "\"")
     nA.extra_field = json.loads(nA.extra_field)


     TABLE_DATA = [
           ["Sr.#","Locations","Methods","Unit","Result",""],
     ]
     sr_no = 1
     if nA.r1 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r1 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r1,"ASTM E1686-16","dB",nA.r1_1,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)

     if nA.r2 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r2 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r2,"ASTM E1686-16","dB",nA.r2_2,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r3 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r3 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r3,"ASTM E1686-16","dB",nA.r3_3,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r4 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r4 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r4,"ASTM E1686-16","dB",nA.r4_4,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r5 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r5 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r5,"ASTM E1686-16","dB",nA.r5_5,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r6 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r6 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r6,"ASTM E1686-16","dB",nA.r6_6,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r7 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r7 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r7,"ASTM E1686-16","dB",nA.r7_7,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r8 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r8 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r8,"ASTM E1686-16","dB",nA.r8_8,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r9 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r9 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r9,"ASTM E1686-16","dB",nA.r9_9,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r10 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r10 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r10,"ASTM E1686-16","dB",nA.r10_10,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r11 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r11 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r11,"ASTM E1686-16","dB",nA.r11_11,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r12 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r12 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r12,"ASTM E1686-16","dB",nA.r12_12,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     if nA.r13 and nA.select1 == "Residential Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Residential Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Commercial Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Commercial Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"55"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Industrial Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"75"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Industrial Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"65"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Silence Day":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"50"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)
     elif nA.r13 and nA.select1 =="Silence Night":
          a = [str(sr_no),nA.r13,"ASTM E1686-16","dB",nA.r13_13,"45"]
          sr_no = sr_no+1
          TABLE_DATA.append(a)


     if nA.select1 == "Custom":
          _na_pairs = [(nA.r1,nA.r1_1),(nA.r2,nA.r2_2),(nA.r3,nA.r3_3),(nA.r4,nA.r4_4),(nA.r5,nA.r5_5),(nA.r6,nA.r6_6),(nA.r7,nA.r7_7),(nA.r8,nA.r8_8),(nA.r9,nA.r9_9),(nA.r10,nA.r10_10),(nA.r11,nA.r11_11),(nA.r12,nA.r12_12),(nA.r13,nA.r13_13)]
          for _loc,_res in _na_pairs:
               if _loc:
                    TABLE_DATA.append([str(sr_no),_loc,"ASTM E1686-16","dB",_res,(nA.custom_limit or "-")])
                    sr_no = sr_no+1
     for extra_field in nA.extra_field:
          areas = extra_field.get("areas")
          methods = extra_field.get("methods")
          unit = extra_field.get("unit")
          result = extra_field.get("result")
          limit = extra_field.get("limit")
               # Check if the "areas" field is not empty before adding the row
          if areas:
               a = [str(sr_no),areas,methods,unit, result, limit]
               sr_no += 1
               TABLE_DATA.append(a)





     pdf = PDFWithPageNumbers(lab_report_no=nA.lab_report_no,invoice_bill_no=nA.invoice_bill_no,reporting_date=nA.reporting_date,report_to=nA.report_to,
                              address=nA.address,attention=nA.attention,email=nA.email,sample_id=nA.sample_id,test_perf_date=nA.test_perf_date,
                              test_desc=nA.test_desc,test_type=nA.test_type,test_perf_by=nA.test_perf_by,select1=nA.select1

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
               if k == 0:
                    data_row[5] = nA.select + ' Limits'

               # watwer mark
               # pdf.set_page_background("static/assets/Capture.PNG")
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]

                    row.cell(datum)

     # data after Table
     Table_Data1 = [
          
     ]
     if nA.editNote:
          a=["Note: "+nA.editNote] 
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
     if nA.legend_1:
          a = [nA.legend_1]
          Table_data_legend.append(a)
          
     if nA.legend_2:
          a = [nA.legend_2]
          Table_data_legend.append(a)
          
     if nA.legend_3:
          a = [nA.legend_3]
          Table_data_legend.append(a)
          
     if nA.legend_4:
          a = [nA.legend_4]
          Table_data_legend.append(a)
          
     if nA.legend_5:
          a = [nA.legend_5]
          Table_data_legend.append(a)
          
     if nA.legend_6:
          a = [nA.legend_6]
          Table_data_legend.append(a)
          
     if nA.legend_7:
          a = [nA.legend_7]
          Table_data_legend.append(a)
          
     if nA.legend_8:
          a = [nA.legend_8]
          Table_data_legend.append(a)
          
     if nA.legend_9:
          a = [nA.legend_9]
          Table_data_legend.append(a)
          
     if nA.legend_10:
          a = [nA.legend_10]
          Table_data_legend.append(a)
          
     if nA.legend_11:
          a = [nA.legend_11]
          Table_data_legend.append(a)
          

     if nA.customlegend:
          a = [nA.customlegend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')



     # pdf.image(nA.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(nA.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,228,22,22)
     # pdf.image(nA.lab_manager_signature.signature,178,233,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if nA.analyst_signature:
         pdf.image(nA.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})"),252)
     pdf.text(26,254.5,f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})")
     if nA.assistant_manager_signature:
         pdf.image(nA.assistant_manager_signature.signature,100,233,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,254.5,f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if nA.lab_manager_signature:
         pdf.image(nA.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})"),252)
     pdf.text(160,254.5,f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})")


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
     # if nA.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if nA.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if nA.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if nA.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     
     if nA.location == "NEQS" and nA.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")

     elif nA.location == "NEQS" and nA.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,262,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
     elif nA.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,261,txt="Disclaimer:")
     elif nA.location == "PEQS":
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
     pdf.text(128,280,txt=nA.doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=nA.doc2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=nA.doc3)
     
     
     if nA.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(nA, f'pdf_image_{i}')
               desc = getattr(nA, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=nA.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/na_pdf/'
     # pdf.output(file_path + nA.lab_report_no +'.pdf')

     # pdf = open(file_path + nA.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={nA.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'
     response.write(pdf_output.getvalue())
     return response



@login_required(login_url="/login")
def noisemonitoring(request):
     if request.method == 'POST':
          
        try:
            # Extract form data
            
            location = request.POST.get('location')
            industry_id = request.POST.get('industry')
            industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
            city_location = request.POST.get('city_location')
            lab_report_no = request.POST.get('lab_rep_no')
            if not lab_report_no:
                return JsonResponse({"error": "Lab Report Number is required"}, status=400)
            invoice_bill_no = request.POST.get('invoice_no')
            reporting_date = request.POST.get('rep_date')
            report_to = request.POST.get('report_to')
            address = request.POST.get('address')
            attention = request.POST.get('attention')
            email = request.POST.get('email')
            sample_id = request.POST.get('testId')
            test_perf_date = request.POST.get('test_perf_date')
            test_type = request.POST.get('test_type')
            test_perf_by = request.POST.get('test_perf_by')
            test_desc = request.POST.get('test_desc')
            select = request.POST.get('select')
            select1 = request.POST.get('select1')
            custom_limit = request.POST.get('custom_limit')
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")
            interval = request.POST.get("time_interval")
            test_method = request.POST.get("test_method")
            test_location = request.POST.get("test_location")
            
            # Process table data
            table_data = []
            index = 1
            while True:
                time_key = f"time_{index}"
                unit_key = f"unit_{index}"
                result_key = f"result_{index}"
                
                if time_key not in request.POST:
                    break
                    
                table_data.append({
                    "time": request.POST.get(time_key),
                    "unit": request.POST.get(unit_key),
                    "result": request.POST.get(result_key),
                })
                index += 1
            graph_type = request.POST.get('graph_type')
            # Extract other form fields
            legend_1 = request.POST.get('legend_1')
            legend_2 = request.POST.get('legend_2')
            legend_3 = request.POST.get('legend_3')
            legend_4 = request.POST.get('legend_4')
            legend_5 = request.POST.get('legend_5')
            legend_6 = request.POST.get('legend_6')
            legend_7 = request.POST.get('legend_7')
            legend_8 = request.POST.get('legend_8')
            legend_9 = request.POST.get('legend_9')
            legend_10 = request.POST.get('legend_10')
            legend_11 = request.POST.get('legend_11')
            editNote = request.POST.get('editNote')
            customlegend = request.POST.get('customlegend')
            doc1 = request.POST.get('doc1')
            doc2 = request.POST.get('doc2')
            doc3 = request.POST.get('doc3')
            extra_field = request.POST.get('extra_field', '[]')
            customer_id = request.POST.get('customer_id')
            
            # Handle signatures
            analyst_sign_id = request.POST.get('analyst_sign')
            review_sign_id = request.POST.get('review_sign')
            approved_sign_id = request.POST.get('approved_sign')
            
            analyst_sign = Signatures.objects.get(id=analyst_sign_id) if analyst_sign_id else None
            review_sign = Signatures.objects.get(id=review_sign_id) if review_sign_id else None
            approved_sign = Signatures.objects.get(id=approved_sign_id) if approved_sign_id else None
            
            pdf_heading = request.POST.get('pdf_heading')
            
            # Process images
            image_data = {}
            for i in range(1, 7):
                image_key = f'pdf_image_{i}'
                desc_key = f'pdf_desc_{i}'

                uploaded_file = request.FILES.get(image_key)
                description = request.POST.get(desc_key, '')
                
                if uploaded_file:
                    try:
                        # Compress if needed
                        if uploaded_file.size > 500 * 1024:
                            uploaded_file.seek(0)
                            compressed_image = compress_image(uploaded_file)
                            if compressed_image:
                                base64_encoded = base64.b64encode(compressed_image).decode('utf-8')
                            else:
                                uploaded_file.seek(0)
                                file_bytes = uploaded_file.read()
                                base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                        else:
                            file_bytes = uploaded_file.read()
                            base64_encoded = base64.b64encode(file_bytes).decode('utf-8')

                        image_data[image_key] = base64_encoded
                        image_data[desc_key] = description

                    except Exception as e:
                        pass
                        # Continue with other images even if one fails

            # Create NoiseMonitoring instance
            noiseForm = NoiseMonitoring(
                lab_report_no=lab_report_no,
                invoice_bill_no=invoice_bill_no,
                reporting_date=reporting_date,
                report_to=report_to,
                address=address,
                attention=attention,
                email=email,
                sample_id=sample_id,
                test_perf_date=test_perf_date,
                test_type=test_type,
                test_perf_by=test_perf_by,
                test_desc=test_desc,
                select=select,
                select1=select1,
                custom_limit=custom_limit,
                legend_1=legend_1,
                legend_2=legend_2,
                legend_3=legend_3,
                legend_4=legend_4,
                legend_5=legend_5,
                legend_6=legend_6,
                legend_7=legend_7,
                legend_8=legend_8,
                legend_9=legend_9,
                legend_10=legend_10,
                legend_11=legend_11,
                editNote=editNote,
                customlegend=customlegend,
                location=location,
                doc1=doc1,
                doc2=doc2,
                doc3=doc3,
                city_location=city_location,
                extra_field=extra_field,
                customer_id=customer_id,
                analyst_signature=analyst_sign,
                assistant_manager_signature=review_sign,
                lab_manager_signature=approved_sign,
                pdf_heading=pdf_heading,
                created_by=request.user,
                industry=industry,
                start_time=start_time,
                end_time=end_time,
                interval=interval,
                table_data=table_data,
                **image_data,
                graph_type=graph_type,
                test_method=test_method,
                test_location=test_location
            )
            
            noiseForm.save()

            # Update logging sheet if customer_id exists
            if customer_id:
                LoggingSheet.objects.filter(id=customer_id).update(rep_date=reporting_date)

            # Create audit log
            user = request.user
            action = f'Noise Analysis Form {noiseForm.lab_report_no} created by {user.username}'
            AuditLog.objects.create(user=user, action=action, timestamp=timezone.now())

            # Handle redirect based on submit button
            id = noiseForm.id
            if "submit_and_view" in request.POST:
                return JsonResponse({
                    "message": "Form saved successfully!", 
                    "url": f"/noiseMonitoring_view/{str(id)}/"
                })
            elif "submit_and_new" in request.POST:
                return JsonResponse({
                    "message": "Form saved successfully!", 
                    "url": "/noisemonitoring/"
                })
            else:
                 return JsonResponse({"message": "Form saved successfully! else"})
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)      
    
     else:
          # GET request - render form
          logs = LoggingSheet.objects.all()
          context = {
               'logs': logs,  # Fixed variable name
               'signs': Signatures.objects.all(),  # Assuming you have a Signatures model
               'industry': Industry_sector.objects.all()  # Assuming you have an Industry_sector model
          }
          return render(request, "noise_monitoring.html", context)
     
def noiseMonitoring_view(request,pk):
     nM =NoiseMonitoring.objects.get(id=pk)
     leq_value = calculate_leq(nM.start_time, nM.end_time, nM.interval, nM.table_data)
     current_url = request.build_absolute_uri()
     qr_filename = f"qr_{nM.lab_report_no}.png"
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
     
     table_data = nM.table_data or []
     table_data.append(leq_value)
     return render(request,'noiseMonitoring_view.html',context = {'data':nM,'qr':qr_relative_path,"table_data": table_data,'logo':logo,'leq_value':leq_value})
     
@login_required(login_url="/login")
def noiseMonitoring_clone(request,pk):
     nM = NoiseMonitoring.objects.get(id=pk)
     table_data = nM.table_data or []
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     limit_values = {
        "Residential Day": 55,
        "Residential Night": 45,
        "Commercial Day": 65,
        "Commercial Night": 55,
        "Industrial Day": 75,
        "Industrial Night": 65,
        "Silence Day": 50,
        "Silence Night": 45,
     }
     limit_value = (nM.custom_limit or "-") if nM.select1 == "Custom" else limit_values.get(nM.select1, "-")
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(nM, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':nM,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
               'pdf_image_2': image_previews.get('pdf_image_2'),
               'pdf_image_3': image_previews.get('pdf_image_3'),
               'pdf_image_4': image_previews.get('pdf_image_4'),
               'pdf_image_5': image_previews.get('pdf_image_5'),
               'pdf_image_6': image_previews.get('pdf_image_6'),"table_data": table_data,"limit_value": limit_value,}
     return render(request,"noiseMonitoring_clone.html",context)


@login_required(login_url="/login")
def noiseMonitoring_clone_update(request,pk):
     nA = NoiseMonitoring.objects.get(id=pk)
     if request.method == 'POST':
          nA.location = request.POST['location']
          industry_id = request.POST.get('industry')
          nA.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          nA.lab_report_no = request.POST['lab_rep_no']
          nA.invoice_bill_no = request.POST['invoice_no']
          nA.reporting_date = request.POST['rep_date']
          nA.report_to = request.POST['report_to']
          nA.address = request.POST['address']
          nA.attention = request.POST['attention']
          nA.email = request.POST['email']
          nA.sample_id = request.POST['testId']
          nA.test_perf_date = request.POST['test_perf_date']
          nA.test_type = request.POST['test_type']
          nA.test_perf_by = request.POST['test_perf_by']
          nA.test_desc = request.POST['test_desc']
          nA.select = request.POST.get('select')
          nA.select1 = request.POST.get('select1')
          nA.custom_limit = request.POST.get('custom_limit')
          nA.test_method = request.POST.get("test_method")
          nA.test_location = request.POST.get("test_location")
          table_data = []
          index = 1
          while True:
              time_key = f"time_{index}"
              unit_key = f"unit_{index}"
              result_key = f"result_{index}"
              
              if time_key not in request.POST:
                  break
                  
              table_data.append({
                  "time": request.POST.get(time_key),
                  "unit": request.POST.get(unit_key),
                  "result": request.POST.get(result_key),
              })
              index += 1
          nA.table_data = table_data
          nA.start_time = request.POST.get("start_time")
          nA.end_time = request.POST.get("end_time")
          nA.interval = request.POST.get("time_interval")
          nA.legend_1 = request.POST['legend_1']
          nA.legend_2 = request.POST['legend_2']
          nA.legend_3 = request.POST['legend_3']
          nA.legend_4 = request.POST['legend_4']
          nA.legend_5 = request.POST['legend_5']
          nA.legend_6 = request.POST['legend_6']
          nA.legend_7 = request.POST['legend_7']
          nA.legend_8 = request.POST['legend_8']
          nA.legend_9 = request.POST['legend_9']
          nA.legend_10 = request.POST['legend_10']
          nA.legend_11 = request.POST['legend_11']
          nA.editNote = request.POST['editNote']
          nA.customlegend = request.POST['customlegend']
          nA.doc1 = request.POST['doc1']
          nA.doc2 = request.POST['doc2']
          nA.doc3 = request.POST['doc3']
          nA.graph_type = request.POST.get('graph_type')
          nA.created_by = request.user
          # nA.analyzedby = request.FILES['analyzedby']
          # nA.reviewedby = request.FILES['reviewedby']
          # nA.approvedby = request.FILES['approvedby']
          # nA.approvedby1 = request.FILES['approvedby1']
          nA.city_location = request.POST['city_location']
          nA.extra_field = json.loads(request.POST['extra_field'])
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          nA.analyst_signature = analyst_sign
          nA.assistant_manager_signature = review_sign
          nA.lab_manager_signature = approved_sign
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               areas = request.POST.getlist('areas[]')[i]
               methods = request.POST.getlist('methods[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               nA.extra_field.append({
                         "sr": sr,
                         "areas": areas,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        

          nA.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(nA, image_key, '')
                    setattr(nA, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(nA, image_key, base64_encoded)
                         setattr(nA, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(nA, desc_key, description)

          nA.pk = None
          nA.save()
          user = request.user
          action = f'Noise Analysis Form {nA.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = nA.id
          if "submit_and_view" in request.POST:
               url = f"/noiseMonitoring_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="noiseMonitoring_clone")
     return render(request,"noiseMonitoring_clone.html")



@login_required(login_url="/login")
def noiseMonitoring_edit(request,pk):
     nM = NoiseMonitoring.objects.get(id=pk)
     table_data = nM.table_data or []
     log = LoggingSheet.objects.all()
     log = serializers.serialize('json',log)
     limit_values = {
        "Residential Day": 55,
        "Residential Night": 45,
        "Commercial Day": 65,
        "Commercial Night": 55,
        "Industrial Day": 75,
        "Industrial Night": 65,
        "Silence Day": 50,
        "Silence Night": 45,
     }
     limit_value = (nM.custom_limit or "-") if nM.select1 == "Custom" else limit_values.get(nM.select1, "-")
     image_previews = {}
     for i in range(1, 7):
         image_key = f'pdf_image_{i}'
         image_data = getattr(nM, image_key)
         if image_data:
             image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
     context = {'data':nM,'log':log,'signs':signs,
                'pdf_image_1': image_previews.get('pdf_image_1'),
                'industry':industries,
               'pdf_image_2': image_previews.get('pdf_image_2'),
               'pdf_image_3': image_previews.get('pdf_image_3'),
               'pdf_image_4': image_previews.get('pdf_image_4'),
               'pdf_image_5': image_previews.get('pdf_image_5'),
               'pdf_image_6': image_previews.get('pdf_image_6'),"table_data": table_data,"limit_value": limit_value,}
     return render(request,"noiseMonitoring_edit.html",context)


@login_required(login_url="/login")
def noiseMonitoring_edit_update(request,pk):
     nA = NoiseMonitoring.objects.get(id=pk)
     if request.method == 'POST':
          nA.location = request.POST['location']
          industry_id = request.POST.get('industry')
          nA.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          nA.lab_report_no = request.POST['lab_rep_no']
          nA.invoice_bill_no = request.POST['invoice_no']
          nA.reporting_date = request.POST['rep_date']
          nA.report_to = request.POST['report_to']
          nA.address = request.POST['address']
          nA.attention = request.POST['attention']
          nA.email = request.POST['email']
          nA.sample_id = request.POST['testId']
          nA.test_perf_date = request.POST['test_perf_date']
          nA.test_type = request.POST['test_type']
          nA.test_perf_by = request.POST['test_perf_by']
          nA.test_desc = request.POST['test_desc']
          nA.select = request.POST.get('select')
          nA.select1 = request.POST.get('select1')
          nA.custom_limit = request.POST.get('custom_limit')
          nA.test_method = request.POST.get("test_method")
          nA.test_location = request.POST.get("test_location")
          table_data = []
          index = 1
          while True:
              time_key = f"time_{index}"
              unit_key = f"unit_{index}"
              result_key = f"result_{index}"
              
              if time_key not in request.POST:
                  break
                  
              table_data.append({
                  "time": request.POST.get(time_key),
                  "unit": request.POST.get(unit_key),
                  "result": request.POST.get(result_key),
              })
              index += 1
          nA.table_data = table_data
          nA.start_time = request.POST.get("start_time")
          nA.end_time = request.POST.get("end_time")
          nA.interval = request.POST.get("time_interval")
          nA.legend_1 = request.POST['legend_1']
          nA.legend_2 = request.POST['legend_2']
          nA.legend_3 = request.POST['legend_3']
          nA.legend_4 = request.POST['legend_4']
          nA.legend_5 = request.POST['legend_5']
          nA.legend_6 = request.POST['legend_6']
          nA.legend_7 = request.POST['legend_7']
          nA.legend_8 = request.POST['legend_8']
          nA.legend_9 = request.POST['legend_9']
          nA.legend_10 = request.POST['legend_10']
          nA.legend_11 = request.POST['legend_11']
          nA.editNote = request.POST['editNote']
          nA.customlegend = request.POST['customlegend']
          nA.doc1 = request.POST['doc1']
          nA.doc2 = request.POST['doc2']
          nA.doc3 = request.POST['doc3']
          nA.graph_type = request.POST.get('graph_type')
          nA.created_by = request.user
          # nA.analyzedby = request.FILES['analyzedby']
          # nA.reviewedby = request.FILES['reviewedby']
          # nA.approvedby = request.FILES['approvedby']
          # nA.approvedby1 = request.FILES['approvedby1']
          nA.city_location = request.POST['city_location']
          nA.extra_field = json.loads(request.POST['extra_field'])
          analyst_sign_id = request.POST.get('analyst_sign')
          review_sign_id = request.POST.get('review_sign')
          approved_sign_id = request.POST.get('approved_sign')

          analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
          review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
          approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

          # Assign to ambientUpdate if needed
          nA.analyst_signature = analyst_sign
          nA.assistant_manager_signature = review_sign
          nA.lab_manager_signature = approved_sign
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               areas = request.POST.getlist('areas[]')[i]
               methods = request.POST.getlist('methods[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               nA.extra_field.append({
                         "sr": sr,
                         "areas": areas,
                         "methods": methods,
                         "unit": unit,
                         "result": result,
                         "limit": limit,
                    })        

          nA.pdf_heading=request.POST.get('pdf_heading')
          
          for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)


               if remove_requested == "on":
                    setattr(nA, image_key, '')
                    setattr(nA, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(nA, image_key, base64_encoded)
                         setattr(nA, desc_key, description or '')
                    except Exception as e:
                         pass
               else:
                    if description is not None:
                         setattr(nA, desc_key, description)


          nA.save()
          user = request.user
          action = f'Noise Analysis Form {nA.lab_report_no} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = nA.id
          if "submit_and_view" in request.POST:
               url = f"/noiseMonitoring_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect(to="noiseMonitoring_edit")
     return render(request,"noiseMonitoring_edit.html")
     
@login_required(login_url="/login")
def noiseMonitoring_list(request):
     nA, _srch = _list_filter(request, NoiseMonitoring)
     context = {'data':nA, 'searched':_srch}
     return render(request,"noiseMonitoring_list.html",context)


def noiseMonitoring_print(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_noiseMonitoring_print as PDFWithPageNumbers




     nA= NoiseMonitoring.objects.get(id=pk)
     # nA.extra_field = nA.extra_field.replace("'", "\"")
     # nA.extra_field = json.loads(nA.extra_field)
     
     leq_value = calculate_leq(nA.start_time, nA.end_time, nA.interval, nA.table_data)
     
     limit_mapping = {
     "Residential Day": 55,
     "Residential Night": 45,
     "Commercial Day": 65,
     "Commercial Night": 55,
     "Industrial Day": 75,
     "Industrial Night": 65,
     "Silence Day": 50,
     "Silence Night": 45,
     }

     # Get the selected limit dynamically (default to 55 if no match).
     # "Custom" zone -> analyst-entered dB value, kept numeric for the chart threshold.
     if nA.select1 == "Custom":
          try:
               limit_value = float(nA.custom_limit)
               if limit_value == int(limit_value):
                    limit_value = int(limit_value)
          except (TypeError, ValueError):
               limit_value = 55
     else:
          limit_value = limit_mapping.get(nA.select1, 55)

     # TABLE_DATA = [
     #       ["Sr.#","Time","Unit","Results","Results -* dB(A) Leq",""],
     # ]
     # sr_no = 1
     # for row in nA.table_data:  # assuming nA.table_data is a list of dicts
     #      a = [
     #           str(sr_no),
     #           row.get("time", ""),          # ✅ access dict safely
     #           row.get("unit", ""),
     #           row.get("result", ""),
     #           f"{leq_value}",
     #           str(limit_value) if sr_no == 1 else "",
     #      ]
     #      sr_no += 1
     #      TABLE_DATA.append(a)
     






     pdf = PDFWithPageNumbers(lab_report_no=nA.lab_report_no,invoice_bill_no=nA.invoice_bill_no,reporting_date=nA.reporting_date,report_to=nA.report_to,
                              address=nA.address,attention=nA.attention,email=nA.email,sample_id=nA.sample_id,test_perf_date=nA.test_perf_date,
                              test_desc=nA.test_desc,test_type=nA.test_type,test_perf_by=nA.test_perf_by,select1=nA.select1,test_method=nA.test_method,test_location=nA.test_location,

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True)







          # Your data preparation
     TABLE_DATA = [
     ["Sr.#", "Time", "Unit", "Results", "*dB(A)Leq - (LAeq)", f"{nA.select} Limits"],
     ]

     sr_no = 1
     for row in nA.table_data:
          # Skip if row is None, empty dict, or missing all fields
          if not row or not any(row.values()):
               continue

          a = [
               str(sr_no),
               row.get("time", "").strip(),
               row.get("unit", "").strip(),
               row.get("result", "").strip(),
               str(leq_value),
               str(limit_value),
          ]
          TABLE_DATA.append(a)
          sr_no += 1

     # Configuration
     total_data_rows = len(TABLE_DATA) - 1
    
     # Configuration
     col_widths = [10, 50, 35, 35, 30, 30]
     table_width = sum(col_widths)
     line_height = 8
     left_margin = (pdf.w - table_width) / 2

     def draw_table_page(data_rows, leq_val, limit_val, is_first_page=True):
         """Draw a table page with the given data rows"""
         start_y = pdf.y
         
         # Check if we have enough space
         required_height = (len(data_rows) + 1) * line_height  # +1 for header
         if pdf.y + required_height > pdf.h - 20:
             pdf.add_page()
             start_y = pdf.y
         
         y = start_y
         
         # Draw header
         for i, (width, header) in enumerate(zip(col_widths, TABLE_DATA[0])):
             x = left_margin + sum(col_widths[:i])
             pdf.set_xy(x, y)
             pdf.cell(width, line_height, header, 1, align='C')
         
         y += line_height
         
         # Draw data rows
         for row_idx, data_row in enumerate(data_rows):
             current_y = y + (row_idx * line_height)
             
             # Draw first 4 columns with actual data
             for col_idx in range(4):
                 width = col_widths[col_idx]
                 x = left_margin + sum(col_widths[:col_idx])
                 pdf.set_xy(x, current_y)
                 align = 'C' if col_idx != 1 else 'L'
                 pdf.cell(width, line_height, data_row[col_idx], 1, align=align)
             
             # Draw last 2 columns with leq_value and limit_value (centered vertically)
             if row_idx == 0:  # Only draw these once per page
                 # Column 4: Leq value
                 x4 = left_margin + sum(col_widths[:4])
                 cell_height4 = len(data_rows) * line_height
                 pdf.set_xy(x4, y)
                 pdf.cell(col_widths[4], cell_height4, leq_val, 1, align='C')
                 
                 # Column 5: Limit value
                 x5 = left_margin + sum(col_widths[:5])
                 pdf.set_xy(x5, y)
                 pdf.cell(col_widths[5], cell_height4, limit_val, 1, align='C')
         
         # Draw vertical borders for last 2 columns
         total_data_height = len(data_rows) * line_height
         for col_idx in [4, 5]:
             x = left_margin + sum(col_widths[:col_idx])
             pdf.line(x, y, x, y + total_data_height)
             pdf.line(x + col_widths[col_idx], y, x + col_widths[col_idx], y + total_data_height)
         
         # Draw horizontal lines between data rows (for first 4 columns only)
         for row_idx in range(1, len(data_rows)):
             y_line = y + (row_idx * line_height)
             pdf.line(left_margin, y_line, left_margin + sum(col_widths[:4]), y_line)
         
         # Update Y position and return it for graph placement decision
         final_y = y + total_data_height + 2
         pdf.set_y(final_y)
         return final_y

     # Main logic with pagination
     data_rows = TABLE_DATA[1:]  # Remove header row
     leq_val = f"{leq_value}"
     limit_val = str(limit_value)

     # Calculate how many rows fit per page
     rows_per_page = math.floor((pdf.h - pdf.y - 30) / line_height)  # -30 for margins

     if rows_per_page < 1:
         rows_per_page = 1

     # Split data into pages and draw tables
     current_y_position = pdf.y
     
     for i in range(0, len(data_rows), rows_per_page):
         page_data = data_rows[i:i + rows_per_page]
         current_y_position = draw_table_page(page_data, leq_val, limit_val, i == 0)

     # Determine graph width based on row count
     if total_data_rows <= 4:
         graph_width = 110  # Smaller width for same page
         # Use current position for graph
         graph_start_y = current_y_position
         # Add some spacing
         pdf.set_y(graph_start_y)
     else:
         graph_width = 190  # Full width for new page
         
         graph_start_y = pdf.y

     # Generate chart data
     _rows = [r for r in nA.table_data if r.get("result")]
     result = []
     time_labels = []
     for _r in _rows:
         try:
             result.append(float(_r.get("result", 0)))
         except (TypeError, ValueError):
             continue
         time_labels.append(str(_r.get("time", "")))
     method_limit = nA.select

     
     # data after Table
     Table_Data1 = [
          
     ]
     if nA.editNote:
          a=["Note: "+nA.editNote] 
          Table_Data1.append(a)
          
     
     with pdf.table(col_widths=(190), width=190, line_height=6, text_align=("LEFT")) as table:
          for k in range(0, len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0, len(data_row)):
                    pdf.set_font("Calibri", "", 9)
                    datum = data_row[i]
                    row.cell(datum,border=0)

     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if nA.legend_1:
          a = [nA.legend_1]
          Table_data_legend.append(a)
          
     if nA.legend_2:
          a = [nA.legend_2]
          Table_data_legend.append(a)
          
     if nA.legend_3:
          a = [nA.legend_3]
          Table_data_legend.append(a)
          
     if nA.legend_4:
          a = [nA.legend_4]
          Table_data_legend.append(a)
          
     if nA.legend_5:
          a = [nA.legend_5]
          Table_data_legend.append(a)
          
     if nA.legend_6:
          a = [nA.legend_6]
          Table_data_legend.append(a)
          
     if nA.legend_7:
          a = [nA.legend_7]
          Table_data_legend.append(a)
          
     if nA.legend_8:
          a = [nA.legend_8]
          Table_data_legend.append(a)
          
     if nA.legend_9:
          a = [nA.legend_9]
          Table_data_legend.append(a)
          
     if nA.legend_10:
          a = [nA.legend_10]
          Table_data_legend.append(a)
          
     if nA.legend_11:
          a = [nA.legend_11]
          Table_data_legend.append(a)
          

     if nA.customlegend:
          a = [nA.customlegend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     old_y = pdf.get_y()
     # Calculate X position to center the graph when width is 130
     if graph_width == 110:
        with pdf.local_context(fill_opacity=0.5):
                  pdf.set_font("Arial", "B", 50)
                  pdf.rotate(0)
                  pdf.set_text_color(192, 192, 180) # Light gray text
                  # pdf.set_xy(50, 260)
                  
                  pdf.text(70, 140,pdf.lab_report_no)
                  
                  pdf.rotate(0)
        graph_x = (pdf.w - graph_width) / 2  # Center the graph horizontally
        if nA.graph_type == 'column':
             
             
             
             pdf.set_y(old_y)
             chart_buffer = generate_leq_chart(result, limit_value, method_limit, leq_value, time_labels)
             
             # Add chart title and info
             pdf.set_font("Calibri", "B", 16)
             pdf.cell(0, 10, "", ln=True, align='C')
             pdf.ln(5)
             
             pdf.set_font("Calibri", "B", 16)
             #     pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
             pdf.ln(5)
             
             # Add the chart image to FPDF with conditional width and positioning
             pdf.image(chart_buffer, x=graph_x, y=old_y-4, w=graph_width)
             pdf.ln(85)  # Adjust spacing after image
        
        elif nA.graph_type == 'line':
             
             
             chart_buffer = generate_leq_line_chart(result, limit_value, leq_value, method_limit, time_labels)
             pdf.set_y(old_y)
             # Add chart title and info
             pdf.set_font("Calibri", "B", 16)
             pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
             pdf.ln(5)
             
             # Add the chart image to FPDF with conditional width and positioning
             pdf.image(chart_buffer, x=graph_x, y=old_y-4, w=graph_width)
             pdf.ln(85)  # Adjust spacing after image
     else:
          
          pdf.show_full_header = False
          pdf.add_page()
          
          # Calculate X position to center the graph
          graph_x = (pdf.w - graph_width) / 2  # Center the graph horizontally
          
          pdf.set_y(60)
          
          # Generate and place the graph based on type
          if nA.graph_type == 'column':
               chart_buffer = generate_leq_chart(result, limit_value, method_limit, leq_value, time_labels)
               
               # Add chart title and info
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, "", ln=True, align='C')
               pdf.ln(5)
               
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
               pdf.ln(5)
               
               # Add the chart image to FPDF with centered positioning
               pdf.image(chart_buffer, x=graph_x, y=pdf.get_y(), w=graph_width)
               pdf.ln(85)  # Adjust spacing after image
          
          elif nA.graph_type == 'line':
               pdf.show_full_header = False
               chart_buffer = generate_leq_line_chart(result, limit_value, leq_value, method_limit, time_labels)
               
               # Add chart title and info
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
               pdf.ln(5)
               
               # Add the chart image to FPDF with centered positioning
               pdf.image(chart_buffer, x=graph_x, y=pdf.get_y(), w=graph_width)
               pdf.ln(85)  # Adjust spacing after image
     
     pdf.set_font("Calibri", "B", 10)
     # col_widths = [10, 50, 35, 35, 30, 30]
     # table_width = sum(col_widths)
     # line_height = 8
     # left_margin = (pdf.w - table_width) / 2

     # def draw_table_page(data_rows, leq_val, limit_val, is_first_page=True):
     #      """Draw a table page with the given data rows"""
     #      start_y = pdf.y
          
     #      # Check if we have enough space
     #      required_height = (len(data_rows) + 1) * line_height  # +1 for header
     #      if pdf.y + required_height > pdf.h - 20:
     #           pdf.add_page()
     #           start_y = pdf.y
          
     #      y = start_y
          
     #      # Draw header
     #      for i, (width, header) in enumerate(zip(col_widths, TABLE_DATA[0])):
     #           x = left_margin + sum(col_widths[:i])
     #           pdf.set_xy(x, y)
     #           pdf.cell(width, line_height, header, 1, align='C')
          
     #      y += line_height
          
     #      # Draw data rows
     #      for row_idx, data_row in enumerate(data_rows):
     #           current_y = y + (row_idx * line_height)
               
     #           # Draw first 4 columns with actual data
     #           for col_idx in range(4):
     #                width = col_widths[col_idx]
     #                x = left_margin + sum(col_widths[:col_idx])
     #                pdf.set_xy(x, current_y)
     #                align = 'C' if col_idx != 1 else 'L'
     #                pdf.cell(width, line_height, data_row[col_idx], 1, align=align)
               
     #           # Draw last 2 columns with leq_value and limit_value (centered vertically)
     #           if row_idx == 0:  # Only draw these once per page
     #                # Column 4: Leq value
     #                x4 = left_margin + sum(col_widths[:4])
     #                cell_height4 = len(data_rows) * line_height
     #                pdf.set_xy(x4, y)
     #                pdf.cell(col_widths[4], cell_height4, leq_val, 1, align='C')
                    
     #                # Column 5: Limit value
     #                x5 = left_margin + sum(col_widths[:5])
     #                pdf.set_xy(x5, y)
     #                pdf.cell(col_widths[5], cell_height4, limit_val, 1, align='C')
          
     #      # Draw vertical borders for last 2 columns
     #      total_data_height = len(data_rows) * line_height
     #      for col_idx in [4, 5]:
     #           x = left_margin + sum(col_widths[:col_idx])
     #           pdf.line(x, y, x, y + total_data_height)
     #           pdf.line(x + col_widths[col_idx], y, x + col_widths[col_idx], y + total_data_height)
          
     #      # Draw horizontal lines between data rows (for first 4 columns only)
     #      for row_idx in range(1, len(data_rows)):
     #           y_line = y + (row_idx * line_height)
     #           pdf.line(left_margin, y_line, left_margin + sum(col_widths[:4]), y_line)
          
     #      # Update Y position
     #      pdf.set_y(y + total_data_height + 10)

     # # Main logic with pagination
     # data_rows = TABLE_DATA[1:]  # Remove header row
     # leq_val = f"{leq_value}"
     # limit_val = str(limit_value)

     # # Calculate how many rows fit per page
     # rows_per_page = math.floor((pdf.h - pdf.y - 30) / line_height)  # -30 for margins

     # if rows_per_page < 1:
     #      rows_per_page = 1

     # # Split data into pages
     # for i in range(0, len(data_rows), rows_per_page):
     #      page_data = data_rows[i:i + rows_per_page]
     #      draw_table_page(page_data, leq_val, limit_val, i == 0)



     # #report data table
     # # with pdf.table(col_widths=(10, 50, 30,30,30,30),width=190,line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




     # #      for k, data_row in enumerate(TABLE_DATA):
     # #           # Update last column header dynamically
     # #           if k == 0:
     # #                data_row[5] = f"{nA.select} Limits"

     # #           row = table.row()

     # #           for i, datum in enumerate(data_row):
     # #                # Simulate merged cells for LEQ/Limits (print only on first row)
     # #                if i in (4, 5) and k > 1:
     # #                     # Skip printing for Leq & Limits after first data row
     # #                     datum = ""
     # #                row.cell(datum)
     # pdf.ln(-10)
     # Table_Data1 = [
          
     # ]
     # pdf.set_font("Calibri", "", 9)
     # if nA.editNote:
     #      a=["Note: "+nA.editNote] 
     #      Table_Data1.append(a)
          
     
     # with pdf.table(col_widths=(190), width=190, line_height=6, text_align=("LEFT")) as table:
     #      for k in range(0, len(Table_Data1)):
     #           data_row = Table_Data1[k]
     #           row = table.row()
     #           for i in range(0, len(data_row)):
     #                pdf.set_font("Calibri", "", 9)
     #                datum = data_row[i]
     #                row.cell(datum,border=0)

     # Table_data_legend = [

     # ]     
     # pdf.set_font_size(8)
     # if nA.legend_1:
     #      a = [nA.legend_1]
     #      Table_data_legend.append(a)
          
     # if nA.legend_2:
     #      a = [nA.legend_2]
     #      Table_data_legend.append(a)
          
     # if nA.legend_3:
     #      a = [nA.legend_3]
     #      Table_data_legend.append(a)
          
     # if nA.legend_4:
     #      a = [nA.legend_4]
     #      Table_data_legend.append(a)
          
     # if nA.legend_5:
     #      a = [nA.legend_5]
     #      Table_data_legend.append(a)
          
     # if nA.legend_6:
     #      a = [nA.legend_6]
     #      Table_data_legend.append(a)
          
     # if nA.legend_7:
     #      a = [nA.legend_7]
     #      Table_data_legend.append(a)
          
     # if nA.legend_8:
     #      a = [nA.legend_8]
     #      Table_data_legend.append(a)
          
     # if nA.legend_9:
     #      a = [nA.legend_9]
     #      Table_data_legend.append(a)
          
     # if nA.legend_10:
     #      a = [nA.legend_10]
     #      Table_data_legend.append(a)
          
     # if nA.legend_11:
     #      a = [nA.legend_11]
     #      Table_data_legend.append(a)
          

     # if nA.customlegend:
     #      a = [nA.customlegend]
     #      Table_data_legend.append(a)
     # for k in range(0,len(Table_data_legend)):
     #           data_row = Table_data_legend[k]
     #           row = table.row()
     #           for i in range(0,len(data_row)):
     #                datum = data_row[i]
     #                row.cell(datum)
     #                pdf.cell(190, 4, datum, border=0, ln=True, align='L')

     
     # method_limit = nA.select
     # # column graph
     # if nA.graph_type =='column':
     #      pdf.show_full_header = False
     #      pdf.add_page()
     #      pdf.set_y(60)
     #      # Generate chart
     #      result = [float(row.get("result", 0)) for row in nA.table_data if row.get("result")]
     #      time_labels = [str(row.get("time", "")) for row in nA.table_data if row.get("time")]
     #      chart_buffer = generate_leq_chart(result, limit_value,method_limit,time_labels)
          
     #      # Add chart title and info
     #      pdf.set_font("Calibri", "B", 16)
     #      pdf.cell(0, 10, "", ln=True, align='C')
     #      pdf.ln(5)
          
     #      pdf.set_font("Calibri", "B", 16)
     #      pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
     #      pdf.ln(5)
          
     #      pdf.set_font("Calibri", "B", 14)
     #      pdf.cell(0, 10, f"", ln=True)
     #      pdf.ln(5)
          
     #      # Add the chart image to FPDF
     #      pdf.image(chart_buffer, x=10, y=pdf.get_y(), w=190)
     #      pdf.ln(85)  # Adjust spacing after image
          
          
     # elif nA.graph_type == 'line':
     #      # Generate chart
     #      pdf.show_full_header = False
     #      pdf.add_page()
     #      pdf.set_y(60)
     #      result = [float(row.get("result", 0)) for row in nA.table_data if row.get("result")]
     #      time_labels = [str(row.get("time", "")) for row in nA.table_data if row.get("time")]
     #      chart_buffer = generate_leq_line_chart(result, limit_value,leq_value,method_limit,time_labels)
          
     #      # Add chart title and info
     #      pdf.set_font("Calibri", "B", 16)
     #      pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
     #      pdf.ln(5)
          
     #      # pdf.set_font("Calibri", "", 12)
     #      # pdf.cell(0, 10, f"Limit Value: {limit_value} dB(A)", ln=True)
     #      # pdf.ln(5)
          
     #      pdf.set_font("Calibri", "B", 14)
     #      pdf.cell(0, 10, f"", ln=True)
     #      pdf.ln(5)
          
     #      # Add the chart image to FPDF
     #      pdf.image(chart_buffer, x=10, y=pdf.get_y(), w=190)
     #      pdf.ln(85)  # Adjust spacing after image
          
         

     


     # pdf.image(nA.analyst_signature.signature,30,238,20.32,20.32)
     # pdf.line(19,257,36+pdf.get_string_width("Analyzed By (Analyst)"),257)
     # pdf.text(26,261,"Analyzed By (Analyst)")
     # pdf.image(nA.assistant_manager_signature.signature,100,239,20.32,20.32)
     # pdf.line(126,257,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),257)
     # pdf.text(87.5,261,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,233,22,22)
     # pdf.image(nA.lab_manager_signature.signature,178,239,20.32,20.32)
     # pdf.line(155,257,165+pdf.get_string_width("Approved By (Lab Manager)"),257)
     # pdf.text(160,261,"Approved By (Lab Manager)")
     pdf.set_font("Calibri", "B", 10)
     if nA.analyst_signature:
         pdf.image(nA.analyst_signature.signature,30,238,20.32,20.32)
     pdf.line(19,257,36+pdf.get_string_width(f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})"),257)
     pdf.text(26,261,f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})")
     if nA.assistant_manager_signature:
         pdf.image(nA.assistant_manager_signature.signature,100,239,20.32,20.32)
     pdf.line(126,257,47.5+pdf.get_string_width(f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})"),257)
     pdf.text(87.5,261,f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,233,22,22)
     if nA.lab_manager_signature:
         pdf.image(nA.lab_manager_signature.signature,178,233,20.32,20.32)
     pdf.line(155,257,165+pdf.get_string_width(f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})"),257)
     pdf.text(160,261,f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})")


     pdf.set_font("Calibri","B", 9)
     pdf.line(10,263,-10+pdf.w,263)
     pdf.text(10,266,txt="Disclaimer:")
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
     # if nA.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if nA.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,263,21,17) 
     # if nA.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
     # if nA.location =='PEQS':
     #      pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,264,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(128.5,281,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,281,txt="(Certificate # 080177424-EMS)")
     
     if nA.location == "NEQS" and nA.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 264, 19, 15)
          pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")

     elif nA.location == "NEQS" and nA.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 155, 263, 21, 17)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     elif nA.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,264,19,15)
          pdf.text(152,281,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     elif nA.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',155,263,21,17)
          pdf.text(155,281,txt="(82/Dir/(ML&I)/EPA/03/2025)")
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
     pdf.text(127,285,txt=nA.doc1)
     pdf.rect(151,282,29,5)
     pdf.text(155,285,txt=nA.doc2)
     pdf.rect(180,282,25,5)
     pdf.text(186.5,285,txt=nA.doc3)
     
     if nA.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(nA, f'pdf_image_{i}')
               desc = getattr(nA, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=nA.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/noiseAnalysis/'
     # pdf.output(file_path + nA.lab_report_no +'.pdf')
     # pdf = open(file_path + nA.lab_report_no +'.pdf', 'rb')

     # # pdf.output(nA.lab_report_no +'.pdf')

     # # pdf = open(nA.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={nA.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def noiseMonitoring_report(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_noiseMonitoring_report as PDFWithPageNumbers




     nA= NoiseMonitoring.objects.get(id=pk)
     # nA.extra_field = nA.extra_field.replace("'", "\"")
     # nA.extra_field = json.loads(nA.extra_field)
     
     leq_value = calculate_leq(nA.start_time, nA.end_time, nA.interval, nA.table_data)
     
     limit_mapping = {
     "Residential Day": 55,
     "Residential Night": 45,
     "Commercial Day": 65,
     "Commercial Night": 55,
     "Industrial Day": 75,
     "Industrial Night": 65,
     "Silence Day": 50,
     "Silence Night": 45,
     }

     # Get the selected limit dynamically (default to 55 if no match).
     # "Custom" zone -> analyst-entered dB value, kept numeric for the chart threshold.
     if nA.select1 == "Custom":
          try:
               limit_value = float(nA.custom_limit)
               if limit_value == int(limit_value):
                    limit_value = int(limit_value)
          except (TypeError, ValueError):
               limit_value = 55
     else:
          limit_value = limit_mapping.get(nA.select1, 55)





     pdf = PDFWithPageNumbers(lab_report_no=nA.lab_report_no,invoice_bill_no=nA.invoice_bill_no,reporting_date=nA.reporting_date,report_to=nA.report_to,
                              address=nA.address,attention=nA.attention,email=nA.email,sample_id=nA.sample_id,test_perf_date=nA.test_perf_date,
                              test_desc=nA.test_desc,test_type=nA.test_type,test_perf_by=nA.test_perf_by,select1=nA.select1,test_method=nA.test_method,test_location=nA.test_location,

                              )
     pdf._rq_request, pdf._rq_pk = request, pk
     pdf.add_page()
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True)












     # Your data preparation
     TABLE_DATA = [
     ["Sr.#", "Time", "Unit", "Results", "*dB(A)Leq - (LAeq)", f"{nA.select} Limits"],
     ]

     sr_no = 1
     for row in nA.table_data:
          # Skip if row is None, empty dict, or missing all fields
          if not row or not any(row.values()):
               continue

          a = [
               str(sr_no),
               row.get("time", "").strip(),
               row.get("unit", "").strip(),
               row.get("result", "").strip(),
               str(leq_value),
               str(limit_value),
          ]
          TABLE_DATA.append(a)
          sr_no += 1

     # Configuration
     total_data_rows = len(TABLE_DATA) - 1
    
     # Configuration
     col_widths = [10, 50, 35, 35, 30, 30]
     table_width = sum(col_widths)
     line_height = 8
     left_margin = (pdf.w - table_width) / 2

     def draw_table_page(data_rows, leq_val, limit_val, is_first_page=True):
         """Draw a table page with the given data rows"""
         start_y = pdf.y
         
         # Check if we have enough space
         required_height = (len(data_rows) + 1) * line_height  # +1 for header
         if pdf.y + required_height > pdf.h - 20:
             pdf.add_page()
             start_y = pdf.y
         
         y = start_y
         
         # Draw header
         for i, (width, header) in enumerate(zip(col_widths, TABLE_DATA[0])):
             x = left_margin + sum(col_widths[:i])
             pdf.set_xy(x, y)
             pdf.cell(width, line_height, header, 1, align='C')
         
         y += line_height
         
         # Draw data rows
         for row_idx, data_row in enumerate(data_rows):
             current_y = y + (row_idx * line_height)
             
             # Draw first 4 columns with actual data
             for col_idx in range(4):
                 width = col_widths[col_idx]
                 x = left_margin + sum(col_widths[:col_idx])
                 pdf.set_xy(x, current_y)
                 align = 'C' if col_idx != 1 else 'L'
                 pdf.cell(width, line_height, data_row[col_idx], 1, align=align)
             
             # Draw last 2 columns with leq_value and limit_value (centered vertically)
             if row_idx == 0:  # Only draw these once per page
                 # Column 4: Leq value
                 x4 = left_margin + sum(col_widths[:4])
                 cell_height4 = len(data_rows) * line_height
                 pdf.set_xy(x4, y)
                 pdf.cell(col_widths[4], cell_height4, leq_val, 1, align='C')
                 
                 # Column 5: Limit value
                 x5 = left_margin + sum(col_widths[:5])
                 pdf.set_xy(x5, y)
                 pdf.cell(col_widths[5], cell_height4, limit_val, 1, align='C')
         
         # Draw vertical borders for last 2 columns
         total_data_height = len(data_rows) * line_height
         for col_idx in [4, 5]:
             x = left_margin + sum(col_widths[:col_idx])
             pdf.line(x, y, x, y + total_data_height)
             pdf.line(x + col_widths[col_idx], y, x + col_widths[col_idx], y + total_data_height)
         
         # Draw horizontal lines between data rows (for first 4 columns only)
         for row_idx in range(1, len(data_rows)):
             y_line = y + (row_idx * line_height)
             pdf.line(left_margin, y_line, left_margin + sum(col_widths[:4]), y_line)
         
         # Update Y position and return it for graph placement decision
         final_y = y + total_data_height + 2
         pdf.set_y(final_y)
         return final_y

     # Main logic with pagination
     data_rows = TABLE_DATA[1:]  # Remove header row
     leq_val = f"{leq_value}"
     limit_val = str(limit_value)

     # Calculate how many rows fit per page
     rows_per_page = math.floor((pdf.h - pdf.y - 30) / line_height)  # -30 for margins

     if rows_per_page < 1:
         rows_per_page = 1

     # Split data into pages and draw tables
     current_y_position = pdf.y
     
     for i in range(0, len(data_rows), rows_per_page):
         page_data = data_rows[i:i + rows_per_page]
         current_y_position = draw_table_page(page_data, leq_val, limit_val, i == 0)

     # Determine graph width based on row count
     if total_data_rows <= 4:
         graph_width = 90  # Smaller width for same page
         # Use current position for graph
         graph_start_y = current_y_position
         # Add some spacing
         pdf.set_y(graph_start_y)
     else:
         graph_width = 190  # Full width for new page
         
         graph_start_y = pdf.y

     # Generate chart data
     _rows = [r for r in nA.table_data if r.get("result")]
     result = []
     time_labels = []
     for _r in _rows:
         try:
             result.append(float(_r.get("result", 0)))
         except (TypeError, ValueError):
             continue
         time_labels.append(str(_r.get("time", "")))
     method_limit = nA.select

     
     # data after Table
     Table_Data1 = [
          
     ]
     if nA.editNote:
          a=["Note: "+nA.editNote] 
          Table_Data1.append(a)
          
     
     with pdf.table(col_widths=(190), width=190, line_height=6, text_align=("LEFT")) as table:
          for k in range(0, len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0, len(data_row)):
                    pdf.set_font("Calibri", "", 9)
                    datum = data_row[i]
                    row.cell(datum,border=0)

     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if nA.legend_1:
          a = [nA.legend_1]
          Table_data_legend.append(a)
          
     if nA.legend_2:
          a = [nA.legend_2]
          Table_data_legend.append(a)
          
     if nA.legend_3:
          a = [nA.legend_3]
          Table_data_legend.append(a)
          
     if nA.legend_4:
          a = [nA.legend_4]
          Table_data_legend.append(a)
          
     if nA.legend_5:
          a = [nA.legend_5]
          Table_data_legend.append(a)
          
     if nA.legend_6:
          a = [nA.legend_6]
          Table_data_legend.append(a)
          
     if nA.legend_7:
          a = [nA.legend_7]
          Table_data_legend.append(a)
          
     if nA.legend_8:
          a = [nA.legend_8]
          Table_data_legend.append(a)
          
     if nA.legend_9:
          a = [nA.legend_9]
          Table_data_legend.append(a)
          
     if nA.legend_10:
          a = [nA.legend_10]
          Table_data_legend.append(a)
          
     if nA.legend_11:
          a = [nA.legend_11]
          Table_data_legend.append(a)
          

     if nA.customlegend:
          a = [nA.customlegend]
          Table_data_legend.append(a)
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     old_y = pdf.get_y()
     # Calculate X position to center the graph when width is 130
     if graph_width == 90:
        graph_x = (pdf.w - graph_width) / 2  # Center the graph horizontally
        if nA.graph_type == 'column':
             
             pdf.set_y(old_y)
             chart_buffer = generate_leq_chart(result, limit_value, method_limit, leq_value, time_labels)
             
             # Add chart title and info
             pdf.set_font("Calibri", "B", 16)
             pdf.cell(0, 10, "", ln=True, align='C')
             pdf.ln(5)
             
             pdf.set_font("Calibri", "B", 16)
             #     pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
             pdf.ln(5)
             
             # Add the chart image to FPDF with conditional width and positioning
             pdf.image(chart_buffer, x=graph_x, y=old_y-4, w=graph_width)
             pdf.ln(85)  # Adjust spacing after image
        
        elif nA.graph_type == 'line':
             
             
             chart_buffer = generate_leq_line_chart(result, limit_value, leq_value, method_limit, time_labels)
             pdf.set_y(old_y)
             # Add chart title and info
             pdf.set_font("Calibri", "B", 16)
          #    pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
             pdf.ln(5)
             
             # Add the chart image to FPDF with conditional width and positioning
             pdf.image(chart_buffer, x=graph_x, y=old_y-4, w=graph_width)
             pdf.ln(85)  # Adjust spacing after image
     else:
          pdf.show_full_header = False
          pdf.add_page()
          
          # Calculate X position to center the graph
          graph_x = (pdf.w - graph_width) / 2  # Center the graph horizontally
          
          pdf.set_y(60)
          
          # Generate and place the graph based on type
          if nA.graph_type == 'column':
               chart_buffer = generate_leq_chart(result, limit_value, method_limit, leq_value, time_labels)
               
               # Add chart title and info
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, "", ln=True, align='C')
               pdf.ln(5)
               
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
               pdf.ln(5)
               
               # Add the chart image to FPDF with centered positioning
               pdf.image(chart_buffer, x=graph_x, y=pdf.get_y(), w=graph_width)
               pdf.ln(85)  # Adjust spacing after image
          
          elif nA.graph_type == 'line':
               pdf.show_full_header = False
               chart_buffer = generate_leq_line_chart(result, limit_value, leq_value, method_limit, time_labels)
               
               # Add chart title and info
               pdf.set_font("Calibri", "B", 16)
               pdf.cell(0, 10, f"Graphical Representation of {nA.test_type}", ln=True, align='C')
               pdf.ln(5)
               
               # Add the chart image to FPDF with centered positioning
               pdf.image(chart_buffer, x=graph_x, y=pdf.get_y(), w=graph_width)
               pdf.ln(85)  # Adjust spacing after image
     
     pdf.set_font("Calibri", "B", 10)



     # pdf.image(nA.analyst_signature.signature,30,233,20.32,20.32)
     # pdf.line(19,252,36+pdf.get_string_width("Analyzed By (Analyst)"),252)
     # pdf.text(26,256,"Analyzed By (Analyst)")
     # pdf.image(nA.assistant_manager_signature.signature,100,234,20.32,20.32)
     # pdf.line(126,252,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),252)
     # pdf.text(87.5,256,"Reviewed By (Assistant Manager)")
     # pdf.image(envitech_logo,154,228,22,22)
     # pdf.image(nA.lab_manager_signature.signature,178,233,20.32,20.32)
     # pdf.line(155,252,165+pdf.get_string_width("Approved By (Lab Manager)"),252)
     # pdf.text(160,256,"Approved By (Lab Manager)")
     
     if nA.analyst_signature:
         pdf.image(nA.analyst_signature.signature,30,233,20.32,20.32)
     pdf.line(19,252,36+pdf.get_string_width(f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})"),252)
     pdf.text(26,256,f"Analyzed By ({(nA.analyst_signature.role if nA.analyst_signature else '')})")
     if nA.assistant_manager_signature:
         pdf.image(nA.assistant_manager_signature.signature,100,233,20.32,20.32)
     pdf.line(126,252,47.5+pdf.get_string_width(f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})"),252)
     pdf.text(87.5,256,f"Reviewed By ({(nA.assistant_manager_signature.role if nA.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if nA.lab_manager_signature:
         pdf.image(nA.lab_manager_signature.signature,178,228,20.32,20.32)
     pdf.line(155,252,165+pdf.get_string_width(f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})"),252)
     pdf.text(160,256,f"Approved By ({(nA.lab_manager_signature.role if nA.lab_manager_signature else '')})")


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
     # if nA.location == 'SEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if nA.location == 'PEQS':
     #      pdf.image('static/assets/EPA_updated.png',155,258,21,17) 
     # if nA.location == 'NEQS':
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
     # if nA.location =='PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     # pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     # pdf.set_font("Calibri","B", 5)
     # pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     # pdf.text(182,276,txt="(Certificate # 080177424-EMS)")
     
     
     if nA.location == "NEQS" and nA.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")

     elif nA.location == "NEQS" and nA.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 155, 258, 21, 17)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     elif nA.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     elif nA.location == "PEQS":
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
     pdf.text(128,280,txt=nA.doc1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=nA.doc2)
     pdf.rect(180,277,25,5)
     pdf.text(186.5,280,txt=nA.doc3)
     
     
     if nA.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(nA, f'pdf_image_{i}')
               desc = getattr(nA, f'pdf_desc_{i}')
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
          
          
          pdf.multi_cell(190,10,txt=nA.pdf_heading,align="C")
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

     # file_path = '/home/django/EnviTechAlApp/na_pdf/'
     # pdf.output(file_path + nA.lab_report_no +'.pdf')

     # pdf = open(file_path + nA.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={nA.lab_report_no}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def noiseAnalysisclone(request,pk):
     existing_form = NoiseAnalysis.objects.get(id=pk)
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
     return render(request,"noiseAnalysisClone.html",context)

def noiseAnalysiscloneSave(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = NoiseAnalysis.objects.get(id=pk)
     except NoiseAnalysis.DoesNotExist:
         return HttpResponse("Form not found", status=404)
     if request.method == 'POST':
          existing_Form.location = request.POST['location']
          industry_id = request.POST.get('industry')
          existing_Form.industry = Industry_sector.objects.get(id=industry_id) if industry_id else None
          existing_Form.lab_report_no = request.POST['lab_rep_no']
          existing_Form.invoice_bill_no = request.POST['invoice_no']
          existing_Form.reporting_date = request.POST['rep_date']
          existing_Form.report_to = request.POST['report_to']
          existing_Form.address = request.POST['address']
          existing_Form.attention = request.POST['attention']
          existing_Form.email = request.POST['email']
          existing_Form.sample_id = request.POST['testId']
          existing_Form.test_perf_date = request.POST['test_perf_date']
          existing_Form.test_type = request.POST['test_type']
          existing_Form.test_perf_by = request.POST['test_perf_by']
          existing_Form.test_desc = request.POST['test_desc']
          existing_Form.select = request.POST.get('select')
          existing_Form.select1 = request.POST.get('select1')
          existing_Form.custom_limit = request.POST.get('custom_limit')
          existing_Form.r1 = request.POST['r1']
          existing_Form.r1_1 = request.POST['r1_1']
          existing_Form.r2 = request.POST['r2']
          existing_Form.r2_2 = request.POST['r2_2']
          existing_Form.r3 = request.POST['r3']
          existing_Form.r3_3 = request.POST['r3_3']
          existing_Form.r4 = request.POST['r4']
          existing_Form.r4_4 = request.POST['r4_4']
          existing_Form.r5 = request.POST['r5']
          existing_Form.r5_5 = request.POST['r5_5']
          existing_Form.r6 = request.POST['r6']
          existing_Form.r6_6 = request.POST['r6_6']
          existing_Form.r7 = request.POST['r7']
          existing_Form.r7_7 = request.POST['r7_7']
          existing_Form.r8 = request.POST['r8']
          existing_Form.r8_8 = request.POST['r8_8']
          existing_Form.r9 = request.POST['r9']
          existing_Form.r9_9 = request.POST['r9_9']
          existing_Form.r10 = request.POST['r10']
          existing_Form.r10_10 = request.POST['r10_10']
          existing_Form.r11 = request.POST['r11']
          existing_Form.r11_11 = request.POST['r11_11']
          existing_Form.r12 = request.POST['r12']
          existing_Form.r12_12 = request.POST['r12_12']
          existing_Form.r13 = request.POST['r13']
          existing_Form.r13_13 = request.POST['r13_13']
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
          existing_Form.city_location = request.POST['city_location']
          existing_Form.extra_field = json.loads(request.POST['extra_field'])
          for i in range(len(request.POST.getlist('sr[]'))):
               sr = request.POST.getlist('sr[]')[i]
               areas = request.POST.getlist('areas[]')[i]
               methods = request.POST.getlist('methods[]')[i]
               unit = request.POST.getlist('unit[]')[i]
               result = request.POST.getlist('result[]')[i]
               limit = request.POST.getlist('limit[]')[i]            

               existing_Form.extra_field.append({
                         "sr": sr,
                         "areas": areas,
                         "methods": methods,
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
          action = f'Noise Analysis Form {existing_Form.lab_report_no} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Operation was successful!')
          id = existing_Form.id
          if "submit_and_view" in request.POST:
              url = f"/noiseAnalysis-view/{str(id)}/"
              return redirect(to=url)
          
          if "submit_and_new" in request.POST:
               # context = {'list': new_dw}
              return redirect(to='noiseAnalysisList')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "noiseAnalysisClone.html")

__all__ = [
    'noiseAnalysis',
    'noiseAnalysisList',
    'noiseAnalysisDelete',
    'noiseAnalysisEdit',
    'noiseAnalysisUpdate',
    'noiseAnalysisView',
    'noiseAnalysisReport',
    'noiseAnalysisReport1',
    'noisemonitoring',
    'noiseMonitoring_view',
    'noiseMonitoring_clone',
    'noiseMonitoring_clone_update',
    'noiseMonitoring_edit',
    'noiseMonitoring_edit_update',
    'noiseMonitoring_list',
    'noiseMonitoring_print',
    'noiseMonitoring_report',
    'noiseAnalysisclone',
    'noiseAnalysiscloneSave',
]
