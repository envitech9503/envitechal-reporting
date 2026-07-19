# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403




@login_required(login_url="/login")
def verification(request):
     if request.method == 'POST':
          cert_num = request.POST['cert_num']
          client = request.POST['client']
          address = request.POST['address']
          date = request.POST['verif_date']
          re_verif_date = request.POST['re_verif_date']
          param1 = request.POST['param1']
          param = request.POST['param']
          equipment = request.POST['equipment']
          manufacturer = request.POST['Manufacturer']
          equip_id = request.POST['equip_id']
          model = request.POST['model']
          equipment_1 = request.POST['equipment_1']
          model_1 = request.POST['model_1']
          serial_no1 = request.POST['serial_no1']
          cert_num1 = request.POST['cert_num1']
          equipment_2 = request.POST['equipment_2']
          model_2 = request.POST['model_2']
          serial_no2 = request.POST['serial_no2']
          cert_num2 = request.POST['cert_num2']
          test1 = request.POST['test1']
          test2 = request.POST['test2']

          test_1 = request.POST['test_1']
          equip_des1 = request.POST['equip_des1']
          obser1 = request.POST['obser1']
          dev1 = request.POST['dev1']

          test_2 = request.POST['test_2']
          equip_des2 = request.POST['equip_des2']
          obser2 = request.POST['obser2']
          dev2 = request.POST['dev2']

          test_3 = request.POST['test_3']
          equip_des3 = request.POST['equip_des3']
          obser3 = request.POST['obser3']
          dev3 = request.POST['dev3']

          test_4 = request.POST['test_4']
          equip_des4 = request.POST['equip_des4']
          obser4 = request.POST['obser4']
          dev4 = request.POST['dev4']

          test_5 = request.POST['test_5']
          equip_des5 = request.POST['equip_des5']
          obser5 = request.POST['obser5']
          dev5 = request.POST['dev5']

          test_6 = request.POST['test_6']
          equip_des6 = request.POST['equip_des6']
          obser6 = request.POST['obser6']
          dev6 = request.POST['dev6']

          test_7 = request.POST['test_7']
          equip_des7 = request.POST['equip_des7']
          obser7 = request.POST['obser7']
          dev7 = request.POST['dev7']

          conc = request.POST['conc']
          verif_status = request.POST['verif_status']
          text = request.POST['text']
          # verif_by = request.FILES['verif_by']
          # checked = request.FILES['checked']
          # checked1 = request.FILES['checked1']
          disc = request.POST['disc']
          extra_field = request.POST['extra_field']
          extra_field1 = request.POST['extra_field1']
          city_location = request.POST['city_location']
          verif_by_id = request.POST.get('verif_sign')
          check_sign_id = request.POST.get('check_sign')
          
          check1_signature = Signatures.objects.get(id=check_sign_id)
          verif_by_signature = Signatures.objects.get(id=verif_by_id)
          
          
          verif = Verification(cert_num=cert_num,client=client,address=address,date=date,re_verif_date=re_verif_date,
                              param1=param1,param=param,equipment=equipment,manufacturer=manufacturer,equip_id=equip_id,model=model,equipment_1=equipment_1,
                              model_1=model_1,serial_no1=serial_no1,cert_num1=cert_num1,equipment_2=equipment_2,model_2=model_2,serial_no2=serial_no2,
                              cert_num2=cert_num2,test1=test1,test2=test2,test_1=test_1,equip_des1=equip_des1,obser1=obser1,dev1=dev1,test_2=test_2,
                              equip_des2=equip_des2,obser2=obser2,dev2=dev2,test_3=test_3,equip_des3=equip_des3,obser3=obser3,dev3=dev3,test_4=test_4,
                              equip_des4=equip_des4,obser4=obser4,dev4=dev4,test_5=test_5,equip_des5=equip_des5,obser5=obser5,dev5=dev5,test_6=test_6,
                              equip_des6=equip_des6,obser6=obser6,dev6=dev6,test_7=test_7,equip_des7=equip_des7,obser7=obser7,dev7=dev7,conc=conc,verif_status=verif_status,
                              text=text,disc=disc,extra_field=extra_field,extra_field1=extra_field1,city_location=city_location,verif_by_signature=verif_by_signature,check1_signature=check1_signature,created_by = request.user
                              )
          verif.save()
          
          
          user = request.user
          action = f'Verification certificate {verif.cert_num} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = (Verification.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/verification_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return render(request, "verification.html")
     else:
          return render(request, "verification.html",{'signs':signs})



