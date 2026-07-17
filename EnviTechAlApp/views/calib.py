# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login") 

def calibration(request):
     if request.method == 'POST':
          cert_num = request.POST['cert_num']
          client = request.POST['client']
          contact_person = request.POST['contact_person']
          address = request.POST['address']
          date = request.POST['date_calib']
          calib_perf_at = request.POST['calib_perf_at']
          re_calib_perf_at = request.POST['re_calib_perf_at']
          cert_issue_date = request.POST['cert_issue_date']
          equipment = request.POST['equipment']
          manufacturer = request.POST['manufacturer']
          cond_item = request.POST['cond_item']
          client_id = request.POST['client_id']
          model = request.POST['model']
          location = request.POST['location']
          param = request.POST['param']
          range = request.POST['range']
          serial_no = request.POST['serial_no']
          tolerance = request.POST['tolerance']
          equipment_1 = request.POST['equipment_1']
          model_1 = request.POST['model_1']
          serial_no1 = request.POST['serial_no1']
          cert_num1 = request.POST['cert_num1']
          traceability = request.POST['traceability']
          procedure = request.POST['procedure']
          method = request.POST['method']
          sindh_wm = request.POST['sindh_wm']
          test1 = request.POST['test1']
          test2 = request.POST['test2']
          weight1 = request.POST['weight1']
          kg1 = request.POST['kg1']
          kg2 = request.POST['kg2']
          kg3 = request.POST['kg3']
          set1 = request.POST['set1']
          master1 = request.POST['master1']
          before1 = request.POST['before1']
          after1 = request.POST['after1']
          dev1 = request.POST['dev1']
          set2 = request.POST['set2']
          master2 = request.POST['master2']
          before2 = request.POST['before2']
          after2 = request.POST['after2']
          dev2 = request.POST['dev2']
          set3 = request.POST['set3']
          master3 = request.POST['master3']
          before3 = request.POST['before3']
          after3 = request.POST['after3']
          dev3 = request.POST['dev3']
          set4 = request.POST['set4']
          master4 = request.POST['master4']
          before4 = request.POST['before4']
          after4 = request.POST['after4']
          dev4 = request.POST['dev4']
          weight2 = request.POST['weight2']
          kg1_1 = request.POST['kg1_1']
          kg2_2 = request.POST['kg2_2']
          kg3_3 = request.POST['kg3_3']
          set1_1 = request.POST['set1_1']
          master1_1 = request.POST['master1_1']
          before1_1 = request.POST['before1_1']
          after1_1 = request.POST['after1_1']
          dev1_1 = request.POST['dev1_1']
          set2_2 = request.POST['set2_2']
          master2_2 = request.POST['master2_2']
          before2_2 = request.POST['before2_2']
          after2_2 = request.POST['after2_2']
          dev2_2 = request.POST['dev2_2']
          set3_3 = request.POST['set3_3']
          master3_3 = request.POST['master3_3']
          before3_3 = request.POST['before3_3']
          after3_3 = request.POST['after3_3']
          dev3_3 = request.POST['dev3_3']
          set4_4 = request.POST['set4_4']
          master4_4 = request.POST['master4_4']
          before4_4 = request.POST['before4_4']
          after4_4 = request.POST['after4_4']
          dev4_4 = request.POST['dev4_4']
          calib_status = request.POST['calib_status']
          max_error = request.POST['max_error']
          text = request.POST['text']
          
          set_val_head_1 = request.POST['set_val_head_1']
          master_read_head_1 = request.POST['master_read_head_1']
          actual_read_head_1 = request.POST['actual_read_head_1']
          deviation_head_1 = request.POST['deviation_head_1']
          before_head_1 = request.POST['before_head_1']
          after_head_1 = request.POST['after_head_1']
          
          set_val_head_2 = request.POST['set_val_head_2']
          master_read_head_2 = request.POST['master_read_head_2']
          actual_read_head_2 = request.POST['actual_read_head_2']
          deviation_head_2 = request.POST['deviation_head_2']
          before_head_2 = request.POST['before_head_2']
          after_head_2 = request.POST['after_head_2']
          
          # calib_by = request.FILES["calibby" ]
          # checked = request.FILES["checked" ]
          # checked1 = request.FILES["checked1" ]
          disc = request.POST['disc']
          extra_field = request.POST['extra_field']
          extra_field1 = request.POST['extra_field1']
          extra_field2 = request.POST['extra_field2']
          city_location = request.POST['city_location']
          calib_sign_id = request.POST.get('calib_sign')
          check_sign_id = request.POST.get('check_sign')
          
          calib_by_signature = Signatures.objects.get(id=calib_sign_id)
          checked1_signature = Signatures.objects.get(id=check_sign_id)
          
          
          calibration = Calibration(cert_num=cert_num,client=client,contact_person=contact_person,address=address,
                                    date=date,calib_perf_at=calib_perf_at,re_calib_perf_at=re_calib_perf_at,
                                    cert_issue_date=cert_issue_date,equipment=equipment,manufacturer=manufacturer,cond_item=cond_item,
                                    client_id=client_id,model=model,location=location,param=param,range=range,serial_no=serial_no,tolerance=tolerance,
                                    equipment_1=equipment_1,model_1=model_1,serial_no1=serial_no1,cert_num1=cert_num1,traceability=traceability,
                                    procedure=procedure,method=method,sindh_wm=sindh_wm,test1=test1,test2=test2,weight1=weight1,kg1=kg1,
                                    kg2=kg2,kg3=kg3,set1=set1,master1=master1,before1=before1,after1=after1,dev1=dev1,set2=set2,
                                    master2=master2,before2=before2,after2=after2,dev2=dev2,set3=set3,master3=master3,before3=before3,
                                    after3=after3,dev3=dev3,set4=set4,master4=master4,before4=before4,after4=after4,dev4=dev4,weight2=weight2,
                                    kg1_1=kg1_1,kg2_2=kg2_2,kg3_3=kg3_3,set1_1=set1_1,master1_1=master1_1,before1_1=before1_1,after1_1=after1_1,
                                    dev1_1=dev1_1,set2_2=set2_2,master2_2=master2_2,before2_2=before2_2,after2_2=after2_2,dev2_2=dev2_2,set3_3=set3_3,
                                    master3_3=master3_3,before3_3=before3_3,after3_3=after3_3,dev3_3=dev3_3,set4_4=set4_4,master4_4=master4_4,before4_4=before4_4,
                                    after4_4=after4_4,dev4_4=dev4_4,calib_status=calib_status,max_error=max_error,text=text,
                                    disc=disc,extra_field=extra_field,extra_field1=extra_field1,extra_field2=extra_field2,city_location=city_location,calib_by_signature=calib_by_signature,checked1_signature=checked1_signature,created_by=request.user,
                                    set_val_head_1=set_val_head_1,master_read_head_1=master_read_head_1,actual_read_head_1=actual_read_head_1,deviation_head_1=deviation_head_1,before_head_1=before_head_1,after_head_1=after_head_1,
                                    set_val_head_2=set_val_head_2,master_read_head_2=master_read_head_2,actual_read_head_2=actual_read_head_2,deviation_head_2=deviation_head_2,before_head_2=before_head_2,after_head_2=after_head_2,
                                    )
          calibration.save()
          
          
          user = request.user
          action = f'Calibration certificate {calibration.cert_num} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = (Calibration.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/calibration_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return render(request, "calibration.html")

     else:
          return render(request,"calibration.html",{'signs':signs})

