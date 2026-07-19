# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@login_required(login_url="/login")
def inspection(request):
     if request.method == 'POST':
          cert_num = request.POST['cert_num']
          client = request.POST['client']
          address = request.POST['address']
          date = request.POST['insp_date']
          re_insp_date = request.POST['re_insp_date']
          equipment = request.POST['equipment']
          manufacturer = request.POST['Manufacturer']
          equip_id = request.POST['equip_id']
          model = request.POST['model']
          equipment_1 = request.POST['equipment_1']
          model_1 = request.POST['model_1']
          serial_no1 = request.POST['serial_no1']
          cert_num1 = request.POST['cert_num1']
          test1 = request.POST['test1']
          test2 = request.POST['test2']
          test3 = request.POST['test3']
          test4 = request.POST['test4']
          test5 = request.POST['test5']
          test6 = request.POST['test6']
          test7 = request.POST['test7']
          test8 = request.POST['test8']
          test9 = request.POST['test9']
          test10 = request.POST['test10']
          conc = request.POST['conc']
          insp_status = request.POST['insp_status']
          text = request.POST['text']
          # calib_by = request.FILES['calib_by']
          # checked = request.FILES['checked']
          # checked1 = request.FILES['checked1']
          disc = request.POST['disc']
          extra_field = request.POST['extra_field']
          extra_field1 = request.POST['extra_field1']
          city_location = request.POST['city_location']
          client_date_table = request.POST['client_date_table']
          client_equipment = request.POST['client_equipment']
          client_equipment_1 = request.POST['client_equipment_1']
          client_manufacturer = request.POST['client_manufacturer']
          client_manufacturer_1 = request.POST['client_manufacturer_1']
          client_equip_id = request.POST['client_equip_id']
          client_equip_id_1 = request.POST['client_equip_id_1']
          client_model = request.POST['client_model']
          client_model_1 = request.POST['client_model_1']
          client_location = request.POST['client_location']
          client_location_1 = request.POST['client_location_1']
          client_param = request.POST['client_param']
          client_param_1 = request.POST['client_param_1']
          client_range = request.POST['client_range']
          client_range_1 = request.POST['client_range_1']
          client_tolerance = request.POST['client_tolerance']
          client_tolerance_1 = request.POST['client_tolerance_1']
          param_1 = request.POST['param_1']
          result_1 = request.POST['result_1']
          load_cond = request.POST['load_cond']
          param_2 = request.POST['param_2']
          result_2 = request.POST['result_2']
          temp_1 = request.POST['temp_1']
          temp_2 = request.POST['temp_2']
          humidity_1 = request.POST['humidity_1']
          humidity_2 = request.POST['humidity_2']
          forklift_table = request.POST['forklift_table']
          kg1 = request.POST['kg1']
          ft_1 = request.POST['ft_1']
          ft_2 = request.POST['ft_2']
          ft_3 = request.POST['ft_3']
          ft_4 = request.POST['ft_4']
          ft_5 = request.POST['ft_5']
          weight1 = request.POST['weight1']
          set1 = request.POST['set1']
          master1 = request.POST['master1']
          before1 = request.POST['before1']
          after1 = request.POST['after1']
          dev1 = request.POST['dev1']
          weight2 = request.POST['weight2']
          set2 = request.POST['set2']
          master2 = request.POST['master2']
          before2 = request.POST['before2']
          after2 = request.POST['after2']
          dev2 = request.POST['dev2']
          weight3 = request.POST['weight3']
          set3 = request.POST['set3']
          master3 = request.POST['master3']
          before3 = request.POST['before3']
          after3 = request.POST['after3']
          dev3 = request.POST['dev3']
          weight4 = request.POST['weight4']
          set4 = request.POST['set4']
          master4 = request.POST['master4']
          before4 = request.POST['before4']
          after4 = request.POST['after4']
          dev4 = request.POST['dev4']
          knife_table = request.POST['knife_table']
          rpm1 = request.POST['rpm1']
          rpm2 = request.POST['rpm2']
          rpm3 = request.POST['rpm3']
          knife_Set_value1 = request.POST['knife_Set_value1']
          knife_master1 = request.POST['knife_master1']
          knife_before1 = request.POST['knife_before1']
          knife_after1 = request.POST['knife_after1']
          knife_dev1 = request.POST['knife_dev1']
          knife_Set_value2 = request.POST['knife_Set_value2']
          knife_master2 = request.POST['knife_master2']
          knife_before2 = request.POST['knife_before2']
          knife_after2 = request.POST['knife_after2']
          knife_dev2 = request.POST['knife_dev2']
          knife_Set_value3 = request.POST['knife_Set_value3']
          knife_master3 = request.POST['knife_master3']
          knife_before3 = request.POST['knife_before3']
          knife_after3 = request.POST['knife_after3']
          knife_dev3 = request.POST['knife_dev3']
          knife_Set_value4 = request.POST['knife_Set_value4']
          knife_master4 = request.POST['knife_master4']
          knife_before4 = request.POST['knife_before4']
          knife_after4 = request.POST['knife_after4']
          knife_dev4 = request.POST['knife_dev4']
          knife_Set_value5 = request.POST['knife_Set_value5']
          knife_master5 = request.POST['knife_master5']
          knife_before5 = request.POST['rpm2']
          knife_after5 = request.POST['knife_after5']
          knife_dev5 = request.POST['knife_dev5']
          client_equip_data = request.POST.get('client_equip_data')
          master_equip = request.POST.get('master_equip')
          physical_inspect = request.POST.get('physical_inspect')
          inspect_sign_id = request.POST.get('inspect_sign')
          check_sign_id = request.POST.get('check_sign')
          
          ispect_by_signature = Signatures.objects.get(id=inspect_sign_id)
          check1_signature = Signatures.objects.get(id=check_sign_id)
          
          inspect = Inspection(cert_num=cert_num,client=client,address=address,date=date,equipment=equipment,
                              manufacturer=manufacturer,equip_id=equip_id,model=model,equipment_1=equipment_1,model_1=model_1,
                              serial_no1=serial_no1,cert_num1=cert_num1,test1=test1,test2=test2,test3=test3,test4=test4,test5=test5,
                              test6=test6,test7=test7,test8=test8,test9=test9,test10=test10,conc=conc,text=text,city_location=city_location,
                              disc=disc,extra_field=extra_field,insp_status=insp_status,re_insp_date=re_insp_date,extra_field1=extra_field1,
                              client_date_table=client_date_table,client_equipment=client_equipment,client_equipment_1=client_equipment_1,client_manufacturer=client_manufacturer,
                              client_manufacturer_1=client_manufacturer_1,client_equip_id=client_equip_id,client_equip_id_1=client_equip_id_1,client_model=client_model,client_model_1=client_model_1,
                              client_location=client_location,client_location_1=client_location_1,client_param=client_param,client_param_1=client_param_1,client_range=client_range,client_range_1=client_range_1,
                              client_tolerance=client_tolerance,client_tolerance_1=client_tolerance_1,param_1=param_1,result_1=result_1,load_cond=load_cond,param_2=param_2,result_2=result_2,temp_1=temp_1,temp_2=temp_2,
                              humidity_1=humidity_1,humidity_2=humidity_2,forklift_table=forklift_table,kg1=kg1,ft_1=ft_1,ft_2=ft_2,ft_3=ft_3,ft_4=ft_4,ft_5=ft_5,weight1=weight1,master1=master1,before1=before1,after1=after1,weight2=weight2,
                              set1=set1,dev1=dev1,set2=set2,master2=master2,before2=before2,after2=after2,dev2=dev2,weight3=weight3,set3=set3,master3=master3,before3=before3,after3=after3,dev3=dev3,weight4=weight4,set4=set4,
                              master4=master4,before4=before4,after4=after4,dev4=dev4,knife_table=knife_table,rpm1=rpm1,rpm2=rpm2,rpm3=rpm3,knife_Set_value1=knife_Set_value1,knife_master1=knife_master1,
                              knife_before1=knife_before1,knife_after1=knife_after1,knife_dev1=knife_dev1,knife_Set_value2=knife_Set_value2,knife_master2=knife_master2,knife_before2=knife_before2,knife_after2=knife_after2,
                              knife_dev2=knife_dev2,knife_Set_value3=knife_Set_value3,knife_master3=knife_master3,knife_before3=knife_before3,knife_after3=knife_after3,knife_dev3=knife_dev3,knife_Set_value4=knife_Set_value4,
                              knife_master4=knife_master4,knife_before4=knife_before4,knife_after4=knife_after4,knife_dev4=knife_dev4,knife_Set_value5=knife_Set_value5,knife_master5=knife_master5,knife_before5=knife_before5,
                              knife_after5=knife_after5,knife_dev5=knife_dev5,client_equip_data=client_equip_data,master_equip=master_equip,physical_inspect=physical_inspect,ispect_by_signature=ispect_by_signature,check1_signature=check1_signature,created_by = request.user
                              
                              )
          inspect.save()  
          
          
          user = request.user
          action = f'Inspection certificate {inspect.cert_num} created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = (Inspection.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/inspection_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return render(request, "inspect.html")
     else:
          return render(request, "inspect.html",{'signs':signs}) 