@login_required(login_url="/login")
def verif_delete(request,pk):
     verif = Verification.objects.get(id=pk)
     verif.delete()
     user = request.user
     action = f'Verification certificate {verif.cert_num} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     return redirect('verification_list')


@login_required(login_url="/login")
def verification_list(request):
     verif, _srch = _cert_filter(request, Verification)
     context = {'searched':_srch, 'data':verif}          
     return render(request,'verif_list.html',context)

@login_required(login_url="/login")
def verif_edit(request,pk):
     verif = Verification.objects.get(id=pk)
     verif.extra_field = verif.extra_field.replace("'", "\"")
     verif.extra_field = json.loads(verif.extra_field)
     verif.extra_field1 = verif.extra_field1.replace("'", "\"")
     verif.extra_field1 = json.loads(verif.extra_field1)
     context = {'data':verif,'signs':signs}
     return render(request,'verif_edit.html',context)     


@login_required(login_url="/login")
def verif_update(request,pk):
     verif = Verification.objects.get(id=pk)
     if request.method == 'POST':   
          verif.cert_num = request.POST['cert_num']
          verif.client = request.POST['client']
          verif.address = request.POST['address']
          verif.date = request.POST['verif_date']
          verif.re_verif_date = request.POST['re_verif_date']
          verif.param1 = request.POST['param1']
          verif.param = request.POST['param']
          verif.equipment = request.POST['equipment']
          verif.manufacturer = request.POST['Manufacturer']
          verif.equip_id = request.POST['equip_id']
          verif.model = request.POST['model']
          verif.equipment_1 = request.POST['equipment_1']
          verif.model_1 = request.POST['model_1']
          verif.serial_no1 = request.POST['serial_no1']
          verif.cert_num1 = request.POST['cert_num1']
          verif.equipment_2 = request.POST['equipment_2']
          verif.model_2 = request.POST['model_2']
          verif.serial_no2 = request.POST['serial_no2']
          verif.cert_num2 = request.POST['cert_num2']
          verif.test1 = request.POST['test1']
          verif.test2 = request.POST['test2']
          verif.test_1 = request.POST['test_1']
          verif.equip_des1 = request.POST['equip_des1']
          verif.obser1 = request.POST['obser1']
          verif.dev1 = request.POST['dev1']
          verif.test_2 = request.POST['test_2']
          verif.equip_des2 = request.POST['equip_des2']
          verif.obser2 = request.POST['obser2']
          verif.dev2 = request.POST['dev2']
          verif.test_3 = request.POST['test_3']
          verif.equip_des3 = request.POST['equip_des3']
          verif.obser3 = request.POST['obser3']
          verif.dev3 = request.POST['dev3']
          verif.test_4 = request.POST['test_4']
          verif.equip_des4 = request.POST['equip_des4']
          verif.obser4 = request.POST['obser4']
          verif.dev4 = request.POST['dev4']
          verif.test_5 = request.POST['test_5']
          verif.equip_des5 = request.POST['equip_des5']
          verif.obser5 = request.POST['obser5']
          verif.dev5 = request.POST['dev5']
          verif.test_6 = request.POST['test_6']
          verif.equip_des6 = request.POST['equip_des6']
          verif.obser6 = request.POST['obser6']
          verif.dev6 = request.POST['dev6']
          verif.test_7 = request.POST['test_7']
          verif.equip_des7 = request.POST['equip_des7']
          verif.obser7 = request.POST['obser7']
          verif.dev7 = request.POST['dev7']
          verif.conc = request.POST['conc']
          verif.verif_status = request.POST['verif_status']
          verif.text = request.POST['text']
          # verif.verif_by = request.FILES['verif_by']
          # verif.checked = request.FILES['checked']
          # verif.checked1 = request.FILES['checked1']
          verif.disc = request.POST['disc']  
          verif.city_location = request.POST['city_location'] 
          verif.extra_field = json.loads(request.POST["extra_field"])
          
          if verif.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    test = request.POST.getlist('test[]')[i]
                    equip = request.POST.getlist('equip[]')[i]
                    obser = request.POST.getlist('obser[]')[i]
                    dev = request.POST.getlist('dev[]')[i]

                    verif.extra_field.append({
                         'sr':sr,
                         'test':test,
                         'equip':equip,
                         'obser':obser,
                         'dev':dev,
                    })
          
          
          verif.extra_field = json.dumps(verif.extra_field)
          
          

          verif.extra_field1 = json.loads(request.POST["extra_field1"])
          
          if verif.extra_field1:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp1 = request.POST.getlist('inp1[]')[i]
                    inp2 = request.POST.getlist('inp2[]')[i]
                    inp3 = request.POST.getlist('inp3[]')[i]
                    inp4 = request.POST.getlist('inp4[]')[i]

                    verif.extra_field1.append({
                         'sr':sr,
                         'inp1':inp1,
                         'inp2':inp2,
                         'inp3':inp3,
                         'inp4':inp4,
                    })
          
          
          verif.extra_field1 = json.dumps(verif.extra_field1)
          
          verif_by_id = request.POST.get('verif_sign')
          check_sign_id = request.POST.get('check_sign')
          
          check1_signature = Signatures.objects.get(id=check_sign_id)
          verif_by_signature = Signatures.objects.get(id=verif_by_id)
          verif.check1_signature =check1_signature
          verif.check_sign_id =check_sign_id
          verif.created_by = request.user
          verif.save()
          user = request.user
          action = f'Verification certificate {verif.cert_num} editied by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = verif.id
          if "submit_and_view" in request.POST:
               url = f'/verification_view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('verification_list')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return render(request,"verif_list.html")                   


