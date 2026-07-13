from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

#lab_rep_no
# invoice_no
# report_date
# report_to
# address
# attention
# email
# testId





class Role(models.Model):
    role = models.CharField(max_length=500, null=True, blank=True)
   
    def __str__(self):
        return self.role or "Unnamed Role"

class Signatures(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signature = models.ImageField(upload_to='signatures',null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    office = models.CharField(max_length=300,null=True,blank=True)
   
    def __str__(self):
        return f"{self.user.username}'s signature"

class Industry_sector(models.Model):
    name = models.CharField(max_length=500,null=True,blank=True)
    
    
    def __str__(self):
        return self.name

# drinking water form model
class DrinkingWaterForm(models.Model):
    form_name = "Drinking Water Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_dw')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_dw')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_dw')
    report_type = models.CharField(default="dw",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500, null=True)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=100)
    attention = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=30)
    sample_collection_date = models.CharField(max_length=500, null=True)
    sample_description = models.CharField(max_length=300)
    sample_type = models.CharField(max_length=100)
    sample_collected_by = models.CharField(max_length=100)
    date_of_analysis_from = models.CharField(max_length=500, null=True)
    date_of_analysis_to = models.CharField(max_length=500, null=True)
    test_description = models.CharField(max_length=500)
    select =  models.CharField(max_length=500, null = True )
    water_sr1 =  models.CharField(max_length=500, null = True )
    water_sr2 =  models.CharField(max_length=500, null = True )
    water_sr3 =  models.CharField(max_length=500, null = True )
    water_sr4 =  models.CharField(max_length=500, null = True )
    water_sr5 =  models.CharField(max_length=500, null = True )
    water_sr6 =  models.CharField(max_length=500, null = True )
    water_sr7 =  models.CharField(max_length=500, null = True )
    water_sr8 =  models.CharField(max_length=500, null = True )
    water_sr9 =  models.CharField(max_length=500, null = True )
    water_sr10 =  models.CharField(max_length=500, null = True )
    water_sr11 =  models.CharField(max_length=500, null = True )
    water_sr12 =  models.CharField(max_length=500, null = True )
    water_sr13 =  models.CharField(max_length=500, null = True )
    water_sr14 =  models.CharField(max_length=500, null = True )
    water_sr15 =  models.CharField(max_length=500, null = True )
    water_sr16 =  models.CharField(max_length=500, null = True )
    water_sr17 =  models.CharField(max_length=500, null = True )
    water_sr18 =  models.CharField(max_length=500, null = True )
    water_sr19 =  models.CharField(max_length=500, null = True )
    water_sr20 =  models.CharField(max_length=500, null = True )
    water_sr21 =  models.CharField(max_length=500, null = True )
    water_sr22 =  models.CharField(max_length=500, null = True )
    water_sr23 =  models.CharField(max_length=500, null = True )
    water_sr24 =  models.CharField(max_length=500, null = True )
    water_sr25 =  models.CharField(max_length=500, null = True )
    water_sr26 =  models.CharField(max_length=500, null = True )
    water_sr27 =  models.CharField(max_length=500, null = True )
    water_sr28 =  models.CharField(max_length=500, null = True )
    water_sr29 =  models.CharField(max_length=500, null = True )
    water_sr30 =  models.CharField(max_length=500, null = True )
    water_sr31 =  models.CharField(max_length=500, null = True )
    water_sr32 =  models.CharField(max_length=500, null = True )
    method_1 = models.CharField(max_length=500, null=True, default="*APHA 4500 H")
    method_2 = models.CharField(max_length=500, null=True, default="*APHA 2540-C")
    method_3 = models.CharField(max_length=500, null=True, default="ASTM D 1126")
    method_4 = models.CharField(max_length=500, null=True, default="HACH 8025")
    method_5 = models.CharField(max_length=500, null=True, default="*APHA 2130")
    method_6 = models.CharField(max_length=500, null=True, default="HACH 8507")
    method_7 = models.CharField(max_length=500, null=True, default="HACH 8039")
    method_8 = models.CharField(max_length=500, null=True, default="*APHA 2160")
    method_9 = models.CharField(max_length=500, null=True, default="*APHA 2150")
    method_10 = models.CharField(max_length=500, null=True, default="*APHA 4500 Cl")
    method_11 = models.CharField(max_length=500, null=True, default="HACH 8029")
    method_12 = models.CharField(max_length=500, null=True, default="*APHA 3111-D")
    method_13 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_14 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_15 = models.CharField(max_length=500, null=True, default="HACH 8014")
    method_16 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_17 = models.CharField(max_length=500, null=True, default="*APHA 3114-B")
    method_18 = models.CharField(max_length=500, null=True, default="HACH 8015")
    method_19 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_20 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_21 = models.CharField(max_length=500, null=True, default="*APHA 3114-B")
    method_22 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_23 = models.CharField(max_length=500, null=True, default="**HACH 8027")
    method_24 = models.CharField(max_length=500, null=True, default="*APHA 3112-B")
    method_25 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_26 = models.CharField(max_length=500, null=True, default="*APHA 3111-B")
    method_27 = models.CharField(max_length=500, null=True, default="HACH 10069")
    method_28 = models.CharField(max_length=500, null=True, default="ASTM-D-1783")
    method_29 = models.CharField(max_length=500, null=True, default="USEPA 1604")
    method_30 = models.CharField(max_length=500, null=True, default="*APHA 922 B")
    method_31 = models.CharField(max_length=500, null=True, default="USEPA 1604")
    method_32 = models.CharField(max_length=500, null=True, default="USEPA-614.1")
    legend_1 = models.CharField(max_length=100, null=True)
    legend_2 = models.CharField(max_length=100, null=True)
    legend_3 = models.CharField(max_length=100, null=True)
    legend_4 = models.CharField(max_length=100, null=True)
    legend_5 = models.CharField(max_length=100, null=True)
    legend_6 = models.CharField(max_length=100, null=True)
    legend_7 = models.CharField(max_length=100, null=True)
    legend_8 = models.CharField(max_length=100, null=True)
    legend_9 = models.CharField(max_length=100, null=True)
    legend_10 = models.CharField(max_length=100, null=True)
    legend_11 = models.CharField(max_length=100, null=True)
    edit_note = models.CharField(max_length=100,null=True)
    custom_legend = models.CharField(max_length=100,null=True)
    doc_controll_1 = models.CharField(max_length=100,null=True)
    doc_controll_2 = models.CharField(max_length=100,null=True)
    doc_controll_3 = models.CharField(max_length=100,null=True)
    analyzed_by = models.ImageField(default="")
    reviewed_by = models.ImageField(default="")
    approved_by = models.ImageField(default="")
    approved_by1 = models.ImageField(default="")
    location =models.CharField(max_length=500,null=True)
    in_out =models.CharField(max_length=500,null=True)
    custominput = models.CharField(max_length=100,null=True)
    custominput1 = models.CharField(max_length=100,null=True) 
    custominput2 = models.CharField(max_length=100,null=True) 
    custominput3 = models.CharField(max_length=100,null=True) 
    custominput4 = models.CharField(max_length=100,null=True) 
    custominput5 = models.CharField(max_length=100,null=True) 
    custominput6 = models.CharField(max_length=100,null=True) 
    custominput7 = models.CharField(max_length=100,null=True) 
    custominput8 = models.CharField(max_length=100,null=True) 
    custominput9 = models.CharField(max_length=100,null=True) 
    custominput10 = models.CharField(max_length=100,null=True) 
    custominput11 = models.CharField(max_length=100,null=True) 
    custominput12 = models.CharField(max_length=100,null=True) 
    custominput13 = models.CharField(max_length=100,null=True) 
    custominput14 = models.CharField(max_length=100,null=True) 
    custominput15 = models.CharField(max_length=100,null=True) 
    custominput16 = models.CharField(max_length=100,null=True) 
    custominput17 = models.CharField(max_length=100,null=True) 
    custominput18 = models.CharField(max_length=100,null=True) 
    custominput19 = models.CharField(max_length=100,null=True) 
    custominput20 = models.CharField(max_length=100,null=True) 
    custominput21 = models.CharField(max_length=100,null=True) 
    custominput22 = models.CharField(max_length=100,null=True) 
    custominput23 = models.CharField(max_length=100,null=True) 
    custominput24 = models.CharField(max_length=100,null=True) 
    custominput25 = models.CharField(max_length=100,null=True) 
    custominput26 = models.CharField(max_length=100,null=True) 
    custominput27 = models.CharField(max_length=100,null=True) 
    custominput28 = models.CharField(max_length=100,null=True) 
    custominput29 = models.CharField(max_length=100,null=True) 
    custominput30 = models.CharField(max_length=100,null=True) 
    custominput31 = models.CharField(max_length=100,null=True) 
    custominput32 = models.CharField(max_length=100,null=True)
    extra_field = models.TextField(default=[])
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="dw_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no 

class GaseousEmissionForm(models.Model):
    form_name = "Gaseous Emission Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_gae')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_gae')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_gae')
    report_type = models.CharField(default="gae",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500, null=True)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=100)
    attention = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=30)
    GaseEm_test_perf_date = models.CharField(max_length=40)
    GaseEm_test_type = models.CharField(max_length=300)
    GasEm_test_type_extra = models.CharField(max_length=300,null=True)
    GaseEm_test_perf_by = models.CharField(max_length=100)
    GasEm_test_desc = models.CharField(max_length=100)
    GaseEm_types = models.CharField(max_length=100)
    GaseEm_select = models.CharField(max_length=100,null=True)
    GaseEm_sr1 = models.CharField(max_length=500,null=True)
    GaseEm_sr2 =  models.CharField(max_length=500, null = True )
    GaseEm_sr3 =  models.CharField(max_length=500, null = True )
    GaseEm_sr4 =  models.CharField(max_length=500, null = True )
    GaseEm_sr5 =  models.CharField(max_length=500, null = True )
    GaseEm_sr6 =  models.CharField(max_length=500, null = True )
    GaseEm_sr7 =  models.CharField(max_length=500, null = True )
    GaseEm_sr8 =  models.CharField(max_length=500, null = True )
    GaseEm_sr9 =  models.CharField(max_length=500, null = True )
    GaseEm_sr10 =  models.CharField(max_length=500, null = True )
    GaseEm_sr11 =  models.CharField(max_length=500, null = True )
    GaseEm_sr12 =  models.CharField(max_length=500, null = True )
    GaseEm_sr13 =  models.CharField(max_length=500, null = True )
    GaseEm_sr14 =  models.CharField(max_length=500, null = True )
    GaseEm_sr15 =  models.CharField(max_length=500, null = True )
    GaseEm_sr16 =  models.CharField(max_length=500, null = True )
    GaseEm_sr17 =  models.CharField(max_length=500, null = True )
    GaseEm_sr18 =  models.CharField(max_length=500, null = True )
    GaseEm_sr19 =  models.CharField(max_length=500, null = True )
    GaseEm_sr20 =  models.CharField(max_length=500, null = True )
    GaseEm_sr21 =  models.CharField(max_length=500, null = True )
    GaseEm_sr22 =  models.CharField(max_length=500, null = True )
    GaseEm_legend_1 = models.CharField(max_length=100, null=True)
    GaseEm_legend_2 = models.CharField(max_length=100, null=True)
    GaseEm_legend_3 = models.CharField(max_length=100, null=True)
    GaseEm_legend_4 = models.CharField(max_length=100, null=True)
    GaseEm_legend_5 = models.CharField(max_length=100, null=True)
    GaseEm_legend_6 = models.CharField(max_length=100, null=True)
    GaseEm_legend_7 = models.CharField(max_length=100, null=True)
    GaseEm_legend_8 = models.CharField(max_length=100, null=True)
    GaseEm_legend_9 = models.CharField(max_length=100, null=True)
    GaseEm_legend_10 = models.CharField(max_length=100, null=True)
    GaseEm_legend_11 = models.CharField(max_length=100, null=True)
    GaseEm_edit_note = models.CharField(max_length=500,null=True)
    GaseEm_custom_legend = models.CharField(max_length=100,null=True)
    GaseEm_doc_con_1 = models.CharField(max_length=100,null=True)
    GaseEm_doc_con_2 = models.CharField(max_length=100,null=True)
    GaseEm_doc_con_3 = models.CharField(max_length=100,null=True)
    GaseEm_analyzed_by = models.ImageField(default="")
    GaseEm_reviewd_by = models.ImageField(default="")
    GaseEm_approved_by = models.ImageField(default="")
    GaseEm_approved_by1 = models.ImageField(default="")
    location =models.CharField(max_length=500,null=True)
    extra_field = models.TextField(default=[])
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="gae_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no 
    