def calib_view(request,pk):
     from PIL import Image
     calib = Calibration.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     calib.extra_field = calib.extra_field.replace("'", "\"")
     calib.extra_field = json.loads(calib.extra_field)
     calib.extra_field1 = calib.extra_field1.replace("'", "\"")
     calib.extra_field1 = json.loads(calib.extra_field1)
     calib.extra_field2 = calib.extra_field2.replace("'", "\"")
     calib.extra_field2 = json.loads(calib.extra_field2)
     # context ={'data':calib,'qr':'media/qr.png'}
     safe_cert_num = calib.cert_num.replace("/", "_").replace("\\", "_")
     qr_filename = f"qr_{safe_cert_num}.png"
     qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)

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

     context ={'data':calib,'qr':qr_relative_path,'logo':logo}

     return render(request,'calib_view.html',context)

@login_required(login_url="/login")
def calib_list(request):
     calib, _srch = _cert_filter(request, Calibration)
     context = {'searched':_srch, 'data':calib}
     return render(request,"calib_list.html",context)

@login_required(login_url="/login")
def calib_delete(request,pk):
     calib = Calibration.objects.get(id=pk)
     calib.delete()
     user = request.user
     action = f'Calibration certificate {calib.cert_num} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     return redirect("calib_list")

@login_required(login_url="/login")
def calib_edit(request,pk):
     calib = Calibration.objects.get(id=pk)
     calib.extra_field = calib.extra_field.replace("'", "\"")
     calib.extra_field = json.loads(calib.extra_field)
     calib.extra_field1 = calib.extra_field1.replace("'", "\"")
     calib.extra_field1 = json.loads(calib.extra_field1)
     calib.extra_field2 = calib.extra_field2.replace("'", "\"")
     calib.extra_field2 = json.loads(calib.extra_field2)
     context = {'data':calib,'signs':signs} 
     return render(request,'calib_edit.html',context) 


@login_required(login_url="/login")
def calib_update(request,pk):       
     calib = Calibration.objects.get(id=pk)  
     if request.method == 'POST':
          calib.cert_num = request.POST['cert_num']
          calib.client = request.POST['client']
          calib.contact_person = request.POST['contact_person']
          calib.address = request.POST['address']
          calib.date = request.POST['date_calib']
          calib.calib_perf_at = request.POST['calib_perf_at']
          calib.re_calib_perf_at = request.POST['re_calib_perf_at']
          calib.cert_issue_date = request.POST['cert_issue_date']
          calib.equipment = request.POST['equipment']
          calib.manufacturer = request.POST['manufacturer']
          calib.cond_item = request.POST['cond_item']
          calib.client_id = request.POST['client_id']
          calib.model = request.POST['model']
          calib.location = request.POST['location']
          calib.param = request.POST['param']
          calib.range = request.POST['range']
          calib.serial_no = request.POST['serial_no']
          calib.tolerance = request.POST['tolerance']
          calib.equipment_1 = request.POST['equipment_1']
          calib.model_1 = request.POST['model_1']
          calib.serial_no1 = request.POST['serial_no1']
          calib.cert_num1 = request.POST['cert_num1']
          calib.traceability = request.POST['traceability']
          calib.procedure = request.POST['procedure']
          calib.method = request.POST['method']
          calib.sindh_wm = request.POST['sindh_wm']
          calib.test1 = request.POST['test1']
          calib.test2 = request.POST['test2']
          calib.weight1 = request.POST['weight1']
          calib.kg1 = request.POST['kg1']
          calib.kg2 = request.POST['kg2']
          calib.kg3 = request.POST['kg3']
          calib.set1 = request.POST['set1']
          calib.master1 = request.POST['master1']
          calib.before1 = request.POST['before1']
          calib.after1 = request.POST['after1']
          calib.dev1 = request.POST['dev1']
          calib.set2 = request.POST['set2']
          calib.master2 = request.POST['master2']
          calib.before2 = request.POST['before2']
          calib.after2 = request.POST['after2']
          calib.dev2 = request.POST['dev2']
          calib.set3 = request.POST['set3']
          calib.master3 = request.POST['master3']
          calib.before3 = request.POST['before3']
          calib.after3 = request.POST['after3']
          calib.dev3 = request.POST['dev3']
          calib.set4 = request.POST['set4']
          calib.master4 = request.POST['master4']
          calib.before4 = request.POST['before4']
          calib.after4 = request.POST['after4']
          calib.dev4 = request.POST['dev4']
          calib.weight2 = request.POST['weight2']
          calib.kg1_1 = request.POST['kg1_1']
          calib.kg2_2 = request.POST['kg2_2']
          calib.kg3_3 = request.POST['kg3_3']
          calib.set1_1 = request.POST['set1_1']
          calib.master1_1 = request.POST['master1_1']
          calib.before1_1 = request.POST['before1_1']
          calib.after1_1 = request.POST['after1_1']
          calib.dev1_1 = request.POST['dev1_1']
          calib.set2_2 = request.POST['set2_2']
          calib.master2_2 = request.POST['master2_2']
          calib.before2_2 = request.POST['before2_2']
          calib.after2_2 = request.POST['after2_2']
          calib.dev2_2 = request.POST['dev2_2']
          calib.set3_3 = request.POST['set3_3']
          calib.master3_3 = request.POST['master3_3']
          calib.before3_3 = request.POST['before3_3']
          calib.after3_3 = request.POST['after3_3']
          calib.dev3_3 = request.POST['dev3_3']
          calib.set4_4 = request.POST['set4_4']
          calib.master4_4 = request.POST['master4_4']
          calib.before4_4 = request.POST['before4_4']
          calib.after4_4 = request.POST['after4_4']
          calib.dev4_4 = request.POST['dev4_4']
          calib.calib_status = request.POST['calib_status']
          calib.max_error = request.POST['max_error']
          calib.text = request.POST['text']
          
          calib.set_val_head_1 = request.POST['set_val_head_1']
          calib.master_read_head_1 = request.POST['master_read_head_1']
          calib.actual_read_head_1 = request.POST['actual_read_head_1']
          calib.deviation_head_1 = request.POST['deviation_head_1']
          calib.before_head_1 = request.POST['before_head_1']
          calib.after_head_1 = request.POST['after_head_1']
          
          calib.set_val_head_2 = request.POST['set_val_head_2']
          calib.master_read_head_2 = request.POST['master_read_head_2']
          calib.actual_read_head_2 = request.POST['actual_read_head_2']
          calib.deviation_head_2 = request.POST['deviation_head_2']
          calib.before_head_2 = request.POST['before_head_2']
          calib.after_head_2 = request.POST['after_head_2']
          
          # calib.calib_by = request.FILES["calibby" ]
          # calib.checked = request.FILES["checked" ]
          # calib.checked1 = request.FILES["checked1" ]
          calib.disc = request.POST['disc'] 
          calib.city_location = request.POST['city_location']
          calib.extra_field = json.loads(request.POST["extra_field"])
          
          if calib.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp1 = request.POST.getlist('inp1[]')[i]
                    inp2 = request.POST.getlist('inp2[]')[i]
                    inp3 = request.POST.getlist('inp3[]')[i]
                    inp4 = request.POST.getlist('inp4[]')[i]

                    calib.extra_field.append({
                         'sr':sr,
                         'inp1':inp1,
                         'inp2':inp2,
                         'inp3':inp3,
                         'inp4':inp4,
                    })
          
          
          calib.extra_field = json.dumps(calib.extra_field)

          calib.extra_field1 = json.loads(request.POST["extra_field1"])
          
          if calib.extra_field1:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp2_1 = request.POST.getlist('inp2_1[]')[i]
                    inp2_2 = request.POST.getlist('inp2_2[]')[i]
                    inp2_3 = request.POST.getlist('inp2_3[]')[i]
                    inp2_4 = request.POST.getlist('inp2_4[]')[i]
                    inp2_5 = request.POST.getlist('inp2_5[]')[i]

                    calib.extra_field1.append({
                         'sr':sr,
                         'inp2_1':inp2_1,
                         'inp2_2':inp2_2,
                         'inp2_3':inp2_3,
                         'inp2_4':inp2_4,
                         'inp2_5':inp2_5,
                    })
          
          
          calib.extra_field1 = json.dumps(calib.extra_field1)

          calib.extra_field2 = json.loads(request.POST["extra_field2"])
          
          if calib.extra_field2:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp3_1 = request.POST.getlist('inp3_1[]')[i]
                    inp3_2 = request.POST.getlist('inp3_2[]')[i]
                    inp3_3 = request.POST.getlist('inp3_3[]')[i]
                    inp3_4 = request.POST.getlist('inp3_4[]')[i]
                    inp3_5 = request.POST.getlist('inp3_5[]')[i]

                    calib.extra_field2.append({
                         'sr':sr,
                         'inp3_1':inp3_1,
                         'inp3_2':inp3_2,
                         'inp3_3':inp3_3,
                         'inp3_4':inp3_4,
                         'inp3_5':inp3_5,
                    })
          
          
          calib.extra_field2 = json.dumps(calib.extra_field2)
          
          calib_sign_id = request.POST.get('calib_sign')
          check_sign_id = request.POST.get('check_sign')
          
          calib_by_signature = Signatures.objects.get(id=calib_sign_id)
          checked1_signature = Signatures.objects.get(id=check_sign_id)
          calib.calib_by_signature=calib_by_signature
          calib.checked1_signature=checked1_signature
          calib.created_by = request.user
          calib.save()
          user = request.user
          action = f'Calibration certificate {calib.cert_num} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = calib.id
          if "submit_and_view" in request.POST:
               url = f'/calibration_view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('calib_list')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return render(request,"calib_list.html")                                                                                                                                                                                                                                                                                                                                                                                                                    

