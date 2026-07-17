# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403




@login_required(login_url="/login")   
def sample_reg(request):
     if request.method == 'POST':
          location = request.POST['location']
          city_location = request.POST['city_location']
          lab_no = request.POST['lab_no']
          issue_date = request.POST['issue_date']
          issue_no = request.POST['issue_no']
          sample_id = request.POST['sample_id']
          checkinp_chemical = request.POST.get('checkinp_chemical') == 'on'
          checkinp_bacteria = request.POST.get('checkinp_bacteria') == 'on'
          inp1 = request.POST['inp1']
          inp2 = request.POST['inp2']
          inp3 = request.POST['inp3']
          inp4 = request.POST['inp4']
          inp5 = request.POST['inp5']
          inp6 = request.POST['inp6']
          inp7 = request.POST['inp7']
          inp8 = request.POST['inp8']
          inp9 = request.POST['inp9']
          inp10 = request.POST['inp10']
          checkinp11 = request.POST.get('checkinp11') == 'on'
          checkinp12 = request.POST.get('checkinp12') == 'on'
          checkinp13 = request.POST.get('checkinp13') == 'on'
          checkinp14 = request.POST.get('checkinp14') == 'on'
          checkinp15 = request.POST.get('checkinp15') == 'on'
          checkinp16 = request.POST.get('checkinp16') == 'on'
          checkinp17 = request.POST.get('checkinp17') == 'on'
          checkinp18 = request.POST.get('checkinp18') == 'on'
          inp19 = request.POST['inp19']
          inp20 = request.POST['inp20']
          checkinp21 = request.POST.get('checkinp21') == 'on'
          checkinp22 = request.POST.get('checkinp22') == 'on'
          checkinp23 = request.POST.get('checkinp23') == 'on'
          checkinp24 = request.POST.get('checkinp24') == 'on'
          checkinp25 = request.POST.get('checkinp25') == 'on'
          checkinp26 = request.POST.get('checkinp26') == 'on'
          checkinp27 = request.POST.get('checkinp27') == 'on'
          checkinp28 = request.POST.get('checkinp28') == 'on'
          checkinp29 = request.POST.get('checkinp29') == 'on'
          checkinp30 = request.POST.get('checkinp30') == 'on'
          checkinp31 = request.POST.get('checkinp31') == 'on'
          checkinp32 = request.POST.get('checkinp32') == 'on'
          checkinp33 = request.POST.get('checkinp33') == 'on'
          checkinp34 = request.POST.get('checkinp34') == 'on'
          checkinp35 = request.POST.get('checkinp35') == 'on'
          checkinp36 = request.POST.get('checkinp36') == 'on'
          checkinp37 = request.POST.get('checkinp37') == 'on'
          checkinp38 = request.POST.get('checkinp38') == 'on'
          checkinp39 = request.POST.get('checkinp39') == 'on'
          checkinp40 = request.POST.get('checkinp40') == 'on'
          checkinp41 = request.POST.get('checkinp41') == 'on'
          checkinp42 = request.POST.get('checkinp42') == 'on'
          checkinp43 = request.POST.get('checkinp43') == 'on'
          checkinp44 = request.POST.get('checkinp44') == 'on'
          checkinp45 = request.POST.get('checkinp45') == 'on'
          checkinp46 = request.POST.get('checkinp46') == 'on'
          checkinp47 = request.POST.get('checkinp47') == 'on'
          checkinp48 = request.POST.get('checkinp48') == 'on'
          checkinp49 = request.POST.get('checkinp49') == 'on'
          checkinp50 = request.POST.get('checkinp50') == 'on'
          checkinp51 = request.POST.get('checkinp51') == 'on'
          checkinp52 = request.POST.get('checkinp52') == 'on'
          checkinp53 = request.POST.get('checkinp53') == 'on'
          checkinp54 = request.POST.get('checkinp54') == 'on'
          checkinp55 = request.POST.get('checkinp55') == 'on'
          checkinp56 = request.POST.get('checkinp56') == 'on'
          checkinp57 = request.POST.get('checkinp57') == 'on'
          checkinp58 = request.POST.get('checkinp58') == 'on'
          checkinp59 = request.POST.get('checkinp59') == 'on'
          checkinp60 = request.POST.get('checkinp60') == 'on'
          checkinp61 = request.POST.get('checkinp61') == 'on'
          checkinp62 = request.POST.get('checkinp62') == 'on'
          checkinp63 = request.POST.get('checkinp63') == 'on'
          checkinp64 = request.POST.get('checkinp64') == 'on'
          checkinp65 = request.POST.get('checkinp65') == 'on'
          checkinp66 = request.POST.get('checkinp66') == 'on'
          checkinp67 = request.POST.get('checkinp67') == 'on'
          checkinp68 = request.POST.get('checkinp68') == 'on'
          checkinp69 = request.POST.get('checkinp69') == 'on'
          checkinp70 = request.POST.get('checkinp70') == 'on'
          checkinp71 = request.POST.get('checkinp71') == 'on'
          checkinp72 = request.POST.get('checkinp72') == 'on'
          checkinp73 = request.POST.get('checkinp73') == 'on'
          checkinp74 = request.POST.get('checkinp74') == 'on'
          checkinp75 = request.POST.get('checkinp75') == 'on'
          checkinp76 = request.POST.get('checkinp76') == 'on'
          checkinp77 = request.POST.get('checkinp77') == 'on'
          checkinp78 = request.POST.get('checkinp78') == 'on'
          checkinp79 = request.POST.get('checkinp79') == 'on'
          checkinp80 = request.POST.get('checkinp80') == 'on'
          checkinp81 = request.POST.get('checkinp81') == 'on'
          checkinp82 = request.POST.get('checkinp82') == 'on'
          checkinp83 = request.POST.get('checkinp83') == 'on'
          checkinp84 = request.POST.get('checkinp84') == 'on'
          checkinp85 = request.POST.get('checkinp85') == 'on'
          checkinp86 = request.POST.get('checkinp86') == 'on'
          checkinp87 = request.POST.get('checkinp87') == 'on'
          checkinp88 = request.POST.get('checkinp88') == 'on'
          checkinp89 = request.POST.get('checkinp89') == 'on'
          checkinp90 = request.POST.get('checkinp90') == 'on'
          checkinp91 = request.POST.get('checkinp91') == 'on'
          checkinp92 = request.POST.get('checkinp92') == 'on'
          checkinp93 = request.POST.get('checkinp93') == 'on'
          checkinp94 = request.POST.get('checkinp94') == 'on'
          checkinp95 = request.POST.get('checkinp95') == 'on'
          checkinp96 = request.POST.get('checkinp96') == 'on'
          checkinp97 = request.POST.get('checkinp97') == 'on'
          checkinp98 = request.POST.get('checkinp98') == 'on'
          checkinp99 = request.POST.get('checkinp99') == 'on'
          checkinp100 = request.POST.get('checkinp100') == 'on'
          checkinp101 = request.POST.get('checkinp101') == 'on'
          checkinp102 = request.POST.get('checkinp102') == 'on'
          checkinp103 = request.POST.get('checkinp103') == 'on'
          checkinp104 = request.POST.get('checkinp104') == 'on'
          checkinp105 = request.POST.get('checkinp105') == 'on'
          inp106 = request.POST['inp106']
          checkinp107 = request.POST.get('checkinp107') == 'on'
          checkinp108 = request.POST.get('checkinp108') == 'on'
          inp109 = request.POST['inp109']
          checkinp110 = request.POST.get('checkinp110') == 'on'
          checkinp111 = request.POST.get('checkinp111') == 'on'
          inp112 = request.POST['inp112']
          checkinp113 = request.POST.get('checkinp113') == 'on'
          checkinp114 = request.POST.get('checkinp114') == 'on'
          inp115 = request.POST['inp115']
          checkinp116 = request.POST.get('checkinp116') == 'on'
          checkinp117 = request.POST.get('checkinp117') == 'on'
          # auth_sign = request.FILES['auth_sign']
          # sampling_by = request.FILES['sampling_by']
          conntrol_1 = request.POST['conntrol_1']
          conntrol_date = request.POST['conntrol_date']
          conntrol_no = request.POST['conntrol_no']
          assign_to = request.POST['assign_to']
          other1 = request.POST.get('other1')
          other2 = request.POST.get('other2')
          sample_by_id = request.POST.get('sample_sign')
          auth_sign_id = request.POST.get('auth_sign')
          
          auth_signature = Signatures.objects.get(id=auth_sign_id)
          sampling_by_signature = Signatures.objects.get(id=sample_by_id)
          # approved_sign = Signatures.objects.get(id=approved_sign_id)
          
          other_params = {}
          ww_other_params = {}
          for i in range(1, 67):  # 1 to 66
               key = f"other_param_{i}"   # your checkbox input id/name
               field = f"other_param_{i}"  # model field
               other_params[field] = request.POST.get(key) == "on"
               
          for i in range(1, 64):  # 1 to 66
               key = f"ww_other_param_{i}"   # your checkbox input id/name
               field = f"ww_other_param_{i}"  # model field
               ww_other_params[field] = request.POST.get(key) == "on"
          print('other param------------->>>',other_params)
          print('ww other param------------->>>',ww_other_params)
          user = request.user
          

          sample = Sample_registration(lab_no=lab_no,issue_date=issue_date,issue_no=issue_no,sample_id=sample_id,checkinp_chemical=checkinp_chemical,checkinp_bacteria=checkinp_bacteria,inp1=inp1,inp2=inp2,inp3=inp3,inp4=inp4,inp5=inp5,inp6=inp6,inp7=inp7,inp8=inp8,inp9=inp9,
                                   inp10=inp10,checkinp11=checkinp11,checkinp12=checkinp12,checkinp13=checkinp13,checkinp14=checkinp14,checkinp15=checkinp15,checkinp16=checkinp16,checkinp17=checkinp17,checkinp18=checkinp18,inp19=inp19,inp20=inp20,checkinp21=checkinp21,checkinp22=checkinp22,
                                   checkinp23=checkinp23,checkinp24=checkinp24,checkinp25=checkinp25,checkinp26=checkinp26,checkinp27=checkinp27,checkinp28=checkinp28,checkinp29=checkinp29,checkinp30=checkinp30,checkinp31=checkinp31,checkinp32=checkinp32,checkinp33=checkinp33,checkinp34=checkinp34,
                                   checkinp35=checkinp35,checkinp36=checkinp36,checkinp37=checkinp37,checkinp38=checkinp38,checkinp39=checkinp39,checkinp40=checkinp40,checkinp41=checkinp41,checkinp42=checkinp42,checkinp43=checkinp43,checkinp44=checkinp44,checkinp45=checkinp45,checkinp46=checkinp46,
                                   checkinp47=checkinp47,checkinp48=checkinp48,checkinp49=checkinp49,checkinp50=checkinp50,checkinp51=checkinp51,checkinp52=checkinp52,checkinp53=checkinp53,checkinp54=checkinp54,checkinp55=checkinp55,checkinp56=checkinp56,checkinp57=checkinp57,checkinp58=checkinp58,
                                   checkinp59=checkinp59,checkinp60=checkinp60,checkinp61=checkinp61,checkinp62=checkinp62,checkinp63=checkinp63,checkinp64=checkinp64,checkinp65=checkinp65,checkinp66=checkinp66,checkinp67=checkinp67,checkinp68=checkinp68,checkinp69=checkinp69,checkinp70=checkinp70,checkinp71=checkinp71,
                                   checkinp72=checkinp72,checkinp73=checkinp73,checkinp74=checkinp74,checkinp75=checkinp75,checkinp76=checkinp76,checkinp77=checkinp77,checkinp78=checkinp78,checkinp79=checkinp79,checkinp80=checkinp80,checkinp81=checkinp81,checkinp82=checkinp82,checkinp83=checkinp83,
                                   checkinp84=checkinp84,checkinp85=checkinp85,checkinp86=checkinp86,checkinp87=checkinp87,checkinp88=checkinp88,checkinp89=checkinp89,checkinp90=checkinp90,checkinp91=checkinp91,checkinp92=checkinp92,checkinp93=checkinp93,checkinp94=checkinp94,checkinp95=checkinp95,checkinp96=checkinp96,checkinp97=checkinp97,checkinp98=checkinp98,
                                   checkinp99=checkinp99,checkinp100=checkinp100,checkinp101=checkinp101,checkinp102=checkinp102,checkinp103=checkinp103,checkinp104=checkinp104,checkinp105=checkinp105,inp106=inp106,checkinp107=checkinp107,checkinp108=checkinp108,inp109=inp109,checkinp110=checkinp110,checkinp111=checkinp111,
                                   inp112=inp112,checkinp113=checkinp113,checkinp114=checkinp114,inp115=inp115,checkinp116=checkinp116,checkinp117=checkinp117,city_location=city_location,location=location,assign_to=assign_to,conntrol_1=conntrol_1,conntrol_date=conntrol_date,conntrol_no=conntrol_no,other1=other1,other2=other2,
                                   auth_signature=auth_signature,sampling_by_signature=sampling_by_signature,created_by=user,**other_params,**ww_other_params)
          sample.save()
          
          action = f'Sample Registration form created by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Sample successfully added!')
          id = (Sample_registration.objects.last()).id
          if "submit_and_view" in request.POST:
               url = f"/sample_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return render(request, "sample_reg.html")                    
     return render(request,"sample_reg.html",context={'signs':signs})