class AmbientAirForm(models.Model):
    form_name = "Ambient Air Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_aa')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_aa')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_aa')
    report_type = models.CharField(default="aa",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500, null=True)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=100)
    attention = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=30)
    ambientAir_test_perf_date = models.CharField(max_length=40)
    ambientAir_test_type_location = models.CharField(max_length=300)
    ambientAir_test_perf_by = models.CharField(max_length=100)
    ambienAir_test_desc = models.CharField(max_length=100)
    ambienAir_select = models.CharField(max_length=100,null=True)
    ambientAir_sr1 = models.CharField(max_length=500,null=True)
    ambientAir_sr2 =  models.CharField(max_length=500, null = True )
    ambientAir_sr3 =  models.CharField(max_length=500, null = True )
    ambientAir_sr4 =  models.CharField(max_length=500, null = True )
    ambientAir_sr5 =  models.CharField(max_length=500, null = True )
    ambientAir_sr6 =  models.CharField(max_length=500, null = True )
    ambientAir_sr7 =  models.CharField(max_length=500, null = True )
    ambientAir_sr8 =  models.CharField(max_length=500, null = True )
    ambientAir_sr9 =  models.CharField(max_length=500, null = True )
    ambientAir_sr10 =  models.CharField(max_length=500, null = True )
    ambientAir_sr11 =  models.CharField(max_length=500, null = True )
    ambientAir_sr12 =  models.CharField(max_length=500, null = True )
    ambientAir_sr13 =  models.CharField(max_length=500, null = True )
    ambientAir_sr14 =  models.CharField(max_length=500, null = True )
    ambientAir_legend_1 = models.CharField(max_length=100, null=True)
    ambientAir_legend_2 = models.CharField(max_length=100, null=True)
    ambientAir_legend_3 = models.CharField(max_length=100, null=True)
    ambientAir_legend_4 = models.CharField(max_length=100, null=True)
    ambientAir_legend_5 = models.CharField(max_length=100, null=True)
    ambientAir_legend_6 = models.CharField(max_length=100, null=True)
    ambientAir_edit_note = models.CharField(max_length=100,null=True)
    ambientAir_custom_legend = models.CharField(max_length=100,null=True)
    ambientAir_doc_con_1 = models.CharField(max_length=100,null=True)
    ambientAir_doc_con_2 = models.CharField(max_length=100,null=True)
    ambientAir_doc_con_3 = models.CharField(max_length=100,null=True)
    ambientAir_analyzed_by = models.ImageField(default="")
    ambientAir_reviewd_by = models.ImageField(default="")
    ambientAir_approved_by = models.ImageField(default="")
    ambientAir_approved_by1 = models.ImageField(default="",null=True)
    location =models.CharField(max_length=500,null=True)
    extra_field = models.TextField(default=[])
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="aa_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no  
    

class WasteWaterSludge(models.Model):
     form_name = "Waste Water Sludge Form"
     id = models.AutoField(primary_key=True)
     analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_ww')
     assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_ww')
     lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_ww')
     report_type = models.CharField(default="ww",max_length=500)
     lab_report_no = models.CharField(max_length=500)
     invoice_bill_no = models.CharField(max_length=500)
     reporting_date = models.CharField(max_length=500)
     report_to = models.CharField(max_length=500)
     address = models.CharField(max_length=500)
     attention = models.CharField(max_length=500)
     email = models.CharField(max_length=500)
     sample_id = models.CharField(max_length=500)
     ww_sample_colec_Date = models.CharField(max_length=500)
     ww_sample_desc = models.CharField(max_length=500)
     ww_sample_type = models.CharField(max_length=500)
     ww_sample_colec_by = models.CharField(max_length=500)
     ww_date_of_analy_from = models.CharField(max_length=500,null=True)
     ww_date_of_analy_to = models.CharField(max_length=500,null=True)
     ww_test_desc = models.CharField(max_length=500)
     ww_sr1 = models.CharField(max_length=500)
     ww_sr2 = models.CharField(max_length=500)
     ww_sr3 = models.CharField(max_length=500)
     ww_sr4 = models.CharField(max_length=500)
     ww_sr5 = models.CharField(max_length=500)
     ww_sr6 = models.CharField(max_length=500)
     ww_sr7 = models.CharField(max_length=500)
     ww_sr8 = models.CharField(max_length=500)
     ww_sr9 = models.CharField(max_length=500)
     ww_sr10 = models.CharField(max_length=500)
     ww_sr11 = models.CharField(max_length=500)
     ww_sr12 = models.CharField(max_length=500)
     ww_sr13 = models.CharField(max_length=500)
     ww_sr14 = models.CharField(max_length=500,null=True)
     ww_sr15 = models.CharField(max_length=500,null=True)
     ww_sr16 = models.CharField(max_length=500,null=True)
     ww_sr17 = models.CharField(max_length=500,null=True)
     ww_legend_1 = models.CharField(max_length=500)
     ww_legend_2 = models.CharField(max_length=500)
     ww_legend_3 = models.CharField(max_length=500)
     ww_legend_4 = models.CharField(max_length=500)
     ww_legend_5 = models.CharField(max_length=500)
     ww_legend_6 = models.CharField(max_length=500)
     ww_legend_7 = models.CharField(max_length=500)
     ww_legend_8 = models.CharField(max_length=500)
     ww_legend_9 = models.CharField(max_length=500)
     ww_legend_10 = models.CharField(max_length=500)
     ww_legend_11 = models.CharField(max_length=500)
     ww_editnote = models.CharField(max_length=500)
     ww_custom_legend = models.CharField(max_length=500)
     ww_doc_con_1 = models.CharField(max_length=500)
     ww_doc_con_2 = models.CharField(max_length=500)
     ww_doc_con_3 = models.CharField(max_length=500)
     ww_analyzed_by = models.ImageField(default="")
     ww_reviewd_by = models.ImageField(default="")
     ww_approved_by = models.ImageField(default="")     
     ww_approved_by1 = models.ImageField(default="", null=True)     
     location =models.CharField(max_length=500,null=True)
     zdhc =models.CharField(max_length=500,null=True)
     city_location =models.CharField(max_length=500,null=True)
     customer_id =models.CharField(max_length=500,null=True)
     pdf_heading = models.CharField(max_length=200,null=True)
     pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_1 = models.TextField(null=True,blank=True)
     pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_2 = models.TextField(null=True,blank=True)
     pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_3 = models.TextField(null=True,blank=True)
     pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_4 = models.TextField(null=True,blank=True)
     pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_5 = models.TextField(null=True,blank=True)
     pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
     pdf_desc_6 = models.TextField(null=True,blank=True)
     created_at = models.DateTimeField(auto_now_add=True,null=True)

     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ww_reports_created")
     industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
     
     class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
     
     def __str__(self):
        return self.form_name +" - "+  self.lab_report_no
     



class VehiculEmissionForm(models.Model):
    form_name = "Vehicular Emission Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_vem')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_vem')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_vem')
    report_type = models.CharField(default="ve",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500,null=True)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    vehEm_test_perf_date = models.CharField(max_length=500)
    vehEm_test_type = models.CharField(max_length=500)
    vehEm_test_type_extra = models.CharField(max_length=500,null=True)
    vehEm_test_perfBy = models.CharField(max_length=500)
    vehEm_test_desc = models.CharField(max_length=500)
    select = models.CharField(max_length=500,null=True)
    vehEm_sr1 = models.CharField(max_length=500)
    vehEm_sr2 = models.CharField(max_length=500)
    vehEm_sr3 = models.CharField(max_length=500)
    vehEm_legend_1 = models.CharField(max_length=500)
    vehEm_legend_2 = models.CharField(max_length=500)
    vehEm_legend_3 = models.CharField(max_length=500)
    vehEm_legend_4 = models.CharField(max_length=500)
    vehEm_legend_5 = models.CharField(max_length=500)
    vehEm_legend_6 = models.CharField(max_length=500)
    vehEm_legend_7 = models.CharField(max_length=500)
    vehEm_legend_8 = models.CharField(max_length=500)
    vehEm_legend_9 = models.CharField(max_length=500)
    vehEm_legend_10 = models.CharField(max_length=500)
    vehEm_legend_11 = models.CharField(max_length=500)
    vehEm_edit_note = models.CharField(max_length=500,null=True)
    vehEm_custom_legend = models.CharField(max_length=500)
    vehEm_doc_con1 = models.CharField(max_length=500)
    vehEm_doc_con2 = models.CharField(max_length=500)
    vehEm_doc_con3 = models.CharField(max_length=500)
    vehEm_analyzedby = models.ImageField(default="")
    vehEm_reviewedby = models.ImageField(default="")
    vehEm_approvedby = models.ImageField(default="")
    vehEm_approvedby1 = models.ImageField(default="",null=True)
    location =models.CharField(max_length=500,null=True)
    extra_field = models.TextField(default=[])
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="vem_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no
    


class LuxAnalysisForm(models.Model):
        form_name = "Lux Analysis Form"
        id = models.AutoField(primary_key=True)
        analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_la')
        assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_la')
        lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_la')
        report_type = models.CharField(default="la",max_length=500)
        lab_report_no = models.CharField(max_length=500)
        invoice_bill_no = models.CharField(max_length=500)
        reporting_date = models.CharField(max_length=500)
        report_to = models.CharField(max_length=500)
        address = models.CharField(max_length=500)
        attention = models.CharField(max_length=500)
        email = models.CharField(max_length=500)
        sample_id = models.CharField(max_length=500)
        lux_test_perf_date = models.CharField(max_length=500)
        lux_test_type = models.CharField(max_length=500)
        lux_test_perfBy = models.CharField(max_length=500)
        lux_test_desc = models.CharField(max_length=500)
        lux_parameters_1 = models.CharField(max_length=500)
        lux_result_1 = models.CharField(max_length=500)
        lux_parameters_2 = models.CharField(max_length=500)
        lux_result_2 = models.CharField(max_length=500)
        lux_parameters_3 = models.CharField(max_length=500)
        lux_result_3 = models.CharField(max_length=500)
        lux_parameters_4 = models.CharField(max_length=500)
        lux_result_4 = models.CharField(max_length=500)
        lux_parameters_5 = models.CharField(max_length=500)
        lux_result_5 = models.CharField(max_length=500)
        lux_parameters_6 = models.CharField(max_length=500)
        lux_result_6 = models.CharField(max_length=500)
        lux_parameters_7 = models.CharField(max_length=500)
        lux_result_7 = models.CharField(max_length=500)
        lux_parameters_8 = models.CharField(max_length=500)
        lux_result_8 = models.CharField(max_length=500)
        lux_parameters_9 = models.CharField(max_length=500)
        lux_result_9 = models.CharField(max_length=500)
        lux_parameters_10 = models.CharField(max_length=500)
        lux_result_10 = models.CharField(max_length=500)
        lux_parameters_11 = models.CharField(max_length=500)
        lux_result_11 = models.CharField(max_length=500)
        lux_parameters_12 = models.CharField(max_length=500)
        lux_result_12 = models.CharField(max_length=500)
        lux_parameters_13 = models.CharField(max_length=500)
        lux_result_13 = models.CharField(max_length=500)
        lux_legend_1 = models.CharField(max_length=500,null=True)
        lux_legend_2 = models.CharField(max_length=500,null=True)
        lux_legend_3 = models.CharField(max_length=500,null=True)
        lux_legend_4 = models.CharField(max_length=500,null=True)
        lux_legend_5 = models.CharField(max_length=500,null=True)
        lux_legend_6 = models.CharField(max_length=500,null=True)
        lux_legend_7 = models.CharField(max_length=500,null=True)
        lux_legend_8 = models.CharField(max_length=500,null=True)
        lux_legend_9 = models.CharField(max_length=500,null=True)
        lux_legend_10 = models.CharField(max_length=500,null=True)
        lux_legend_11 = models.CharField(max_length=500,null=True)
        lux_edit_note = models.CharField(max_length=500,null=True)
        lux_custom_legend = models.CharField(max_length=500)
        lux_doc_con1 = models.CharField(max_length=500)
        lux_doc_con2 = models.CharField(max_length=500)
        lux_doc_con3 = models.CharField(max_length=500)
        lux_analyzedby = models.ImageField(default="")
        lux_reviewedby = models.ImageField(default="")
        lux_approvedby = models.ImageField(default="")
        lux_approvedby1 = models.ImageField(default="",null=True)
        location =models.CharField(max_length=500,null=True)
        city_location =models.CharField(max_length=500,null=True)
        extra_field = models.TextField(default=[])
        customer_id =models.CharField(max_length=500,null=True)
        pdf_heading = models.CharField(max_length=200,null=True)
        pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_1 = models.TextField(null=True,blank=True)
        pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_2 = models.TextField(null=True,blank=True)
        pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_3 = models.TextField(null=True,blank=True)
        pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_4 = models.TextField(null=True,blank=True)
        pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_5 = models.TextField(null=True,blank=True)
        pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
        pdf_desc_6 = models.TextField(null=True,blank=True)

        created_at = models.DateTimeField(auto_now_add=True,null=True)

        created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="la_reports_created")
        industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
        
        class Meta:
            indexes = [
                models.Index(fields=['reporting_date']),
                models.Index(fields=['report_to']),
                models.Index(fields=['sample_id']),
                models.Index(fields=['city_location']),
                models.Index(fields=['lab_report_no']),
            ]
    
        def __str__(self):
            return self.form_name +" - "+ self.lab_report_no
    