@login_required(login_url="/login")
def calib_clone(request,pk):
     calib = Calibration.objects.get(id=pk)
     calib.extra_field = calib.extra_field.replace("'", "\"")
     calib.extra_field = json.loads(calib.extra_field)
     calib.extra_field1 = calib.extra_field1.replace("'", "\"")
     calib.extra_field1 = json.loads(calib.extra_field1)
     calib.extra_field2 = calib.extra_field2.replace("'", "\"")
     calib.extra_field2 = json.loads(calib.extra_field2)
     context = {'data':calib,'signs':signs} 
     return render(request,'calib_clone.html',context) 


@login_required(login_url="/login")
def calib_clone_update(request,pk):     
     try:
        # Fetch the existing form instance by ID
         existing_Form = Calibration.objects.get(id=pk)
     except Calibration.DoesNotExist:
         return HttpResponse("Form not found", status=404)  
     if request.method == 'POST':
          existing_Form.cert_num = request.POST['cert_num']
          existing_Form.client = request.POST['client']
          existing_Form.contact_person = request.POST['contact_person']
          existing_Form.address = request.POST['address']
          existing_Form.date = request.POST['date_calib']
          existing_Form.calib_perf_at = request.POST['calib_perf_at']
          existing_Form.re_calib_perf_at = request.POST['re_calib_perf_at']
          existing_Form.cert_issue_date = request.POST['cert_issue_date']
          existing_Form.equipment = request.POST['equipment']
          existing_Form.manufacturer = request.POST['manufacturer']
          existing_Form.cond_item = request.POST['cond_item']
          existing_Form.client_id = request.POST['client_id']
          existing_Form.model = request.POST['model']
          existing_Form.location = request.POST['location']
          existing_Form.param = request.POST['param']
          existing_Form.range = request.POST['range']
          existing_Form.serial_no = request.POST['serial_no']
          existing_Form.tolerance = request.POST['tolerance']
          existing_Form.equipment_1 = request.POST['equipment_1']
          existing_Form.model_1 = request.POST['model_1']
          existing_Form.serial_no1 = request.POST['serial_no1']
          existing_Form.cert_num1 = request.POST['cert_num1']
          existing_Form.traceability = request.POST['traceability']
          existing_Form.procedure = request.POST['procedure']
          existing_Form.method = request.POST['method']
          existing_Form.sindh_wm = request.POST['sindh_wm']
          existing_Form.test1 = request.POST['test1']
          existing_Form.test2 = request.POST['test2']
          existing_Form.weight1 = request.POST['weight1']
          existing_Form.kg1 = request.POST['kg1']
          existing_Form.kg2 = request.POST['kg2']
          existing_Form.kg3 = request.POST['kg3']
          existing_Form.set1 = request.POST['set1']
          existing_Form.master1 = request.POST['master1']
          existing_Form.before1 = request.POST['before1']
          existing_Form.after1 = request.POST['after1']
          existing_Form.dev1 = request.POST['dev1']
          existing_Form.set2 = request.POST['set2']
          existing_Form.master2 = request.POST['master2']
          existing_Form.before2 = request.POST['before2']
          existing_Form.after2 = request.POST['after2']
          existing_Form.dev2 = request.POST['dev2']
          existing_Form.set3 = request.POST['set3']
          existing_Form.master3 = request.POST['master3']
          existing_Form.before3 = request.POST['before3']
          existing_Form.after3 = request.POST['after3']
          existing_Form.dev3 = request.POST['dev3']
          existing_Form.set4 = request.POST['set4']
          existing_Form.master4 = request.POST['master4']
          existing_Form.before4 = request.POST['before4']
          existing_Form.after4 = request.POST['after4']
          existing_Form.dev4 = request.POST['dev4']
          existing_Form.weight2 = request.POST['weight2']
          existing_Form.kg1_1 = request.POST['kg1_1']
          existing_Form.kg2_2 = request.POST['kg2_2']
          existing_Form.kg3_3 = request.POST['kg3_3']
          existing_Form.set1_1 = request.POST['set1_1']
          existing_Form.master1_1 = request.POST['master1_1']
          existing_Form.before1_1 = request.POST['before1_1']
          existing_Form.after1_1 = request.POST['after1_1']
          existing_Form.dev1_1 = request.POST['dev1_1']
          existing_Form.set2_2 = request.POST['set2_2']
          existing_Form.master2_2 = request.POST['master2_2']
          existing_Form.before2_2 = request.POST['before2_2']
          existing_Form.after2_2 = request.POST['after2_2']
          existing_Form.dev2_2 = request.POST['dev2_2']
          existing_Form.set3_3 = request.POST['set3_3']
          existing_Form.master3_3 = request.POST['master3_3']
          existing_Form.before3_3 = request.POST['before3_3']
          existing_Form.after3_3 = request.POST['after3_3']
          existing_Form.dev3_3 = request.POST['dev3_3']
          existing_Form.set4_4 = request.POST['set4_4']
          existing_Form.master4_4 = request.POST['master4_4']
          existing_Form.before4_4 = request.POST['before4_4']
          existing_Form.after4_4 = request.POST['after4_4']
          existing_Form.dev4_4 = request.POST['dev4_4']
          existing_Form.calib_status = request.POST['calib_status']
          existing_Form.max_error = request.POST['max_error']
          existing_Form.text = request.POST['text']
          
          existing_Form.set_val_head_1 = request.POST['set_val_head_1']
          existing_Form.master_read_head_1 = request.POST['master_read_head_1']
          existing_Form.actual_read_head_1 = request.POST['actual_read_head_1']
          existing_Form.deviation_head_1 = request.POST['deviation_head_1']
          existing_Form.before_head_1 = request.POST['before_head_1']
          existing_Form.after_head_1 = request.POST['after_head_1']
          
          existing_Form.set_val_head_2 = request.POST['set_val_head_2']
          existing_Form.master_read_head_2 = request.POST['master_read_head_2']
          existing_Form.actual_read_head_2 = request.POST['actual_read_head_2']
          existing_Form.deviation_head_2 = request.POST['deviation_head_2']
          existing_Form.before_head_2 = request.POST['before_head_2']
          existing_Form.after_head_2 = request.POST['after_head_2']
          
          # existing_Form.calib_by = request.FILES["calibby" ]
          # existing_Form.checked = request.FILES["checked" ]
          # existing_Form.checked1 = request.FILES["checked1" ]
          existing_Form.disc = request.POST['disc']
          existing_Form.city_location = request.POST['city_location']
          existing_Form.extra_field = json.loads(request.POST["extra_field"])
          existing_Form.extra_field = json.loads(request.POST["extra_field"])
          
          if existing_Form.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp1 = request.POST.getlist('inp1[]')[i]
                    inp2 = request.POST.getlist('inp2[]')[i]
                    inp3 = request.POST.getlist('inp3[]')[i]
                    inp4 = request.POST.getlist('inp4[]')[i]

                    existing_Form.extra_field.append({
                         'sr':sr,
                         'inp1':inp1,
                         'inp2':inp2,
                         'inp3':inp3,
                         'inp4':inp4,
                    })
          
          
          existing_Form.extra_field = json.dumps(existing_Form.extra_field)

          existing_Form.extra_field1 = json.loads(request.POST["extra_field1"])
          
          if existing_Form.extra_field1:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp2_1 = request.POST.getlist('inp2_1[]')[i]
                    inp2_2 = request.POST.getlist('inp2_2[]')[i]
                    inp2_3 = request.POST.getlist('inp2_3[]')[i]
                    inp2_4 = request.POST.getlist('inp2_4[]')[i]
                    inp2_5 = request.POST.getlist('inp2_5[]')[i]

                    existing_Form.extra_field1.append({
                         'sr':sr,
                         'inp2_1':inp2_1,
                         'inp2_2':inp2_2,
                         'inp2_3':inp2_3,
                         'inp2_4':inp2_4,
                         'inp2_5':inp2_5,
                    })
          
          
          existing_Form.extra_field1 = json.dumps(existing_Form.extra_field1)

          existing_Form.extra_field2 = json.loads(request.POST["extra_field2"])
          
          if existing_Form.extra_field2:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp3_1 = request.POST.getlist('inp3_1[]')[i]
                    inp3_2 = request.POST.getlist('inp3_2[]')[i]
                    inp3_3 = request.POST.getlist('inp3_3[]')[i]
                    inp3_4 = request.POST.getlist('inp3_4[]')[i]
                    inp3_5 = request.POST.getlist('inp3_5[]')[i]

                    existing_Form.extra_field2.append({
                         'sr':sr,
                         'inp3_1':inp3_1,
                         'inp3_2':inp3_2,
                         'inp3_3':inp3_3,
                         'inp3_4':inp3_4,
                         'inp3_5':inp3_5,
                    })
          
          
          existing_Form.extra_field2 = json.dumps(existing_Form.extra_field2)
          

          calib_sign_id = request.POST.get('calib_sign')
          check_sign_id = request.POST.get('check_sign')
          
          calib_by_signature = Signatures.objects.get(id=calib_sign_id)
          checked1_signature = Signatures.objects.get(id=check_sign_id)
          existing_Form.calib_by_signature=calib_by_signature
          existing_Form.checked1_signature=checked1_signature
          existing_Form.id = None
          existing_Form.created_by = request.user
          existing_Form.save()
          user = request.user
          action = f'Calibration certificate {existing_Form.cert_num} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = existing_Form.id
          if "submit_and_view" in request.POST:
                url = f"/calibration_view/{str(id)}/"
                return redirect(to=url)
          
          if "submit_and_new" in request.POST:
             # context = {'list': new_dw}
              return redirect(to='calib_list')
          else:
              return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "calib_clone.html")