def sample_main(request):
     return render(request,"sample_main.html")


def sample_list(request):
     sample, _srch = _sampling_filter(request, Sample_registration)
     context = {'searched':_srch, 'data':sample}
     return render(request,"sample_list.html",context)

def sample_view(request,pk):
     sample = Sample_registration.objects.get(id=pk)
     context = {'data':sample}
     return render(request,"sample_view.html",context)
def sample_delete(request,pk):
     sample = Sample_registration.objects.get(id=pk)
     user = request.user
     action = f'Sample Registration form {sample.sample_id} Deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     sample.delete()
     return redirect("sample_list")


def sample_edit(request,pk):
     sample = Sample_registration.objects.get(id=pk)
     context = {'data':sample,'signs':signs}
     return render(request,'sample_edit.html',context)

def sample_update(request,pk):
     sample = Sample_registration.objects.get(id=pk)
     if request.method == 'POST':
          sample.location = request.POST['location']
          sample.city_location = request.POST['city_location']
          sample.lab_no = request.POST['lab_no']
          sample.issue_date = request.POST['issue_date']
          sample.issue_no = request.POST['issue_no']
          sample.sample_id = request.POST['sample_id']
          
          checkbox_fields = [
                    'checkinp_chemical', 'checkinp_bacteria', 
                    'checkinp11', 'checkinp12', 'checkinp13', 'checkinp14', 'checkinp15', 'checkinp16', 'checkinp17', 
                    'checkinp18', 'checkinp21', 'checkinp22', 'checkinp23', 'checkinp24', 
                    'checkinp25', 'checkinp26', 'checkinp27', 'checkinp28', 'checkinp29', 'checkinp30', 'checkinp31', 
                    'checkinp32', 'checkinp33', 'checkinp34', 'checkinp35', 'checkinp36', 'checkinp37', 'checkinp38', 
                    'checkinp39', 'checkinp40', 'checkinp41', 'checkinp42', 'checkinp43', 'checkinp44', 'checkinp45', 
                    'checkinp46', 'checkinp47', 'checkinp48', 'checkinp49', 'checkinp50', 'checkinp51', 'checkinp52', 
                    'checkinp53', 'checkinp54', 'checkinp55', 'checkinp56', 'checkinp57', 'checkinp58', 'checkinp59', 
                    'checkinp60', 'checkinp61', 'checkinp62', 'checkinp63', 'checkinp64', 'checkinp65', 'checkinp66', 
                    'checkinp67', 'checkinp68', 'checkinp69', 'checkinp70', 'checkinp71', 'checkinp72', 'checkinp73', 
                    'checkinp74', 'checkinp75', 'checkinp76', 'checkinp77', 'checkinp78', 'checkinp79', 'checkinp80', 
                    'checkinp81', 'checkinp82', 'checkinp83', 'checkinp84', 'checkinp85', 'checkinp86', 'checkinp87', 
                    'checkinp88', 'checkinp89', 'checkinp90', 'checkinp91', 'checkinp92', 'checkinp93', 'checkinp94', 
                    'checkinp95', 'checkinp96', 'checkinp97', 'checkinp98', 'checkinp99', 'checkinp100', 'checkinp101', 
                    'checkinp102', 'checkinp103', 'checkinp104', 'checkinp105', 'checkinp107', 'checkinp108', 
                     'checkinp110', 'checkinp111',  'checkinp113', 'checkinp114',  
                    'checkinp116', 'checkinp117'
                    ]
          checkbox_fields.extend([f"other_param_{i}" for i in range(1, 67)])
          checkbox_fields.extend([f"ww_other_param_{i}" for i in range(1, 64)])
          sample.inp1 = request.POST['inp1']
          sample.inp2 = request.POST['inp2']
          sample.inp3 = request.POST['inp3']
          sample.inp4 = request.POST['inp4']
          sample.inp5 = request.POST['inp5']
          sample.inp6 = request.POST['inp6']
          sample.inp7 = request.POST['inp7']
          sample.inp8 = request.POST['inp8']
          sample.inp9 = request.POST['inp9']
          sample.inp10 = request.POST['inp10']
          
          sample.inp19 = request.POST['inp19']
          sample.inp20 = request.POST['inp20']
          
          sample.inp106 = request.POST['inp106']
          
          sample.inp109 = request.POST['inp109']
          
          sample.inp112 = request.POST['inp112']
          sample.other1 = request.POST.get('other1')
          sample.other2 = request.POST.get('other2')
          
          sample.inp115 = request.POST['inp115']
          sample.assign_to = request.POST['assign_to']
          # sample.sampling_by = request.FILES['sampling_by']
          sample.conntrol_1 = request.POST['conntrol_1']
          sample.conntrol_date = request.POST['conntrol_date']
          sample.conntrol_no = request.POST['conntrol_no']
          # sample.auth_sign = request.FILES['auth_sign']
          auth_sign_id =request.POST.get('auth_sign')
          sample_by_id =request.POST.get('sample_sign')
          
          auth_signature = Signatures.objects.get(id=auth_sign_id)
          sampling_by_signature = Signatures.objects.get(id=sample_by_id)
          
          sample.auth_signature = auth_signature
          sample.sampling_by_signature = sampling_by_signature

          for field in checkbox_fields:
               new_value = field in request.POST   
               #setattr(class_variable,attribute_name_to_set,attribute_value_to_set)         
               setattr(sample, field, new_value)
               
          
          
          user = request.user
          sample.created_by =user
          sample.save()
          action = f'Sample Registration form {sample.sample_id} edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = sample.id
          if "submit_and_view" in request.POST:
               url = f"/sample_view/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST:
               
               return redirect("sample_list")                    
     return render(request,"sample_list.html")


def sample_clone(request,pk):
     sample = Sample_registration.objects.get(id=pk)
     context = {'data':sample,'signs':signs}
     return render(request,'sample_clone.html',context)