class PackingPolyBagForm(models.Model):
    form_name ="Packing Poly Bag"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_ppb')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_ppb')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_ppb')
    report_type = models.CharField(default="pp",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    pack_sample_colc_date = models.CharField(max_length=500)
    pack_sample_desc = models.CharField(max_length=500)
    pack_sample_type = models.CharField(max_length=500)
    pack_sample_colc_by = models.CharField(max_length=500)
    pack_test_desc = models.CharField(max_length=500)
    pack_sr1 = models.CharField(max_length=500)
    pack_legend_1 = models.CharField(max_length=500)
    pack_edit_note = models.CharField(max_length=500)
    pack_custom_legend = models.CharField(max_length=500)
    doc_con1 = models.CharField(max_length=500)
    doc_con2 = models.CharField(max_length=500)
    doc_con3 = models.CharField(max_length=500)
    pack_analyzed_by = models.ImageField(default="")
    pack_reviewed_by = models.ImageField(default="")
    pack_approved_by = models.ImageField(default="")
    pack_approved_by1 = models.ImageField(default="",null=True)
    location =models.CharField(max_length=500,null=True)
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="pp_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no

class MachineOilForm(models.Model):
    form_name = "Machine Oil Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_mo')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_mo')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_mo')
    report_type = models.CharField(default="mo",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    machine_sample_col_date = models.CharField(max_length=500)
    machine_sample_desc = models.CharField(max_length=500)
    machine_sample_type = models.CharField(max_length=500)
    machine_sample_col_by = models.CharField(max_length=500)
    machine_test_desc = models.CharField(max_length=500)
    machine_sr1 = models.CharField(max_length=500)
    machine_sr2 = models.CharField(max_length=500)
    machine_sr3 = models.CharField(max_length=500)
    machine_sr4 = models.CharField(max_length=500)
    machine_sr5 = models.CharField(max_length=500)
    machine_sr6 = models.CharField(max_length=500)
    machine_sr7 = models.CharField(max_length=500)
    machine_sr8 = models.CharField(max_length=500)
    machine_sr9 = models.CharField(max_length=500)
    machine_sr10 = models.CharField(max_length=500)
    machine_sr11 = models.CharField(max_length=500)
    machine_sr12 = models.CharField(max_length=500)
    machine_sr13 = models.CharField(max_length=500)
    machine_sr14 = models.CharField(max_length=500)
    machine_sr15 = models.CharField(max_length=500)
    machine_sr16 = models.CharField(max_length=500)
    machine_legend_1 = models.CharField(max_length=500)
    machine_legend_2 = models.CharField(max_length=500)
    custom_legend = models.CharField(max_length=500,null=True)    
    machine_edit_note = models.CharField(max_length=500)
    machine_custom_legend = models.CharField(max_length=500)
    machine_doc1 = models.CharField(max_length=500)
    machine_doc2 = models.CharField(max_length=500)
    machine_doc3 = models.CharField(max_length=500)
    machine_analyzedby = models.ImageField(max_length=500)
    machine_reviewedby = models.ImageField(max_length=500)
    machine_approvedby = models.ImageField(max_length=500)    
    machine_approvedby1 = models.ImageField(max_length=500,null=True)  
    location =models.CharField(max_length=500,null=True)  
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
        

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="mo_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no    
    


class MicrobialAnalysis(models.Model):
    form_name = "Microbial Analysis Form"    
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_mb')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_mb')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_mb')
    report_type = models.CharField(default="ma",max_length=500)
    lab_report_no = models.CharField(max_length=150)
    invoice_bill_no = models.CharField(max_length=150)
    reporting_date = models.CharField(max_length=150)
    report_to = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    attention = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    sample_id = models.CharField(max_length=150)
    micro_sample_col_date = models.CharField(max_length=150)
    micro_sample_desc = models.CharField(max_length=150)
    micro_sample_type = models.CharField(max_length=150)
    micro_sample_col_by = models.CharField(max_length=150)
    micro_date_analysis_from = models.CharField(max_length=150,null=True)
    micro_date_analysis_to = models.CharField(max_length=150,null=True)
    micro_test_desc = models.CharField(max_length=150)
    micro_sr1 = models.CharField(max_length=150)
    micro_sr2 = models.CharField(max_length=150)
    micro_sr3 = models.CharField(max_length=150)
    micro_sr4 = models.CharField(max_length=150)
    micro_sr5 = models.CharField(max_length=150)
    micro_sr6 = models.CharField(max_length=150)
    micro_ex_1_1 = models.CharField(max_length=150,null=True)
    micro_ex_1_2 = models.CharField(max_length=150,null=True)
    micro_ex_1_3 = models.CharField(max_length=150,null=True)
    micro_ex_1_4 = models.CharField(max_length=150,null=True)
    micro_ex_1_5 = models.CharField(max_length=150,null=True)
    micro_ex_1_6 = models.CharField(max_length=150,null=True)
    micro_ex_1_7 = models.CharField(max_length=150,null=True)
    micro_ex_1_1 = models.CharField(max_length=150,null=True)
    micro_ex_2_1 = models.CharField(max_length=150,null=True)
    micro_ex_2_2 = models.CharField(max_length=150,null=True)
    micro_ex_2_3 = models.CharField(max_length=150,null=True)
    micro_ex_2_4 = models.CharField(max_length=150,null=True)
    micro_ex_2_5 = models.CharField(max_length=150,null=True)
    micro_ex_2_6 = models.CharField(max_length=150,null=True)
    micro_ex_2_7 = models.CharField(max_length=150,null=True)
    unit_head = models.CharField(max_length=150,null=True)
    unit_1 = models.CharField(max_length=150,null=True)
    unit_2 = models.CharField(max_length=150,null=True)
    unit_3 = models.CharField(max_length=150,null=True)
    unit_4 = models.CharField(max_length=150,null=True)
    unit_5 = models.CharField(max_length=150,null=True)
    unit_6 = models.CharField(max_length=150,null=True)
    micro_p1 = models.CharField(max_length=150,null=True)
    micro_p2 = models.CharField(max_length=150,null=True)
    micro_p3 = models.CharField(max_length=150,null=True)
    micro_p4 = models.CharField(max_length=150,null=True)
    micro_p5 = models.CharField(max_length=150,null=True)
    micro_p6 = models.CharField(max_length=150,null=True)
    micro_p7 = models.CharField(max_length=150,null=True)
    micro_legend_1 = models.CharField(max_length=150)
    micro_legend_2 = models.CharField(max_length=150)
    micro_editnote = models.CharField(max_length=250)
    micro_custom_legend = models.CharField(max_length=150)
    micro_doc1 = models.CharField(max_length=150)
    micro_doc2 = models.CharField(max_length=150)
    micro_doc3 = models.CharField(max_length=150)
    micro_analyzedby = models.ImageField(default="")
    micro_reviewedby = models.ImageField(default="")
    micro_approvedby = models.ImageField(default="")
    micro_approvedby1 = models.ImageField(default="",null=True)
    location =models.CharField(max_length=500,null=True)
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    extra_field = models.TextField(default=[])
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="mb_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no 
    

class ViscousLiquid(models.Model):
    form_name="Viscous Liquid Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_vl')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_vl')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_vl')
    report_type = models.CharField(default="vl",max_length=500)
    lab_report_no = models.CharField(max_length=350)
    invoice_bill_no = models.CharField(max_length=350)
    reporting_date = models.CharField(max_length=350)
    report_to = models.CharField(max_length=350)
    address = models.CharField(max_length=350)
    attention = models.CharField(max_length=350)
    email = models.CharField(max_length=350)
    sample_id = models.CharField(max_length=350)
    sample_Col_date = models.CharField(max_length=350)
    sample_Desc = models.CharField(max_length=350)
    sample_type = models.CharField(max_length=350)
    sample_col_by = models.CharField(max_length=350)
    date_of_analysis_from = models.CharField(max_length=350,null=True)
    date_of_analysis_to = models.CharField(max_length=350,null=True)
    test_desc = models.CharField(max_length=350)
    viscous_select = models.CharField(max_length=350)
    sr1 = models.CharField(max_length=350)
    legend_1 = models.CharField(max_length=350)
    legend_2 = models.CharField(max_length=350)
    edit_note = models.CharField(max_length=350)
    custom_legend = models.CharField(max_length=350)
    doc1 = models.CharField(max_length=350)
    doc2 = models.CharField(max_length=350)
    doc3 = models.CharField(max_length=350)
    analyzedby = models.ImageField(max_length=350)
    reviewedby = models.ImageField(max_length=350)
    approvedby = models.ImageField(max_length=350)
    approvedby1 = models.ImageField(max_length=350,null=True)
    location =models.CharField(max_length=500,null=True)
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="vl_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no

class AmbientAir2(models.Model):
    form_name= "Ambient Air Quality 2 Form"
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_aa2')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_aa2')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_aa2')
    report_type = models.CharField(default="aa2",max_length=500)
    lab_report_no = models.CharField(max_length=350)
    invoice_bill_no = models.CharField(max_length=350)
    reporting_date = models.CharField(max_length=350)
    report_to = models.CharField(max_length=350)
    address = models.CharField(max_length=350)
    attention = models.CharField(max_length=350)
    email = models.CharField(max_length=350)
    sample_id = models.CharField(max_length=350)
    test_perf_date = models.CharField(max_length=350)
    test_type = models.CharField(max_length=350)
    test_desc = models.CharField(max_length=350)
    test_test_perf_by = models.CharField(max_length=350)
    sr1_1 = models.CharField(max_length=350)
    sr1_2 = models.CharField(max_length=350)
    sr1_3 = models.CharField(max_length=350)
    sr1_4 = models.CharField(max_length=350)
    sr1_5 = models.CharField(max_length=350)
    sr1_6 = models.CharField(max_length=350)
    sr1_7 = models.CharField(max_length=350)
    sr1_8 = models.CharField(max_length=350,null=True)
    sr1_9 = models.CharField(max_length=350)
    sr1_10 = models.CharField(max_length=350)
    sr2_0 = models.CharField(max_length=350)
    sr2_1 = models.CharField(max_length=350)
    sr2_2 = models.CharField(max_length=350)
    sr2_3 = models.CharField(max_length=350)
    sr2_4 = models.CharField(max_length=350)
    sr2_5 = models.CharField(max_length=350)
    sr2_6 = models.CharField(max_length=350)
    sr2_7 = models.CharField(max_length=350)
    sr2_8 = models.CharField(max_length=350)
    sr2_9 = models.CharField(max_length=350)
    sr3_0 = models.CharField(max_length=350)
    sr3_1 = models.CharField(max_length=350)
    sr3_2 = models.CharField(max_length=350)
    sr3_3 = models.CharField(max_length=350)
    sr3_4 = models.CharField(max_length=350)
    sr3_5 = models.CharField(max_length=350)
    sr3_6 = models.CharField(max_length=350)
    sr3_7 = models.CharField(max_length=350)
    sr3_8 = models.CharField(max_length=350)
    sr3_9 = models.CharField(max_length=350)
    sr4_0 = models.CharField(max_length=350)
    sr4_1 = models.CharField(max_length=350)
    sr4_2 = models.CharField(max_length=350)
    sr4_3 = models.CharField(max_length=350)
    sr4_4 = models.CharField(max_length=350)
    sr4_5 = models.CharField(max_length=350)
    sr4_6 = models.CharField(max_length=350)
    sr4_7 = models.CharField(max_length=350)
    sr4_8 = models.CharField(max_length=350)
    sr4_9 = models.CharField(max_length=350)
    sr5_0 = models.CharField(max_length=350)
    sr5_1 = models.CharField(max_length=350)
    sr5_2 = models.CharField(max_length=350)
    sr5_3 = models.CharField(max_length=350)
    sr5_4 = models.CharField(max_length=350)
    sr5_5 = models.CharField(max_length=350)
    sr5_6 = models.CharField(max_length=350)
    sr5_7 = models.CharField(max_length=350)
    sr5_8 = models.CharField(max_length=350)
    sr5_9 = models.CharField(max_length=350)
    sr6_0 = models.CharField(max_length=350)
    sr6_1 = models.CharField(max_length=350)
    sr6_2 = models.CharField(max_length=350)
    sr6_3 = models.CharField(max_length=350)
    sr6_4 = models.CharField(max_length=350)
    sr6_5 = models.CharField(max_length=350)
    sr6_6 = models.CharField(max_length=350)
    sr6_7 = models.CharField(max_length=350)
    sr6_8 = models.CharField(max_length=350)
    sr6_9 = models.CharField(max_length=350)
    sr7_0 = models.CharField(max_length=350)
    sr7_1 = models.CharField(max_length=350)
    sr7_2 = models.CharField(max_length=350)
    sr7_3 = models.CharField(max_length=350)
    sr7_4 = models.CharField(max_length=350)
    sr7_5 = models.CharField(max_length=350)
    sr7_6 = models.CharField(max_length=350)
    sr7_7 = models.CharField(max_length=350)
    sr7_8 = models.CharField(max_length=350)
    sr7_9 = models.CharField(max_length=350)
    sr8_0 = models.CharField(max_length=350)
    sr8_1 = models.CharField(max_length=350)
    sr8_2 = models.CharField(max_length=350)
    sr8_3 = models.CharField(max_length=350)
    sr8_4 = models.CharField(max_length=350)
    sr8_5 = models.CharField(max_length=350)
    sr8_6 = models.CharField(max_length=350)
    sr8_7 = models.CharField(max_length=350)
    sr8_8 = models.CharField(max_length=350)
    sr8_9 = models.CharField(max_length=350)
    sr9_0 = models.CharField(max_length=350)
    sr9_1 = models.CharField(max_length=350)
    sr9_2 = models.CharField(max_length=350)
    sr9_3 = models.CharField(max_length=350)
    sr9_4 = models.CharField(max_length=350)
    sr9_5 = models.CharField(max_length=350)
    sr9_6 = models.CharField(max_length=350)
    sr9_7 = models.CharField(max_length=350)
    sr9_8 = models.CharField(max_length=350)
    sr9_9 = models.CharField(max_length=350)
    sr10_0 = models.CharField(max_length=350)
    sr10_1 = models.CharField(max_length=350)
    sr10_2 = models.CharField(max_length=350)
    sr10_3 = models.CharField(max_length=350)
    sr10_4 = models.CharField(max_length=350)
    sr10_5 = models.CharField(max_length=350)
    sr10_6 = models.CharField(max_length=350)
    sr10_7 = models.CharField(max_length=350)
    sr10_8 = models.CharField(max_length=350)
    sr10_9 = models.CharField(max_length=350)
    sr11_0 = models.CharField(max_length=350)
    sr11_1 = models.CharField(max_length=350)
    sr11_2 = models.CharField(max_length=350)
    sr11_3 = models.CharField(max_length=350)
    sr11_4 = models.CharField(max_length=350)
    sr11_5 = models.CharField(max_length=350)
    sr11_6 = models.CharField(max_length=350)
    sr11_7 = models.CharField(max_length=350)
    sr11_8 = models.CharField(max_length=350)
    sr11_9 = models.CharField(max_length=350)
    sr12_0 = models.CharField(max_length=350)
    sr12_1 = models.CharField(max_length=350)
    sr12_2 = models.CharField(max_length=350)
    sr12_3 = models.CharField(max_length=350)
    sr12_4 = models.CharField(max_length=350)
    sr12_5 = models.CharField(max_length=350)
    sr12_6 = models.CharField(max_length=350)
    sr12_7 = models.CharField(max_length=350)
    sr12_8 = models.CharField(max_length=350)
    sr12_9 = models.CharField(max_length=350)
    sr13_0 = models.CharField(max_length=350)
    sr13_1 = models.CharField(max_length=350)
    sr13_2 = models.CharField(max_length=350)
    sr13_3 = models.CharField(max_length=350)
    sr13_4 = models.CharField(max_length=350)
    sr13_5 = models.CharField(max_length=350)
    sr13_6 = models.CharField(max_length=350)
    sr13_7 = models.CharField(max_length=350)
    sr13_8 = models.CharField(max_length=350)
    sr13_9 = models.CharField(max_length=350)
    sr14_0 = models.CharField(max_length=350)
    sr14_1 = models.CharField(max_length=350)
    sr14_2 = models.CharField(max_length=350)
    sr14_3 = models.CharField(max_length=350)
    sr14_4 = models.CharField(max_length=350)
    sr14_5 = models.CharField(max_length=350)
    sr14_6 = models.CharField(max_length=350)
    sr14_7 = models.CharField(max_length=350)
    sr14_8 = models.CharField(max_length=350)
    sr14_9 = models.CharField(max_length=350)
    sr15_0 = models.CharField(max_length=350)
    sr15_1 = models.CharField(max_length=350)
    sr15_2 = models.CharField(max_length=350)
    sr15_3 = models.CharField(max_length=350)
    sr15_4 = models.CharField(max_length=350)
    sr15_5 = models.CharField(max_length=350)
    sr15_6 = models.CharField(max_length=350)
    sr15_7 = models.CharField(max_length=350)
    sr15_8 = models.CharField(max_length=350)
    sr15_9 = models.CharField(max_length=350)
    sr16_0 = models.CharField(max_length=350)
    sr16_1 = models.CharField(max_length=350)
    sr16_2 = models.CharField(max_length=350)
    sr16_3 = models.CharField(max_length=350)
    sr16_4 = models.CharField(max_length=350)
    sr16_5 = models.CharField(max_length=350)
    sr16_6 = models.CharField(max_length=350)
    sr16_7 = models.CharField(max_length=350)
    sr16_8 = models.CharField(max_length=350)
    sr16_9 = models.CharField(max_length=350)
    sr17_0 = models.CharField(max_length=350)
    sr17_1 = models.CharField(max_length=350)
    sr17_2 = models.CharField(max_length=350)
    sr17_3 = models.CharField(max_length=350,null=True)
    sr17_4 = models.CharField(max_length=350)
    sr17_5 = models.CharField(max_length=350)
    sr17_6 = models.CharField(max_length=350)
    sr17_7 = models.CharField(max_length=350)
    sr17_8 = models.CharField(max_length=350)
    sr17_9 = models.CharField(max_length=350)
    sr18_0 = models.CharField(max_length=350)
    sr18_1 = models.CharField(max_length=350)
    sr18_2 = models.CharField(max_length=350)
    sr18_3 = models.CharField(max_length=350)
    sr18_4 = models.CharField(max_length=350)
    sr18_5 = models.CharField(max_length=350)
    sr18_6 = models.CharField(max_length=350)
    sr18_7 = models.CharField(max_length=350)
    sr18_8 = models.CharField(max_length=350)
    sr18_9 = models.CharField(max_length=350)
    sr19_0 = models.CharField(max_length=350)
    sr19_1 = models.CharField(max_length=350)
    sr19_2 = models.CharField(max_length=350)
    sr19_3 = models.CharField(max_length=350)
    sr19_4 = models.CharField(max_length=350)
    sr19_5 = models.CharField(max_length=350)
    sr19_6 = models.CharField(max_length=350)
    sr19_7 = models.CharField(max_length=350)
    sr19_8 = models.CharField(max_length=350)
    sr19_9 = models.CharField(max_length=350)
    sr20_0 = models.CharField(max_length=350)
    sr20_1 = models.CharField(max_length=350)
    sr20_2 = models.CharField(max_length=350)
    sr20_3 = models.CharField(max_length=350)
    sr20_4 = models.CharField(max_length=350)
    sr20_5 = models.CharField(max_length=350)
    sr20_6 = models.CharField(max_length=350)
    sr20_7 = models.CharField(max_length=350)
    sr20_8 = models.CharField(max_length=350)
    sr20_9 = models.CharField(max_length=350)
    sr21_0 = models.CharField(max_length=350)
    sr21_1 = models.CharField(max_length=350)
    sr21_2 = models.CharField(max_length=350)
    sr21_3 = models.CharField(max_length=350)
    sr21_4 = models.CharField(max_length=350)
    sr21_5 = models.CharField(max_length=350)
    sr21_6 = models.CharField(max_length=350)
    sr21_7 = models.CharField(max_length=350)
    sr21_8 = models.CharField(max_length=350)
    sr21_9 = models.CharField(max_length=350)
    sr22_0 = models.CharField(max_length=350)
    sr22_1 = models.CharField(max_length=350)
    sr22_2 = models.CharField(max_length=350)
    sr22_3 = models.CharField(max_length=350)
    sr22_4 = models.CharField(max_length=350)
    sr22_5 = models.CharField(max_length=350)
    sr22_6 = models.CharField(max_length=350)
    sr22_7 = models.CharField(max_length=350)
    sr22_8 = models.CharField(max_length=350)
    sr22_9 = models.CharField(max_length=350)
    sr23_0 = models.CharField(max_length=350)
    sr23_1 = models.CharField(max_length=350)
    sr23_2 = models.CharField(max_length=350)
    sr23_3 = models.CharField(max_length=350)
    sr23_4 = models.CharField(max_length=350)
    sr23_5 = models.CharField(max_length=350)
    sr23_6 = models.CharField(max_length=350)
    sr23_7 = models.CharField(max_length=350)
    sr23_8 = models.CharField(max_length=350)
    sr23_9 = models.CharField(max_length=350)
    sr24_0 = models.CharField(max_length=350)
    sr24_1 = models.CharField(max_length=350)
    sr24_2 = models.CharField(max_length=350)
    sr24_3 = models.CharField(max_length=350)
    sr24_4 = models.CharField(max_length=350)
    sr24_5 = models.CharField(max_length=350)
    sr24_6 = models.CharField(max_length=350)
    sr24_7 = models.CharField(max_length=350)
    sr24_8 = models.CharField(max_length=350)
    sr24_9 = models.CharField(max_length=350)
    sr25_0 = models.CharField(max_length=350)
    sr25_1 = models.CharField(max_length=350)
    sr25_2 = models.CharField(max_length=350)
    sr25_3 = models.CharField(max_length=350)
    sr25_4 = models.CharField(max_length=350)
    sr25_5 = models.CharField(max_length=350)
    sr25_6 = models.CharField(max_length=350)
    sr25_7 = models.CharField(max_length=350)
    sr25_8 = models.CharField(max_length=350)
    
    seqs_lim_1 = models.CharField(max_length=350,null=True)
    seqs_lim_2 = models.CharField(max_length=350,null=True)
    seqs_lim_3 = models.CharField(max_length=350,null=True)
    seqs_lim_4 = models.CharField(max_length=350,null=True)
    seqs_lim_5 = models.CharField(max_length=350,null=True)
    seqs_lim_6 = models.CharField(max_length=350,null=True)
    seqs_lim_7 = models.CharField(max_length=350,null=True)
    seqs_lim_8 = models.CharField(max_length=350,null=True)
    seqs_lim_9 = models.CharField(max_length=350,null=True)
    peqs_lim_1 = models.CharField(max_length=350,null=True)
    peqs_lim_2 = models.CharField(max_length=350,null=True)
    peqs_lim_3 = models.CharField(max_length=350,null=True)
    peqs_lim_4 = models.CharField(max_length=350,null=True)
    peqs_lim_5 = models.CharField(max_length=350,null=True)
    peqs_lim_6 = models.CharField(max_length=350,null=True)
    peqs_lim_7 = models.CharField(max_length=350,null=True)
    peqs_lim_8 = models.CharField(max_length=350,null=True)
    peqs_lim_9 = models.CharField(max_length=350,null=True)
    neqs_lim_1 = models.CharField(max_length=350,null=True)
    neqs_lim_2 = models.CharField(max_length=350,null=True)
    neqs_lim_3 = models.CharField(max_length=350,null=True)
    neqs_lim_4 = models.CharField(max_length=350,null=True)
    neqs_lim_5 = models.CharField(max_length=350,null=True)
    neqs_lim_6 = models.CharField(max_length=350,null=True)
    neqs_lim_7 = models.CharField(max_length=350,null=True)
    neqs_lim_8 = models.CharField(max_length=350,null=True)
    neqs_lim_9 = models.CharField(max_length=350,null=True)
    
    
    select = models.CharField(max_length=350)
    legend_1 = models.CharField(max_length=350)
    legend_2 = models.CharField(max_length=350)
    legend_3 = models.CharField(max_length=350)
    legend_4 = models.CharField(max_length=350)
    legend_5 = models.CharField(max_length=350)
    legend_6 = models.CharField(max_length=350)
    legend_7 = models.CharField(max_length=350)
    legend_8 = models.CharField(max_length=350)
    legend_9 = models.CharField(max_length=350)
    legend_10 = models.CharField(max_length=350)
    legend_11 = models.CharField(max_length=350)
    edit_note = models.CharField(max_length=350)
    custom_legend = models.CharField(max_length=350)
    doc1 = models.CharField(max_length=350)
    doc2 = models.CharField(max_length=350)
    doc3 = models.CharField(max_length=350)
    analyzedby = models.ImageField(max_length=500)
    reviewedby = models.ImageField(max_length=500)
    approvedby = models.ImageField(max_length=500)    
    approvedby1 = models.ImageField(max_length=500,null=True)  
    location =models.CharField(max_length=500,null=True)  
    method_checkBox =models.CharField(max_length=500,null=True)  
    hours_checkBox =models.CharField(max_length=500,null=True)  
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="aa2_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no
    