def calib_pdf(request,pk):
     from fpdf import FPDF
     
     from EnviTechAlApp.pdf_common import PDF_calib_pdf as PDFWithPageNumbers
               


               





     try:
          calib = Calibration.objects.get(id=pk)
          
          calib.extra_field = calib.extra_field.replace("'", "\"")
          calib.extra_field = json.loads(calib.extra_field)
          calib.extra_field1 = calib.extra_field1.replace("'", "\"")
          calib.extra_field1 = json.loads(calib.extra_field1)
          calib.extra_field2 = calib.extra_field2.replace("'", "\"")
          calib.extra_field2 = json.loads(calib.extra_field2)
          pdf = PDFWithPageNumbers()
          pdf._rq_calib, pdf._rq_pk, pdf._rq_request = calib, pk, request
          pdf.add_page()
          
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True, margin=15)
          
         

          pdf.rect(10,60,45,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,64, txt="Client")

          pdf.rect(55,60,55,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(57,64, txt=(calib.client or ""))

          pdf.rect(110,60,35,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(112,64, txt="Contact Person")

          pdf.rect(145,60,55,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(147,64, txt=calib.contact_person)

          pdf.rect(10,66,45,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,70, txt="Address")

          pdf.rect(55,66,145,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(57,70, txt=calib.address)

          pdf.rect(10,72,45,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,76, txt="Date of Calibration")

          pdf.rect(55,72,145,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(57,76, txt=calib.date)

          pdf.rect(10,78,45,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,82, txt="Calibration Performed At")

          pdf.rect(55,78,40,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(57,82, txt=calib.calib_perf_at)

          pdf.rect(95,78,50,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(97,82, txt="Recom. Re-Calibration Date")

          pdf.rect(145,78,55,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(147,82, txt=calib.re_calib_perf_at)

          pdf.rect(10,84,45,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,88, txt="Certificate Issuance Date")

          pdf.rect(55,84,145,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(57,88, txt=calib.cert_issue_date)
          
          pdf.rect(10,92,190,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,96, txt="Client's Equipment Date")

          pdf.rect(10,98,20,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,102, txt="Equipment")

          pdf.rect(30,98,50,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(32,102, txt=calib.equipment)

          pdf.rect(80,98,30,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(82,102, txt="Manufacturer")

          pdf.rect(110,98,35,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(112,102, txt=calib.manufacturer)

          pdf.rect(145,98,35,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(147,102, txt="Condition of item")

          pdf.rect(180,98,20,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(182,102, txt=calib.cond_item)

          pdf.rect(10,104,20,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,108, txt="Client ID")
          
          pdf.rect(30,104,50,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(32,108, txt=calib.client_id)
          
          pdf.rect(80,104,30,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(82,108, txt="Model/Type")

          pdf.rect(110,104,90,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(112,108, txt=calib.model)

          pdf.rect(10,110,20,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,114, txt="Location")

          pdf.rect(30,110,170,6)
          pdf.set_font("Calibri","", 11)
          pdf.text(32,114, txt=calib.location)

          pdf.rect(10,116,190,10)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,120, txt="Parameter(s)")
          pdf.set_font("Calibri","", 10)
          # pdf.text(38,120, txt=calib.param)
          
          # pdf.multi_cell(30, 5, txt=str(calib.param), border=True)
          pdf.set_font("Calibri","B", 11)
          pdf.text(82,120, txt="Range / L.C.")
          pdf.set_font("Calibri","", 11)
          pdf.text(112,120, txt=calib.range)
          pdf.set_font("Calibri","B", 11)
          pdf.text(82,124, txt="Serial No.")
          pdf.set_font("Calibri","", 11)
          pdf.text(112,124, txt=calib.serial_no)

          pdf.set_font("Calibri","B", 11)
          pdf.text(147,120, txt="Tolerance")
          pdf.set_font("Calibri","", 11)
          # pdf.text(178,120, txt=calib.tolerance)
          
          pdf.set_font("Calibri", "", 9)
          pdf.set_xy(38, 116.6)
          pdf.multi_cell(40, 5, txt=str(calib.param) if calib.param else "", border=0, align="L")

          # Tolerance — label "Tolerance" is at x=147, value area x=178 to page edge (~200)
          # only ~20mm available, so width is naturally tight
          pdf.set_font("Calibri", "", 9)
          pdf.set_xy(165, 116.6)
          pdf.multi_cell(35, 5, txt=str(calib.tolerance) if calib.tolerance else "", border=0, align="L")

          pdf.rect(10,128,190,6)
          pdf.set_font("Calibri","B", 11)
          pdf.text(12,132, txt="Master Equipment And References")

          pdf.set_y(134)
          pdf.set_font("Calibri","B", 11)
          table_1 = [['Equipment', 'Model', 'Serial No', 'Certificate Number']]

     # Your row of data
          a = [calib.equipment_1, calib.model_1, calib.serial_no1, calib.cert_num1]

     # Append the row as a new sublist
          table_1.append(a)
          for extra_field in calib.extra_field:
               inp1 = extra_field.get('inp1')       
               inp2 = extra_field.get('inp2')       
               inp3 = extra_field.get('inp3')       
               inp4 = extra_field.get('inp4')       
               if inp1:
                    a = [inp1,inp2,inp3,inp4]
                    table_1.append(a)

     # Rest of your code for creating the table in the PDF
          with pdf.table(col_widths=(30, 15, 15, 30), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
               for k in range(0, len(table_1)):
                    data_row = table_1[k]
                    
                    row = table.row()
                    for i in range(0, len(data_row)):
                         pdf.set_font("Calibri","", 9)
                         datum = data_row[i]
                         row.cell(datum)


               
          pdf.set_font("Calibri","B", 11)
          pdf.cell(40,6,txt="Traceability", border=1) 
          pdf.set_font("Calibri","", 11)            
          pdf.cell(150,6,txt=calib.traceability,border=1,ln=True)   
          pdf.set_font("Calibri","B", 11)          
          pdf.cell(40,6,txt="Procedure",border=1)        
          pdf.set_font("Calibri","", 11)     
          pdf.cell(55,6,txt=calib.procedure,border=1)
          pdf.set_font("Calibri","B", 11)   
          pdf.cell(40,6,txt="Method/Reference", border=1) 
          pdf.set_font("Calibri","", 11)           
          pdf.cell(55,6,txt=calib.method,border=1,ln=True)          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(55,6,txt="Sindh Weight And Measures",border=1)     
          pdf.set_font("Calibri","", 11)        
          pdf.cell(135,6,txt=calib.sindh_wm,border=1,ln=True)                 
          

          pdf.ln(2)
          
          

          pdf.cell(63.5,6,txt="Test Environment",border=1 ,align='L')
          pdf.cell(63.5,6,txt=calib.test1,border=1 ,align='L')
          pdf.cell(63.5,6,txt=calib.test2,border=1,ln=True ,align='L')
     

     
          pdf.ln(2)
          
          pdf.set_font("Calibri","B", 11)

          pdf.cell(13,6,txt="Table :",align='L')
          pdf.cell(100,6,txt=calib.weight1 ,ln=True,align="L")
          

          pdf.set_font("Calibri","B", 11)
          
          pdf.cell(38,10,txt=f"{calib.set_val_head_1 or 'Set Value'}",border=1,align="C")

          
          pdf.cell(38,10,txt=f"{calib.master_read_head_1 or 'Master Reading'}",border=1,align="C")
          
          
          pdf.cell(38,10,txt=f"{calib.before_head_1 or 'Actual Reading(Before)'}",align='C', border=1)
          pdf.cell(38,10,txt=f"{calib.after_head_1 or 'Actual Reading(After)'}",align='C', border=1)
          pdf.cell(38,10,txt=f"{calib.deviation_head_1 or 'Deviation'}",border=1,ln=True,align="c")

          
          # pdf.cell(35,5,txt='Before',align='C', border=1)
          
          # pdf.cell(35,5,txt='After',align='C', border=1,ln=True)

          pdf.cell(76,5,txt=calib.kg1,border=1,align="c")
          pdf.cell(76,5,txt=calib.kg2,border=1,align="c")
          pdf.cell(38,5,txt=calib.kg3,border=1,align="c",ln=True)



          

          pdf.set_font("Calibri","", 9)
          if calib.set1:
               pdf.cell(38,5,txt=calib.set1, border=1, align="C")
               
               
               pdf.cell(38,5,txt=calib.master1, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before1, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after1, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev1,ln=True, border=1, align="C")

          
          if calib.set2:
               pdf.cell(38,5,txt=calib.set2, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.master2, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before2, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after2, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev2,ln=True, border=1, align="C")

          if calib.set3:
               pdf.cell(38,5,txt=calib.set3, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.master3, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before3, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after3, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev3,ln=True, border=1, align="C")

          if calib.set4:
               pdf.cell(38,5,txt=calib.set4, border=1, align="C")
               pdf.cell(38,5,txt=calib.master4, border=1, align="C")
               pdf.cell(38,5,txt=calib.before4, border=1, align="C")
               pdf.cell(38,5,txt=calib.after4, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev4,ln=True, border=1, align="C")
          
          pdf.set_font("Calibri","", 9)
          for extra_field in calib.extra_field1:
               pdf.set_font("Calibri","", 9)
               inp2_1 = extra_field.get('inp2_1')       
               inp2_2 = extra_field.get('inp2_2')       
               inp2_3 = extra_field.get('inp2_3')       
               inp2_4 = extra_field.get('inp2_4')       
               inp2_5 = extra_field.get('inp2_5')

               if inp2_1:
                    pdf.set_font("Calibri","", 9)
                    pdf.cell(38,5,txt=inp2_1, border=1, align="C")
                    pdf.cell(38,5,txt=inp2_2, border=1, align="C")
                    pdf.cell(38,5,txt=inp2_3, border=1, align="C")
                    pdf.cell(38,5,txt=inp2_4, border=1, align="C")
                    pdf.cell(38,5,txt=inp2_5,ln=True, border=1, align="C")
          pdf.set_font("Calibri","", 9)

          
          
          if calib.weight2:
               pdf.add_page()
               pdf.set_y(60)
               pdf.ln(2)
               pdf.set_font("Calibri","B", 11)

               pdf.cell(13,6,txt="Table :",align='L')
               pdf.cell(100,6,txt=calib.weight2 ,ln=True,align="L")

               
          
               pdf.cell(38,10,txt=f"{calib.set_val_head_2 or 'Set Value'}",border=1,align="C")

               
               pdf.cell(38,10,txt=f"{calib.master_read_head_2 or 'Master Reading'}",border=1,align="C")
               
               pdf.cell(38,10,txt=f"{calib.before_head_2 or 'Actual Reading(Before)'}",align='C', border=1)
               pdf.cell(38,10,txt=f"{calib.after_head_2 or 'Actual Reading(After)'}",align='C', border=1)
               pdf.cell(38,10,txt=f"{calib.deviation_head_2 or 'Deviation'}",border=1,ln=True,align="c")

               
               pdf.cell(76,5,txt=calib.kg1_1,border=1,align="c")
               pdf.cell(76,5,txt=calib.kg2_2,border=1,align="c")
               pdf.cell(38,5,txt=calib.kg3_3,border=1,align="c",ln=True)



               

               pdf.set_font("Calibri","", 9)
               if calib.set1_1:
                    pdf.cell(38,5,txt=calib.set1_1, border=1, align="C")
                    
                    
                    pdf.cell(38,5,txt=calib.master1_1, border=1, align="C")

                    
                    pdf.cell(38,5,txt=calib.before1_1, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.after1_1, border=1, align="C")
                    pdf.cell(38,5,txt=calib.dev1_1,ln=True, border=1, align="C")

               
               if calib.set2_2:
                    pdf.cell(38,5,txt=calib.set2_2, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.master2_2, border=1, align="C")

                    
                    pdf.cell(38,5,txt=calib.before2_2, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.after2_2, border=1, align="C")
                    pdf.cell(38,5,txt=calib.dev2_2,ln=True, border=1, align="C")

               if calib.set3_3:
                    pdf.cell(38,5,txt=calib.set3_3, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.master3_3, border=1, align="C")

                    
                    pdf.cell(38,5,txt=calib.before3_3, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.after3_3, border=1, align="C")
                    pdf.cell(38,5,txt=calib.dev3_3,ln=True, border=1, align="C")

               if calib.set4_4:
                    pdf.cell(38,5,txt=calib.set4_4, border=1, align="C")
                    
                    pdf.cell(38,5,txt=calib.master4_4, border=1, align="C")

                    pdf.cell(38,5,txt=calib.before4_4, border=1, align="C")
                    pdf.cell(38,5,txt=calib.after4_4, border=1, align="C")
                    pdf.cell(38,5,txt=calib.dev4_4,ln=True, border=1, align="C")
               
               

               pdf.set_font("Calibri","", 9)
               ex_table2 = []
               pdf.set_font("Calibri","", 9)
               for extra_field in calib.extra_field2:
                    pdf.set_font("Calibri","", 9)
                    inp3_1 = extra_field.get('inp3_1')       
                    inp3_2 = extra_field.get('inp3_2')       
                    inp3_3 = extra_field.get('inp3_3')       
                    inp3_4 = extra_field.get('inp3_4')       
                    inp3_5 = extra_field.get('inp3_5') 
                    
                    if inp3_1:
                         pdf.set_font("Calibri","", 9)
                         a = [inp3_1,inp3_2,inp3_3,inp3_4,inp3_5]
                         ex_table2.append(a)

          # Rest of your code for creating the table in the PDF
               with pdf.table(col_widths=(38, 38, 38, 38,38), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER","CENTER")) as table:
                    for k in range(0, len(ex_table2)):
                         data_row = ex_table2[k]
                         
                         row = table.row()
                         for i in range(0, len(data_row)):
                              pdf.set_font("Calibri","", 9)
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
          pdf.ln(2)
          pdf.cell(47.5,6,txt="Calibration Status",border=1,align="L")
          pdf.cell(47.5,6,txt=calib.calib_status,border=1,align="L")
          pdf.cell(47.5,6,txt="Maximum Error",border=1,align="L")
          pdf.cell(47.5,6,txt=calib.max_error,border=1,align="L",ln=True)

          pdf.ln(2)
          pdf.set_font("Calibri","", 10)
          pdf.multi_cell(190, 4, txt=calib.text, border=0, ln=True, align='L')

          pdf.set_font("Calibri","", 7)
          if calib.calib_by_signature:
              pdf.image(calib.calib_by_signature.signature,20,248,18,18)
          pdf.line(19,269,30+pdf.get_string_width("Calibrated By"),269)
          pdf.text(26,271,"Calibrated By")

          pdf.image('static/assets/SEPA-Sindh-LOGO-removebg-preview.png',54,250,20,18)
          pdf.text(54,270,"(License # R-K\ 242)")

          pdf.image('static/assets/ISO-9001_2015 LOGO.png',82,250,23,18)
          pdf.text(81,270,"(Certificate # 080177324-QMS)")
          

          pdf.image('static/assets/ISO-14001_2015 LOGO.png',117,250,23,18)
          pdf.text(116,270,"(Certificate # 080177424-EMS)")

          pdf.image(envitech_logo,150,248,18,18)
          if calib.checked1_signature:
              pdf.image(calib.checked1_signature.signature,170,248,18,18)
          pdf.line(190,269,140+pdf.get_string_width("Checked By"),269)
          pdf.text(165,271,"Checked By")





          pdf.set_font("Calibri","", 9)
          pdf.set_y(274)
          pdf.set_fill_color(10, 41, 120) 
          pdf.rect(10,275,190,6,"F")
          pdf.set_text_color(255, 255, 255)
          pdf.text(12,278.5,txt=calib.disc)
          

          pdf.set_encryption(
          owner_password="karachi123",  # Replace with a strong owner password
          user_password="1234",    # Replace with a user password
          encryption_method=fpdf.enums.EncryptionMethod.AES_256,
          permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
     )

          
          response = HttpResponse(content_type='application/pdf')
          response['Content-Disposition'] = f'inline; filename={calib.cert_num}.pdf'

               # Output the PDF to the response
          pdf_output = BytesIO()
          pdf_output.write(pdf.output(dest='S'))
          response.write(pdf_output.getvalue())

          return response
     except Exception as e:
          import traceback
          traceback.print_exc()  # prints full stack trace to console
          return HttpResponse("PDF generation failed. Please try again or contact the administrator.", status=500)

def calib_pdf1(request,pk):
     from fpdf import FPDF
     
     from EnviTechAlApp.pdf_common import PDF_calib_pdf1 as PDFWithPageNumbers
          
               
          

               





     calib = Calibration.objects.get(id=pk)
     calib.extra_field = calib.extra_field.replace("'", "\"")
     calib.extra_field = json.loads(calib.extra_field)
     calib.extra_field1 = calib.extra_field1.replace("'", "\"")
     calib.extra_field1 = json.loads(calib.extra_field1)
     calib.extra_field2 = calib.extra_field2.replace("'", "\"")
     calib.extra_field2 = json.loads(calib.extra_field2)
     
     pdf = PDFWithPageNumbers()
     pdf._rq_calib, pdf._rq_pk, pdf._rq_request = calib, pk, request
     pdf.add_page()
     
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=15)
     
     
     
     pdf.rect(10,60,45,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,64, txt="Client")

     pdf.rect(55,60,55,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(57,64, txt=(calib.client or ""))

     pdf.rect(110,60,35,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(112,64, txt="Contact Person")

     pdf.rect(145,60,55,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(147,64, txt=calib.contact_person)

     pdf.rect(10,66,45,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,70, txt="Address")

     pdf.rect(55,66,145,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(57,70, txt=calib.address)

     pdf.rect(10,72,45,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,76, txt="Date of Calibration")

     pdf.rect(55,72,145,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(57,76, txt=calib.date)

     pdf.rect(10,78,45,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,82, txt="Calibration Performed At")

     pdf.rect(55,78,40,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(57,82, txt=calib.calib_perf_at)

     pdf.rect(95,78,50,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(97,82, txt="Recom. Re-Calibration Date")

     pdf.rect(145,78,55,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(147,82, txt=calib.re_calib_perf_at)

     pdf.rect(10,84,45,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,88, txt="Certificate Issuance Date")

     pdf.rect(55,84,145,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(57,88, txt=calib.cert_issue_date)

     pdf.rect(10,92,190,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,96, txt="Client's Equipment Date")

     pdf.rect(10,98,20,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,102, txt="Equipment")

     pdf.rect(30,98,50,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(32,102, txt=calib.equipment)

     pdf.rect(80,98,30,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(82,102, txt="Manufacturer")

     pdf.rect(110,98,35,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(112,102, txt=calib.manufacturer)

     pdf.rect(145,98,35,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(147,102, txt="Condition of item")

     pdf.rect(180,98,20,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(182,102, txt=calib.cond_item)

     pdf.rect(10,104,20,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,108, txt="Client ID")
     
     pdf.rect(30,104,50,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(32,108, txt=calib.client_id)
     
     pdf.rect(80,104,30,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(82,108, txt="Model/Type")

     pdf.rect(110,104,90,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(112,108, txt=calib.model)

     pdf.rect(10,110,20,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,114, txt="Location")

     pdf.rect(30,110,170,6)
     pdf.set_font("Calibri","", 11)
     pdf.text(32,114, txt=calib.location)

     pdf.rect(10,116,190,10)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,120, txt="Parameter(s)")
     pdf.set_font("Calibri","", 11)
     # pdf.text(47,120, txt=calib.param)
     pdf.set_font("Calibri","B", 11)
     pdf.text(82,120, txt="Range / L.C.")
     pdf.set_font("Calibri","", 11)
     pdf.text(112,120, txt=calib.range)
     pdf.set_font("Calibri","B", 11)
     pdf.text(82,124, txt="Serial No.")
     pdf.set_font("Calibri","", 11)
     pdf.text(112,124, txt=calib.serial_no)

     pdf.set_font("Calibri","B", 11)
     pdf.text(147,120, txt="Tolerance")
     pdf.set_font("Calibri","", 11)
     # pdf.text(178,120, txt=calib.tolerance)
     
     pdf.set_font("Calibri", "", 10)
     pdf.set_xy(38, 116.6)
     pdf.multi_cell(40, 5, txt=str(calib.param) if calib.param else "", border=0, align="L")

          # Tolerance — label "Tolerance" is at x=147, value area x=178 to page edge (~200)
          # only ~20mm available, so width is naturally tight
     pdf.set_font("Calibri", "", 10)
     pdf.set_xy(165, 116.6)
     pdf.multi_cell(38, 5, txt=str(calib.tolerance) if calib.tolerance else "", border=0, align="L")


     pdf.rect(10,128,190,6)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,132, txt="Master Equipment And References")

     pdf.set_y(134)
     pdf.set_font("Calibri","", 11)
     table_1 = [['Equipment', 'Model', 'Serial No', 'Certificate Number']]

# Your row of data
     a = [calib.equipment_1, calib.model_1, calib.serial_no1, calib.cert_num1]

# Append the row as a new sublist
     table_1.append(a)
     for extra_field in calib.extra_field:
           inp1 = extra_field.get('inp1')       
           inp2 = extra_field.get('inp2')       
           inp3 = extra_field.get('inp3')       
           inp4 = extra_field.get('inp4')       
           if inp1:
                a = [inp1,inp2,inp3,inp4]
                table_1.append(a)

# Rest of your code for creating the table in the PDF
     with pdf.table(col_widths=(30, 15, 15, 30), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
          for k in range(0, len(table_1)):
               data_row = table_1[k]
               
               row = table.row()
               for i in range(0, len(data_row)):
                    pdf.set_font("Calibri","", 9)
                    datum = data_row[i]
                    row.cell(datum)
        

            
     pdf.set_font("Calibri","B", 11)
     pdf.cell(40,6,txt="Traceability", border=1) 
     pdf.set_font("Calibri","", 11)            
     pdf.cell(150,6,txt=calib.traceability,border=1,ln=True)   
     pdf.set_font("Calibri","B", 11)          
     pdf.cell(40,6,txt="Procedure",border=1)        
     pdf.set_font("Calibri","", 11)     
     pdf.cell(55,6,txt=calib.procedure,border=1)
     pdf.set_font("Calibri","B", 11)   
     pdf.cell(40,6,txt="Method/Reference", border=1) 
     pdf.set_font("Calibri","", 11)           
     pdf.cell(55,6,txt=calib.method,border=1,ln=True)          
     pdf.set_font("Calibri","B", 11)
     pdf.cell(55,6,txt="Sindh Weight And Measures",border=1)     
     pdf.set_font("Calibri","", 11)        
     pdf.cell(135,6,txt=calib.sindh_wm,border=1,ln=True)                 
     

     pdf.ln(2)
     
     

     pdf.cell(63.5,6,txt="Test Environment",border=1 ,align='L')
     pdf.cell(63.5,6,txt=calib.test1,border=1 ,align='L')
     pdf.cell(63.5,6,txt=calib.test2,border=1,ln=True ,align='L')
   

    
     pdf.ln(2)
     
     pdf.set_font("Calibri","B", 11)

     pdf.cell(13,6,txt="Table :",align='L')
     pdf.cell(100,6,txt=calib.weight1 ,ln=True,align="L")
     

     pdf.set_font("Calibri","B", 11)
     
     pdf.cell(38,10,txt=f"{calib.set_val_head_1 or 'Set Value'}",border=1,align="C")

          
     pdf.cell(38,10,txt=f"{calib.master_read_head_1 or 'Master Reading'}",border=1,align="C")
          
          
     pdf.cell(38,10,txt=f"{calib.before_head_1 or 'Actual Reading(Before)'}",align='C', border=1)
     pdf.cell(38,10,txt=f"{calib.after_head_1 or 'Actual Reading(After)'}",align='C', border=1)
     pdf.cell(38,10,txt=f"{calib.deviation_head_1 or 'Deviation'}",border=1,ln=True,align="c")


     
     

     pdf.cell(76,5,txt=calib.kg1,border=1,align="c")
     pdf.cell(76,5,txt=calib.kg2,border=1,align="c")
     pdf.cell(38,5,txt=calib.kg3,border=1,align="c",ln=True)



     

     pdf.set_font("Calibri","", 9)
     if calib.set1:
          pdf.cell(38,5,txt=calib.set1, border=1, align="C")
          
          
          pdf.cell(38,5,txt=calib.master1, border=1, align="C")

          
          pdf.cell(38,5,txt=calib.before1, border=1, align="C")
          
          pdf.cell(38,5,txt=calib.after1, border=1, align="C")
          pdf.cell(38,5,txt=calib.dev1,ln=True, border=1, align="C")

     
     if calib.set2:
          pdf.cell(38,5,txt=calib.set2, border=1, align="C")
          
          pdf.cell(38,5,txt=calib.master2, border=1, align="C")

          
          pdf.cell(38,5,txt=calib.before2, border=1, align="C")
          
          pdf.cell(38,5,txt=calib.after2, border=1, align="C")
          pdf.cell(38,5,txt=calib.dev2,ln=True, border=1, align="C")

     if calib.set3:
          pdf.cell(38,5,txt=calib.set3, border=1, align="C")
          
          pdf.cell(38,5,txt=calib.master3, border=1, align="C")

          
          pdf.cell(38,5,txt=calib.before3, border=1, align="C")
          
          pdf.cell(38,5,txt=calib.after3, border=1, align="C")
          pdf.cell(38,5,txt=calib.dev3,ln=True, border=1, align="C")

     if calib.set4:
          pdf.cell(38,5,txt=calib.set4, border=1, align="C")
          pdf.cell(38,5,txt=calib.master4, border=1, align="C")
          pdf.cell(38,5,txt=calib.before4, border=1, align="C")
          pdf.cell(38,5,txt=calib.after4, border=1, align="C")
          pdf.cell(38,5,txt=calib.dev4,ln=True, border=1, align="C")
     
     pdf.set_font("Calibri","", 11)
     ex_table1 = []
     pdf.set_font("Calibri","", 9)
     for extra_field in calib.extra_field1:
          pdf.set_font("Calibri","", 9)
          inp2_1 = extra_field.get('inp2_1')       
          inp2_2 = extra_field.get('inp2_2')       
          inp2_3 = extra_field.get('inp2_3')       
          inp2_4 = extra_field.get('inp2_4')       
          inp2_5 = extra_field.get('inp2_5') 
             
          if inp2_1:
               pdf.set_font("Calibri","", 9)
               a = [inp2_1,inp2_2,inp2_3,inp2_4,inp2_5]
               ex_table1.append(a)

# Rest of your code for creating the table in the PDF
     pdf.set_font("Calibri","", 9)
     with pdf.table(col_widths=(38, 38, 38, 38,38), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER","CENTER")) as table:
          for k in range(0, len(ex_table1)):
               pdf.set_font("Calibri","", 9)
               data_row = ex_table1[k]
               pdf.set_font("Calibri","", 9)
               row = table.row()
               for i in range(0, len(data_row)):
                    pdf.set_font("Calibri","", 9)
                    datum = data_row[i]
                    pdf.set_font("Calibri","", 9)
                    row.cell(datum)

     
     
     
     
     
     
     if calib.weight2:
          pdf.add_page()
          pdf.set_y(60)
          pdf.ln(2)
          pdf.set_font("Calibri","B", 9)

          pdf.cell(13,6,txt="Table :",align='L')
          pdf.cell(100,6,txt=calib.weight2 ,ln=True,align="L")

          

          pdf.cell(38,10,txt=f"{calib.set_val_head_2 or 'Set Value'}",border=1,align="C")

               
          pdf.cell(38,10,txt=f"{calib.master_read_head_2 or 'Master Reading'}",border=1,align="C")
               
          pdf.cell(38,10,txt=f"{calib.before_head_2 or 'Actual Reading(Before)'}",align='C', border=1)
          pdf.cell(38,10,txt=f"{calib.after_head_2 or 'Actual Reading(After)'}",align='C', border=1)
          pdf.cell(38,10,txt=f"{calib.deviation_head_2 or 'Deviation'}",border=1,ln=True,align="c")

               
               

          
          pdf.cell(76,5,txt=calib.kg1_1,border=1,align="c")
          pdf.cell(76,5,txt=calib.kg2_2,border=1,align="c")
          pdf.cell(38,5,txt=calib.kg3_3,border=1,align="c",ln=True)



          

          pdf.set_font("Calibri","", 11)
          if calib.set1_1:
               pdf.cell(38,5,txt=calib.set1_1, border=1, align="C")
               
               
               pdf.cell(38,5,txt=calib.master1_1, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before1_1, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after1_1, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev1_1,ln=True, border=1, align="C")

          
          if calib.set2_2:
               pdf.cell(38,5,txt=calib.set2_2, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.master2_2, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before2_2, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after2_2, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev2_2,ln=True, border=1, align="C")

          if calib.set3_3:
               pdf.cell(38,5,txt=calib.set3_3, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.master3_3, border=1, align="C")

               
               pdf.cell(38,5,txt=calib.before3_3, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.after3_3, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev3_3,ln=True, border=1, align="C")

          if calib.set4_4:
               pdf.cell(38,5,txt=calib.set4_4, border=1, align="C")
               
               pdf.cell(38,5,txt=calib.master4_4, border=1, align="C")

               
               
               pdf.cell(38,5,txt=calib.before4_4, border=1, align="C")
               pdf.cell(38,5,txt=calib.after4_4, border=1, align="C")
               pdf.cell(38,5,txt=calib.dev4_4, border=1, ln=True, align="C")

          pdf.set_font("Calibri","", 11)
          ex_table2 = []
          pdf.set_font("Calibri","", 9)
          for extra_field in calib.extra_field2:
               inp3_1 = extra_field.get('inp3_1')       
               inp3_2 = extra_field.get('inp3_2')       
               inp3_3 = extra_field.get('inp3_3')       
               inp3_4 = extra_field.get('inp3_4')       
               inp3_5 = extra_field.get('inp3_5') 
               
               if inp3_1:
                    a = [inp3_1,inp3_2,inp3_3,inp3_4,inp3_5]
                    ex_table2.append(a)

     # Rest of your code for creating the table in the PDF
          with pdf.table(col_widths=(38, 38, 38, 38,38), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER","CENTER")) as table:
               for k in range(0, len(ex_table2)):
                    data_row = ex_table2[k]
                    
                    row = table.row()
                    for i in range(0, len(data_row)):
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
     pdf.ln(2)
     pdf.cell(47.5,6,txt="Calibration Status",border=1,align="L")
     pdf.cell(47.5,6,txt=calib.calib_status,border=1,align="L")
     pdf.cell(47.5,6,txt="Maximum Error",border=1,align="L")
     pdf.cell(47.5,6,txt=calib.max_error,border=1,align="L",ln=True)

     pdf.ln(2)
     pdf.set_font("Calibri","", 10)
     pdf.multi_cell(190, 4, txt=calib.text, border=0, ln=True, align='L')

     pdf.set_font("Calibri","", 7)
     if calib.calib_by_signature:
         pdf.image(calib.calib_by_signature.signature,20,248,18,18)
     pdf.line(19,269,30+pdf.get_string_width("Calibrated By"),269)
     pdf.text(26,271,"Calibrated By")

     pdf.image('static/assets/SEPA-Sindh-LOGO-removebg-preview.png',54,250,20,18)
     pdf.text(56,270,"(License # R-K\ 242)")

     pdf.image('static/assets/ISO-9001_2015 LOGO.png',82,250,23,18)
     pdf.text(81,270,"(Certificate # 080177324-QMS)")
     

     pdf.image('static/assets/ISO-14001_2015 LOGO.png',117,250,23,18)
     pdf.text(116,270,"(Certificate # 080177424-EMS)")

     pdf.image(envitech_logo,150,248,18,18)
     if calib.checked1_signature:
         pdf.image(calib.checked1_signature.signature,170,248,18,18)
     pdf.line(190,269,140+pdf.get_string_width("Checked By"),269)
     pdf.text(165,271,"Checked By")





     pdf.set_font("Calibri","", 9)
     pdf.set_y(278)
     pdf.set_fill_color(10, 41, 120) 
     pdf.rect(10,275,190,6,"F")
     pdf.set_text_color(255, 255, 255)
     pdf.text(12,278.5,txt=calib.disc)
     

     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)


     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={calib.cert_num}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

__all__ = [
    'calibration',
    'calib_view',
    'calib_list',
    'calib_delete',
    'calib_edit',
    'calib_update',
    'calib_clone',
    'calib_clone_update',
    'calib_pdf',
    'calib_pdf1',
]