def sample_clone_update(request,pk):
     try:
        # Fetch the existing form instance by ID
         sample = Sample_registration.objects.get(id=pk)
     except Sample_registration.DoesNotExist:
         return HttpResponse("Form not found", status=404)  
     if request.method == 'POST':
          sample.location = request.POST['location']
          sample.city_location = request.POST['city_location']
          sample.lab_no = request.POST['lab_no']
          sample.issue_date = request.POST['issue_date']
          sample.issue_no = request.POST['issue_no']
          sample.sample_id = request.POST['sample_id']
          
          checkbox_fields = [
                    'checkinp_chemical', 'checkinp_bacteria', 
                    'checkinp11', 'checkinp12', 'checkinp13', 'checkinp14', 'checkinp15', 'checkinp16', 'checkinp17', 
                    'checkinp18', 'checkinp21', 'checkinp22', 'checkinp23', 'checkinp24', 
                    'checkinp25', 'checkinp26', 'checkinp27', 'checkinp28', 'checkinp29', 'checkinp30', 'checkinp31', 
                    'checkinp32', 'checkinp33', 'checkinp34', 'checkinp35', 'checkinp36', 'checkinp37', 'checkinp38', 
                    'checkinp39', 'checkinp40', 'checkinp41', 'checkinp42', 'checkinp43', 'checkinp44', 'checkinp45', 
                    'checkinp46', 'checkinp47', 'checkinp48', 'checkinp49', 'checkinp50', 'checkinp51', 'checkinp52', 
                    'checkinp53', 'checkinp54', 'checkinp55', 'checkinp56', 'checkinp57', 'checkinp58', 'checkinp59', 
                    'checkinp60', 'checkinp61', 'checkinp62', 'checkinp63', 'checkinp64', 'checkinp65', 'checkinp66', 
                    'checkinp67', 'checkinp68', 'checkinp69', 'checkinp70', 'checkinp71', 'checkinp72', 'checkinp73', 
                    'checkinp74', 'checkinp75', 'checkinp76', 'checkinp77', 'checkinp78', 'checkinp79', 'checkinp80', 
                    'checkinp81', 'checkinp82', 'checkinp83', 'checkinp84', 'checkinp85', 'checkinp86', 'checkinp87', 
                    'checkinp88', 'checkinp89', 'checkinp90', 'checkinp91', 'checkinp92', 'checkinp93', 'checkinp94', 
                    'checkinp95', 'checkinp96', 'checkinp97', 'checkinp98', 'checkinp99', 'checkinp100', 'checkinp101', 
                    'checkinp102', 'checkinp103', 'checkinp104', 'checkinp105', 'checkinp107', 'checkinp108', 
                     'checkinp110', 'checkinp111',  'checkinp113', 'checkinp114',  
                    'checkinp116', 'checkinp117'
                    ]
          checkbox_fields.extend([f"other_param_{i}" for i in range(1, 67)])
          checkbox_fields.extend([f"ww_other_param_{i}" for i in range(1, 64)])
          sample.inp1 = request.POST['inp1']
          sample.inp2 = request.POST['inp2']
          sample.inp3 = request.POST['inp3']
          sample.inp4 = request.POST['inp4']
          sample.inp5 = request.POST['inp5']
          sample.inp6 = request.POST['inp6']
          sample.inp7 = request.POST['inp7']
          sample.inp8 = request.POST['inp8']
          sample.inp9 = request.POST['inp9']
          sample.inp10 = request.POST['inp10']
          
          sample.inp19 = request.POST['inp19']
          sample.inp20 = request.POST['inp20']
          
          sample.inp106 = request.POST['inp106']
          
          sample.inp109 = request.POST['inp109']
          
          sample.inp112 = request.POST['inp112']
          sample.other1 = request.POST['other1']
          sample.other2 = request.POST['other2']
          
          sample.inp115 = request.POST['inp115']
          sample.assign_to = request.POST['assign_to']
          # sample.sampling_by = request.FILES['sampling_by']
          sample.conntrol_1 = request.POST['conntrol_1']
          sample.conntrol_date = request.POST['conntrol_date']
          sample.conntrol_no = request.POST['conntrol_no']
          # sample.auth_sign = request.FILES['auth_sign']
          auth_sign_id =request.POST.get('auth_sign')
          sample_by_id =request.POST.get('sample_sign')
          
          auth_signature = Signatures.objects.get(id=auth_sign_id)
          sampling_by_signature = Signatures.objects.get(id=sample_by_id)
          
          sample.auth_signature = auth_signature
          sample.sampling_by_signature = sampling_by_signature

          for field in checkbox_fields:
               new_value = field in request.POST            
               setattr(sample, field, new_value)
               
          
          
          user = request.user
          sample.created_by=user
          sample.id = None
          sample.save()
          action = f'Sample Registration form {sample.sample_id} cloned by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          id = sample.id
          if "submit_and_view" in request.POST:
              url = f"/sample_view/{str(id)}/"
              return redirect(to=url)
     
          if "submit_and_new" in request.POST:
             # context = {'list': new_dw}
              return redirect(to='sample_list')
          else:
               return HttpResponse("Invalid request method", status=400)
     # context = {'list': existing_dw}
     return render(request, "sample_clone.html")