class WasteWaterForm2(models.Model):
    form_name= "Waste Water Form"    
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_ww2')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_ww2')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_ww2')
    report_type = models.CharField(default="ww2",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    sample_Col_date = models.CharField(max_length=500)
    sample_desc = models.CharField(max_length=500)
    sampling_method = models.CharField(max_length=500)
    sample_type = models.CharField(max_length=500)
    sample_collected_by = models.CharField(max_length=500)
    date_of_analysis_from = models.CharField(max_length=500,null=True)
    date_of_analysis_to = models.CharField(max_length=500,null=True)
    test_description = models.CharField(max_length=500)
    select = models.CharField(max_length=500)
    result_1 = models.CharField(max_length=500)
    result_1_1 = models.CharField(max_length=500)
    result_2 = models.CharField(max_length=500)
    result_2_2 = models.CharField(max_length=500)
    result_3 = models.CharField(max_length=500)
    result_3_3 = models.CharField(max_length=500)
    result_4 = models.CharField(max_length=500)
    result_4_4 = models.CharField(max_length=500)
    result_5 = models.CharField(max_length=500)
    result_5_5 = models.CharField(max_length=500)
    result_6 = models.CharField(max_length=500)
    result_6_6 = models.CharField(max_length=500,null=True)
    result_7 = models.CharField(max_length=500,null=True)
    result_7_7 = models.CharField(max_length=500)
    metho_select = models.CharField(max_length=500)
    result_8 = models.CharField(max_length=500)
    result_8_8 = models.CharField(max_length=500)
    result_9 = models.CharField(max_length=500)
    result_9_9 = models.CharField(max_length=500)
    result_10 = models.CharField(max_length=500)
    result_10_10 = models.CharField(max_length=500)
    result_11 = models.CharField(max_length=500)
    result_11_11= models.CharField(max_length=500)
    result_12 = models.CharField(max_length=500)
    result_12_12 = models.CharField(max_length=500)
    result_13 = models.CharField(max_length=500)
    result_13_13 = models.CharField(max_length=500)
    result_14 = models.CharField(max_length=500)
    result_14_14 = models.CharField(max_length=500)
    result_15 = models.CharField(max_length=500)
    result_15_15 = models.CharField(max_length=500)
    result_16 = models.CharField(max_length=500)
    result_16_16 = models.CharField(max_length=500)
    result_17 = models.CharField(max_length=500)
    result_17_17 = models.CharField(max_length=500)
    result_18 = models.CharField(max_length=500)
    result_18_18 = models.CharField(max_length=500)
    result_19 = models.CharField(max_length=500)
    result_19_19 = models.CharField(max_length=500)
    result_20 = models.CharField(max_length=500)
    result_20_20 = models.CharField(max_length=500)
    result_21 = models.CharField(max_length=500)
    result_21_21 = models.CharField(max_length=500)
    result_22 = models.CharField(max_length=500)
    result_22_22 = models.CharField(max_length=500)
    result_23 = models.CharField(max_length=500)
    result_23_23 = models.CharField(max_length=500)
    result_24 = models.CharField(max_length=500)
    result_24_24 = models.CharField(max_length=500)
    result_25 = models.CharField(max_length=500)
    result_25_25 = models.CharField(max_length=500)
    result_26 = models.CharField(max_length=500)
    result_26_26 = models.CharField(max_length=500)
    result_27 = models.CharField(max_length=500)
    result_27_27 = models.CharField(max_length=500)
    result_28 = models.CharField(max_length=500)
    result_28_28 = models.CharField(max_length=500)
    result_29 = models.CharField(max_length=500)
    result_29_29 = models.CharField(max_length=500)
    result_30 = models.CharField(max_length=500)
    result_30_30 = models.CharField(max_length=500)
    result_31 = models.CharField(max_length=500)
    result_31_31 = models.CharField(max_length=500)
    result_32 = models.CharField(max_length=500)
    result_32_32 = models.CharField(max_length=500)
    legend_1 = models.CharField(max_length=500)
    legend_2 = models.CharField(max_length=500)
    legend_3 = models.CharField(max_length=500)
    legend_4 = models.CharField(max_length=500)
    legend_5 = models.CharField(max_length=500)
    legend_6 = models.CharField(max_length=500)
    legend_7 = models.CharField(max_length=500)
    legend_8 = models.CharField(max_length=500)
    legend_9 = models.CharField(max_length=500)
    legend_10 = models.CharField(max_length=500)
    legend_11 = models.CharField(max_length=500)
    editNote = models.CharField(max_length=500)
    customlegend = models.CharField(max_length=500)
    doc1 = models.CharField(max_length=500)
    doc2 = models.CharField(max_length=500)
    doc3 = models.CharField(max_length=500)
    analyzedby = models.ImageField(max_length=500)
    reviewedby = models.ImageField(max_length=500)
    approvedby = models.ImageField(max_length=500)
    approvedby1 = models.ImageField(max_length=500,null=True)
    location =models.CharField(max_length=500,null=True)
    in_out =models.CharField(max_length=500,null=True)
    inlet_result = models.CharField(max_length=500,null=True)
    extra_field = models.TextField(default=[])
    structured_data = models.TextField(default=[])
    cutomLimit1 = models.CharField(max_length=500,null=True)
    cutomLimit2 = models.CharField(max_length=500,null=True)
    cutomLimit3 = models.CharField(max_length=500,null=True)
    cutomLimit4 = models.CharField(max_length=500,null=True)
    cutomLimit5 = models.CharField(max_length=500,null=True)
    cutomLimit6 = models.CharField(max_length=500,null=True)
    cutomLimit7 = models.CharField(max_length=500,null=True)
    cutomLimit8 = models.CharField(max_length=500,null=True)
    cutomLimit9 = models.CharField(max_length=500,null=True)
    cutomLimit10 = models.CharField(max_length=500,null=True)
    cutomLimit11 = models.CharField(max_length=500,null=True)
    cutomLimit12 = models.CharField(max_length=500,null=True)
    cutomLimit13 = models.CharField(max_length=500,null=True)
    cutomLimit14 = models.CharField(max_length=500,null=True)
    cutomLimit15 = models.CharField(max_length=500,null=True)
    cutomLimit16 = models.CharField(max_length=500,null=True)
    cutomLimit17 = models.CharField(max_length=500,null=True)
    cutomLimit18 = models.CharField(max_length=500,null=True)
    cutomLimit19 = models.CharField(max_length=500,null=True)
    cutomLimit20 = models.CharField(max_length=500,null=True)
    cutomLimit21 = models.CharField(max_length=500,null=True)
    cutomLimit22 = models.CharField(max_length=500,null=True)
    cutomLimit23 = models.CharField(max_length=500,null=True)
    cutomLimit24 = models.CharField(max_length=500,null=True)
    cutomLimit25 = models.CharField(max_length=500,null=True)
    cutomLimit26 = models.CharField(max_length=500,null=True)
    cutomLimit27 = models.CharField(max_length=500,null=True)
    cutomLimit28 = models.CharField(max_length=500,null=True)
    cutomLimit29 = models.CharField(max_length=500,null=True)
    cutomLimit30 = models.CharField(max_length=500,null=True)
    cutomLimit31 = models.CharField(max_length=500,null=True)
    cutomLimit32 = models.CharField(max_length=500,null=True)
    cutomLimit33 = models.CharField(max_length=500,null=True)
    city_location =models.CharField(max_length=500,null=True)
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ww2_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no
    

class NoiseAnalysis(models.Model):
    form_name = "Noise Analysis Form"  
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_na')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_na')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_na')
    report_type = models.CharField(default="na",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    test_perf_date = models.CharField(max_length=500)
    test_type = models.CharField(max_length=500)
    test_perf_by = models.CharField(max_length=500)
    test_desc = models.CharField(max_length=500)
    select1 = models.CharField(max_length=500,null=True)
    select = models.CharField(max_length=500,null=True)
    r1 = models.CharField(max_length=500)
    r1_1 = models.CharField(max_length=500)
    r2 = models.CharField(max_length=500)
    r2_2 = models.CharField(max_length=500)
    r3 = models.CharField(max_length=500)
    r3_3 = models.CharField(max_length=500)
    r4 = models.CharField(max_length=500)
    r4_4 = models.CharField(max_length=500)
    r5 = models.CharField(max_length=500)
    r5_5 = models.CharField(max_length=500)
    r6 = models.CharField(max_length=500)
    r6_6 = models.CharField(max_length=500)
    r7 = models.CharField(max_length=500)
    r7_7 = models.CharField(max_length=500)
    r8 = models.CharField(max_length=500)
    r8_8 = models.CharField(max_length=500)
    r9 = models.CharField(max_length=500)
    r9_9 = models.CharField(max_length=500)
    r10 = models.CharField(max_length=500)
    r10_10 = models.CharField(max_length=500)
    r11 = models.CharField(max_length=500)
    r11_11 = models.CharField(max_length=500)
    r12 = models.CharField(max_length=500)
    r12_12 = models.CharField(max_length=500)
    r13 = models.CharField(max_length=500)
    r13_13 = models.CharField(max_length=500)
    legend_1 = models.CharField(max_length=500)
    legend_2 = models.CharField(max_length=500)
    legend_3 = models.CharField(max_length=500)
    legend_4 = models.CharField(max_length=500)
    legend_5 = models.CharField(max_length=500)
    legend_6 = models.CharField(max_length=500)
    legend_7 = models.CharField(max_length=500)
    legend_8 = models.CharField(max_length=500)
    legend_9 = models.CharField(max_length=500)
    legend_10 = models.CharField(max_length=500)
    legend_11 = models.CharField(max_length=500)
    editNote = models.CharField(max_length=500)
    customlegend = models.CharField(max_length=500)
    doc1 = models.CharField(max_length=500)
    doc2 = models.CharField(max_length=500)
    doc3 = models.CharField(max_length=500)
    analyzedby = models.ImageField(max_length=500)
    reviewedby = models.ImageField(max_length=500)
    approvedby = models.ImageField(max_length=500)  
    approvedby1 = models.ImageField(max_length=500,null=True)  
    location =models.CharField(max_length=500,null=True)
    city_location =models.CharField(max_length=500,null=True)
    extra_field = models.TextField(default=[])
    customer_id =models.CharField(max_length=500,null=True)
    pdf_heading = models.CharField(max_length=200,null=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="na_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no
    
    
class NoiseMonitoring(models.Model):
    form_name = "Noise Monitoring Form"  
    id = models.AutoField(primary_key=True)
    analyst_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='analyst_reports_na_mo')
    assistant_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='assistant_reports_na_mo')
    lab_manager_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='lab_manager_reports_na_mo')
    report_type = models.CharField(default="na",max_length=500)
    lab_report_no = models.CharField(max_length=500)
    invoice_bill_no = models.CharField(max_length=500)
    reporting_date = models.CharField(max_length=500)
    report_to = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    attention = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    sample_id = models.CharField(max_length=500)
    test_perf_date = models.CharField(max_length=500)
    test_type = models.CharField(max_length=500)
    test_perf_by = models.CharField(max_length=500)
    test_desc = models.CharField(max_length=500)
    select1 = models.CharField(max_length=500,null=True)
    select = models.CharField(max_length=500,null=True)
    test_method = models.CharField(max_length=500,null=True)
    test_location = models.CharField(max_length=500,null=True)
    GRAPH_CHOICES = [
        ('line', 'Line Graph'),
        ('column', 'Column Graph'),
    ]

    graph_type = models.CharField(
        max_length=10,
        choices=GRAPH_CHOICES,
        default='line',
        null=True,
        blank=True
    )
    times = models.JSONField(default=list,null=True,blank=True)   # e.g. ["09:00 AM", "10:00 AM", ...]
    units = models.JSONField(default=list,null=True,blank=True)   # e.g. ["mg/L", "ppm", ...]
    results = models.JSONField(default=list,null=True,blank=True) # e.g. ["45", "52", ...]
    table_data = models.JSONField(default=list,null=True,blank=True) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.CharField(null=True,blank=True,max_length=20)
    legend_1 = models.CharField(null=True,blank=True,max_length=500)
    legend_2 = models.CharField(null=True,blank=True,max_length=500)
    legend_3 = models.CharField(null=True,blank=True,max_length=500)
    legend_4 = models.CharField(null=True,blank=True,max_length=500)
    legend_5 = models.CharField(null=True,blank=True,max_length=500)
    legend_6 = models.CharField(null=True,blank=True,max_length=500)
    legend_7 = models.CharField(null=True,blank=True,max_length=500)
    legend_8 = models.CharField(null=True,blank=True,max_length=500)
    legend_9 = models.CharField(null=True,blank=True,max_length=500)
    legend_10 = models.CharField(null=True,blank=True,max_length=500)
    legend_11 = models.CharField(null=True,blank=True,max_length=500)
    editNote = models.CharField(null=True,blank=True,max_length=500)
    customlegend = models.CharField(null=True,blank=True,max_length=500)
    doc1 = models.CharField(null=True,blank=True,max_length=500)
    doc2 = models.CharField(null=True,blank=True,max_length=500)
    doc3 = models.CharField(null=True,blank=True,max_length=500)
    analyzedby = models.ImageField(null=True,blank=True,max_length=500)
    reviewedby = models.ImageField(null=True,blank=True,max_length=500)
    approvedby = models.ImageField(null=True,blank=True,max_length=500)  
    approvedby1 = models.ImageField(max_length=500,null=True,blank=True)  
    location =models.CharField(max_length=500,null=True,blank=True)
    city_location =models.CharField(max_length=500,null=True,blank=True)
    extra_field = models.TextField(default=[],null=True,blank=True)
    customer_id =models.CharField(max_length=500,null=True,blank=True)
    pdf_heading = models.CharField(max_length=200,null=True,blank=True)
    pdf_image_1 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_1 = models.TextField(null=True,blank=True)
    pdf_image_2 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_2 = models.TextField(null=True,blank=True)
    pdf_image_3 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_3 = models.TextField(null=True,blank=True)
    pdf_image_4 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_4 = models.TextField(null=True,blank=True)
    pdf_image_5 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_5 = models.TextField(null=True,blank=True)
    pdf_image_6 = models.TextField(null=True,blank=True)  # base64 string
    pdf_desc_6 = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="na_mo_reports_created")
    industry = models.ForeignKey(Industry_sector,on_delete=models.SET_NULL,null=True,blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['reporting_date']),
            models.Index(fields=['report_to']),
            models.Index(fields=['sample_id']),
            models.Index(fields=['city_location']),
            models.Index(fields=['lab_report_no']),
        ]
    
    
    def __str__(self):
        return self.form_name +" - "+ self.lab_report_no
    