@login_required(login_url="/login")
def verif_clone(request,pk):
     verif = Verification.objects.get(id=pk)
     verif.extra_field = verif.extra_field.replace("'", "\"")
     verif.extra_field = json.loads(verif.extra_field)
     verif.extra_field1 = verif.extra_field1.replace("'", "\"")
     verif.extra_field1 = json.loads(verif.extra_field1)
     context = {'data':verif,'signs':signs}
     return render(request,'verif_clone.html',context) 


@login_required(login_url="/login")
def verif_clone_update(request,pk):
     try:
        # Fetch the existing form instance by ID
         existing_Form = Verification.objects.get(id=pk)
     except Verification.DoesNotExist:
         return HttpResponse("Form not found", status=404)  
     if request.method == 'POST':   
          existing_Form.cert_num = request.POST['cert_num']
          existing_Form.client = request.POST['client']
          existing_Form.address = request.POST['address']
          existing_Form.date = request.POST['verif_date']
          existing_Form.re_verif_date = request.POST['re_verif_date']
          existing_Form.param1 = request.POST['param1']
          existing_Form.param = request.POST['param']
          existing_Form.equipment = request.POST['equipment']
          existing_Form.manufacturer = request.POST['Manufacturer']
          existing_Form.equip_id = request.POST['equip_id']
          existing_Form.model = request.POST['model']
          existing_Form.equipment_1 = request.POST['equipment_1']
          existing_Form.model_1 = request.POST['model_1']
          existing_Form.serial_no1 = request.POST['serial_no1']
          existing_Form.cert_num1 = request.POST['cert_num1']
          existing_Form.equipment_2 = request.POST['equipment_2']
          existing_Form.model_2 = request.POST['model_2']
          existing_Form.serial_no2 = request.POST['serial_no2']
          existing_Form.cert_num2 = request.POST['cert_num2']
          existing_Form.test1 = request.POST['test1']
          existing_Form.test2 = request.POST['test2']
          existing_Form.test_1 = request.POST['test_1']
          existing_Form.equip_des1 = request.POST['equip_des1']
          existing_Form.obser1 = request.POST['obser1']
          existing_Form.dev1 = request.POST['dev1']
          existing_Form.test_2 = request.POST['test_2']
          existing_Form.equip_des2 = request.POST['equip_des2']
          existing_Form.obser2 = request.POST['obser2']
          existing_Form.dev2 = request.POST['dev2']
          existing_Form.test_3 = request.POST['test_3']
          existing_Form.equip_des3 = request.POST['equip_des3']
          existing_Form.obser3 = request.POST['obser3']
          existing_Form.dev3 = request.POST['dev3']
          existing_Form.test_4 = request.POST['test_4']
          existing_Form.equip_des4 = request.POST['equip_des4']
          existing_Form.obser4 = request.POST['obser4']
          existing_Form.dev4 = request.POST['dev4']
          existing_Form.test_5 = request.POST['test_5']
          existing_Form.equip_des5 = request.POST['equip_des5']
          existing_Form.obser5 = request.POST['obser5']
          existing_Form.dev5 = request.POST['dev5']
          existing_Form.test_6 = request.POST['test_6']
          existing_Form.equip_des6 = request.POST['equip_des6']
          existing_Form.obser6 = request.POST['obser6']
          existing_Form.dev6 = request.POST['dev6']
          existing_Form.test_7 = request.POST['test_7']
          existing_Form.equip_des7 = request.POST['equip_des7']
          existing_Form.obser7 = request.POST['obser7']
          existing_Form.dev7 = request.POST['dev7']
          existing_Form.conc = request.POST['conc']
          existing_Form.verif_status = request.POST['verif_status']
          existing_Form.text = request.POST['text']
          # existing_Form.verif_by = request.FILES['verif_by']
          # existing_Form.checked = request.FILES['checked']
          # existing_Form.checked1 = request.FILES['checked1']
          existing_Form.disc = request.POST['disc']  
          existing_Form.city_location = request.POST['city_location']
          existing_Form.extra_field = json.loads(request.POST["extra_field"])
          
          if existing_Form.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    test = request.POST.getlist('test[]')[i]
                    equip = request.POST.getlist('equip[]')[i]
                    obser = request.POST.getlist('obser[]')[i]
                    dev = request.POST.getlist('dev[]')[i]

                    existing_Form.extra_field.append({
                         'sr':sr,
                         'test':test,
                         'equip':equip,
                         'obser':obser,
                         'dev':dev,
                    })
          
          
          existing_Form.extra_field = json.dumps(existing_Form.extra_field)

          existing_Form.extra_field1 = json.loads(request.POST["extra_field1"])
          
          if existing_Form.extra_field1:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp1 = request.POST.getlist('inp1[]')[i]
                    inp2 = request.POST.getlist('inp2[]')[i]
                    inp3 = request.POST.getlist('inp3[]')[i]
                    inp4 = request.POST.getlist('inp4[]')[i]

                    existing_Form.extra_field1.append({
                         'sr':sr,
                         'inp1':inp1,
                         'inp2':inp2,
                         'inp3':inp3,
                         'inp4':inp4,
                    })
          
          
          existing_Form.extra_field1 = json.dumps(existing_Form.extra_field1)

     
          city_location_clean = existing_Form.city_location.strip().lower().rstrip('.')

          verif_by_id = request.POST.get('verif_sign')
          check_sign_id = request.POST.get('check_sign')
          
          check1_signature = Signatures.objects.get(id=check_sign_id)
          verif_by_signature = Signatures.objects.get(id=verif_by_id)
          existing_Form.check1_signature =check1_signature
          existing_Form.check_sign_id =check_sign_id
          

          existing_Form.id = None
          existing_Form.created_by = request.user
          existing_Form.save()
          user = request.user
          action = f'Verification certificate {existing_Form.cert_num} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = existing_Form.id
          if "submit_and_view" in request.POST:
               url = f'/verification_view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('verification_list')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return render(request,"verif_list.html")                   