@login_required(login_url="/login")
def inspection_list(request):
     inspect, _srch = _cert_filter(request, Inspection)
     context = {'searched':_srch, 'data':inspect}
     return render(request,"inspect_list.html",context)

@login_required(login_url="/login")
def inspect_edit(request,pk):
     inspect = Inspection.objects.get(id=pk)
     inspect.extra_field = inspect.extra_field.replace("'", "\"")
     inspect.extra_field = json.loads(inspect.extra_field)
     inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     inspect.extra_field1 = json.loads(inspect.extra_field1)
     context = {'data':inspect,'signs':signs}
     return render(request,'inspect_edit.html',context)


@login_required(login_url="/login")
def inspect_update(request,pk):
     inspect = Inspection.objects.get(id=pk)
     if request.method == 'POST':
          inspect.cert_num = request.POST['cert_num']
          inspect.client = request.POST['client']
          inspect.address = request.POST['address']
          inspect.date = request.POST['insp_date']
          inspect.re_insp_date = request.POST['re_insp_date']
          inspect.equipment = request.POST['equipment']
          inspect.manufacturer = request.POST['Manufacturer']
          inspect.equip_id = request.POST['equip_id']
          inspect.model = request.POST['model']
          inspect.equipment_1 = request.POST.get('equipment_1',"")
          inspect.model_1 = request.POST.get('model_1',"")
          inspect.serial_no1 = request.POST.get('serial_no1',"")
          inspect.cert_num1 = request.POST.get('cert_num1',"")
          inspect.test1 = request.POST.get('test1',"")
          inspect.test2 = request.POST.get('test2',"")
          inspect.test3 = request.POST.get('test3',"")
          inspect.test4 = request.POST.get('test4',"")
          inspect.test5 = request.POST.get('test5',"")
          inspect.test6 = request.POST.get('test6',"")
          inspect.test7 = request.POST.get('test7',"")
          inspect.test8 = request.POST.get('test8',"")
          inspect.test9 = request.POST.get('test9',"")
          inspect.test10 = request.POST.get('test10',"")
          inspect.conc = request.POST.get('conc',"")
          inspect.insp_status = request.POST.get('insp_status',"")
          inspect.text = request.POST.get('text',"")
          # inspect.calib_by = request.FILES['calibby']
          # inspect.checked = request.FILES['checked']
          # inspect.checked1 = request.FILES['checked1']
          inspect.disc = request.POST.get('disc',"")
          inspect.city_location = request.POST['city_location']
          inspect.client_date_table = request.POST.get('client_date_table',"")
          inspect.client_equipment = request.POST.get('client_equipment',"")
          inspect.client_equipment_1 = request.POST.get('client_equipment_1',"")
          inspect.client_manufacturer = request.POST.get('client_manufacturer',"")
          inspect.client_manufacturer_1 = request.POST.get('client_manufacturer_1',"")
          inspect.client_equip_id = request.POST.get('client_equip_id',"")
          inspect.client_equip_id_1 = request.POST.get('client_equip_id_1',"")
          inspect.client_model = request.POST.get('client_model',"")
          inspect.client_model_1 = request.POST.get('client_model_1',"")
          inspect.client_location = request.POST.get('client_location',"")
          inspect.client_location_1 = request.POST.get('client_location_1',"")
          inspect.client_param = request.POST.get('client_param',"")
          inspect.client_param_1 = request.POST.get('client_param_1',"")
          inspect.client_range = request.POST.get('client_range',"")
          inspect.client_range_1 = request.POST.get('client_range_1',"")
          inspect.client_tolerance = request.POST.get('client_tolerance',"")
          inspect.client_tolerance_1 = request.POST.get('client_tolerance_1',"")
          inspect.param_1 = request.POST.get('param_1',"")
          inspect.result_1 = request.POST.get('result_1',"")
          inspect.load_cond = request.POST.get('load_cond',"")
          inspect.param_2 = request.POST.get('param_2',"")
          inspect.result_2 = request.POST.get('result_2',"")
          inspect.temp_1 = request.POST.get('temp_1',"")
          inspect.temp_2 = request.POST.get('temp_2',"")
          inspect.humidity_1 = request.POST.get('humidity_1',"")
          inspect.humidity_2 = request.POST.get('humidity_2',"")
          inspect.forklift_table = request.POST.get('forklift_table',"")
          inspect.kg1 = request.POST.get('kg1',"")
          inspect.ft_1 = request.POST.get('ft_1',"")
          inspect.ft_2 = request.POST.get('ft_2',"")
          inspect.ft_3 = request.POST.get('ft_3',"")
          inspect.ft_4 = request.POST.get('ft_4',"")
          inspect.ft_5 = request.POST.get('ft_5',"")
          inspect.weight1 = request.POST.get('weight1',"")
          inspect.set1 = request.POST.get('set1',"")
          inspect.master1 = request.POST.get('master1',"")
          inspect.before1 = request.POST.get('before1',"")
          inspect.after1 = request.POST.get('after1',"")
          inspect.dev1 = request.POST.get('dev1',"")
          inspect.weight2 = request.POST.get('weight2',"")
          inspect.set2 = request.POST.get('set2',"")
          inspect.master2 = request.POST.get('master2',"")
          inspect.before2 = request.POST.get('before2',"")
          inspect.after2 = request.POST.get('after2',"")
          inspect.dev2 = request.POST.get('dev2',"")
          inspect.weight3 = request.POST.get('weight3',"")
          inspect.set3 = request.POST.get('set3',"")
          inspect.master3 = request.POST.get('master3',"")
          inspect.before3 = request.POST.get('before3',"")
          inspect.after3 = request.POST.get('after3',"")
          inspect.dev3 = request.POST.get('dev3',"")
          inspect.weight4 = request.POST.get('weight4',"")
          inspect.set4 = request.POST.get('set4',"")
          inspect.master4 = request.POST.get('master4',"")
          inspect.before4 = request.POST.get('before4',"")
          inspect.after4 = request.POST.get('after4',"")
          inspect.dev4 = request.POST.get('dev4',"")
          inspect.knife_table = request.POST.get('knife_table')
          inspect.rpm1 = request.POST.get('rpm1')
          inspect.rpm2 = request.POST.get('rpm2')
          inspect.rpm3 = request.POST.get('rpm3')
          inspect.knife_Set_value1 = request.POST.get('knife_Set_value1',"")
          inspect.knife_master1 = request.POST.get('knife_master1',"")
          inspect.knife_before1 = request.POST.get('knife_before1',"")
          inspect.knife_after1 = request.POST.get('knife_after1',"")
          inspect.knife_dev1 = request.POST.get('knife_dev1',"")
          inspect.knife_Set_value2 = request.POST.get('knife_Set_value2',"")
          inspect.knife_master2 = request.POST.get('knife_master2',"")
          inspect.knife_before2 = request.POST.get('knife_before2',"")
          inspect.knife_after2 = request.POST.get('knife_after2',"")
          inspect.knife_dev2 = request.POST.get('knife_dev2',"")
          inspect.knife_Set_value3 = request.POST.get('knife_Set_value3',"")
          inspect.knife_master3 = request.POST.get('knife_master3',"")
          inspect.knife_before3 = request.POST.get('knife_before3',"")
          inspect.knife_after3 = request.POST.get('knife_after3',"")
          inspect.knife_dev3 = request.POST.get('knife_dev3',"")
          inspect.knife_Set_value4 = request.POST.get('knife_Set_value4',"")
          inspect.knife_master4 = request.POST.get('knife_master4',"")
          inspect.knife_before4 = request.POST.get('knife_before4',"")
          inspect.knife_after4 = request.POST.get('knife_after4',"")
          inspect.knife_dev4 = request.POST.get('knife_dev4',"")
          inspect.knife_Set_value5 = request.POST.get('knife_Set_value5',"")
          inspect.knife_master5 = request.POST.get('knife_master5',"")
          inspect.knife_before5 = request.POST.get('rpm2',"")
          inspect.knife_after5 = request.POST.get('knife_after5',"")
          inspect.knife_dev5 = request.POST.get('knife_dev5',"")
          inspect.client_equip_data = request.POST.get('client_equip_data',"")
          inspect.master_equip = request.POST.get('master_equip',"")
          inspect.physical_inspect = request.POST.get('physical_inspect',"")
          inspect.extra_field = json.loads(request.POST["extra_field"])
          
          
          if inspect.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    test = request.POST.getlist('test[]')[i]
                    observation = request.POST.getlist('observation[]')[i]

                    inspect.extra_field.append({
                         'sr':sr,
                         'test':test,
                         'observation':observation,
                    })
          
          
          inspect.extra_field = json.dumps(inspect.extra_field)

          inspect.extra_field1 = json.loads(request.POST["extra_field1"])
          
          if inspect.extra_field1:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    inp1 = request.POST.getlist('inp1[]')[i]
                    inp2 = request.POST.getlist('inp2[]')[i]
                    inp3 = request.POST.getlist('inp3[]')[i]
                    inp4 = request.POST.getlist('inp4[]')[i]

                    inspect.extra_field1.append({
                         'sr':sr,
                         'inp1':inp1,
                         'inp2':inp2,
                         'inp3':inp3,
                         'inp4':inp4,
                    })
          
          
          inspect.extra_field1 = json.dumps(inspect.extra_field1)
          city_location_clean = inspect.city_location.strip().lower().rstrip('.')

          inspect_sign_id = request.POST.get('inspect_sign')
          check_sign_id = request.POST.get('check_sign')
          
          ispect_by_signature = Signatures.objects.get(id=inspect_sign_id)
          check1_signature = Signatures.objects.get(id=check_sign_id)
          inspect.ispect_by_signature=ispect_by_signature
          inspect.check1_signature=check1_signature
          inspect.created_by = request.user
          inspect.save()
          user = request.user
          action = f'Inspection certificate {inspect.cert_num} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = inspect.id
          if "submit_and_view" in request.POST:
               url = f'/inspection_view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('inspection_list')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return render(request,"inspect_list.html")                                                                                                                                                                                                                                                                                                                                                                                                                    