class Calibration(models.Model):
    id = models.AutoField(primary_key=True,)
    cert_type = models.CharField(default="calib",max_length=500,null=True)
    city_location = models.CharField(max_length=200,null=True,default="")
    cert_num = models.CharField(max_length=200,null=True,default="")
    client = models.CharField(max_length=200,null=True,default="")
    contact_person = models.CharField(max_length=200,null=True,default="")
    address = models.CharField(max_length=200,null=True,default="")
    date = models.CharField(max_length=200,null=True,default="")
    calib_perf_at = models.CharField(max_length=200,null=True,default="")
    re_calib_perf_at = models.CharField(max_length=200,null=True,default="")
    cert_issue_date = models.CharField(max_length=200,null=True,default="")
    equipment = models.CharField(max_length=200,null=True,default="")
    manufacturer = models.CharField(max_length=200,null=True,default="")
    cond_item = models.CharField(max_length=200,null=True,default="")
    client_id = models.CharField(max_length=200,null=True,default="")
    model = models.CharField(max_length=200,null=True,default="")
    location = models.CharField(max_length=200,null=True,default="")
    param = models.CharField(max_length=200,null=True,default="")
    range = models.CharField(max_length=200,null=True,default="")
    serial_no = models.CharField(max_length=200,null=True,default="")
    tolerance = models.CharField(max_length=200,null=True,default="")
    equipment_1 = models.CharField(max_length=200,null=True,default="")
    model_1 = models.CharField(max_length=200,null=True,default="")
    serial_no1 = models.CharField(max_length=200,null=True,default="")
    cert_num1 = models.CharField(max_length=200,null=True,default="")
    traceability = models.CharField(max_length=200,null=True,default="")
    procedure = models.CharField(max_length=200,null=True,default="")
    method = models.CharField(max_length=200,null=True,default="")
    sindh_wm = models.CharField(max_length=200,null=True,default="")
    test1 = models.CharField(max_length=200,null=True,default="")
    test2 = models.CharField(max_length=200,null=True,default="")
    weight1 = models.CharField(max_length=200,null=True,default="")
    set_val_head_1 = models.CharField(max_length=200,null=True,default="")
    master_read_head_1 = models.CharField(max_length=200,null=True,default="")
    actual_read_head_1 = models.CharField(max_length=200,null=True,default="")
    deviation_head_1 = models.CharField(max_length=200,null=True,default="")
    before_head_1 = models.CharField(max_length=200,null=True,default="")
    after_head_1 = models.CharField(max_length=200,null=True,default="")
    
    set_val_head_2 = models.CharField(max_length=200,null=True,default="")
    master_read_head_2 = models.CharField(max_length=200,null=True,default="")
    actual_read_head_2 = models.CharField(max_length=200,null=True,default="")
    deviation_head_2 = models.CharField(max_length=200,null=True,default="")
    before_head_2 = models.CharField(max_length=200,null=True,default="")
    after_head_2 = models.CharField(max_length=200,null=True,default="")
    
    kg1 = models.CharField(max_length=200,null=True,default="")
    kg2 = models.CharField(max_length=200,null=True,default="")
    kg3 = models.CharField(max_length=200,null=True,default="")
    set1 = models.CharField(max_length=200,null=True,default="")
    master1 = models.CharField(max_length=200,null=True,default="")
    before1 = models.CharField(max_length=200,null=True,default="")
    after1 = models.CharField(max_length=200,null=True,default="")
    dev1 = models.CharField(max_length=200,null=True,default="")
    set2 = models.CharField(max_length=200,null=True,default="")
    master2 = models.CharField(max_length=200,null=True,default="")
    before2 = models.CharField(max_length=200,null=True,default="")
    after2 = models.CharField(max_length=200,null=True,default="")
    dev2 = models.CharField(max_length=200,null=True,default="")
    set3 = models.CharField(max_length=200,null=True,default="")
    master3 = models.CharField(max_length=200,null=True,default="")
    before3 = models.CharField(max_length=200,null=True,default="")
    after3 = models.CharField(max_length=200,null=True,default="")
    dev3 = models.CharField(max_length=200,null=True,default="")
    set4 = models.CharField(max_length=200,null=True,default="")
    master4 = models.CharField(max_length=200,null=True,default="")
    before4 = models.CharField(max_length=200,null=True,default="")
    after4 = models.CharField(max_length=200,null=True,default="")
    dev4 = models.CharField(max_length=200,null=True,default="")
    weight2 = models.CharField(max_length=200,null=True,default="")
    kg1_1 = models.CharField(max_length=200,null=True,default="")
    kg2_2 = models.CharField(max_length=200,null=True,default="")
    kg3_3 = models.CharField(max_length=200,null=True,default="")
    set1_1 = models.CharField(max_length=200,null=True,default="")
    master1_1 = models.CharField(max_length=200,null=True,default="")
    before1_1 = models.CharField(max_length=200,null=True,default="")
    after1_1 = models.CharField(max_length=200,null=True,default="")
    dev1_1 = models.CharField(max_length=200,null=True,default="")
    set2_2 = models.CharField(max_length=200,null=True,default="")
    master2_2 = models.CharField(max_length=200,null=True,default="")
    before2_2 = models.CharField(max_length=200,null=True,default="")
    after2_2 = models.CharField(max_length=200,null=True,default="")
    dev2_2 = models.CharField(max_length=200,null=True,default="")
    set3_3 = models.CharField(max_length=200,null=True,default="")
    master3_3 = models.CharField(max_length=200,null=True,default="")
    before3_3 = models.CharField(max_length=200,null=True,default="")
    after3_3 = models.CharField(max_length=200,null=True,default="")
    dev3_3 = models.CharField(max_length=200,null=True,default="")
    set4_4 = models.CharField(max_length=200,null=True,default="")
    master4_4 = models.CharField(max_length=200,null=True,default="")
    before4_4 = models.CharField(max_length=200,null=True,default="")
    after4_4 = models.CharField(max_length=200,null=True,default="")
    dev4_4 = models.CharField(max_length=200,null=True,default="")
    calib_status = models.CharField(max_length=200,null=True,default="")
    max_error = models.CharField(max_length=200,null=True,default="")
    text = models.CharField(max_length=1000,null=True,default="")
    calib_by_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='calib')
    checked_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='calib_check')
    checked1_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='calib_check1')
    calib_by = models.ImageField(max_length=500,null=True,default="")
    checked = models.ImageField(max_length=500,null=True,default="")
    checked1 = models.ImageField(max_length=500,null=True,default="")
    disc = models.CharField(max_length=1000,null=True,default="")
    extra_field = models.TextField(default=[],null=True,)
    extra_field1 = models.TextField(default=[],null=True,)
    extra_field2 = models.TextField(default=[],null=True,)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cl_cert_created")
    