def samplePdf(request,pk):
     from fpdf import FPDF
     
     from EnviTechAlApp.pdf_common import PDF_samplePdf as PDFWithPageNumbers
               
               # # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
               # self.set_fill_color(40, 25, 105)    
               # self.rect(0,self.h-14,self.w,12,"F")
               # self.image("static/assets/Picture1.png",5,self.h-16,14,14)
               # self.set_text_color(255, 255, 255)
               # # self.set_font("Calibri","", 9)
               # self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
               # self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
               # self.set_fill_color(255, 255, 255)   
               # self.image("static/assets/earth.png",165,self.h-12,7,7)
               # self.text(175,self.h-7,txt="info@envitechal.com")
               # self.text(175,self.h-10,txt="www.envitechal.com")


     sample = Sample_registration.objects.get(id=pk)

     pdf = PDFWithPageNumbers()
     pdf._rq_sample = sample
     pdf.add_page()
     
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=15)

     pdf.set_font("Calibri","B", 11)
     pdf.set_fill_color(217, 226, 243)
     pdf.set_draw_color(25, 27, 2)
     pdf.rect(10,39,190,8,'DF')
     pdf.text(12,44,txt="Sample Information:")
     pdf.text(130,44,txt="Sample ID:")
     pdf.line(150,44.5,185,44.5)
     pdf.set_font("Calibri","", 11)
     pdf.text(150,44,txt=sample.sample_id)


     pdf.rect(10,47,190,16)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,52,txt="Analysis Requested:")
     

     checked = '/home/django/EnviTechAlApp/static/assets/checked-removebg-preview.png'
     unchecked = '/home/django/EnviTechAlApp/static/assets/unchecked-removebg-preview.png'
     
     pdf.set_font("Calibri","B", 11)
     pdf.text(20,58,txt="Chemical Analysis")
     if sample.checkinp_chemical:

          pdf.image(checked,12.5,55,4,4)
     else:
          pdf.image(unchecked,12.5,55,4,4)


     pdf.text(70,58,txt="Bacterial Analysis")
     if sample.checkinp_bacteria:

          pdf.image(checked,62.5,55,4,4)
     else:
          pdf.image(unchecked,62.5,55,4,4)

     pdf.text(110,58,txt="Others (Please Specify)") 
     pdf.line(150,58.5,195,58.5)
     if sample.inp1:
          pdf.set_font("Calibri","", 11)
          pdf.text(153,58,txt=sample.inp1)

     pdf.rect(10,63,190,53)
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,69,txt="Sampling By :")
     pdf.set_font("Calibri","", 11)
     pdf.line(36,69.5,90,69.5)
     pdf.text(39,69,txt=sample.inp2)

     pdf.set_font("Calibri","B", 11)
     pdf.text(110,69,txt="Registration Date & Time:")
     pdf.set_font("Calibri","", 11)
     pdf.line(153,69.5,195,69.5)
     pdf.text(156,69,txt=sample.inp3)

     
     pdf.set_font("Calibri","B", 11)
     pdf.text(12,76,txt="Location Of Sample:")
     pdf.set_font("Calibri","", 11)
     pdf.line(47,76.5,90,76.5)
     pdf.text(50,76,txt=sample.inp4)

     pdf.set_font("Calibri","B", 11)
     pdf.text(110,76,txt="Sample Method:")
     pdf.set_font("Calibri","", 11)
     pdf.line(138,76.5,195,76.5)
     pdf.text(141,76,txt=sample.inp5)


     pdf.set_font("Calibri","B", 11)
     pdf.text(12,83,txt="Sample Collected By:")
     pdf.set_font("Calibri","", 11)
     pdf.line(47,83.5,90,83.5)
     pdf.text(50,83,txt=sample.inp6)

     pdf.set_font("Calibri","B", 11)
     pdf.text(110,83,txt="Sampling/Receiving Date:")
     pdf.set_font("Calibri","", 11)
     pdf.line(152,83.5,195,83.5)
     pdf.text(155,83,txt=sample.inp7)

     pdf.set_font("Calibri","B", 11)
     pdf.text(12,90,txt="Sampling/Receiving Time:")
     pdf.set_font("Calibri","", 11)
     pdf.line(55,90.5,90,90.5)
     pdf.text(58,90,txt=sample.inp8)

     pdf.set_font("Calibri","B", 11)
     pdf.text(110,90,txt="Estimated Reporting Date:")
     pdf.set_font("Calibri","", 11)
     pdf.line(155,90.5,195,90.5)
     pdf.text(158,90,txt=sample.inp9)

     pdf.set_font("Calibri","B", 11)
     pdf.text(12,97,txt="No. of Samples:")
     pdf.set_font("Calibri","", 11)
     pdf.line(38,97.5,90,97.5)
     pdf.text(41,97,txt=sample.inp10)

     pdf.set_font("Calibri","B", 11)
     pdf.text(92,97,txt="Types of Sample:")
     pdf.text(127,97,txt="Drinking Water")
     if sample.checkinp11:
          pdf.image(checked,121,93.8,4,4)
     else:
          pdf.image(unchecked,121,93.8,4,4)

     pdf.text(158,97,txt="Sludge")
     if sample.checkinp12:
          pdf.image(checked,153,93.8,4,4)
     else:
          pdf.image(unchecked,153,93.8,4,4)


     pdf.text(182,97,txt="Influent")
     if sample.checkinp13:
          pdf.image(checked,177,93.8,4,4)
     else:
          pdf.image(unchecked,177,93.8,4,4)         

     pdf.text(127,104,txt="Effluent")
     if sample.checkinp16:
          pdf.image(checked,121,100.8,4,4)
     else:
          pdf.image(unchecked,121,100.8,4,4)

     pdf.text(158,104,txt="Bore Water")
     if sample.checkinp17:
          pdf.image(checked,153,100.8,4,4)
     else:
          pdf.image(unchecked,153,100.8,4,4)

     pdf.text(182,104,txt="R.O Water")
     if sample.checkinp18:
          pdf.image(checked,177,100.8,4,4)
     else:
          pdf.image(unchecked,177,100.8,4,4)         



     pdf.text(12,104,txt="Sampling Methodology:")
     pdf.text(58,104,txt="Grab")
     if sample.checkinp14:
          pdf.image(checked,53,100.8,4,4)
     else:
          pdf.image(unchecked,53,100.8,4,4)

     
     pdf.text(75,104,txt="Composite")
     if sample.checkinp15:
          pdf.image(checked,70,100.8,4,4)
     else:
          pdf.image(unchecked,70,100.8,4,4) 

     pdf.text(12,111,txt="Environmental Conditions (When Sample Received): Temp:")
     pdf.text(111,111,txt=sample.inp19)
     pdf.line(107,111.5,130,111.5)
     pdf.text(132,111,txt="pH")    
     pdf.text(140,111,txt=sample.inp20)  
     pdf.line(137,111.5,159,111.5)   


     pdf.set_fill_color(217, 226, 243)
     pdf.set_draw_color(25, 27, 2)
     pdf.rect(10,116,190,8,"DF")
     
     pdf.text(12,121,txt="Analysis Request For Wastewater:")

     pdf.rect(10,124,190,107)
     if sample.checkinp21:
          pdf.image(checked,12,125.8,4,4)
     else:
          pdf.image(unchecked,12,125.8,4,4)
     
     if sample.city_location == 'Lahore':
          pdf.text(18,129,txt="pH")   
     else:
          pdf.text(18,129,txt="pH*")   
          
     if sample.checkinp22:
          pdf.image(checked,26,125.8,4,4)
     else:
          pdf.image(unchecked,26,125.8,4,4)
     if sample.city_location == 'Lahore':     
          pdf.text(32,129,txt="Fluoride") 
     else:
          pdf.text(32,129,txt="Fluoride*") 
          

     if sample.checkinp23:
          pdf.image(checked,48,125.8,4,4)
     else:
          pdf.image(unchecked,48,125.8,4,4)
     pdf.text(54,129,txt="Chromium") 

     if sample.checkinp24:
          pdf.image(checked,74,125.8,4,4)
     else:
          pdf.image(unchecked,74,125.8,4,4)
     pdf.text(80,129,txt="BOD") 

     if sample.checkinp25:
          pdf.image(checked,90,125.8,4,4)
     else:
          pdf.image(unchecked,90,125.8,4,4)
     pdf.text(96,129,txt="Cyanide")

     if sample.checkinp26:
          pdf.image(checked,112,125.8,4,4)
     else:
          pdf.image(unchecked,112,125.8,4,4)
     pdf.text(118,129,txt="Copper")


     if sample.checkinp27:
          pdf.image(checked,134,125.8,4,4)
     else:
          pdf.image(unchecked,134,125.8,4,4)
     
     
     if sample.city_location == 'Lahore':
          pdf.text(140,129,txt="COD")
     else:
          pdf.text(140,129,txt="COD*")
          

     if sample.checkinp28:
          pdf.image(checked,150,125.8,4,4)
     else:
          pdf.image(unchecked,150,125.8,4,4)
     pdf.text(156,129,txt="An-ionic detergent")

     if sample.checkinp29:
          pdf.image(checked,188,125.8,4,4)
     else:
          pdf.image(unchecked,188,125.8,4,4)
     
     pdf.text(192.5,129,txt="TSS")
     
     
     if sample.checkinp30:
          pdf.image(checked,12,132.8,4,4)
     else:
          pdf.image(unchecked,12,132.8,4,4)
     pdf.text(18,136,txt="Lead")   

     if sample.checkinp31:
          pdf.image(checked,26,132.8,4,4)
     else:
          pdf.image(unchecked,26,132.8,4,4)
     
     if sample.city_location == 'Lahore':
          pdf.text(32,136,txt="TDS") 
     else:
          pdf.text(32,136,txt="TDS*") 
          

     if sample.checkinp32:
          pdf.image(checked,41.5,132.8,4,4)
     else:
          pdf.image(unchecked,41.5,132.8,4,4)
     pdf.text(46,136,txt="Sulphide") 

     if sample.checkinp33:
          pdf.image(checked,62,132.8,4,4)
     else:
          pdf.image(unchecked,62,132.8,4,4)
     pdf.text(68,136,txt="Mercury") 

     if sample.checkinp34:
          pdf.image(checked,86,132.8,4,4)
     else:
          pdf.image(unchecked,86,132.8,4,4)
     pdf.text(92,136,txt="Oil & Grease")

     if sample.checkinp35:
          pdf.image(checked,116,132.8,4,4)
     else:
          pdf.image(unchecked,116,132.8,4,4)
     pdf.text(122,136,txt="Ammonia")


     if sample.checkinp36:
          pdf.image(checked,142,132.8,4,4)
     else:
          pdf.image(unchecked,142,132.8,4,4)
     pdf.text(148,136,txt="Phenol")


     if sample.checkinp37:
          pdf.image(checked,162,132.8,4,4)
     else:
          pdf.image(unchecked,162,132.8,4,4)
     pdf.text(168,136,txt="Pesticides")

     if sample.checkinp38:
          pdf.image(checked,187,132.8,4,4)
     else:
          pdf.image(unchecked,187,132.8,4,4)
     
     if sample.city_location == 'Lahore':          
          pdf.text(191.8,136,txt="Iron")
     else:
          pdf.text(191.8,136,txt="Iron*")
          
     if sample.checkinp39:
          pdf.image(checked,12,139.8,4,4)
     else:
          pdf.image(unchecked,12,139.8,4,4)
     pdf.text(18,143,txt="Boron")   

     if sample.checkinp40:
          pdf.image(checked,30,139.8,4,4)
     else:
          pdf.image(unchecked,30,139.8,4,4)
     
     if sample.city_location == 'Lahore':
          pdf.text(36,143,txt="Nickel") 
     else:
          pdf.text(36,143,txt="Nickel*") 
          
          
     if sample.checkinp41:
          pdf.image(checked,50,139.8,4,4)
     else:
          pdf.image(unchecked,50,139.8,4,4)
     pdf.text(56,143,txt="Silver") 

     if sample.checkinp42:
          pdf.image(checked,70,139.8,4,4)
     else:
          pdf.image(unchecked,70,139.8,4,4)
     pdf.text(76,143,txt="Zinc") 

     if sample.checkinp43:
          pdf.image(checked,86,139.8,4,4)
     else:
          pdf.image(unchecked,86,139.8,4,4)
     pdf.text(92,143,txt="Arsenic")

     if sample.checkinp44:
          pdf.image(checked,106,139.8,4,4)
     else:
          pdf.image(unchecked,106,139.8,4,4)
     pdf.text(112,143,txt="Barium")
     
     


     if sample.checkinp45:
          pdf.image(checked,126,139.8,4,4)
     else:
          pdf.image(unchecked,126,139.8,4,4)
     pdf.text(132,143,txt="Manganese")


     if sample.checkinp46:
          pdf.image(checked,154,139.8,4,4)
     else:
          pdf.image(unchecked,154,139.8,4,4)
     pdf.text(160,143,txt="Toxic Metal")

     if sample.checkinp47:
          pdf.image(checked,188,139.8,4,4)
     else:
          pdf.image(unchecked,188,139.8,4,4)
     pdf.text(193,143,txt="TOC")
     
     if sample.checkinp48:
          pdf.image(checked,12,146.8,4,4)
     else:
          pdf.image(unchecked,12,146.8,4,4)
     
     
     pdf.text(18,150,txt="Chlorine")             

     if sample.checkinp49:
          pdf.image(checked,34,146.8,4,4)
     else:
          pdf.image(unchecked,34,146.8,4,4)
     
     
     if sample.city_location == 'Lahore':
          pdf.text(40,150,txt="Sulphate") 
     else:
          pdf.text(40,150,txt="Sulphate*") 
          
          
     if sample.checkinp50:
          pdf.image(checked,58,146.8,4,4)
     else:
          pdf.image(unchecked,58,146.8,4,4)
     pdf.text(64,150,txt="Cadmium") 

     if sample.checkinp51:
          pdf.image(checked,86,146.8,4,4)
     else:
          pdf.image(unchecked,86,146.8,4,4)
     
     if sample.city_location == 'Lahore':
          pdf.text(92,150,txt="Chloride") 
     else:
          pdf.text(92,150,txt="Chloride*") 
          
          
          
     if sample.checkinp52:
          pdf.image(checked,112,146.8,4,4)
     else:
          pdf.image(unchecked,112,146.8,4,4)
     pdf.text(118,150,txt="Selenium")

     if sample.checkinp53:
          pdf.image(checked,138,146.8,4,4)
     else:
          pdf.image(unchecked,138,146.8,4,4)
     pdf.text(144,150,txt="DO")
     

     if sample.checkinp54:
          pdf.image(checked,154,146.8,4,4)
     else:
          pdf.image(unchecked,154,146.8,4,4)
     pdf.text(160,150,txt="MLSS")


     if sample.checkinp55:
          pdf.image(checked,174,146.8,4,4)
     else:
          pdf.image(unchecked,174,146.8,4,4)
     pdf.text(180,150,txt="MLVSS")


     if sample.checkinp56:
          pdf.image(checked,12,153.8,4,4)
     else:
          pdf.image(unchecked,12,153.8,4,4)
     pdf.text(18,157,txt="Total N")   

     if sample.checkinp57:
          pdf.image(checked,34,153.8,4,4)
     else:
          pdf.image(unchecked,34,153.8,4,4)
     pdf.text(40,157,txt="Phosphorus") 

     if sample.checkinp58:
          pdf.image(checked,60,153.8,4,4)
     else:
          pdf.image(unchecked,60,153.8,4,4)
     pdf.text(66,157,txt="Coliform") 

    
     
     if sample.ww_other_param_1:
          pdf.image(checked, 82, 153.8, 4, 4)
     else:
          pdf.image(unchecked, 82, 153.8, 4, 4)
     pdf.text(88, 157, txt="Temperature")

     if sample.ww_other_param_2:
          pdf.image(checked, 110, 153.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 153.8, 4, 4)
     pdf.text(116, 157, txt="Colour")

     if sample.ww_other_param_3:
          pdf.image(checked, 128, 153.8, 4, 4)
     else:
          pdf.image(unchecked, 128, 153.8, 4, 4)
     pdf.text(134, 157, txt="Odour")

     if sample.ww_other_param_4:
          pdf.image(checked, 148, 153.8, 4, 4)
     else:
          pdf.image(unchecked, 148, 153.8, 4, 4)
     pdf.text(154, 157, txt="Turbidity")

     if sample.ww_other_param_5:
          pdf.image(checked, 176, 153.8, 4, 4)
     else:
          pdf.image(unchecked, 176, 153.8, 4, 4)
     pdf.text(182, 157, txt="Calcium")

     if sample.ww_other_param_6:
          pdf.image(checked, 12, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 160.8, 4, 4)
     pdf.text(18, 164, txt="Sodium")

     if sample.ww_other_param_7:
          pdf.image(checked, 36, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 160.8, 4, 4)
     pdf.text(42, 164, txt="Magnesium")

     # Row 9
     if sample.ww_other_param_8:
          pdf.image(checked, 66, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 66, 160.8, 4, 4)
     pdf.text(72, 164, txt="Potassium")

     if sample.ww_other_param_9:
          pdf.image(checked, 92, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 92, 160.8, 4, 4)
     pdf.text(98, 164, txt="Silica")

     if sample.ww_other_param_10:
          pdf.image(checked, 112, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 112, 160.8, 4, 4)
     pdf.text(118, 164, txt="Reactive Silica")

     if sample.ww_other_param_11:
          pdf.image(checked, 144, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 144, 160.8, 4, 4)
     pdf.text(150, 164, txt="Alkalinity")

     if sample.ww_other_param_12:
          pdf.image(checked, 170, 160.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 160.8, 4, 4)
     pdf.text(176, 164, txt="Ammonium")

     if sample.ww_other_param_13:
          pdf.image(checked, 12, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 167.8, 4, 4)
     pdf.text(18, 171, txt="Carbonates")

     # Row 10
     if sample.ww_other_param_14:
          pdf.image(checked, 38, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 38, 167.8, 4, 4)
     pdf.text(44, 171, txt="Bicarbonates")

     if sample.ww_other_param_15:
          pdf.image(checked, 66, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 66, 167.8, 4, 4)
     pdf.text(72, 171, txt="Conductivity")

     if sample.ww_other_param_16:
          pdf.image(checked, 94, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 94, 167.8, 4, 4)
     pdf.text(100, 171, txt="Salinity")

     if sample.ww_other_param_17:
          pdf.image(checked, 118, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 118, 167.8, 4, 4)
     pdf.text(124, 171, txt="Resistivity")

     if sample.ww_other_param_18:
          pdf.image(checked, 142, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 142, 167.8, 4, 4)
     pdf.text(148, 171, txt="Total Solid")

     # Row 11
     if sample.ww_other_param_19:
          pdf.image(checked, 168, 167.8, 4, 4)
     else:
          pdf.image(unchecked, 168, 167.8, 4, 4)
     pdf.text(174, 171, txt="Acidity")

     if sample.ww_other_param_20:
          pdf.image(checked, 12, 174.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 174.8, 4, 4)
     pdf.text(18, 178, txt="Total Hardness")

     if sample.ww_other_param_21:
          pdf.image(checked, 44, 174.8, 4, 4)
     else:
          pdf.image(unchecked, 44, 174.8, 4, 4)
     pdf.text(50, 178, txt="Calcium Hardness")

     if sample.ww_other_param_22:
          pdf.image(checked, 82, 174.8, 4, 4)
     else:
          pdf.image(unchecked, 82, 174.8, 4, 4)
     pdf.text(88, 178, txt="Magnesium Hardness")

     if sample.ww_other_param_23:
          pdf.image(checked, 126, 174.8, 4, 4)
     else:
          pdf.image(unchecked, 126, 174.8, 4, 4)
     pdf.text(132, 178, txt="Carbonate Hardness")
     
     
     if sample.ww_other_param_27:
          pdf.image(checked, 170, 174.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 174.8, 4, 4)
     pdf.text(176, 178, txt="Cobalt")

     # Row 12
     if sample.ww_other_param_24:
          pdf.image(checked, 12, 181.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 181.8, 4, 4)
     pdf.text(18, 185, txt="Non-Carbonate Hardness")

     if sample.ww_other_param_25:
          pdf.image(checked, 60, 181.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 181.8, 4, 4)
     pdf.text(66, 185, txt="Temporary Hardness")

     if sample.ww_other_param_26:
          pdf.image(checked, 102, 181.8, 4, 4)
     else:
          pdf.image(unchecked, 102, 181.8, 4, 4)
     pdf.text(108, 185, txt="Strontium")

     # Row 13 - Continuing with remaining parameters
     if sample.ww_other_param_28:
          pdf.image(checked, 128, 181.8, 4, 4)
     else:
          pdf.image(unchecked, 128, 181.8, 4, 4)
     pdf.text(134, 185, txt="Aluminium (Al)")

     if sample.ww_other_param_30:
          pdf.image(checked, 166, 181.8, 4, 4)
     else:
          pdf.image(unchecked, 166, 181.8, 4, 4)
     pdf.text(172, 185, txt="Chromium III")

     if sample.ww_other_param_31:
          pdf.image(checked, 12, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 188.8, 4, 4)
     pdf.text(18, 192, txt="Chromium VI")

     if sample.ww_other_param_32:
          pdf.image(checked, 42, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 42, 188.8, 4, 4)
     pdf.text(48, 192, txt="Ferrous (Fe+2)")

     if sample.ww_other_param_33:
          pdf.image(checked, 74, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 74, 188.8, 4, 4)
     pdf.text(80, 192, txt="Ferric (Fe+3)")

     # Row 14
     if sample.ww_other_param_34:
          pdf.image(checked, 102, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 102, 188.8, 4, 4)
     pdf.text(108, 192, txt="Tin (Sn)")

     if sample.ww_other_param_35:
          pdf.image(checked, 122, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 122, 188.8, 4, 4)
     pdf.text(128, 192, txt="Beryllium")

     if sample.ww_other_param_36:
          pdf.image(checked, 146, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 188.8, 4, 4)
     pdf.text(152, 192, txt="Free CO₂")

     if sample.ww_other_param_37:
          pdf.image(checked, 170, 188.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 188.8, 4, 4)
     pdf.text(176, 192, txt="Hydroxide Alk")

     if sample.ww_other_param_38:
          pdf.image(checked, 12, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 195.8, 4, 4)
     pdf.text(18, 199, txt="Methyl Orange Alk")

     if sample.ww_other_param_39:
          pdf.image(checked, 50, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 50, 195.8, 4, 4)
     pdf.text(56, 199, txt="Phenolphthalein Alk")

     # Row 15
     if sample.ww_other_param_40:
          pdf.image(checked, 90, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 90, 195.8, 4, 4)
     pdf.text(96, 199, txt="Particulate Matter")

     if sample.ww_other_param_41:
          pdf.image(checked, 128, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 128, 195.8, 4, 4)
     pdf.text(134, 199, txt="SDI")

     if sample.ww_other_param_42:
          pdf.image(checked, 142, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 142, 195.8, 4, 4)
     pdf.text(148, 199, txt="Particles Size")

     if sample.ww_other_param_43:
          pdf.image(checked, 170, 195.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 195.8, 4, 4)
     pdf.text(176, 199, txt="AOx")

     if sample.ww_other_param_44:
          pdf.image(checked, 12, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 202.8, 4, 4)
     pdf.text(18, 206, txt="Free Chlorine")

     if sample.ww_other_param_45:
          pdf.image(checked, 40, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 40, 202.8, 4, 4)
     pdf.text(46, 206, txt="Residual Chlorine")

     # Row 16
     if sample.ww_other_param_46:
          pdf.image(checked, 76, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 76, 202.8, 4, 4)
     pdf.text(82, 206, txt="Persistent Foam")

     if sample.ww_other_param_47:
          pdf.image(checked, 110, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 202.8, 4, 4)
     pdf.text(116, 206, txt="Flow rate")

     if sample.ww_other_param_48:
          pdf.image(checked, 132, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 132, 202.8, 4, 4)
     pdf.text(138, 206, txt="Phosphate")

     if sample.ww_other_param_49:
          pdf.image(checked, 156, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 156, 202.8, 4, 4)
     pdf.text(162, 206, txt="Nitrate")

     if sample.ww_other_param_50:
          pdf.image(checked, 178, 202.8, 4, 4)
     else:
          pdf.image(unchecked, 178, 202.8, 4, 4)
     pdf.text(184, 206, txt="Nitrite")

     if sample.ww_other_param_51:
          pdf.image(checked, 12, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 209.8, 4, 4)
     pdf.text(18, 213, txt="VSS")

     # Row 17
     if sample.ww_other_param_52:
          pdf.image(checked, 30, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 30, 209.8, 4, 4)
     pdf.text(36, 213, txt="Settleable solids")

     if sample.ww_other_param_53:
          pdf.image(checked, 64, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 64, 209.8, 4, 4)
     pdf.text(70, 213, txt="ORP")

     if sample.ww_other_param_54:
          pdf.image(checked, 84, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 209.8, 4, 4)
     pdf.text(90, 213, txt="VOX")

     if sample.ww_other_param_55:
          pdf.image(checked, 106, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 106, 209.8, 4, 4)
     pdf.text(112, 213, txt="SAR")

     if sample.ww_other_param_56:
          pdf.image(checked, 122, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 122, 209.8, 4, 4)
     pdf.text(128, 213, txt="RSC")

     if sample.ww_other_param_57:
          pdf.image(checked, 136, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 136, 209.8, 4, 4)
     pdf.text(142, 213, txt="Total Plate Count")

     # Row 18 - Final row
     if sample.ww_other_param_58:
          pdf.image(checked, 172, 209.8, 4, 4)
     else:
          pdf.image(unchecked, 172, 209.8, 4, 4)
     pdf.text(178, 213, txt="E. Coli")

     if sample.ww_other_param_59:
          pdf.image(checked, 12, 217.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 217.8, 4, 4)
     pdf.text(18, 221, txt="Faecal Coliform")

     if sample.ww_other_param_60:
          pdf.image(checked, 44, 217.8, 4, 4)
     else:
          pdf.image(unchecked, 44, 217.8, 4, 4)
     pdf.text(50, 221, txt="Faecal Enterococci")

     if sample.ww_other_param_61:
          pdf.image(checked, 82, 217.8, 4, 4)
     else:
          pdf.image(unchecked, 82, 217.8, 4, 4)
     pdf.text(88, 221, txt="Total Bacterial Count")

     if sample.ww_other_param_62:
          pdf.image(checked, 124, 217.8, 4, 4)
     else:
          pdf.image(unchecked, 124, 217.8, 4, 4)
     pdf.text(130, 221, txt="Legionella")

     # Row 19 - Last parameters
     if sample.ww_other_param_63:
          pdf.image(checked, 148, 217.8, 4, 4)
     else:
          pdf.image(unchecked, 148, 217.8, 4, 4)
     pdf.text(154, 221, txt="Pseudomonas aeruginosa")

     if sample.ww_other_param_64:
          pdf.image(checked, 12, 224.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 224.8, 4, 4)
     pdf.text(18, 228, txt="Bioassay Test")
     
     if sample.ww_other_param_29:
          pdf.image(checked, 42, 224.8, 4, 4)
     else:
          pdf.image(unchecked, 42, 224.8, 4, 4)
     pdf.text(48, 228, txt="Antimony")
     
     
     if sample.checkinp59:
          pdf.image(checked,72,224.8,4,4)
     else:
          pdf.image(unchecked,72,224.8,4,4)
     pdf.text(78,228,txt="Other") 
     pdf.set_font("Calibri","B", 9)
     if sample.other1:
          pdf.text(88,228,txt=sample.other1)
     
     
     
     
     
     
     
     
     
     
          
     


     pdf.set_font("Calibri","B", 11)


     pdf.add_page()
     pdf.set_y(35)

     pdf.set_fill_color(217, 226, 243)
     pdf.set_draw_color(25, 27, 2)
     pdf.rect(10, 35, 190, 8, 'DF')  # Changed Y from 161 to 35
     pdf.text(12, 40, txt="Analysis Request for Water (Drinking water, Bore water or R.O water etc.):")  # Changed Y from 166 to 40

     pdf.rect(10, 43, 190, 139)  # Changed Y from 169 to 43

     # First row of checkboxes (adjusted Y positions)
     if sample.checkinp60:
          pdf.image(checked, 12, 44.8, 4, 4)  # Changed Y from 170.8 to 44.8
     else:
          pdf.image(unchecked, 12, 44.8, 4, 4)
     pdf.text(18, 48, txt="Color")  # Changed Y from 174 to 48

     if sample.checkinp61:
          pdf.image(checked, 36, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 44.8, 4, 4)
     pdf.text(42, 48, txt="Taste")

     if sample.checkinp62:
          pdf.image(checked, 60, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 44.8, 4, 4)
     pdf.text(66, 48, txt="Odor")

     if sample.checkinp63:
          pdf.image(checked, 84, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 44.8, 4, 4)
     pdf.text(90, 48, txt="Turbidity")

     if sample.checkinp64:
          pdf.image(checked, 110, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 44.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(116, 48, txt="Total Hardness")
     else:
          pdf.text(116, 48, txt="Total Hardness*")

     if sample.checkinp65:
          pdf.image(checked, 146, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 44.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(152, 48, txt="TDS")
     else:
          pdf.text(152, 48, txt="TDS*")

     if sample.checkinp66:
          pdf.image(checked, 170, 44.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 44.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(176, 48, txt="Fluoride")
     else:
          pdf.text(176, 48, txt="Fluoride*")

     # Second row of checkboxes
     if sample.checkinp67:
          pdf.image(checked, 12, 51.8, 4, 4)  # Changed Y from 177.8 to 51.8
     else:
          pdf.image(unchecked, 12, 51.8, 4, 4)
     pdf.text(18, 55, txt="Chromium")  # Changed Y from 181 to 55

     if sample.checkinp68:
          pdf.image(checked, 36, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 51.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(42, 55, txt="Chloride")
     else:
          pdf.text(42, 55, txt="Chloride*")

     if sample.checkinp69:
          pdf.image(checked, 60, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 51.8, 4, 4)
     pdf.text(66, 55, txt="Cyanide")

     if sample.checkinp70:
          pdf.image(checked, 84, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 51.8, 4, 4)
     pdf.text(90, 55, txt="Copper")

     if sample.checkinp71:
          pdf.image(checked, 110, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 51.8, 4, 4)
     pdf.text(116, 55, txt="Antimony")

     if sample.checkinp72:
          pdf.image(checked, 146, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 51.8, 4, 4)
     pdf.text(152, 55, txt="Aluminum")

     if sample.checkinp73:
          pdf.image(checked, 170, 51.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 51.8, 4, 4)
     pdf.text(176, 55, txt="Arsenic")

     # Third row of checkboxes
     if sample.checkinp74:
          pdf.image(checked, 12, 58.8, 4, 4)  # Changed Y from 184.8 to 58.8
     else:
          pdf.image(unchecked, 12, 58.8, 4, 4)
     pdf.text(18, 62, txt="Boron")  # Changed Y from 188 to 62

     if sample.checkinp75:
          pdf.image(checked, 36, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 58.8, 4, 4)
     pdf.text(42, 62, txt="Lead")

     if sample.checkinp76:
          pdf.image(checked, 60, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 58.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(66, 62, txt="Nickel")
     else:
          pdf.text(66, 62, txt="Nickel*")

     if sample.checkinp77:
          pdf.image(checked, 84, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 58.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(90, 62, txt="Nitrate")
     else:
          pdf.text(90, 62, txt="Nitrate*")

     if sample.checkinp78:
          pdf.image(checked, 110, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 58.8, 4, 4)
     pdf.text(116, 62, txt="Mercury")

     if sample.checkinp79:
          pdf.image(checked, 146, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 58.8, 4, 4)
     pdf.text(152, 62, txt="Nitrite")

     if sample.checkinp80:
          pdf.image(checked, 170, 58.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 58.8, 4, 4)
     pdf.text(176, 62, txt="Selenium")

     # Fourth row of checkboxes
     if sample.checkinp81:
          pdf.image(checked, 12, 65.8, 4, 4)  # Changed Y from 191.8 to 65.8
     else:
          pdf.image(unchecked, 12, 65.8, 4, 4)
     pdf.text(18, 69, txt="Residual Chlorine")  # Changed Y from 195 to 69

     if sample.checkinp82:
          pdf.image(checked, 60, 65.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 65.8, 4, 4)
     pdf.text(66, 69, txt="Zinc")

     if sample.checkinp83:
          pdf.image(checked, 84, 65.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 65.8, 4, 4)
     pdf.text(90, 69, txt="DO")

     if sample.checkinp84:
          pdf.image(checked, 110, 65.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 65.8, 4, 4)
     pdf.text(116, 69, txt="Conductivity")

     if sample.checkinp85:
          pdf.image(checked, 146, 65.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 65.8, 4, 4)
     pdf.text(152, 69, txt="TKN")

     if sample.checkinp86:
          pdf.image(checked, 170, 65.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 65.8, 4, 4)
     pdf.text(176, 69, txt="Phenol")

     # Fifth row of checkboxes
     if sample.checkinp87:
          pdf.image(checked, 12, 72.8, 4, 4)  # Changed Y from 198.8 to 72.8
     else:
          pdf.image(unchecked, 12, 72.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(18, 76, txt="Sodium")  # Changed Y from 202 to 76
     else:
          pdf.text(18, 76, txt="Sodium*")

     if sample.checkinp88:
          pdf.image(checked, 36, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 72.8, 4, 4)
     pdf.text(42, 76, txt="Acidity")

     if sample.checkinp89:
          pdf.image(checked, 60, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 72.8, 4, 4)
     pdf.text(66, 76, txt="Potassium")

     if sample.checkinp90:
          pdf.image(checked, 84, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 72.8, 4, 4)
     pdf.text(90, 76, txt="Carbonates")

     if sample.checkinp91:
          pdf.image(checked, 110, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 72.8, 4, 4)
     pdf.text(116, 76, txt="Bicarbonates")

     if sample.checkinp92:
          pdf.image(checked, 146, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 72.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(152, 76, txt="Alkalinity")
     else:
          pdf.text(152, 76, txt="Alkalinity*")

     if sample.checkinp93:
          pdf.image(checked, 170, 72.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 72.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(176, 76, txt="Calcium")
     else:
          pdf.text(176, 76, txt="Calcium*")

     # Sixth row of checkboxes
     if sample.checkinp94:
          pdf.image(checked, 12, 79.8, 4, 4)  # Changed Y from 205.8 to 79.8
     else:
          pdf.image(unchecked, 12, 79.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(18, 83, txt="Magnesium")  # Changed Y from 209 to 83
     else:
          pdf.text(18, 83, txt="Magnesium*")

     if sample.checkinp95:
          pdf.image(checked, 60, 79.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 79.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(66, 83, txt="pH")
     else:
          pdf.text(66, 83, txt="pH*")

     if sample.checkinp96:
          pdf.image(checked, 84, 79.8, 4, 4)
     else:
          pdf.image(unchecked, 84, 79.8, 4, 4)

     if sample.city_location == 'Lahore':
          pdf.text(90, 83, txt="Sulphate")
     else:
          pdf.text(90, 83, txt="Sulphate*")

     if sample.checkinp97:
          pdf.image(checked, 110, 79.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 79.8, 4, 4)
     pdf.text(116, 83, txt="Silica")

     if sample.checkinp98:
          pdf.image(checked, 146, 79.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 79.8, 4, 4)
     pdf.text(152, 83, txt="Coliform")

     if sample.checkinp99:
          pdf.image(checked, 170, 79.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 79.8, 4, 4)
     pdf.text(176, 83, txt="E.Coli")

     # Seventh row of checkboxes
     if sample.checkinp100:
          pdf.image(checked, 12, 86.8, 4, 4)  # Changed Y from 212.8 to 86.8
     else:
          pdf.image(unchecked, 12, 86.8, 4, 4)
     pdf.text(18, 90, txt="Faecal Coliform")  # Changed Y from 216 to 90

     if sample.checkinp101:
          pdf.image(checked, 60, 86.8, 4, 4)
     else:
          pdf.image(unchecked, 60, 86.8, 4, 4)
     pdf.text(66, 90, txt="Pseudomonas aeruginosa")

     if sample.checkinp102:
          pdf.image(checked, 110, 86.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 86.8, 4, 4)
     pdf.text(116, 90, txt="Total Bacterial Count")

     if sample.checkinp103:
          pdf.image(checked, 12, 177.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 177.8, 4, 4)
     pdf.text(18, 181, txt="Others")

     pdf.set_font("Calibri", "B", 9)
     if sample.other2:
          pdf.text(28, 181, txt=sample.other2)

     pdf.set_font("Calibri", "B", 11)
     
     
     
     # start new rows after previous block (next checkbox Y = 93.8 -> text Y = 97)
# Row A (other_param_1 .. other_param_7)
     if sample.other_param_1:
          pdf.image(checked, 152, 86.8, 4, 4)
     else:
          pdf.image(unchecked, 152, 86.8, 4, 4)
     pdf.text(158, 90, txt="Barium")

     if sample.other_param_2:
          pdf.image(checked, 172, 86.8, 4, 4)
     else:
          pdf.image(unchecked, 172, 86.8, 4, 4)
     pdf.text(178, 90, txt="Manganese")

     if sample.other_param_3:
          pdf.image(checked, 12, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 93.8, 4, 4)
     pdf.text(18, 97, txt="Cadmium")

     if sample.other_param_4:
          pdf.image(checked, 36, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 93.8, 4, 4)
     pdf.text(42, 97, txt="Silver")

     if sample.other_param_5:
          pdf.image(checked, 56, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 56, 93.8, 4, 4)
     pdf.text(62, 97, txt="Reactive Silica")

     if sample.other_param_6:
          pdf.image(checked, 86, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 86, 93.8, 4, 4)
     pdf.text(92, 97, txt="Silicic Acid")

     if sample.other_param_7:
          pdf.image(checked, 110, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 110, 93.8, 4, 4)
     pdf.text(116, 97, txt="COD")

     # Row B (other_param_8 .. other_param_14)
     if sample.other_param_8:
          pdf.image(checked, 126, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 126, 93.8, 4, 4)
     pdf.text(132, 97, txt="BOD")

     if sample.other_param_9:
          pdf.image(checked, 144, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 144, 93.8, 4, 4)
     pdf.text(150, 97, txt="Cobalt")

     if sample.other_param_10:
          pdf.image(checked, 12, 100.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 100.8, 4, 4)
     pdf.text(18, 104, txt="Polyaromatic Hydrocarbons (PAH)")

     if sample.other_param_11:
          pdf.image(checked, 164, 93.8, 4, 4)
     else:
          pdf.image(unchecked, 164, 93.8, 4, 4)
     pdf.text(170, 97, txt="Pesticides")

     if sample.other_param_12:
          pdf.image(checked, 78, 100.8, 4, 4)
     else:
          pdf.image(unchecked, 78, 100.8, 4, 4)
     pdf.text(84, 104, txt="Oil & Grease")

     if sample.other_param_13:
          pdf.image(checked, 106, 100.8, 4, 4)
     else:
          pdf.image(unchecked, 106, 100.8, 4, 4)
     pdf.text(112, 104, txt="Alpha Emitters")

     if sample.other_param_14:
          pdf.image(checked, 138, 100.8, 4, 4)
     else:
          pdf.image(unchecked, 138, 100.8, 4, 4)
     pdf.text(144, 104, txt="Beta Emitters")

     # # Row C (other_param_15 .. other_param_21)
     if sample.other_param_15:
          pdf.image(checked, 168, 100.8, 4, 4)
     else:
          pdf.image(unchecked, 168, 100.8, 4, 4)
     pdf.text(174, 104, txt="Salinity")

     if sample.other_param_16:
          pdf.image(checked, 12, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 107.8, 4, 4)
     pdf.text(18, 111, txt="Resistivity")

     if sample.other_param_17:
          pdf.image(checked, 36, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 107.8, 4, 4)
     pdf.text(42, 111, txt="TOC")

     if sample.other_param_18:
          pdf.image(checked, 54, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 54, 107.8, 4, 4)
     pdf.text(60, 111, txt="VOC")

     if sample.other_param_19:
          pdf.image(checked, 72, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 72, 107.8, 4, 4)
     pdf.text(78, 111, txt="Phosphorus")

     if sample.other_param_20:
          pdf.image(checked, 98, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 98, 107.8, 4, 4)
     pdf.text(104, 111, txt="Calcium Hardness")

     if sample.other_param_21:
          pdf.image(checked, 135, 107.8, 4, 4)
     else:
          pdf.image(unchecked, 135, 107.8, 4, 4)
     pdf.text(141, 111, txt="Magnesium Hardness")

     # Row D (other_param_22 .. other_param_28)
     if sample.other_param_22:
          pdf.image(checked, 12, 114.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 114.8, 4, 4)
     pdf.text(18, 118, txt="Carbonate Hardness")

     if sample.other_param_23:
          pdf.image(checked, 54, 114.8, 4, 4)
     else:
          pdf.image(unchecked, 54, 114.8, 4, 4)
     pdf.text(60, 118, txt="Non-Carbonate Hardness")

     if sample.other_param_24:
          pdf.image(checked, 102, 114.8, 4, 4)
     else:
          pdf.image(unchecked, 102, 114.8, 4, 4)
     pdf.text(108, 118, txt="Temporary Hardness")

     if sample.other_param_25:
          pdf.image(checked, 144, 114.8, 4, 4)
     else:
          pdf.image(unchecked, 144, 114.8, 4, 4)
     pdf.text(150, 118, txt="Strontium")

     if sample.other_param_26:
          pdf.image(checked, 170, 114.8, 4, 4)
     else:
          pdf.image(unchecked, 170, 114.8, 4, 4)
     pdf.text(176, 118, txt="Chromium III")

     if sample.other_param_27:
          pdf.image(checked, 12, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 121.8, 4, 4)
     pdf.text(18, 125, txt="Chromium VI")

     if sample.other_param_28:
          pdf.image(checked, 42, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 42, 121.8, 4, 4)
     pdf.text(48, 125, txt="Iron")

     # # Row E (other_param_29 .. other_param_35)
     if sample.other_param_29:
          pdf.image(checked, 59, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 59, 121.8, 4, 4)
     pdf.text(65, 125, txt="Ferrous (Fe+2)")

     if sample.other_param_30:
          pdf.image(checked, 90, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 90, 121.8, 4, 4)
     pdf.text(96, 125, txt="Ferric (Fe+3)")

     if sample.other_param_31:
          pdf.image(checked, 120, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 120, 121.8, 4, 4)
     pdf.text(126, 125, txt="Ammonia")

     if sample.other_param_32:
          pdf.image(checked, 144, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 144, 121.8, 4, 4)
     pdf.text(150, 125, txt="Tin")

     if sample.other_param_33:
          pdf.image(checked, 162, 121.8, 4, 4)
     else:
          pdf.image(unchecked, 162, 121.8, 4, 4)
     pdf.text(168, 125, txt="Ammonium")

     if sample.other_param_34:
          pdf.image(checked, 12, 128.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 128.8, 4, 4)
     pdf.text(18, 132, txt="Free CO2")

     if sample.other_param_35:
          pdf.image(checked, 36, 128.8, 4, 4)
     else:
          pdf.image(unchecked, 36, 128.8, 4, 4)
     pdf.text(42, 132, txt="Hydroxide Alkalinity as CaCO₃")

     # Row F (other_param_36 .. other_param_42)
     if sample.other_param_36:
          pdf.image(checked, 94, 128.8, 4, 4)
     else:
          pdf.image(unchecked, 94, 128.8, 4, 4)
     pdf.text(100, 132, txt="Methyl Orange Alkalinity as CaCO₃")

     if sample.other_param_37:
          pdf.image(checked, 12, 135.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 135.8, 4, 4)
     pdf.text(18, 139, txt="Phenolphthalein Alkalinity as CaCO₃")

     if sample.other_param_38:
          pdf.image(checked, 160, 128.8, 4, 4)
     else:
          pdf.image(unchecked, 160, 128.8, 4, 4)
     pdf.text(166, 132, txt="Particulate Matter")

     if sample.other_param_39:
          pdf.image(checked, 80, 135.8, 4, 4)
     else:
          pdf.image(unchecked, 80, 135.8, 4, 4)
     pdf.text(86, 139, txt="Silt Density Index")

     if sample.other_param_40:
          pdf.image(checked, 116, 135.8, 4, 4)
     else:
          pdf.image(unchecked, 116, 135.8, 4, 4)
     pdf.text(122, 139, txt="Particles Size")

     if sample.other_param_41:
          pdf.image(checked, 146, 135.8, 4, 4)
     else:
          pdf.image(unchecked, 146, 135.8, 4, 4)
     pdf.text(152, 139, txt="AOx")

     if sample.other_param_42:
          pdf.image(checked, 166, 135.8, 4, 4)
     else:
          pdf.image(unchecked, 166, 135.8, 4, 4)
     pdf.text(172, 139, txt="Chlorine")

     # # Row G (other_param_43 .. other_param_49)
     if sample.other_param_43:
          pdf.image(checked, 12, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 142.8, 4, 4)
     pdf.text(18, 146, txt="free Chlorine")

     if sample.other_param_44:
          pdf.image(checked, 42, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 42, 142.8, 4, 4)
     pdf.text(48, 146, txt="Sulphide")

     if sample.other_param_45:
          pdf.image(checked, 66, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 66, 142.8, 4, 4)
     pdf.text(72, 146, txt="Total Solid")

     if sample.other_param_46:
          pdf.image(checked, 92, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 92, 142.8, 4, 4)
     pdf.text(98, 146, txt="Beryllium")

     

     if sample.other_param_47:
          pdf.image(checked, 118, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 118, 142.8, 4, 4)
     pdf.text(124, 146, txt="Phosphate")

     # # Row H (other_param_50 .. other_param_56)
     if sample.other_param_48:
          pdf.image(checked, 142, 142.8, 4, 4)
     else:
          pdf.image(unchecked, 142, 142.8, 4, 4)
     pdf.text(148, 146, txt="Volatile Suspended Solids (VSS)")

     if sample.other_param_49:
          pdf.image(checked, 106, 170.8, 4, 4)
     else:
          pdf.image(unchecked, 106, 170.8, 4, 4)
     pdf.text(112, 174, txt="Settleable solids (Imhoff cone)")

     if sample.other_param_50:
          pdf.image(checked, 12, 149.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 149.8, 4, 4)
     pdf.text(18, 153, txt="Oxidation–Reduction Potential (ORP)")

     if sample.other_param_51:
          pdf.image(checked, 82, 149.8, 4, 4)
     else:
          pdf.image(unchecked, 82, 149.8, 4, 4)
     pdf.text(88, 153, txt="Volatile Organic Halogens (VOX)")

     if sample.other_param_52:
          pdf.image(checked, 142, 149.8, 4, 4)
     else:
          pdf.image(unchecked, 142, 149.8, 4, 4)
     pdf.text(148, 153, txt="Sodium Adsorption Ratio (SAR)")

     if sample.other_param_53:
          pdf.image(checked, 12, 156.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 156.8, 4, 4)
     pdf.text(18, 160, txt="Residual Sodium Carbonate (RSC)")


     if sample.other_param_54:
          pdf.image(checked, 75, 156.8, 4, 4)
     else:
          pdf.image(unchecked, 75, 156.8, 4, 4)
     pdf.text(81, 160, txt="Temperature")

     if sample.other_param_55:
          pdf.image(checked, 105, 156.8, 4, 4)
     else:
          pdf.image(unchecked, 105, 156.8, 4, 4)
     pdf.text(111, 160, txt="TSS")

     # # # Row I (other_param_57 .. other_param_63)
     if sample.other_param_56:
          pdf.image(checked, 122, 156.8, 4, 4)
     else:
          pdf.image(unchecked, 122, 156.8, 4, 4)
     pdf.text(128, 160, txt="Anionic Surfactants as MBAS")

     if sample.other_param_57:
          pdf.image(checked, 12, 163.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 163.8, 4, 4)
     pdf.text(18, 167, txt="Total Plate Count")

     if sample.other_param_58:
          pdf.image(checked, 48, 163.8, 4, 4)
     else:
          pdf.image(unchecked, 48, 163.8, 4, 4)
     pdf.text(54, 167, txt="Legionella")

     # # if sample.other_param_60:
     # #      pdf.image(checked, 168, 163.8, 4, 4)
     # # else:
     # #      pdf.image(unchecked, 168, 163.8, 4, 4)
     # # pdf.text(167, 167, txt="Total Plate Count")

     if sample.other_param_59:
          pdf.image(checked, 76, 163.8, 4, 4)
     else:
          pdf.image(unchecked, 76, 163.8, 4, 4)
     pdf.text(82, 167, txt="Fecal Enterococci")

     if sample.other_param_60:
          pdf.image(checked, 112, 163.8, 4, 4)
     else:
          pdf.image(unchecked, 112, 163.8, 4, 4)
     pdf.text(118, 167, txt="Heterotrophic Bacteria")

     if sample.other_param_61:
          pdf.image(checked, 160, 163.8, 4, 4)
     else:
          pdf.image(unchecked, 160, 163.8, 4, 4)
     pdf.text(166, 167, txt="Enterobacteriaceae")

     # # # Row J (other_param_64 .. other_param_66)
     if sample.other_param_62:
          pdf.image(checked, 12, 170.8, 4, 4)
     else:
          pdf.image(unchecked, 12, 170.8, 4, 4)
     pdf.text(18, 174, txt="Listeria Spp.")

     if sample.other_param_63:
          pdf.image(checked, 48, 170.8, 4, 4)
     else:
          pdf.image(unchecked, 48, 170.8, 4, 4)
     pdf.text(54, 174, txt="Salmonella")

     if sample.other_param_64:
          pdf.image(checked, 74, 170.8, 4, 4)
     else:
          pdf.image(unchecked, 74, 170.8, 4, 4)
     pdf.text(80, 174, txt="Yeasts & Molds")


     # Add wastewater section title
     # pdf.set_fill_color(217, 226, 243)
     # pdf.rect(10, 186, 190, 8, 'DF')
     # pdf.text(12, 192, txt="Additional Wastewater Parameters:")
     

     # Additional Requirements section (adjusted Y positions)
     pdf.set_fill_color(217, 226, 243)
     pdf.set_draw_color(25, 27, 2)
     pdf.rect(10, 193, 190, 8, 'DF')  # Changed Y from 219 to 93
     pdf.text(12, 198, txt="Additional Requirements of Customer:")  # Changed Y from 224 to 98

     pdf.rect(10, 201, 190, 25)  # Changed Y from 227 to 101

     pdf.text(12, 205, txt="Customer Specification Limits:")  # Changed Y from 231 to 105
     if sample.checkinp104:
          pdf.image(checked, 62, 201.8, 4, 4)  # Changed Y from 227.8 to 101.8
     else:
          pdf.image(unchecked, 62, 201.8, 4, 4)
     pdf.text(68, 205, txt="Required")

     if sample.checkinp105:
          pdf.image(checked, 85, 201.8, 4, 4)
     else:
          pdf.image(unchecked, 85, 201.8, 4, 4)
     pdf.text(91, 205, txt="Not Required")

     pdf.text(120, 205, txt="Detail(if requred):")
     pdf.text(153, 205, txt=sample.inp106)
     pdf.line(152, 206, 192, 206)

     pdf.text(12, 211, txt="Measurement of Uncertainty:")  # Changed Y from 237 to 211
     if sample.checkinp107:
          pdf.image(checked, 62, 207.8, 4, 4)  # Changed Y from 233.8 to 207.8
     else:
          pdf.image(unchecked, 62, 207.8, 4, 4)
     pdf.text(68, 211, txt="Required")

     if sample.checkinp108:
          pdf.image(checked, 85, 207.8, 4, 4)
     else:
          pdf.image(unchecked, 85, 207.8, 4, 4)
     pdf.text(91, 211, txt="Not Required")

     pdf.text(120, 211, txt="Detail(if requred):")
     pdf.text(153, 211, txt=sample.inp109)
     pdf.line(152, 212, 192, 212)

     pdf.text(12, 217, txt="Statement of Conformity:")  # Changed Y from 243 to 217
     if sample.checkinp110:
          pdf.image(checked, 62, 213.8, 4, 4)  # Changed Y from 239.8 to 213.8
     else:
          pdf.image(unchecked, 62, 213.8, 4, 4)
     pdf.text(68, 217, txt="Required")

     if sample.checkinp111:
          pdf.image(checked, 85, 213.8, 4, 4)
     else:
          pdf.image(unchecked, 85, 213.8, 4, 4)
     pdf.text(91, 217, txt="Not Required")

     pdf.text(120, 217, txt="Detail(if requred):")
     pdf.text(153, 217, txt=sample.inp112)
     pdf.line(152, 218, 192, 218)

     pdf.text(12, 223, txt="Opinion & Interpretations:")  # Changed Y from 249 to 123
     if sample.checkinp113:
          pdf.image(checked, 62, 219.8, 4, 4)  # Changed Y from 245.8 to 219.8
     else:
          pdf.image(unchecked, 62, 219.8, 4, 4)
     pdf.text(68, 223, txt="Required")

     if sample.checkinp114:
          pdf.image(checked, 85, 219.8, 4, 4)
     else:
          pdf.image(unchecked, 85, 219.8, 4, 4)
     pdf.text(91, 223, txt="Not Required")

     pdf.text(120, 223, txt="Detail(if requred):")
     pdf.text(153, 223, txt=sample.inp115)
     pdf.line(152, 224, 192, 224)


     pdf.set_fill_color(217, 226, 243)
     pdf.set_draw_color(25, 27, 2)
     pdf.rect(10,252,190,8,'DF')
     if sample.assign_to:
          pdf.text(12,257,txt="Assigned to(Analyst Name): "+sample.assign_to)
     else:
          pdf.text(12,257,txt="Assigned to():")
     pdf.rect(10,260,190,19)

     if sample.checkinp116:
          pdf.image(checked,12,262.8,4,4)
     else:
          pdf.image(unchecked,12,262.8,4,4)
     pdf.text(18,266,txt="Accepted")


     if sample.checkinp117:
          pdf.image(checked,12,272.8,4,4)
     else:
          pdf.image(unchecked,12,272.8,4,4)
     pdf.text(18,276,txt="Rejected")


     pdf.line(100,260,100,279)

     pdf.text(102,273,txt="Authorize Signature:")
     pdf.text(102,277.5,txt="Lab Manager/Deputy Manager Lab")
     pdf.line(135,274,170,274)
     
     if sample.auth_signature:
         pdf.image(sample.auth_signature.signature,142,261,15,15)




     # pdf.output('Sample Registration'+' '+ sample.sample_id +'.pdf')

     # pdf = open('Sample Registration'+' '+ sample.sample_id +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response
     # Create a response object
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={sample.sample_id}.pdf'

    # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response


def samplePdf1(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_samplePdf1 as PDFWithPageNumbers
               # self.image("static/assets/header.PNG",0,0,self.w,22.5)


     sample = Sample_registration.objects.get(id=pk)
     pdf = PDFWithPageNumbers()
     pdf.add_page()
     
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","",font_path,uni=True)
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","", 9)
     pdf.set_auto_page_break(auto=True, margin=15)


     pdf.rect(30,15,160,47)
     pdf.rect(30,15,160,11)
     pdf.image("static/assets/EnviTechAL LOGO.png",35,16,9,9)
     font_path_alger = "static/fonts/ALGER.TTF"
     pdf.add_font("Algerian","",font_path_alger)
     pdf.set_font("Algerian","", 12)
     pdf.set_text_color(13, 46, 145)
     pdf.text(85,20,txt="ENVI TECH AL")
     font_path = "static/fonts/calibri.ttf"
     font_path_bold = "static/fonts/calibrib.ttf"
     pdf.add_font("Calibri","B",font_path_bold,uni=True)
     pdf.set_font("Calibri","B", 10)
     pdf.set_text_color(25, 27, 28)
     pdf.text(75,24,txt="SAMPLE IDENTIFICATION LABEL")


     current_date = sample.inp9
     current_date=current_date.replace("/","-")
     given_date = datetime.strptime(current_date,"%d-%m-%Y")
     date_five_days_ahead = given_date + timedelta(days=6)
     date_five_days_ahead_str = date_five_days_ahead.strftime("%d-%m-%Y")
     

     pdf.set_font("Calibri","B", 8 )
     pdf.rect(158,16,30,9)
     if sample.conntrol_1:
          pdf.text(160,19,txt=sample.conntrol_1)
          pdf.text(160,21.5,txt=sample.conntrol_date)
          pdf.text(160,24,txt=sample.conntrol_no)



     pdf.set_y(26)
     pdf.set_x(30)
     pdf.cell(40,7,txt="Sample ID",border=1)
     pdf.cell(40,7,txt=sample.sample_id,border=1)
     if sample.checkinp11:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Drinking Water",border=1,ln=True)
     elif sample.checkinp12:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Sludge",border=1,ln=True)
     elif sample.checkinp13 and sample.checkinp16:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Influent/Effluent",border=1,ln=True)
     elif sample.checkinp13:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Influent",border=1,ln=True)
     elif sample.checkinp16:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Effluent",border=1,ln=True)
     elif sample.checkinp17:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="Bore Water",border=1,ln=True)
     elif sample.checkinp18:
          pdf.cell(40,7,txt="Sample Type",border=1)
          pdf.cell(40,7,txt="R.O Water",border=1,ln=True)
     
     pdf.set_x(30)
     pdf.cell(40,7,txt="Sampling Date & Time",border=1)
     pdf.cell(40,7,txt=sample.inp7+", "+sample.inp8,border=1)
     pdf.cell(40,7,txt="Sampling Location",border=1)
     pdf.cell(40,7,txt=sample.inp4,border=1,ln=True)

     pdf.set_x(30)
     pdf.cell(40,8,txt="Env.Condition @ Receiving Time",border=1)
     pdf.rect(70,40,40,8)
     pdf.set_font("Calibri","B", 8 )
     pdf.text(72,43,txt="Temp:")
     pdf.text(72,46.5,txt="pH:")
     pdf.text(80,43,txt=sample.inp19)
     pdf.text(78,46.5,txt=sample.inp20)
     pdf.set_x(110)
     pdf.cell(40,8,txt="Registration Date & Time",border=1)
     pdf.cell(40,8,txt=sample.inp3,border=1,ln=True)

     pdf.set_x(30)
     pdf.cell(40,7,txt="Estimated Disposal Date",border=1)
     pdf.cell(40,7,txt=date_five_days_ahead_str,border=1)
     pdf.cell(40,7,txt="Sample Collected By",border=1)
     pdf.cell(40,7,txt=sample.inp6,border=1,ln=True)

     pdf.set_x(30)
     pdf.cell(40,7,txt="Received By/Sign",border=1)
     pdf.rect(70,55,40,7)
     if sample.auth_signature:
         pdf.image(sample.auth_signature.signature,80,56,6,5)
     pdf.set_x(110)
     pdf.cell(40,7,txt="Sampling By/Sign",border=1)
     pdf.rect(150,55,40,7)
     if sample.sampling_by_signature:
         pdf.image(sample.sampling_by_signature.signature,160,56,6,5)

     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={sample.sample_id}.pdf'

    # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

__all__ = [
    'sample_reg',
    'sample_main',
    'sample_list',
    'sample_view',
    'sample_delete',
    'sample_edit',
    'sample_update',
    'sample_clone',
    'sample_clone_update',
    'samplePdf',
    'samplePdf1',
]