@login_required(login_url="/login")
def inspect_delete(request,pk):
     inspect = Inspection.objects.get(id=pk)
     inspect.delete()
     user = request.user
     action = f'Inspection certificate {inspect.cert_num} deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     return redirect(to='inspection_list')



@login_required(login_url="/login")
def inspect_clone(request,pk):
     inspect = Inspection.objects.get(id=pk)
     inspect.extra_field = inspect.extra_field.replace("'", "\"")
     inspect.extra_field = json.loads(inspect.extra_field)
     inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     inspect.extra_field1 = json.loads(inspect.extra_field1)
     context = {'data':inspect,'signs':signs} 
     return render(request,'inspect_clone.html',context) 


@login_required(login_url="/login")
def inspect_clone_update(request,pk):     
     try:
        # Fetch the existing form instance by ID
         existing_Form = Inspection.objects.get(id=pk)
     except Inspection.DoesNotExist:
         return HttpResponse("Form not found", status=404)  
     if request.method == 'POST':
          existing_Form.cert_num = request.POST['cert_num']
          existing_Form.client = request.POST['client']
          existing_Form.address = request.POST['address']
          existing_Form.date = request.POST['insp_date']
          existing_Form.re_insp_date = request.POST['re_insp_date']
          existing_Form.equipment = request.POST['equipment']
          existing_Form.manufacturer = request.POST['Manufacturer']
          existing_Form.equip_id = request.POST['equip_id']
          existing_Form.model = request.POST['model']
          existing_Form.equipment_1 = request.POST['equipment_1']
          existing_Form.model_1 = request.POST['model_1']
          existing_Form.serial_no1 = request.POST['serial_no1']
          existing_Form.cert_num1 = request.POST['cert_num1']
          existing_Form.test1 = request.POST.get('test1',"")
          existing_Form.test2 = request.POST.get('test2',"")
          existing_Form.test3 = request.POST.get('test3',"")
          existing_Form.test4 = request.POST.get('test4',"")
          existing_Form.test5 = request.POST.get('test5',"")
          existing_Form.test6 = request.POST.get('test6',"")
          existing_Form.test7 = request.POST.get('test7',"")
          existing_Form.test8 = request.POST.get('test8',"")
          existing_Form.test9 = request.POST.get('test9',"")
          existing_Form.test10 = request.POST.get('test10',"")
          existing_Form.conc = request.POST.get('conc',"")
          existing_Form.insp_status = request.POST.get('insp_status',"")
          existing_Form.text = request.POST.get('text',"")
          # existing_Form.calib_by = request.FILES['calibby']
          # existing_Form.checked = request.FILES['checked']
          # existing_Form.checked1 = request.FILES['checked1']
          existing_Form.disc = request.POST.get('disc',"")
          existing_Form.city_location = request.POST.get('city_location',"")
          existing_Form.client_date_table = request.POST.get('client_date_table',"")
          existing_Form.client_equipment = request.POST.get('client_equipment',"")
          existing_Form.client_equipment_1 = request.POST.get('client_equipment_1',"")
          existing_Form.client_manufacturer = request.POST.get('client_manufacturer',"")
          existing_Form.client_manufacturer_1 = request.POST.get('client_manufacturer_1',"")
          existing_Form.client_equip_id = request.POST.get('client_equip_id',"")
          existing_Form.client_equip_id_1 = request.POST.get('client_equip_id_1',"")
          existing_Form.client_model = request.POST.get('client_model',"")
          existing_Form.client_model_1 = request.POST.get('client_model_1',"")
          existing_Form.client_location = request.POST.get('client_location',"")
          existing_Form.client_location_1 = request.POST.get('client_location_1',"")
          existing_Form.client_param = request.POST.get('client_param',"")
          existing_Form.client_param_1 = request.POST.get('client_param_1',"")
          existing_Form.client_range = request.POST.get('client_range',"")
          existing_Form.client_range_1 = request.POST.get('client_range_1',"")
          existing_Form.client_tolerance = request.POST.get('client_tolerance',"")
          existing_Form.client_tolerance_1 = request.POST.get('client_tolerance_1',"")
          existing_Form.param_1 = request.POST.get('param_1',"")
          existing_Form.result_1 = request.POST.get('result_1',"")
          existing_Form.load_cond = request.POST.get('load_cond',"")
          existing_Form.param_2 = request.POST.get('param_2',"")
          existing_Form.result_2 = request.POST.get('result_2',"")
          existing_Form.temp_1 = request.POST.get('temp_1',"")
          existing_Form.temp_2 = request.POST.get('temp_2',"")
          existing_Form.humidity_1 = request.POST.get('humidity_1',"")
          existing_Form.humidity_2 = request.POST.get('humidity_2',"")
          existing_Form.forklift_table = request.POST.get('forklift_table',"")
          existing_Form.kg1 = request.POST.get('kg1',"")
          existing_Form.ft_1 = request.POST.get('ft_1',"")
          existing_Form.ft_2 = request.POST.get('ft_2',"")
          existing_Form.ft_3 = request.POST.get('ft_3',"")
          existing_Form.ft_4 = request.POST.get('ft_4',"")
          existing_Form.ft_5 = request.POST.get('ft_5',"")
          existing_Form.weight1 = request.POST.get('weight1',"")
          existing_Form.set1 = request.POST.get('set1',"")
          existing_Form.master1 = request.POST.get('master1',"")
          existing_Form.before1 = request.POST.get('before1',"")
          existing_Form.after1 = request.POST.get('after1',"")
          existing_Form.dev1 = request.POST.get('dev1',"")
          existing_Form.weight2 = request.POST.get('weight2',"")
          existing_Form.set2 = request.POST.get('set2',"")
          existing_Form.master2 = request.POST.get('master2',"")
          existing_Form.before2 = request.POST.get('before2',"")
          existing_Form.after2 = request.POST.get('after2',"")
          existing_Form.dev2 = request.POST.get('dev2',"")
          existing_Form.weight3 = request.POST.get('weight3',"")
          existing_Form.set3 = request.POST.get('set3',"")
          existing_Form.master3 = request.POST.get('master3',"")
          existing_Form.before3 = request.POST.get('before3',"")
          existing_Form.after3 = request.POST.get('after3',"")
          existing_Form.dev3 = request.POST.get('dev3',"")
          existing_Form.weight4 = request.POST.get('weight4',"")
          existing_Form.set4 = request.POST.get('set4',"")
          existing_Form.master4 = request.POST.get('master4',"")
          existing_Form.before4 = request.POST.get('before4',"")
          existing_Form.after4 = request.POST.get('after4',"")
          existing_Form.dev4 = request.POST.get('dev4',"")
          existing_Form.knife_table = request.POST.get('knife_table',"")
          existing_Form.rpm1 = request.POST.get('rpm1',"")
          existing_Form.rpm2 = request.POST.get('rpm2',"")
          existing_Form.rpm3 = request.POST.get('rpm3',"")
          existing_Form.knife_Set_value1 = request.POST.get('knife_Set_value1',"")
          existing_Form.knife_master1 = request.POST.get('knife_master1',"")
          existing_Form.knife_before1 = request.POST.get('knife_before1',"")
          existing_Form.knife_after1 = request.POST.get('knife_after1',"")
          existing_Form.knife_dev1 = request.POST.get('knife_dev1',"")
          existing_Form.knife_Set_value2 = request.POST.get('knife_Set_value2',"")
          existing_Form.knife_master2 = request.POST.get('knife_master2',"")
          existing_Form.knife_before2 = request.POST.get('knife_before2',"")
          existing_Form.knife_after2 = request.POST.get('knife_after2',"")
          existing_Form.knife_dev2 = request.POST.get('knife_dev2',"")
          existing_Form.knife_Set_value3 = request.POST.get('knife_Set_value3',"")
          existing_Form.knife_master3 = request.POST.get('knife_master3',"")
          existing_Form.knife_before3 = request.POST.get('knife_before3',"")
          existing_Form.knife_after3 = request.POST.get('knife_after3',"")
          existing_Form.knife_dev3 = request.POST.get('knife_dev3',"")
          existing_Form.knife_Set_value4 = request.POST.get('knife_Set_value4',"")
          existing_Form.knife_master4 = request.POST.get('knife_master4',"")
          existing_Form.knife_before4 = request.POST.get('knife_before4',"")
          existing_Form.knife_after4 = request.POST.get('knife_after4',"")
          existing_Form.knife_dev4 = request.POST.get('knife_dev4',"")
          existing_Form.knife_Set_value5 = request.POST.get('knife_Set_value5',"")
          existing_Form.knife_master5 = request.POST.get('knife_master5',"")
          existing_Form.knife_before5 = request.POST.get('rpm2',"")
          existing_Form.knife_after5 = request.POST.get('knife_after5',"")
          existing_Form.knife_dev5 = request.POST.get('knife_dev5',"")
          existing_Form.client_equip_data = request.POST.get('client_equip_data')
          existing_Form.master_equip = request.POST.get('master_equip')
          existing_Form.physical_inspect = request.POST.get('physical_inspect')
          existing_Form.extra_field = json.loads(request.POST["extra_field"])
          
          if existing_Form.extra_field:
               for i in range(len(request.POST.getlist('sr[]'))):
                    sr = request.POST.getlist('sr[]')[i]
                    test = request.POST.getlist('test[]')[i]
                    observation = request.POST.getlist('observation[]')[i]

                    existing_Form.extra_field.append({
                         'sr':sr,
                         'test':test,
                         'observation':observation,
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
          
          
          inspect_sign_id = request.POST.get('inspect_sign')
          check_sign_id = request.POST.get('check_sign')
          
          ispect_by_signature = Signatures.objects.get(id=inspect_sign_id)
          check1_signature = Signatures.objects.get(id=check_sign_id)
          existing_Form.ispect_by_signature=ispect_by_signature
          existing_Form.check1_signature=check1_signature
          existing_Form.id = None
          existing_Form.created_by = request.user
          existing_Form.save()
          user = request.user
          action = f'Inspection certificate {existing_Form.cert_num} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = existing_Form.id
          if "submit_and_view" in request.POST:
               url = f'/inspection_view/{str(id)}/'
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               return redirect('inspection_list')
          else:
               return HttpResponse('Invalid Request Method',status=400)
     return render(request,"inspect_list.html")                          


def inspect_view(request,pk):
     from PIL import Image
     inspect = Inspection.objects.get(id=pk)
     current_url = request.build_absolute_uri()
     inspect.extra_field = inspect.extra_field.replace("'", "\"")
     inspect.extra_field = json.loads(inspect.extra_field)
     inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     inspect.extra_field1 = json.loads(inspect.extra_field1)
     


     qr_filename = f"qr_{inspect.cert_num}.png"
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

     context ={'data':inspect,'qr':qr_relative_path,'logo':logo}

     return render(request,'inspect_view.html',context)   


def inspect_pdf(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_inspect_pdf as PDFWithPageNumbers

               





     inspect = Inspection.objects.get(id=pk)
     inspect.extra_field = inspect.extra_field.replace("'", "\"")
     inspect.extra_field = json.loads(inspect.extra_field)
     inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     inspect.extra_field1 = json.loads(inspect.extra_field1)
     pdf = PDFWithPageNumbers()
     pdf._rq_envitech_logo, pdf._rq_inspect, pdf._rq_pk, pdf._rq_request = envitech_logo, inspect, pk, request
     pdf.add_page()
     
     # font_path = "static/fonts/calibri.ttf"
     # font_path_bold = "static/fonts/calibrib.ttf"
     # pdf.add_font("Calibri","",font_path,uni=True)
     # pdf.add_font("Calibri","B",font_path_bold,uni=True)
     # pdf.set_font("Calibri","", 9)
     # pdf.set_auto_page_break(auto=True, margin=5)
     
     # pdf.add_font("Calibri","B",font_path_bold,uni=True)
     # pdf.add_font('ScriptMT', '', 'static/fonts/SCRIPTBL.TTF', uni=True)
     # pdf.set_font('ScriptMT', '', 25)
     # pdf.text(60,43,txt='Certificate of Inspection')
     # pdf.set_font("Calibri","B", 11)
     # pdf.text(10,60,txt='Certificate Number:')
     # pdf.line(42,61.5,60,61.5)
     # pdf.set_font("Calibri","", 11)
     # pdf.text(43,60,txt=(inspect.cert_num or ""))

     # target_url = request.build_absolute_uri(reverse('inspect_view', kwargs={'pk': pk}))
    
     # # Generate the QR code for the target URL
     # qr_filename = f"qr_{pk}.png"
     # qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
  
     # qr = qrcode.QRCode(
     #      version=1,
     #      error_correction=qrcode.constants.ERROR_CORRECT_L,
     #      box_size=10,
     #      border=6,
     # )
     # qr.add_data(target_url)  # Add the dynamically generated URL
     # qr.make(fit=True)
     # img = qr.make_image(fill_color="black", back_color="white")
     # img.save(qr_file_path)


     # pdf.image(qr_file_path,"R",y=46,w=20,h=20)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,70,40,6)
     pdf.cell(47.5,6,txt="Client",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,70,150,6)
     pdf.cell(142.5,6,txt=inspect.client,border=True,ln=True)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,76,40,6)
     pdf.cell(47.5,6,txt="Address",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,76,150,6)
     pdf.cell(142.5,6,txt=inspect.address,ln=True,border=True,)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,82,40,6)
     pdf.cell(47.5,6,txt="Inspection Date",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,82,55,6)
     pdf.cell(47.5,6,txt=inspect.date,border=True)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(105,82,40,6)
     pdf.cell(47.5,6,txt="Re-Inspection Date",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(145,82,55,6)
     pdf.cell(47.5,6,txt=inspect.re_insp_date,border=True,ln=True)



     if inspect.client_equip_data:
          pdf.ln(3)
          pdf.set_font("Calibri","B", 11)
          # pdf.rect(10,91,190,6)
          pdf.cell(190,6,txt="Client's Equipment Data",border=True,ln=True)

          # pdf.rect(10,97,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Equipment",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(50,97,50,6)
          pdf.cell(47.5,6,txt=inspect.equipment,border=True)

          # pdf.rect(100,97,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Manufacturer",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(140,97,60,6)
          pdf.cell(47.5,6,txt=inspect.manufacturer,ln=True,border=True)

          # pdf.rect(10,103,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Equipment ID",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(50,103,50,6)
          pdf.cell(47.5,6,txt=inspect.equip_id,border=True)

          # pdf.rect(100,103,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Model / Type",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(140,103,60,6)
          pdf.cell(47.5,6,txt=inspect.model,border=True,ln=True)
     
     
     # pdf.rect(10,112,190,6)
     # pdf.set_font("Calibri","B", 11)
     # pdf.text(12,116,txt="Master Equipment and References")

     
     pdf.ln(3)
     # pdf.set_y(112)
     pdf.set_font("Calibri","B", 11)
     if inspect.master_equip:
          pdf.cell(190,6,"Master Equipment and References",border=True,ln=True)
          pdf.set_y(118)
     
     
          pdf.cell(47.5,6,"Equipment",align="C",border=True)
          pdf.cell(47.5,6,"Model",align="C",border=True)
          pdf.cell(47.5,6,"Serial No",align="C",border=True)
          pdf.cell(47.5,6,"Certificate",align="C",border=True,ln=True)
          
          pdf.cell(47.5,6,f"{inspect.equipment_1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.model_1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.serial_no1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.cert_num1}",border=True,align="C",ln=True)

          
          if inspect.extra_field1:
               for extra_field in inspect.extra_field1:
                    inp1 = extra_field.get('inp1')
                    inp2 = extra_field.get('inp2')
                    inp3 = extra_field.get('inp3')
                    inp4 = extra_field.get('inp4') 
                    pdf.cell(47.5,6,f"{inp1}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp2}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp3}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp4}",border=True,align="C",ln=True)    
                    pdf.ln(3)

     pdf.ln(3)
     if inspect.client_date_table:
          pdf.set_font("Calibri","B", 12)
          # pdf.text(10,136,txt='Physical Inspection & Testing')
          pdf.cell(190,6,txt=f"{inspect.client_date_table}",ln=True,border=1)
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_equipment}",border=True)
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(47.5,6,txt=inspect.client_equipment_1,border=True)

          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_manufacturer}",border=True)
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(47.5,6,txt=inspect.client_manufacturer_1,border=True,ln=True)

          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_equip_id}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_equip_id_1,border=True)
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_model}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_model_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_location}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(142.5,6,txt=inspect.client_location_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_param}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_param_1,border=True,)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_range}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_range_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_tolerance}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(142.5,6,txt=inspect.client_tolerance_1,border=True,ln=True)
          
          pdf.ln(3)
     
     if inspect.param_1:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(63.3,6,txt=f"Parameters",border=True,align='C')
          pdf.cell(63.3,6,txt=f"Results",border=True,align='C')
          pdf.cell(63.3,6,txt=f"Load Condition Static/Dynamic",border=True,align='C',ln=True)
          
          old_x = pdf.get_x()
          pdf.cell(63.3,6,txt=f"{inspect.param_1}",border=True)
          pdf.cell(63.3,6,txt=f"{inspect.result_1}",border=True,)
          
          pdf.cell(63.3,12,txt=f"{inspect.load_cond}",border=True,align="C")
          
          pdf.set_x(old_x)
          pdf.set_y(pdf.get_y()+6)
          pdf.cell(63.3,6,txt=f"{inspect.param_2}",border=True)
          pdf.cell(63.3,6,txt=f"{inspect.result_2}",border=True,ln=True)
          pdf.ln(3)
     
     
     pdf.ln(3)
     
     if inspect.physical_inspect:
          pdf.set_font("Calibri","B", 12)
          # pdf.text(10,136,txt='Physical Inspection & Testing')
          pdf.cell(190,6,txt="Physical Inspection & Testing",ln=True,border=1)

          table_2 =[['Testing Parameter','Observation']]

          pdf.set_font("Calibri","", 11)
          if inspect.test1:
               a = [inspect.test1,inspect.test2]
               table_2.append(a)
          if inspect.test3:
               a = [inspect.test3,inspect.test4]
               table_2.append(a)
          if inspect.test5:
               a = [inspect.test5,inspect.test6]
               table_2.append(a)
          if inspect.test7:
               a = [inspect.test7,inspect.test8]
               table_2.append(a)
          if inspect.test9:
               a = [inspect.test9,inspect.test10]
               table_2.append(a)
          
          
          for extra_field in inspect.extra_field:
               test = extra_field.get('test')       
               observation = extra_field.get('observation') 
               if test :
                    a = [test,observation]
                    table_2.append(a)
          
          with pdf.table(col_widths=(90, 90),width=190,line_height=6,text_align=("LEFT","LEFT")) as table:
                    num_rows = 0
                    for k in range(0,len(table_2)):
                         data_row = table_2[k]
                         num_rows = num_rows + 1
                         
                         # watwer mark
                         # pdf.set_page_background("static/assets/Capture.PNG")
                         row = table.row()
                         for i in range(0,len(data_row)):
                              datum = data_row[i]
                              row.cell(datum)
     
          

     if inspect.temp_1:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(38,6,"Test Environment",border=True,)
          pdf.set_font("Calibri","", 11)
          pdf.cell(38,6,f"{inspect.temp_1}",border=True,)
          pdf.cell(38,6,f"{inspect.temp_2}",border=True,)
          pdf.cell(38,6,f"{inspect.humidity_1}",border=True,)
          pdf.cell(38,6,f"{inspect.humidity_2}",border=True,ln=True)
          
          
     if pdf.get_y() > 230:  # Adjust the threshold as per your footer height
          pdf.add_page()
     pdf.ln(3)
     
     if inspect.forklift_table:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(190,6,f"{inspect.forklift_table}",border=True,ln=True)
          
          pdf.cell(15,6,f"Weight",border=True,align="C")
          pdf.cell(27.5,6,f"Set Value Height",border=True,align="C")
          pdf.cell(38.5,6,f"Master Reading Height",border=True,align="C")
          pdf.cell(41,6,f"Actual Reading (Before)",border=True,align="C")
          pdf.cell(39,6,f"Actual Reading (After)",border=True,align="C")
          pdf.cell(29,6,f"Deviation Height",border=True,ln=True,align="C")
          
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(15,6,f"{inspect.kg1}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.ft_1}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.ft_2}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.ft_3}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.ft_4}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.ft_5}",border=True,ln=True,align="C")
          
          
          pdf.cell(15,6,f"{inspect.weight1}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set1}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master1}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before1}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after1}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev1}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(15,6,f"{inspect.weight2}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set2}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master2}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before2}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after2}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev2}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(15,6,f"{inspect.weight3}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set3}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master3}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before3}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after3}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev3}",border=True,ln=True,align="C")
     
     if pdf.get_y() > 230:  # Adjust the threshold as per your footer height
          pdf.add_page()
     pdf.ln(3)
     
     
     if inspect.knife_table:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(190,6,f"{inspect.knife_table}",border=True,ln=True)
          
          
          pdf.cell(38,6,f"Set Value",border=True,align="C")
          pdf.cell(38,6,f"Master Reading",border=True,align="C")
          pdf.cell(38,6,f"Actual Reading (Before)",border=True,align="C")
          pdf.cell(38,6,f"Actual Reading (After)",border=True,align="C")
          pdf.cell(38,6,f"Deviation",border=True,ln=True,align="C")
          
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(76,6,f"{inspect.rpm1}",border=True,align="C")
          pdf.cell(76,6,f"{inspect.rpm2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.rpm3}",border=True,align="C",ln=True)
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev1}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev2}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev3}",border=True,ln=True,align="C")
     
     
          
          if inspect.knife_Set_value4:
               pdf.cell(38,6,f"{inspect.knife_Set_value4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_master4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_before4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_after4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_dev4}",border=True,ln=True,align="C")
     
     
          
          
          pdf.ln(3)          
     
     pdf.multi_cell(190,5,txt="Conclusion: " +" "+ inspect.conc,border=1,ln=True)
     pdf.cell(190,6,txt="Inspection Status :"+ " "+ inspect.insp_status,border=1,ln=True)

     pdf.ln(2)
     pdf.set_font("Calibri","", 10)
     pdf.multi_cell(190,4,txt=inspect.text,ln=True)
     
     # number_of_rows = 98  # Replace with the actual number of rows
     # row_height = 2  # Replace with the actual row height in your table
     # table_height = (number_of_rows) * row_height  
     
     # if pdf.y + number_of_rows * row_height >= pdf.h:
     #      pdf.add_page()   
     
     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
     )
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={inspect.cert_num}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def inspect_pdf1(request,pk):
     from fpdf import FPDF
     inspect = Inspection.objects.get(id=pk)
     inspect.extra_field = inspect.extra_field.replace("'", "\"")
     inspect.extra_field = json.loads(inspect.extra_field)
     inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     inspect.extra_field1 = json.loads(inspect.extra_field1)
     from EnviTechAlApp.pdf_common import PDF_inspect_pdf1 as PDFWithPageNumbers

     # inspect = Inspection.objects.get(id=pk)
     # inspect.extra_field = inspect.extra_field.replace("'", "\"")
     # inspect.extra_field = json.loads(inspect.extra_field)
     # inspect.extra_field1 = inspect.extra_field1.replace("'", "\"")
     # inspect.extra_field1 = json.loads(inspect.extra_field1)
     pdf = PDFWithPageNumbers()
     pdf._rq_envitech_logo, pdf._rq_inspect, pdf._rq_pk, pdf._rq_request = envitech_logo, inspect, pk, request
     pdf.set_auto_page_break(auto=True, margin=10)  # Enable automatic page breaks
     pdf.add_page()
     
     
     
     

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,70,40,6)
     pdf.cell(47.5,6,txt="Client",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,70,150,6)
     pdf.cell(142.5,6,txt=inspect.client,border=True,ln=True)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,76,40,6)
     pdf.cell(47.5,6,txt="Address",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,76,150,6)
     pdf.cell(142.5,6,txt=inspect.address,ln=True,border=True,)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(10,82,40,6)
     pdf.cell(47.5,6,txt="Inspection Date",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(50,82,55,6)
     pdf.cell(47.5,6,txt=inspect.date,border=True)

     pdf.set_font("Calibri","B", 11)
     # pdf.rect(105,82,40,6)
     pdf.cell(47.5,6,txt="Re-Inspection Date",border=True)
     pdf.set_font("Calibri","", 11)
     # pdf.rect(145,82,55,6)
     pdf.cell(47.5,6,txt=inspect.re_insp_date,border=True,ln=True)

     

     if inspect.client_equip_data:
          pdf.ln(3)
          pdf.set_font("Calibri","B", 11)
          # pdf.rect(10,91,190,6)
          pdf.cell(190,6,txt="Client's Equipment Data",border=True,ln=True)

          # pdf.rect(10,97,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Equipment",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(50,97,50,6)
          pdf.cell(47.5,6,txt=inspect.equipment,border=True)

          # pdf.rect(100,97,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Manufacturer",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(140,97,60,6)
          pdf.cell(47.5,6,txt=inspect.manufacturer,ln=True,border=True)

          # pdf.rect(10,103,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Equipment ID",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(50,103,50,6)
          pdf.cell(47.5,6,txt=inspect.equip_id,border=True)

          # pdf.rect(100,103,40,6)
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt="Model / Type",border=True)
          pdf.set_font("Calibri","", 11)
          # pdf.rect(140,103,60,6)
          pdf.cell(47.5,6,txt=inspect.model,border=True,ln=True)
     
     
     # pdf.rect(10,112,190,6)
     # pdf.set_font("Calibri","B", 11)
     # pdf.text(12,116,txt="Master Equipment and References")

     
     pdf.ln(3)
     # pdf.set_y(112)
     pdf.set_font("Calibri","B", 11)
     if inspect.master_equip:
          pdf.cell(190,6,"Master Equipment and References",border=True,ln=True)
          pdf.set_y(118)
     
     
          pdf.cell(47.5,6,"Equipment",align="C",border=True)
          pdf.cell(47.5,6,"Model",align="C",border=True)
          pdf.cell(47.5,6,"Serial No",align="C",border=True)
          pdf.cell(47.5,6,"Certificate",align="C",border=True,ln=True)
          
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(47.5,6,f"{inspect.equipment_1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.model_1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.serial_no1}",border=True,align="C")
          pdf.cell(47.5,6,f"{inspect.cert_num1}",border=True,align="C",ln=True)

          
          if inspect.extra_field1:
               for extra_field in inspect.extra_field1:
                    inp1 = extra_field.get('inp1')
                    inp2 = extra_field.get('inp2')
                    inp3 = extra_field.get('inp3')
                    inp4 = extra_field.get('inp4') 
                    pdf.cell(47.5,6,f"{inp1}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp2}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp3}",border=True,align="C")
                    pdf.cell(47.5,6,f"{inp4}",border=True,align="C",ln=True)    
                    pdf.ln(3)
     #      table_1.append(a)
     # table_1 = [['Equipment','Model','Serial No.','Certificate']]
     # pdf.set_font("Calibri","", 11)
     # a = [inspect.equipment_1,inspect.model_1,inspect.serial_no1,inspect.cert_num1]
     # table_1.append(a)
     # if inspect.extra_field1:
     #      for extra_field in inspect.extra_field1:
     #           inp1 = extra_field.get('inp1')
     #           inp2 = extra_field.get('inp2')
     #           inp3 = extra_field.get('inp3')
     #           inp4 = extra_field.get('inp4')
     #      a =[inp1,inp2,inp3,inp4]     
     #      table_1.append(a)

     # with pdf.table(col_widths=(20, 20, 20, 30), line_height=6, text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
     #      for k in range(0, len(table_1)):
     #           data_row = table_1[k]
               
     #           row = table.row()
     #           for i in range(0, len(data_row)):
     #                datum = data_row[i]
     #                row.cell(datum)

     pdf.ln(3)
     if inspect.client_date_table:
          pdf.set_font("Calibri","B", 12)
          # pdf.text(10,136,txt='Physical Inspection & Testing')
          pdf.cell(190,6,txt=f"{inspect.client_date_table}",ln=True,border=1)
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_equipment}",border=True)
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(47.5,6,txt=inspect.client_equipment_1,border=True)

          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_manufacturer}",border=True)
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(47.5,6,txt=inspect.client_manufacturer_1,border=True,ln=True)

          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_equip_id}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_equip_id_1,border=True)
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_model}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_model_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_location}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(142.5,6,txt=inspect.client_location_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_param}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_param_1,border=True,)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_range}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(47.5,6,txt=inspect.client_range_1,border=True,ln=True)
          
          
          pdf.set_font("Calibri","B", 11)
          pdf.cell(47.5,6,txt=f"{inspect.client_tolerance}",border=True)
          pdf.set_font("Calibri","", 11)
          pdf.cell(142.5,6,txt=inspect.client_tolerance_1,border=True,ln=True)
          
          pdf.ln(3)
     
     if inspect.param_1:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(63.3,6,txt=f"Parameters",border=True,align='C')
          pdf.cell(63.3,6,txt=f"Results",border=True,align='C')
          pdf.cell(63.3,6,txt=f"Load Condition Static/Dynamic",border=True,align='C',ln=True)
          
          old_x = pdf.get_x()
          pdf.cell(63.3,6,txt=f"{inspect.param_1}",border=True)
          pdf.cell(63.3,6,txt=f"{inspect.result_1}",border=True,)
          
          pdf.cell(63.3,12,txt=f"{inspect.load_cond}",border=True,align="C")
          
          pdf.set_x(old_x)
          pdf.set_y(pdf.get_y()+6)
          pdf.cell(63.3,6,txt=f"{inspect.param_2}",border=True)
          pdf.cell(63.3,6,txt=f"{inspect.result_2}",border=True,ln=True)
          # pdf.cell(63.3,6,txt=f"",border="LBR")
          # pdf.set_y(178)
          # pdf.set_x(136.89)
          
          pdf.ln(3)
     
     if inspect.physical_inspect:
          pdf.set_font("Calibri","B", 12)
          # pdf.text(10,136,txt='Physical Inspection & Testing')
          pdf.cell(190,6,txt="Physical Inspection & Testing",ln=True,border=1)

          table_2 =[['Testing Parameter','Observation']]

          pdf.set_font("Calibri","", 11)
          if inspect.test1:
               a = [inspect.test1,inspect.test2]
               table_2.append(a)
          if inspect.test3:
               a = [inspect.test3,inspect.test4]
               table_2.append(a)
          if inspect.test5:
               a = [inspect.test5,inspect.test6]
               table_2.append(a)
          if inspect.test7:
               a = [inspect.test7,inspect.test8]
               table_2.append(a)
          if inspect.test9:
               a = [inspect.test9,inspect.test10]
               table_2.append(a)
          
          
          for extra_field in inspect.extra_field:
               test = extra_field.get('test')       
               observation = extra_field.get('observation') 
               if test :
                    a = [test,observation]
                    table_2.append(a)
          
          with pdf.table(col_widths=(90, 90),width=190,line_height=6,text_align=("LEFT","LEFT")) as table:
                    num_rows = 0
                    for k in range(0,len(table_2)):
                         data_row = table_2[k]
                         num_rows = num_rows + 1
                         
                         # watwer mark
                         # pdf.set_page_background("static/assets/Capture.PNG")
                         row = table.row()
                         for i in range(0,len(data_row)):
                              datum = data_row[i]
                              row.cell(datum)
    

     
     if inspect.temp_1:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(38,6,"Test Environment",border=True,)
          pdf.set_font("Calibri","", 11)
          pdf.cell(38,6,f"{inspect.temp_1}",border=True,)
          pdf.cell(38,6,f"{inspect.temp_2}",border=True,)
          pdf.cell(38,6,f"{inspect.humidity_1}",border=True,)
          pdf.cell(38,6,f"{inspect.humidity_2}",border=True,ln=True)
     
     if pdf.get_y() > 240:  # Adjust the threshold as per your footer height
          pdf.add_page()           
          
     
          

     # pdf.set_font("Calibri","B", 11)
     # pdf.cell(38,6,"Test Environment",border=True,)
     # pdf.set_font("Calibri","", 11)
     # pdf.cell(38,6,f"{inspect.temp_1}",border=True,)
     # pdf.cell(38,6,f"{inspect.temp_2}",border=True,)
     # pdf.cell(38,6,f"{inspect.humidity_1}",border=True,)
     # pdf.cell(38,6,f"{inspect.humidity_2}",border=True,ln=True)
     
     pdf.ln(3)
     
     if inspect.forklift_table:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(190,6,f"{inspect.forklift_table}",border=True,ln=True)
          
          pdf.cell(15,6,f"Weight",border=True,align="C")
          pdf.cell(27.5,6,f"Set Value Height",border=True,align="C")
          pdf.cell(38.5,6,f"Master Reading Height",border=True,align="C")
          pdf.cell(41,6,f"Actual Reading (Before)",border=True,align="C")
          pdf.cell(39,6,f"Actual Reading (After)",border=True,align="C")
          pdf.cell(29,6,f"Deviation Height",border=True,ln=True,align="C")
          
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(15,6,f"{inspect.kg1}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.ft_1}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.ft_2}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.ft_3}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.ft_4}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.ft_5}",border=True,ln=True,align="C")
          
          
          pdf.cell(15,6,f"{inspect.weight1}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set1}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master1}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before1}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after1}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev1}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(15,6,f"{inspect.weight2}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set2}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master2}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before2}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after2}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev2}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(15,6,f"{inspect.weight3}",border=True,align="C")
          pdf.cell(27.5,6,f"{inspect.set3}",border=True,align="C")
          pdf.cell(38.5,6,f"{inspect.master3}",border=True,align="C")
          pdf.cell(41,6,f"{inspect.before3}",border=True,align="C")
          pdf.cell(39,6,f"{inspect.after3}",border=True,align="C")
          pdf.cell(29,6,f"{inspect.dev3}",border=True,ln=True,align="C")
     
     
     pdf.ln(3)
     
     
     if inspect.knife_table:
          pdf.set_font("Calibri","B", 11)
          pdf.cell(190,6,f"{inspect.knife_table}",border=True,ln=True)
          
          
          pdf.cell(38,6,f"Set Value",border=True,align="C")
          pdf.cell(38,6,f"Master Reading",border=True,align="C")
          pdf.cell(38,6,f"Actual Reading (Before)",border=True,align="C")
          pdf.cell(38,6,f"Actual Reading (After)",border=True,align="C")
          pdf.cell(38,6,f"Deviation",border=True,ln=True,align="C")
          
          pdf.set_font("Calibri","", 11)
          
          pdf.cell(76,6,f"{inspect.rpm1}",border=True,align="C")
          pdf.cell(76,6,f"{inspect.rpm2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.rpm3}",border=True,align="C",ln=True)
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after1}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev1}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after2}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev2}",border=True,ln=True,align="C")
     
     
          
          
          pdf.cell(38,6,f"{inspect.knife_Set_value3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_master3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_before3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_after3}",border=True,align="C")
          pdf.cell(38,6,f"{inspect.knife_dev3}",border=True,ln=True,align="C")
     
     
          
          if inspect.knife_Set_value4:
               pdf.cell(38,6,f"{inspect.knife_Set_value4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_master4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_before4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_after4}",border=True,align="C")
               pdf.cell(38,6,f"{inspect.knife_dev4}",border=True,ln=True,align="C")
     
     
          
          
          pdf.ln(3)          
     
     pdf.multi_cell(190,5,txt="Conclusion: " +" "+ inspect.conc,border=1,ln=True)
     pdf.cell(190,6,txt="Inspection Status :"+ " "+ inspect.insp_status,border=1,ln=True)
     
     # number_of_rows = 98  # Replace with the actual number of rows
     # row_height = 2  # Replace with the actual row height in your table
     # table_height = (number_of_rows) * row_height      
     # if pdf.y + number_of_rows * row_height >= pdf.h:
     #      pdf.add_page() 
      
     pdf.ln(2)
     pdf.set_font("Calibri","", 10)
     pdf.multi_cell(190,4,txt=inspect.text,ln=True)
     


     
     
     
     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={inspect.cert_num}.pdf'
     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
     response['Pragma'] = 'no-cache'
     response['Expires'] = '0'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

__all__ = [
    'inspection',
    'inspection_list',
    'inspect_edit',
    'inspect_update',
    'inspect_delete',
    'inspect_clone',
    'inspect_clone_update',
    'inspect_view',
    'inspect_pdf',
    'inspect_pdf1',
]