class Inspection(models.Model):
    id = models.AutoField(primary_key=True)
    cert_type = models.CharField(default="insp",max_length=500)
    city_location = models.CharField(max_length=200,null=True)
    cert_num = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    re_insp_date = models.CharField(max_length=200,null=True)
    client_equip_data = models.CharField(max_length=200,null=True)
    equipment = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    equip_id = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    master_equip = models.CharField(max_length=200,null=True)
    equipment_1 = models.CharField(max_length=200)
    model_1 = models.CharField(max_length=200)
    serial_no1 = models.CharField(max_length=200)
    cert_num1 = models.CharField(max_length=200)
    physical_inspect = models.CharField(max_length=200,null=True)
    test1 = models.CharField(max_length=200,null=True)
    test2 = models.CharField(max_length=200,null=True)
    test3 = models.CharField(max_length=200,null=True)
    test4 = models.CharField(max_length=200,null=True)
    test5 = models.CharField(max_length=200,null=True)
    test6 = models.CharField(max_length=200,null=True)
    test7 = models.CharField(max_length=200,null=True)
    test8 = models.CharField(max_length=200,null=True)
    test9 = models.CharField(max_length=200,null=True)
    test10 = models.CharField(max_length=200,null=True)
    conc = models.CharField(max_length=200,null=True)
    insp_status = models.CharField(max_length=200,null=True)
    text = models.CharField(max_length=200,null=True)
    ispect_by_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='inspect')
    check_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='inspect_check')
    check1_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='inspect_check1')
    calib_by = models.ImageField(max_length=500,null=True)
    checked = models.ImageField(max_length=500,null=True)
    checked1 = models.ImageField(max_length=500,null=True)
    disc = models.CharField(max_length=200,null=True)

    client_date_table = models.CharField(max_length=200,null=True,blank=True)
    client_equipment = models.CharField(max_length=200,null=True,blank=True)
    client_equipment_1 = models.CharField(max_length=200,null=True,blank=True)
    client_manufacturer = models.CharField(max_length=200,null=True,blank=True)
    client_manufacturer_1 = models.CharField(max_length=200,null=True,blank=True)
    client_equip_id = models.CharField(max_length=200,null=True,blank=True)
    client_equip_id_1 = models.CharField(max_length=200,null=True,blank=True)
    client_model = models.CharField(max_length=200,null=True,blank=True)
    client_model_1 = models.CharField(max_length=200,null=True,blank=True)
    client_location = models.CharField(max_length=200,null=True,blank=True)
    client_location_1 = models.CharField(max_length=200,null=True,blank=True)
    client_param = models.CharField(max_length=200,null=True,blank=True)
    client_param_1 = models.CharField(max_length=200,null=True,blank=True)
    client_range = models.CharField(max_length=200,null=True,blank=True)
    client_range_1 = models.CharField(max_length=200,null=True,blank=True)
    client_tolerance = models.CharField(max_length=200,null=True,blank=True)
    client_tolerance_1 = models.CharField(max_length=200,null=True,blank=True)
    param_1 = models.CharField(max_length=200,null=True,blank=True)
    result_1 = models.CharField(max_length=200,null=True,blank=True)
    load_cond = models.CharField(max_length=200,null=True,blank=True)
    param_2 = models.CharField(max_length=200,null=True,blank=True)
    result_2 = models.CharField(max_length=200,null=True,blank=True)
    temp_1 = models.CharField(max_length=200,null=True,blank=True)
    temp_2 = models.CharField(max_length=200,null=True,blank=True)
    humidity_1 = models.CharField(max_length=200,null=True,blank=True)
    humidity_2 = models.CharField(max_length=200,null=True,blank=True)
    forklift_table = models.CharField(max_length=200,null=True,blank=True)
    kg1 = models.CharField(max_length=200,null=True,blank=True)
    ft_1 = models.CharField(max_length=200,null=True,blank=True)
    ft_2 = models.CharField(max_length=200,null=True,blank=True)
    ft_3 = models.CharField(max_length=200,null=True,blank=True)
    ft_4 = models.CharField(max_length=200,null=True,blank=True)
    ft_5 = models.CharField(max_length=200,null=True,blank=True)
    weight1 = models.CharField(max_length=200,null=True,blank=True)
    set1 = models.CharField(max_length=200,null=True,blank=True)
    master1 = models.CharField(max_length=200,null=True,blank=True)
    before1 = models.CharField(max_length=200,null=True,blank=True)
    after1 = models.CharField(max_length=200,null=True,blank=True)
    dev1 = models.CharField(max_length=200,null=True,blank=True)
    weight2 = models.CharField(max_length=200,null=True,blank=True)
    set2 = models.CharField(max_length=200,null=True,blank=True)
    master2 = models.CharField(max_length=200,null=True,blank=True)
    before2 = models.CharField(max_length=200,null=True,blank=True)
    after2 = models.CharField(max_length=200,null=True,blank=True)
    dev2 = models.CharField(max_length=200,null=True,blank=True)
    weight3 = models.CharField(max_length=200,null=True,blank=True)
    set3 = models.CharField(max_length=200,null=True,blank=True)
    master3 = models.CharField(max_length=200,null=True,blank=True)
    before3 = models.CharField(max_length=200,null=True,blank=True)
    after3 = models.CharField(max_length=200,null=True,blank=True)
    dev3 = models.CharField(max_length=200,null=True,blank=True)
    weight4 = models.CharField(max_length=200,null=True,blank=True)
    set4 = models.CharField(max_length=200,null=True,blank=True)
    master4 = models.CharField(max_length=200,null=True,blank=True)
    before4 = models.CharField(max_length=200,null=True,blank=True)
    after4 = models.CharField(max_length=200,null=True,blank=True)
    dev4 = models.CharField(max_length=200,null=True,blank=True)
    knife_table = models.CharField(max_length=200,null=True,blank=True)
    rpm1 = models.CharField(max_length=200,null=True,blank=True)
    rpm2 = models.CharField(max_length=200,null=True,blank=True)
    rpm3 = models.CharField(max_length=200,null=True,blank=True)
    knife_Set_value1 = models.CharField(max_length=200,null=True,blank=True)
    knife_master1 = models.CharField(max_length=200,null=True,blank=True)
    knife_before1 = models.CharField(max_length=200,null=True,blank=True)
    knife_after1 = models.CharField(max_length=200,null=True,blank=True)
    knife_dev1 = models.CharField(max_length=200,null=True,blank=True)
    knife_Set_value2 = models.CharField(max_length=200,null=True,blank=True)
    knife_master2 = models.CharField(max_length=200,null=True,blank=True)
    knife_before2 = models.CharField(max_length=200,null=True,blank=True)
    knife_after2 = models.CharField(max_length=200,null=True,blank=True)
    knife_dev2 = models.CharField(max_length=200,null=True,blank=True)
    knife_Set_value3 = models.CharField(max_length=200,null=True,blank=True)
    knife_master3 = models.CharField(max_length=200,null=True,blank=True)
    knife_before3 = models.CharField(max_length=200,null=True,blank=True)
    knife_after3 = models.CharField(max_length=200,null=True,blank=True)
    knife_dev3 = models.CharField(max_length=200,null=True,blank=True)
    knife_Set_value4 = models.CharField(max_length=200,null=True,blank=True)
    knife_master4 = models.CharField(max_length=200,null=True,blank=True)
    knife_before4 = models.CharField(max_length=200,null=True,blank=True)
    knife_after4 = models.CharField(max_length=200,null=True,blank=True)
    knife_dev4 = models.CharField(max_length=200,null=True,blank=True)
    knife_Set_value5 = models.CharField(max_length=200,null=True,blank=True)
    knife_master5 = models.CharField(max_length=200,null=True,blank=True)
    knife_before5 = models.CharField(max_length=200,null=True,blank=True)
    knife_after5 = models.CharField(max_length=200,null=True,blank=True)
    knife_dev5 = models.CharField(max_length=200,null=True,blank=True)
    
    
    extra_field = models.TextField(default=[])
    extra_field1 = models.TextField(default=[])
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="insp_cert_created")
    def __str__(self):
        return self.cert_num



class Verification(models.Model):
    id = models.AutoField(primary_key=True)
    cert_type = models.CharField(default="verif",max_length=500)
    city_location = models.CharField(max_length=200,null=True)
    cert_num = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    re_verif_date = models.CharField(max_length=200)
    param1 = models.CharField(max_length=200)
    param = models.CharField(max_length=200)
    equipment = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    equip_id = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    equipment_1 = models.CharField(max_length=200)
    model_1 = models.CharField(max_length=200)
    serial_no1 = models.CharField(max_length=200)
    cert_num1 = models.CharField(max_length=200)
    equipment_2 = models.CharField(max_length=200)
    model_2 = models.CharField(max_length=200)
    serial_no2 = models.CharField(max_length=200)
    cert_num2 = models.CharField(max_length=200)
    test1 = models.CharField(max_length=200)
    test2 = models.CharField(max_length=200)

    test_1 = models.CharField(max_length=200)
    equip_des1 = models.CharField(max_length=200)
    obser1 = models.CharField(max_length=200)
    dev1 = models.CharField(max_length=500)

    test_2 = models.CharField(max_length=200)
    equip_des2 = models.CharField(max_length=200)
    obser2 = models.CharField(max_length=200)
    dev2 = models.CharField(max_length=500)

    test_3 = models.CharField(max_length=200)
    equip_des3 = models.CharField(max_length=200)
    obser3 = models.CharField(max_length=200)
    dev3 = models.CharField(max_length=500)

    test_4 = models.CharField(max_length=200)
    equip_des4 = models.CharField(max_length=200)
    obser4 = models.CharField(max_length=200)
    dev4 = models.CharField(max_length=500)


    
    test_5 = models.CharField(max_length=200)
    equip_des5 = models.CharField(max_length=200)
    obser5 = models.CharField(max_length=200)
    dev5 = models.CharField(max_length=500)

    test_6 = models.CharField(max_length=200)
    equip_des6 = models.CharField(max_length=200)
    obser6 = models.CharField(max_length=200)
    dev6 = models.CharField(max_length=500)

    test_7 = models.CharField(max_length=200)
    equip_des7 = models.CharField(max_length=200)
    obser7 = models.CharField(max_length=200)
    dev7 = models.CharField(max_length=500)
    conc =  models.CharField(max_length=500)
    verif_status =  models.CharField(max_length=500)
    text =  models.CharField(max_length=500)
    verif_by_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='verif')
    check_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='verif_check')
    check1_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='verif_check1')
    verif_by = models.ImageField(max_length=500)
    checked = models.ImageField(max_length=500)
    checked1 = models.ImageField(max_length=500)
    disc = models.CharField(max_length=200)
    extra_field = models.TextField(default=[])
    extra_field1 = models.TextField(default=[])
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="verif_cert_created")