def verif_view(request,pk):
     from PIL import Image
     verif = Verification.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     verif.extra_field = verif.extra_field.replace("'", "\"")
     verif.extra_field = json.loads(verif.extra_field)
     verif.extra_field1 = verif.extra_field1.replace("'", "\"")
     verif.extra_field1 = json.loads(verif.extra_field1)
     


      # Generate a unique file name for the QR code
     qr_filename = f"qr_{verif.cert_num}.png"
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

     context ={'data':verif,'qr':qr_relative_path,'logo':logo}

     return render(request,'verif_view.html',context)   

def verif_pdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import EtalReportPDF as PDFWithPageNumbers

               


               





     verif = Verification.objects.get(id=pk)
     verif.extra_field = verif.extra_field.replace("'", "\"")
     verif.extra_field = json.loads(verif.extra_field)
     verif.extra_field1 = verif.extra_field1.replace("'", "\"")
     verif.extra_field1 = json.loads(verif.extra_field1)
     pdf = PDFWithPageNumbers()
     pdf.add_page()
     
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=5)
     
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.add_font('ScriptMT', '', 'static/fonts/SCRIPTBL.TTF', uni=True)
     pdf.set_font('ScriptMT', '', 25)
     pdf.text(60,43,txt='Certificate of Verification')
     pdf.set_font("Calibri","B", 11)
     pdf.text(10,56,txt='Certificate Number:')
     pdf.line(42,57.5,43+pdf.get_string_width(verif.cert_num),57.5)
     pdf.set_font("Calibri","", 11)
     pdf.text(43,56,txt=verif.cert_num)


     target_url = request.build_absolute_uri(reverse('verif_view', kwargs={'pk': pk}))
    
     # Generate the QR code for the target URL
     qr_filename = f"qr_{pk}.png"
     qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
  
     qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=6,
     )
     qr.add_data(target_url)  # Add the dynamically generated URL
     qr.make(fit=True)
     img = qr.make_image(fill_color="black", back_color="white")
     img.save(qr_file_path)


     pdf.image(qr_file_path,"R",y=46,w=20,h=20)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,66,40,6)
     pdf.text(12,70,txt="Client")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,66,150,6)
     pdf.text(52,70,txt=verif.client)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,72,40,6)
     pdf.text(12,76,txt="Address")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,72,150,6)
     pdf.text(52,76,txt=verif.address)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,78,40,6)
     pdf.text(12,82,txt="verification Date")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,78,50,6)
     pdf.text(52,82,txt=verif.date)


     pdf.set_font("Calibri","B", 11)
     pdf.rect(100,78,40,6)
     pdf.text(102,82,txt="Re-Verification Date")
     pdf.set_font("Calibri","", 11)
     pdf.rect(140,78,60,6)
     pdf.text(142,82,txt=verif.re_verif_date)

     pdf.set_y(93)
     pdf.rect(10,87,190,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,91,txt="Client's Equipment Data")
     pdf.cell(40,6,txt="Equipment",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt=verif.equipment,border=1,align="L")
     pdf.set_font("Calibri","B", 11)
     pdf.cell(30,6,txt="Manufacturer",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(40,6,txt=verif.manufacturer,border=1,align="L",ln=True)

     pdf.set_font("Calibri","B", 11)
     pdf.cell(40,6,txt="Equipment ID",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt=verif.equip_id,border=1,align="L")
     pdf.set_font("Calibri","B", 11)
     pdf.cell(30,6,txt="Model",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(40,6,txt=verif.model,border=1,align="L",ln=True)

     pdf.set_font("Calibri","B", 11)
     pdf.cell(40,6,txt="Parameters",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt="1."+" "+ verif.param1,border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(70,6,txt="2."+" "+ verif.param,border=1,align="L",ln=True)

     pdf.ln(3)
     table_1 = [['Equipment','Model','Serial No.','Certificate']]
     pdf.set_font("Calibri","", 11)
     a = [verif.equipment_1,verif.model_1,verif.serial_no1,verif.cert_num1]
     table_1.append(a)
     a = [verif.equipment_2,verif.model_2,verif.serial_no2,verif.cert_num2]
     table_1.append(a)
     if verif.extra_field1:
          for extra_field in verif.extra_field1:
               inp1 = extra_field.get('inp1')
               inp2 = extra_field.get('inp2')
               inp3 = extra_field.get('inp3')
               inp4 = extra_field.get('inp4')
          a =[inp1,inp2,inp3,inp4]     
          table_1.append(a)

     with pdf.table(col_widths=(20, 20, 20, 30), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
          for k in range(0, len(table_1)):
               data_row = table_1[k]
               
               row = table.row()
               for i in range(0, len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)

     


     pdf.ln(3)
     table_1 = [["Testing Parameters","Equipment Design Specs","Observations","Deviation"]]


     if verif.test_1:
          a = [verif.test_1,verif.equip_des1,verif.obser1,verif.dev1]
          table_1.append(a)
     if verif.test_2:
          a = [verif.test_2,verif.equip_des2,verif.obser2,verif.dev2]
          table_1.append(a)
     if verif.test_3:
          a = [verif.test_3,verif.equip_des3,verif.obser3,verif.dev3]
          table_1.append(a)
     if verif.test_4:
          a = [verif.test_4,verif.equip_des4,verif.obser4,verif.dev4]
          table_1.append(a)
     if verif.test_5:
          a = [verif.test_5,verif.equip_des5,verif.obser5,verif.dev5]
          table_1.append(a)
     if verif.test_6:
          a = [verif.test_6,verif.equip_des6,verif.obser6,verif.dev6]
          table_1.append(a)
     if verif.test_7:
          a = [verif.test_7,verif.equip_des7,verif.obser7,verif.dev7]
          table_1.append(a)

     for extra_field in verif.extra_field:
          test = extra_field.get('test')       
          equip = extra_field.get('equip') 
          obser = extra_field.get('obser') 
          dev = extra_field.get('dev') 
          if test :
               a = [test,equip,obser,dev]
               table_1.append(a)
     
     with pdf.table(col_widths=(63.5, 63.5,63.5,63.5),width=190,line_height=6,text_align=("LEFT","CENTER","CENTER","CENTER")) as table:
               num_rows = 0
               for k in range(0,len(table_1)):
                    data_row = table_1[k]
                    num_rows = num_rows + 1
                    
                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]
                         row.cell(datum)


     def check_new_page(pdf, required_space):
          current_y = pdf.get_y()
          space_left = pdf.h - pdf.b_margin - current_y  # Calculate the space left on the page
          if required_space > space_left:
               pdf.add_page()
               pdf.set_y(pdf.t_margin)  # Reset the Y position after adding a new page

# When you're about to add content that needs more space
     required_space = 50  # The space needed for the upcoming content
     check_new_page(pdf, required_space)
     pdf.ln(3)


     pdf.multi_cell(190,5,txt="Conclusion: " +" "+ verif.conc,border=1,ln=True)
     pdf.cell(190,6,txt="verifion Status :"+ " "+ verif.verif_status,border=1,ln=True)

     pdf.ln(2)
     pdf.multi_cell(190,4,txt=verif.text,ln=True)



     pdf.set_font("Calibri","B", 9)
     if verif.verif_by_signature:
         pdf.image(verif.verif_by_signature.signature,20,248,18,18)
     pdf.line(19,269,30+pdf.get_string_width("verifed By"),269)
     pdf.text(26,271,"verifed By")
     pdf.image('static/assets/SEPA-Sindh-LOGO-removebg-preview.png',54,248,20,18)
     pdf.set_font("Calibri","B", 7)
     pdf.text(56,268,"(License # R-K\242)")
     pdf.image('static/assets/ISO-9001_2015 LOGO.png',82,248,23,18)
     pdf.text(81,268,"(Certificate # 080177324-QMS)")
     
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',117,248,23,18)
     pdf.text(116,268,"(Certificate # 080177424-EMS)")
     pdf.image(envitech_logo,150,248,18,18)
     if verif.check1_signature:
         pdf.image(verif.check1_signature.signature,170,248,18,18)
     pdf.set_font("Calibri","B", 9)
     pdf.line(190,269,140+pdf.get_string_width("Checked By"),269)
     pdf.text(165,271,"Checked By")





     pdf.set_font("Calibri","", 9)
     pdf.set_y(274)
     pdf.set_fill_color(10, 41, 120) 
     pdf.rect(10,275,190,6,"F")
     pdf.set_text_color(255, 255, 255)
     pdf.text(12,278.5,txt=verif.disc)
     
     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={verif.cert_num}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response


def verif_pdf1(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_verif_pdf1 as PDFWithPageNumbers

               


               





     verif = Verification.objects.get(id=pk)
     verif.extra_field = verif.extra_field.replace("'", "\"")
     verif.extra_field = json.loads(verif.extra_field)
     verif.extra_field1 = verif.extra_field1.replace("'", "\"")
     verif.extra_field1 = json.loads(verif.extra_field1)
     pdf = PDFWithPageNumbers()
     pdf.add_page()
     
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=5)
     
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.add_font('ScriptMT', '', 'static/fonts/SCRIPTBL.TTF', uni=True)
     pdf.set_font('ScriptMT', '', 25)
     pdf.text(60,43,txt='Certificate of Verification')
     pdf.set_font("Calibri","B", 11)
     pdf.text(10,56,txt='Certificate Number:')
     pdf.line(42,57.5,43+pdf.get_string_width(verif.cert_num),57.5)
     pdf.set_font("Calibri","", 11)
     pdf.text(43,56,txt=verif.cert_num)

     target_url = request.build_absolute_uri(reverse('verif_view', kwargs={'pk': pk}))
    
     # Generate the QR code for the target URL
     qr_filename = f"qr_{pk}.png"
     qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
  
     qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=6,
     )
     qr.add_data(target_url)  # Add the dynamically generated URL
     qr.make(fit=True)
     img = qr.make_image(fill_color="black", back_color="white")
     img.save(qr_file_path)

     pdf.image(qr_file_path,"R",y=46,w=20,h=20)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,66,40,6)
     pdf.text(12,70,txt="Client")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,66,150,6)
     pdf.text(52,70,txt=verif.client)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,72,40,6)
     pdf.text(12,76,txt="Address")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,72,150,6)
     pdf.text(52,76,txt=verif.address)

     pdf.set_font("Calibri","B", 11)
     pdf.rect(10,78,40,6)
     pdf.text(12,82,txt="verification Date")
     pdf.set_font("Calibri","", 11)
     pdf.rect(50,78,50,6)
     pdf.text(52,82,txt=verif.date)


     pdf.set_font("Calibri","B", 11)
     pdf.rect(100,78,40,6)
     pdf.text(102,82,txt="Re-Verification Date")
     pdf.set_font("Calibri","", 11)
     pdf.rect(140,78,60,6)
     pdf.text(142,82,txt=verif.re_verif_date)

     pdf.set_y(93)
     pdf.rect(10,87,190,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,91,txt="Client's Equipment Data")
     pdf.cell(40,6,txt="Equipment",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt=verif.equipment,border=1,align="L")
     pdf.set_font("Calibri","B", 11)
     pdf.cell(30,6,txt="Manufacturer",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(40,6,txt=verif.manufacturer,border=1,align="L",ln=True)

     pdf.set_font("Calibri","B", 11)
     pdf.cell(40,6,txt="Equipment ID",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt=verif.equip_id,border=1,align="L")
     pdf.set_font("Calibri","B", 11)
     pdf.cell(30,6,txt="Model",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(40,6,txt=verif.model,border=1,align="L",ln=True)

     pdf.set_font("Calibri","B", 11)
     pdf.cell(40,6,txt="Parameters",border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(80,6,txt="1."+" "+ verif.param1,border=1,align="L")
     pdf.set_font("Calibri","", 11)
     pdf.cell(70,6,txt="2."+" "+ verif.param,border=1,align="L",ln=True)

     pdf.ln(3)
     table_1 = [['Equipment','Model','Serial No.','Certificate']]
     pdf.set_font("Calibri","", 11)
     a = [verif.equipment_1,verif.model_1,verif.serial_no1,verif.cert_num1]
     table_1.append(a)
     a = [verif.equipment_2,verif.model_2,verif.serial_no2,verif.cert_num2]
     table_1.append(a)
     if verif.extra_field1:
          for extra_field in verif.extra_field1:
               inp1 = extra_field.get('inp1')
               inp2 = extra_field.get('inp2')
               inp3 = extra_field.get('inp3')
               inp4 = extra_field.get('inp4')
          a =[inp1,inp2,inp3,inp4]     
          table_1.append(a)

     with pdf.table(col_widths=(20, 20, 20, 30), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
          for k in range(0, len(table_1)):
               data_row = table_1[k]
               
               row = table.row()
               for i in range(0, len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
     


     pdf.ln(3)
     table_1 = [["Testing Parameters","Equipment Design Specs","Observations","Deviation"]]


     if verif.test_1:
          a = [verif.test_1,verif.equip_des1,verif.obser1,verif.dev1]
          table_1.append(a)
     if verif.test_2:
          a = [verif.test_2,verif.equip_des2,verif.obser2,verif.dev2]
          table_1.append(a)
     if verif.test_3:
          a = [verif.test_3,verif.equip_des3,verif.obser3,verif.dev3]
          table_1.append(a)
     if verif.test_4:
          a = [verif.test_4,verif.equip_des4,verif.obser4,verif.dev4]
          table_1.append(a)
     if verif.test_5:
          a = [verif.test_5,verif.equip_des5,verif.obser5,verif.dev5]
          table_1.append(a)
     if verif.test_6:
          a = [verif.test_6,verif.equip_des6,verif.obser6,verif.dev6]
          table_1.append(a)
     if verif.test_7:
          a = [verif.test_7,verif.equip_des7,verif.obser7,verif.dev7]
          table_1.append(a)

     for extra_field in verif.extra_field:
          test = extra_field.get('test')       
          equip = extra_field.get('equip') 
          obser = extra_field.get('obser') 
          dev = extra_field.get('dev') 
          if test :
               a = [test,equip,obser,dev]
               table_1.append(a)
     
     with pdf.table(col_widths=(63.5, 63.5,63.5,63.5),width=190,line_height=6,text_align=("LEFT","CENTER","CENTER","CENTER")) as table:
               num_rows = 0
               for k in range(0,len(table_1)):
                    data_row = table_1[k]
                    num_rows = num_rows + 1
                    
                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]
                         row.cell(datum)


     def check_new_page(pdf, required_space):
          current_y = pdf.get_y()
          space_left = pdf.h - pdf.b_margin - current_y  # Calculate the space left on the page
          if required_space > space_left:
               pdf.add_page()
               pdf.set_y(pdf.t_margin)  # Reset the Y position after adding a new page

# When you're about to add content that needs more space
     required_space = 50  # The space needed for the upcoming content
     check_new_page(pdf, required_space)
     pdf.ln(3)


     pdf.multi_cell(190,5,txt="Conclusion: " +" "+ verif.conc,border=1,ln=True)
     pdf.cell(190,6,txt="verifion Status :"+ " "+ verif.verif_status,border=1,ln=True)

     pdf.ln(2)
     pdf.multi_cell(190,4,txt=verif.text,ln=True)



     pdf.set_font("Calibri","B", 9)
     if verif.verif_by_signature:
         pdf.image(verif.verif_by_signature.signature,20,248,18,18)
     pdf.line(19,269,30+pdf.get_string_width("verifed By"),269)
     pdf.text(26,271,"verifed By")
     pdf.image('static/assets/SEPA-Sindh-LOGO-removebg-preview.png',54,248,20,18)
     pdf.set_font("Calibri","B", 7)
     pdf.text(56,268,"(License # R-K\242)")
     pdf.image('static/assets/ISO-9001_2015 LOGO.png',82,248,23,18)
     pdf.text(81,268,"(Certificate # 080177324-QMS)")
     
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',117,248,23,18)
     pdf.text(116,268,"(Certificate # 080177424-EMS)")
     pdf.image(envitech_logo,150,248,18,18)
     if verif.check1_signature:
         pdf.image(verif.check1_signature.signature,170,248,18,18)
     pdf.set_font("Calibri","B", 9)
     pdf.line(190,269,140+pdf.get_string_width("Checked By"),269)
     pdf.text(165,271,"Checked By")





     pdf.set_font("Calibri","", 9)
     pdf.set_y(274)
     pdf.set_fill_color(10, 41, 120) 
     pdf.rect(10,275,190,6,"F")
     pdf.set_text_color(255, 255, 255)
     pdf.text(12,278.5,txt=verif.disc)
     
     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)
     


     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={verif.cert_num}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

__all__ = [
    'verification',
    'verif_delete',
    'verification_list',
    'verif_edit',
    'verif_update',
    'verif_clone',
    'verif_clone_update',
    'verif_view',
    'verif_pdf',
    'verif_pdf1',
]