class Customer(models.Model):
    sampleId = models.CharField(max_length=500)
    client_name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    name_of_person = models.CharField(max_length=500)
    contact_detail = models.CharField(max_length=500)
    nature_of_sample = models.CharField(max_length=500)
    recieving_date = models.CharField(max_length=500)
    expected_reported  = models.CharField(max_length=500)
    recieved_by = models.CharField(max_length=500)


class Sample_registration(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=500,null=True,blank=True)
    city_location = models.CharField(max_length=500,null=True,blank=True)
    lab_no = models.CharField(max_length=500,null=True,blank=True)
    issue_date = models.CharField(max_length=500,null=True,blank=True)
    issue_no = models.CharField(max_length=500,null=True,blank=True)
    sample_id = models.CharField(max_length=500,null=True,blank=True)
    checkinp_chemical = models.BooleanField(default=False)
    checkinp_bacteria = models.BooleanField(default=False)
    inp1 = models.CharField(max_length=500,null=True,blank=True)
    inp2 = models.CharField(max_length=500,null=True,blank=True)
    inp3 = models.CharField(max_length=500,null=True,blank=True)
    inp4 = models.CharField(max_length=500,null=True,blank=True)
    inp5 = models.CharField(max_length=500,null=True,blank=True)
    inp6 = models.CharField(max_length=500,null=True,blank=True)
    inp7 = models.CharField(max_length=500,null=True,blank=True)
    inp8 = models.CharField(max_length=500,null=True,blank=True)
    inp9 = models.CharField(max_length=500,null=True,blank=True)
    inp10 = models.CharField(max_length=500,null=True,blank=True)
    checkinp11 = models.BooleanField(default=False)
    checkinp12 = models.BooleanField(default=False)
    checkinp13 = models.BooleanField(default=False)
    checkinp14 = models.BooleanField(default=False)
    checkinp15 = models.BooleanField(default=False)
    checkinp16 = models.BooleanField(default=False)
    checkinp17 = models.BooleanField(default=False)
    checkinp18 = models.BooleanField(default=False)
    inp19 = models.CharField(max_length=500,null=True,blank=True)
    inp20 = models.CharField(max_length=500,null=True,blank=True)
    checkinp21 = models.BooleanField(default=False)
    checkinp22 = models.BooleanField(default=False)
    checkinp23 = models.BooleanField(default=False)
    checkinp24 = models.BooleanField(default=False)
    checkinp25 = models.BooleanField(default=False)
    checkinp26 = models.BooleanField(default=False)
    checkinp27 = models.BooleanField(default=False)
    checkinp28 = models.BooleanField(default=False)
    checkinp29 = models.BooleanField(default=False)
    checkinp30 = models.BooleanField(default=False)
    checkinp31 = models.BooleanField(default=False)
    checkinp32 = models.BooleanField(default=False)
    checkinp33 = models.BooleanField(default=False)
    checkinp34 = models.BooleanField(default=False)
    checkinp35 = models.BooleanField(default=False)
    checkinp36 = models.BooleanField(default=False)
    checkinp37 = models.BooleanField(default=False)
    checkinp38 = models.BooleanField(default=False)
    checkinp39 = models.BooleanField(default=False)
    checkinp40 = models.BooleanField(default=False)
    checkinp41 = models.BooleanField(default=False)
    checkinp42 = models.BooleanField(default=False)
    checkinp43 = models.BooleanField(default=False)
    checkinp44 = models.BooleanField(default=False)
    checkinp45 = models.BooleanField(default=False)
    checkinp46 = models.BooleanField(default=False)
    checkinp47 = models.BooleanField(default=False)
    checkinp48 = models.BooleanField(default=False)
    checkinp49 = models.BooleanField(default=False)
    checkinp50 = models.BooleanField(default=False)
    checkinp51 = models.BooleanField(default=False)
    checkinp52 = models.BooleanField(default=False)
    checkinp53 = models.BooleanField(default=False)
    checkinp54 = models.BooleanField(default=False)
    checkinp55 = models.BooleanField(default=False)
    checkinp56 = models.BooleanField(default=False)
    checkinp57 = models.BooleanField(default=False)
    checkinp58 = models.BooleanField(default=False)
    checkinp59 = models.BooleanField(default=False)
    checkinp60 = models.BooleanField(default=False)
    checkinp61 = models.BooleanField(default=False)
    checkinp62 = models.BooleanField(default=False)
    checkinp63 = models.BooleanField(default=False)
    checkinp64 = models.BooleanField(default=False)
    checkinp65 = models.BooleanField(default=False)
    checkinp66 = models.BooleanField(default=False)
    checkinp67 = models.BooleanField(default=False)
    checkinp68 = models.BooleanField(default=False)
    checkinp69 = models.BooleanField(default=False)
    checkinp70 = models.BooleanField(default=False)
    checkinp71 = models.BooleanField(default=False)
    checkinp72 = models.BooleanField(default=False)
    checkinp73 = models.BooleanField(default=False)
    checkinp74 = models.BooleanField(default=False)
    checkinp75 = models.BooleanField(default=False)
    checkinp76 = models.BooleanField(default=False)
    checkinp77 = models.BooleanField(default=False)
    checkinp78 = models.BooleanField(default=False)
    checkinp79 = models.BooleanField(default=False)
    checkinp80 = models.BooleanField(default=False)
    checkinp81 = models.BooleanField(default=False)
    checkinp82 = models.BooleanField(default=False)
    checkinp83 = models.BooleanField(default=False)
    checkinp84 = models.BooleanField(default=False)
    checkinp85 = models.BooleanField(default=False)
    checkinp86 = models.BooleanField(default=False)
    checkinp87 = models.BooleanField(default=False)
    checkinp88 = models.BooleanField(default=False)
    checkinp89 = models.BooleanField(default=False)
    checkinp90 = models.BooleanField(default=False)
    checkinp91 = models.BooleanField(default=False)
    checkinp92 = models.BooleanField(default=False)
    checkinp93 = models.BooleanField(default=False)
    checkinp94 = models.BooleanField(default=False)
    checkinp95 = models.BooleanField(default=False)
    checkinp96 = models.BooleanField(default=False)
    checkinp97 = models.BooleanField(default=False)
    checkinp98 = models.BooleanField(default=False)
    checkinp99 = models.BooleanField(default=False)
    checkinp100 =models.BooleanField(default=False)
    checkinp101 =models.BooleanField(default=False)
    checkinp102 =models.BooleanField(default=False)
    checkinp103 =models.BooleanField(default=False)
    checkinp104 =models.BooleanField(default=False)
    checkinp105 =models.BooleanField(default=False)
    other1 =models.CharField(max_length=500,null=True,blank=True,default="")
    other2 =models.CharField(max_length=500,null=True,blank=True,default="")
    
    inp106 = models.CharField(max_length=500,null=True,blank=True)
    checkinp107 = models.BooleanField(default=False)
    checkinp108 = models.BooleanField(default=False)
    inp109 = models.CharField(max_length=500,null=True,blank=True)
    checkinp110 = models.BooleanField(default=False)
    checkinp111 = models.BooleanField(default=False)
    inp112 = models.CharField(max_length=500,null=True,blank=True)
    checkinp113 = models.BooleanField(default=False)
    checkinp114 = models.BooleanField(default=False)
    inp115 = models.CharField(max_length=500,null=True,blank=True)
    checkinp116 = models.BooleanField(default=False)
    checkinp117 = models.BooleanField(default=False)
    
    other_param_1 = models.BooleanField(default=False, blank=True)
    other_param_2 = models.BooleanField(default=False, blank=True)
    other_param_3 = models.BooleanField(default=False, blank=True)
    other_param_4 = models.BooleanField(default=False, blank=True)
    other_param_5 = models.BooleanField(default=False, blank=True)
    other_param_6 = models.BooleanField(default=False, blank=True)
    other_param_7 = models.BooleanField(default=False, blank=True)
    other_param_8 = models.BooleanField(default=False, blank=True)
    other_param_9 = models.BooleanField(default=False, blank=True)
    other_param_10 = models.BooleanField(default=False, blank=True)
    other_param_11 = models.BooleanField(default=False, blank=True)
    other_param_12 = models.BooleanField(default=False, blank=True)
    other_param_13 = models.BooleanField(default=False, blank=True)
    other_param_14 = models.BooleanField(default=False, blank=True)
    other_param_15 = models.BooleanField(default=False, blank=True)
    other_param_16 = models.BooleanField(default=False, blank=True)
    other_param_17 = models.BooleanField(default=False, blank=True)
    other_param_18 = models.BooleanField(default=False, blank=True)
    other_param_19 = models.BooleanField(default=False, blank=True)
    other_param_20 = models.BooleanField(default=False, blank=True)
    other_param_21 = models.BooleanField(default=False, blank=True)
    other_param_22 = models.BooleanField(default=False, blank=True)
    other_param_23 = models.BooleanField(default=False, blank=True)
    other_param_24 = models.BooleanField(default=False, blank=True)
    other_param_25 = models.BooleanField(default=False, blank=True)
    other_param_26 = models.BooleanField(default=False, blank=True)
    other_param_27 = models.BooleanField(default=False, blank=True)
    other_param_28 = models.BooleanField(default=False, blank=True)
    other_param_29 = models.BooleanField(default=False, blank=True)
    other_param_30 = models.BooleanField(default=False, blank=True)
    other_param_31 = models.BooleanField(default=False, blank=True)
    other_param_32 = models.BooleanField(default=False, blank=True)
    other_param_33 = models.BooleanField(default=False, blank=True)
    other_param_34 = models.BooleanField(default=False, blank=True)
    other_param_35 = models.BooleanField(default=False, blank=True)
    other_param_36 = models.BooleanField(default=False, blank=True)
    other_param_37 = models.BooleanField(default=False, blank=True)
    other_param_38 = models.BooleanField(default=False, blank=True)
    other_param_39 = models.BooleanField(default=False, blank=True)
    other_param_40 = models.BooleanField(default=False, blank=True)
    other_param_41 = models.BooleanField(default=False, blank=True)
    other_param_42 = models.BooleanField(default=False, blank=True)
    other_param_43 = models.BooleanField(default=False, blank=True)
    other_param_44 = models.BooleanField(default=False, blank=True)
    other_param_45 = models.BooleanField(default=False, blank=True)
    other_param_46 = models.BooleanField(default=False, blank=True)
    other_param_47 = models.BooleanField(default=False, blank=True)
    other_param_48 = models.BooleanField(default=False, blank=True)
    other_param_49 = models.BooleanField(default=False, blank=True)
    other_param_50 = models.BooleanField(default=False, blank=True)
    other_param_51 = models.BooleanField(default=False, blank=True)
    other_param_52 = models.BooleanField(default=False, blank=True)
    other_param_53 = models.BooleanField(default=False, blank=True)
    other_param_54 = models.BooleanField(default=False, blank=True)
    other_param_55 = models.BooleanField(default=False, blank=True)
    other_param_56 = models.BooleanField(default=False, blank=True)
    other_param_57 = models.BooleanField(default=False, blank=True)
    other_param_58 = models.BooleanField(default=False, blank=True)
    other_param_59 = models.BooleanField(default=False, blank=True)
    other_param_60 = models.BooleanField(default=False, blank=True)
    other_param_61 = models.BooleanField(default=False, blank=True)
    other_param_62 = models.BooleanField(default=False, blank=True)
    other_param_63 = models.BooleanField(default=False, blank=True)
    other_param_64 = models.BooleanField(default=False, blank=True)
    other_param_65 = models.BooleanField(default=False, blank=True)
    other_param_66 = models.BooleanField(default=False, blank=True)
    
        # Wastewater Parameters
    ww_other_param_1 = models.BooleanField(default=False, blank=True)   # Temperature
    ww_other_param_2 = models.BooleanField(default=False, blank=True)   # Colour
    ww_other_param_3 = models.BooleanField(default=False, blank=True)   # Odour
    ww_other_param_4 = models.BooleanField(default=False, blank=True)   # Turbidity
    ww_other_param_5 = models.BooleanField(default=False, blank=True)   # Calcium
    ww_other_param_6 = models.BooleanField(default=False, blank=True)   # Sodium
    ww_other_param_7 = models.BooleanField(default=False, blank=True)   # Magnesium
    ww_other_param_8 = models.BooleanField(default=False, blank=True)   # Potassium
    ww_other_param_9 = models.BooleanField(default=False, blank=True)   # Silica
    ww_other_param_10 = models.BooleanField(default=False, blank=True)  # Reactive Silica
    ww_other_param_11 = models.BooleanField(default=False, blank=True)  # Alkalinity
    ww_other_param_12 = models.BooleanField(default=False, blank=True)  # Ammonium
    ww_other_param_13 = models.BooleanField(default=False, blank=True)  # Carbonates
    ww_other_param_14 = models.BooleanField(default=False, blank=True)  # Bicarbonates
    ww_other_param_15 = models.BooleanField(default=False, blank=True)  # Conductivity
    ww_other_param_16 = models.BooleanField(default=False, blank=True)  # Salinity
    ww_other_param_17 = models.BooleanField(default=False, blank=True)  # Resistivity
    ww_other_param_18 = models.BooleanField(default=False, blank=True)  # Total Solid
    ww_other_param_19 = models.BooleanField(default=False, blank=True)  # Acidity
    ww_other_param_20 = models.BooleanField(default=False, blank=True)  # Total Hardness
    ww_other_param_21 = models.BooleanField(default=False, blank=True)  # Calcium Hardness
    ww_other_param_22 = models.BooleanField(default=False, blank=True)  # Magnesium Hardness
    ww_other_param_23 = models.BooleanField(default=False, blank=True)  # Carbonate Hardness
    ww_other_param_24 = models.BooleanField(default=False, blank=True)  # Non-Carbonate Hardness
    ww_other_param_25 = models.BooleanField(default=False, blank=True)  # Temporary Hardness
    ww_other_param_26 = models.BooleanField(default=False, blank=True)  # Strontium
    ww_other_param_27 = models.BooleanField(default=False, blank=True)  # Cobalt
    ww_other_param_28 = models.BooleanField(default=False, blank=True)  # Aluminium (Al)
    ww_other_param_29 = models.BooleanField(default=False, blank=True)  # Chromium III
    ww_other_param_30 = models.BooleanField(default=False, blank=True)  # Chromium VI
    ww_other_param_31 = models.BooleanField(default=False, blank=True)  # Ferrous (Fe+2)
    ww_other_param_32 = models.BooleanField(default=False, blank=True)  # Ferric (Fe+3)
    ww_other_param_33 = models.BooleanField(default=False, blank=True)  # Tin (Sn)
    ww_other_param_34 = models.BooleanField(default=False, blank=True)  # Beryllium
    ww_other_param_35 = models.BooleanField(default=False, blank=True)  # Free CO2
    ww_other_param_36 = models.BooleanField(default=False, blank=True)  # Hydroxide Alkalinity as CaCO3
    ww_other_param_37 = models.BooleanField(default=False, blank=True)  # Methyl Orange Alkalinity as CaCO3
    ww_other_param_38 = models.BooleanField(default=False, blank=True)  # Phenolphthalein Alkalinity as CaCO3
    ww_other_param_39 = models.BooleanField(default=False, blank=True)  # Particulate Matter
    ww_other_param_40 = models.BooleanField(default=False, blank=True)  # Silt Density Index (SDI)
    ww_other_param_41 = models.BooleanField(default=False, blank=True)  # Particles Size
    ww_other_param_42 = models.BooleanField(default=False, blank=True)  # AOx
    ww_other_param_43 = models.BooleanField(default=False, blank=True)  # Free Chlorine
    ww_other_param_44 = models.BooleanField(default=False, blank=True)  # Residual Chlorine
    ww_other_param_45 = models.BooleanField(default=False, blank=True)  # Persistent Foam
    ww_other_param_46 = models.BooleanField(default=False, blank=True)  # Flow rate
    ww_other_param_47 = models.BooleanField(default=False, blank=True)  # Phosphate
    ww_other_param_48 = models.BooleanField(default=False, blank=True)  # Nitrate
    ww_other_param_49 = models.BooleanField(default=False, blank=True)  # Nitrite
    ww_other_param_50 = models.BooleanField(default=False, blank=True)  # Volatile Suspended Solids (VSS)
    ww_other_param_51 = models.BooleanField(default=False, blank=True)  # Settleable solids (Imhoff cone)
    ww_other_param_52 = models.BooleanField(default=False, blank=True)  # Oxidation–Reduction Potential (ORP)
    ww_other_param_53 = models.BooleanField(default=False, blank=True)  # Volatile Organic Halogens (VOX)
    ww_other_param_54 = models.BooleanField(default=False, blank=True)  # Sodium Adsorption Ratio (SAR)
    ww_other_param_55 = models.BooleanField(default=False, blank=True)  # Residual Sodium Carbonate (RSC)
    ww_other_param_56 = models.BooleanField(default=False, blank=True)  # Total Plate Count
    ww_other_param_57 = models.BooleanField(default=False, blank=True)  # E. Coli
    ww_other_param_58 = models.BooleanField(default=False, blank=True)  # Faecal Coliform
    ww_other_param_59 = models.BooleanField(default=False, blank=True)  # Faecal Enterococci
    ww_other_param_60 = models.BooleanField(default=False, blank=True)  # Total Bacterial Count
    ww_other_param_61 = models.BooleanField(default=False, blank=True)  # Legionella
    ww_other_param_62 = models.BooleanField(default=False, blank=True)  # Pseudomonas aeruginosa
    ww_other_param_63 = models.BooleanField(default=False, blank=True)  # Bioassay Test
    ww_other_param_64 = models.BooleanField(default=False, blank=True)  

    auth_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='auth')
    sampling_by_signature = models.ForeignKey(Signatures, on_delete=models.SET_NULL, null=True, related_name='sampling_by')
    auth_sign = models.ImageField()
    sampling_by = models.ImageField(null=True)
    assign_to = models.CharField(max_length=500,null=True,blank=True)
    conntrol_1 = models.CharField(max_length=500,null=True,blank=True)
    conntrol_date = models.CharField(max_length=500,null=True,blank=True)
    conntrol_no = models.CharField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sr_created")


class LoggingSheet(models.Model):
    id = models.AutoField(primary_key=True)
    city_location = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=500)
    client_name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    att_person = models.CharField(max_length=500)
    email = models.CharField(max_length=500,null=True)
    sample_nature = models.CharField(max_length=500)
    rec_date = models.CharField(max_length=500, null=True)
    exp_date = models.CharField(max_length=500, null=True)
    rep_date = models.CharField(max_length=500, null=True)
    rec_by = models.CharField(max_length=500)
    remarks = models.CharField(max_length=500)
    month = models.DateField(null=True)
    lab = models.CharField(max_length=500,null=True)
    issue_date = models.CharField(max_length=500,null=True)
    issue_no = models.CharField(max_length=500,null=True)
    issue = models.CharField(max_length=500,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="log_reports_created")



class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.TextField(max_length=1000)
    timestamp = models.CharField(max_length=100,null=True)

    
    created_at = models.DateTimeField(auto_now_add=True,null=True)# 
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="log_created")
    def __str__(self):
        return self.action 
    

class ClientDetails(models.Model):
    company_name = models.CharField(max_length=500, unique=True)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=500, blank=True)
    contact_number = models.CharField(max_length=500, blank=True)
    email = models.CharField(max_length=500, blank=True)
    po_reference = models.CharField(max_length=500, blank=True, null=True)  # Main PO reference
    custom_po_fields = models.JSONField(default=list, blank=True, null=True)  # Custom PO fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name


class JobCompletionForm(models.Model):
    company = models.ForeignKey(
        ClientDetails, 
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    job_number = models.CharField(max_length=500, unique=True, editable=False, blank=True, null=True)
    invoice_ref = models.CharField(max_length=200, blank=True, null=True)
    po_reference = models.CharField(max_length=200, blank=True, null=True)
    custom_po_fields = models.JSONField(null=True)
    service_details = models.JSONField()
    representative_name = models.CharField(max_length=500,null=True)
    representative_sign = models.CharField(max_length=20,null=True)
    service_receiver = models.CharField(max_length=20,null=True)
    location = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.job_number:
            self.job_number = self.generate_job_number()
        super().save(*args, **kwargs)
    
    def generate_job_number(self):
        """Generate job number based on location: JOB-2026-001-KHI or JOB-2026-001-LHR"""
        current_year = timezone.now().year
        
        # Determine location code
        location_code = ''
        if self.location:
            location_lower = self.location.lower()
            if 'karachi' in location_lower:
                location_code = 'KHI'
            elif 'lahore' in location_lower:
                location_code = 'LHR'
            else:
                location_code = 'OTHER'
        else:
            location_code = 'OTHER'
        
        # Get the last job number for this year and location
        last_job = JobCompletionForm.objects.filter(
            job_number__startswith=f'{current_year}-',
            job_number__endswith=f'-{location_code}'
        ).order_by('-job_number').first()
        
        if last_job:
            # Extract sequence number from last job
            # Format: JOB-2026-001-KHI
            match = re.search(r'\d+-(\d+)-\w+', last_job.job_number)
            if match:
                last_sequence = int(match.group(1))
                new_sequence = last_sequence + 1
            else:
                new_sequence = 1
        else:
            new_sequence = 1
        
        # Format: JOB-2026-001-KHI (3-digit sequence with leading zeros)
        return f'{current_year}-{new_sequence:03d}-{location_code}'
    
    def __str__(self):
        return f"{self.job_number} - {self.company.company_name}"
    
    

# --- Phase 1 audit trail: field-level history (django-simple-history) 12-07-2026 ---
from simple_history import register as _sh_register

def _etal_register_history(model):
    excluded = [f.name for f in model._meta.fields if 'image' in f.name.lower()]
    if excluded:
        _sh_register(model, excluded_fields=excluded)
    else:
        _sh_register(model)

for _m in (DrinkingWaterForm, GaseousEmissionForm, AmbientAirForm, WasteWaterSludge,
           VehiculEmissionForm, LuxAnalysisForm, PackingPolyBagForm, MachineOilForm,
           MicrobialAnalysis, ViscousLiquid, AmbientAir2, WasteWaterForm2, NoiseAnalysis,
           NoiseMonitoring, Calibration, Inspection, Verification,
           Sample_registration, LoggingSheet, JobCompletionForm):
    _etal_register_history(_m)


# --- Phase 1 approval workflow (12-07-2026) ---
class ApprovalStatus(models.Model):
    model_key = models.CharField(max_length=20)
    record_id = models.IntegerField()
    approved_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('model_key', 'record_id')

    def __str__(self):
        return f"{self.model_key}#{self.record_id} approved"


from EnviTechAlApp.approval import wire_guards as _etal_wire
_etal_wire({DrinkingWaterForm: 'dw', GaseousEmissionForm: 'gae', AmbientAirForm: 'aa',
            WasteWaterSludge: 'ww', VehiculEmissionForm: 've', LuxAnalysisForm: 'la',
            PackingPolyBagForm: 'pp', MachineOilForm: 'mo', MicrobialAnalysis: 'ma',
            ViscousLiquid: 'vl', AmbientAir2: 'aa2', WasteWaterForm2: 'ww2',
            NoiseAnalysis: 'na', NoiseMonitoring: 'nm',
            Calibration: 'calib', Inspection: 'insp', Verification: 'verif'})


# --- Phase 1 sample lifecycle board (12-07-2026) ---
class SampleLifecycle(models.Model):
    sample_id = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=30, default='Registered')
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sample_id}: {self.status}"


# --- Audit the audit controls (12-07-2026) ---
_sh_register(ApprovalStatus)
_sh_register(SampleLifecycle)


# --- Phase 2: equipment & calibration register (12-07-2026) ---
class Equipment(models.Model):
    lab = models.CharField(max_length=20, default='Karachi')
    name = models.CharField(max_length=200)
    serial_no = models.CharField(max_length=120, blank=True, default='')
    location = models.CharField(max_length=60, default='Karachi')
    frequency_months = models.IntegerField(default=12)
    last_calibrated = models.DateField(null=True, blank=True)
    cert_ref = models.CharField(max_length=120, blank=True, default='')
    notes = models.CharField(max_length=300, blank=True, default='')
    active = models.BooleanField(default=True)
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_no})"

_sh_register(Equipment)


# --- Phase 2: regulatory limits library (12-07-2026) ---
class RegulatoryLimit(models.Model):
    parameter = models.CharField(max_length=120)
    standard = models.CharField(max_length=20)  # SEQS / PEQS / NEQS / WHO
    limit_min = models.FloatField(null=True, blank=True)
    limit_max = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=40, blank=True, default='')
    notes = models.CharField(max_length=200, blank=True, default='')
    active = models.BooleanField(default=True)
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('parameter', 'standard')

    def __str__(self):
        return f"{self.parameter} [{self.standard}]"

_sh_register(RegulatoryLimit)


# --- Phase 2: chemical & consumable inventory (13-07-2026) ---
class ChemicalItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=40, default='Reagent')
    grade = models.CharField(max_length=80, blank=True, default='')
    cas_no = models.CharField(max_length=40, blank=True, default='')
    unit = models.CharField(max_length=30, default='g')
    storage = models.CharField(max_length=120, blank=True, default='')
    hazard = models.CharField(max_length=120, blank=True, default='')
    reorder_level = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=300, blank=True, default='')
    active = models.BooleanField(default=True)
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChemicalLot(models.Model):
    item = models.ForeignKey(ChemicalItem, on_delete=models.CASCADE, related_name='lots')
    location = models.CharField(max_length=20, default='Karachi')
    lot_no = models.CharField(max_length=80, blank=True, default='')
    supplier = models.CharField(max_length=150, blank=True, default='')
    po_ref = models.CharField(max_length=60, blank=True, default='')
    received = models.DateField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    opened = models.DateField(null=True, blank=True)
    qty_received = models.FloatField(default=0)
    coa = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='In use')
    remarks = models.CharField(max_length=200, blank=True, default='')
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s [%s] %s' % (self.item.name, self.location, self.lot_no)


class ChemicalMovement(models.Model):
    lot = models.ForeignKey(ChemicalLot, on_delete=models.CASCADE, related_name='moves')
    mtype = models.CharField(max_length=10)
    qty = models.FloatField()
    on_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True, default='')
    by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    at = models.DateTimeField(auto_now_add=True)


class InventoryDocControl(models.Model):
    module = models.CharField(max_length=20, default='chemicals')
    location = models.CharField(max_length=20)
    doc_no = models.CharField(max_length=60, blank=True, default='')
    issue_date = models.CharField(max_length=20, blank=True, default='')
    issue_no = models.CharField(max_length=10, blank=True, default='01')
    rev_no = models.CharField(max_length=10, blank=True, default='00')
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('module', 'location')


_sh_register(ChemicalItem)
_sh_register(ChemicalLot)
_sh_register(InventoryDocControl)
