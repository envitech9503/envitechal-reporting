from django.shortcuts import render
from django.http import HttpResponse
from detox.models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from EnviTechAlApp.models import *
import qrcode
from EnviTechAlApp import settings
import os
from fpdf import FPDF
from django.urls import reverse
from io import BytesIO
from PIL import Image
import base64
import tempfile
from django.shortcuts import get_object_or_404

def compress_image(uploaded_file, max_size_kb=500):
    """Compress image to under max_size_kb while preserving quality"""
    try:
        # Open the image file
        img = Image.open(BytesIO(uploaded_file.read()))
        
        # Convert to RGB if PNG with alpha channel
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Try saving with different quality settings
        for quality in [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]:
            output_buffer = BytesIO()
            
            # Use JPEG for better compression, but could use original format if preferred
            img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            
            # Check if we're under the size limit
            if len(output_buffer.getvalue()) / 1024 <= max_size_kb:
                return output_buffer.getvalue()
                
        # If still too large after quality reduction, resize dimensions
        original_width, original_height = img.size
        new_width = int(original_width * 0.9)
        new_height = int(original_height * 0.9)
        
        while len(output_buffer.getvalue()) / 1024 > max_size_kb and new_width > 100:
            img = img.resize((new_width, new_height), Image.LANCZOS)
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG', quality=70, optimize=True)
            new_width = int(new_width * 0.9)
            new_height = int(new_height * 0.9)
            
        return output_buffer.getvalue()
        
    except Exception as e:
        print(f"Error compressing image: {e}")
        return None
    




envitech_logo = '/home/django/EnviTechAlApp/static/assets/approvedby-removebg-preview.png'
logo = '/static/assets/approvedby-removebg-preview.png'




def safe_load(field):
    return json.loads(field) if isinstance(field, str) else field




def detox(request):
     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",signs)
     return render(request,'detox.html', {'signs':signs})

def create_detox(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        city_location = request.POST.get('city_location')
        lab_report_no = request.POST.get('lab_report_no')
        invoice_bill_no = request.POST.get('invoice_bill_no')
        reporting_date = request.POST.get('reporting_date')
        report_1 = request.POST.get('report_1')
        report_2 = request.POST.get('report_2')
        attention_1 = request.POST.get('attention_1')
        attention_2 = request.POST.get('attention_2')
        sample_id_1 = request.POST.get('sample_id_1')
        sample_id_2 = request.POST.get('sample_id_2')
        sample_col_date = request.POST.get('sample_col_date')
        sample_des_1 = request.POST.get('sample_des_1')
        sample_des_2 = request.POST.get('sample_des_2')
        sample_method_1 = request.POST.get('sample_method_1')
        sample_method_2 = request.POST.get('sample_method_2')
        sample_type_1 = request.POST.get('sample_type_1')
        sample_type_2 = request.POST.get('sample_type_2')
        sample_tech_1 = request.POST.get('sample_tech_1')
        sample_tech_2 = request.POST.get('sample_tech_2')
        sample_col_by = request.POST.get('sample_col_by')
        date_analysis = request.POST.get('date_analysis')
        date_analysis_to = request.POST.get('date_analysis_to')
        test_desc = request.POST.get('test_desc')
        raw_water_1 = request.POST.get('raw_water_1')
        wastewater_1 = request.POST.get('wastewater_1')
        sludge_1 = request.POST.get('sludge_1')
        raw_water_2 = request.POST.get('raw_water_2')
        wastewater_2 = request.POST.get('wastewater_2')
        sludge_2 = request.POST.get('sludge_2')
        raw_water_3 = request.POST.get('raw_water_3')
        wastewater_3 = request.POST.get('wastewater_3')
        sludge_3 = request.POST.get('sludge_3')
        extra_field = request.POST.get('extra_field')
        extra_field_2 = request.POST.get('extra_field_2')
        extra_field_3 = request.POST.get('extra_field_3')
        extra_field_3_1 = request.POST.get('extra_field_3_1')
        extra_field_4 = request.POST.get('extra_field_4')
        extra_field_4_1 = request.POST.get('extra_field_4_1')
        extra_field_5 = request.POST.get('extra_field_5')
        extra_field_6 = request.POST.get('extra_field_6')
        extra_field_7 = request.POST.get('extra_field_7')
        extra_field_8 = request.POST.get('extra_field_8')
        extra_field_8_1 = request.POST.get('extra_field_8_1')
        extra_field_9 = request.POST.get('extra_field_9')
        extra_field_10 = request.POST.get('extra_field_10')
        extra_field_11 = request.POST.get('extra_field_11')
        extra_field_12 = request.POST.get('extra_field_12')
        extra_field_13 = request.POST.get('extra_field_13')
        extra_field_14 = request.POST.get('extra_field_14')
        extra_field_15 = request.POST.get('extra_field_15')
        extra_field_16 = request.POST.get('extra_field_16')
        extra_field_17 = request.POST.get('extra_field_17')
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
        edit_note = request.POST.get('edit_note')
        doc_1 = request.POST.get('doc_1')
        doc_2 = request.POST.get('doc_2')
        doc_3 = request.POST.get('doc_3')
        
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
                       print(f"Processing {image_key} - Original: {original_size_kb:.2f}KB")
                       
                       if uploaded_file.size > 500 * 1024:
                            uploaded_file.seek(0)
                            compressed_image = compress_image(uploaded_file)
                            
                            if compressed_image:
                                 compressed_size_kb = len(compressed_image) / 1024
                                 print(f"Compressed to: {compressed_size_kb:.2f}KB")
                                 base64_encoded = base64.b64encode(compressed_image).decode('utf-8')
                            else:
                                 print("Compression failed, using original")
                                 uploaded_file.seek(0)
                                 file_bytes = uploaded_file.read()
                                 base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                       else:
                            file_bytes = uploaded_file.read()
                            base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                            print("No compression needed")

                       image_data[image_key] = base64_encoded
                       image_data[desc_key] = description or ''

                  except Exception as e:
                       print(f"Error processing image {i}: {e}")
        
        analyst_sign_id = request.POST.get('analyst_sign')
        review_sign_id = request.POST.get('review_sign')
        approved_sign_id = request.POST.get('approved_sign')
        analyst_sign = Signatures.objects.get(id=analyst_sign_id)
        review_sign = Signatures.objects.get(id=review_sign_id)
        approved_sign = Signatures.objects.get(id=approved_sign_id)
        
        
        inlet_json = {}
        outlet_json = {}
        test_json = {}
        for i in range(1,456):
            inlet = f'inlet_{i}'
            outlet = f'outlet_{i}'
            test = f'test_{i}'
            
            inlet_data = request.POST.get(inlet)
            outlet_data = request.POST.get(outlet)
            test_data = request.POST.get(test)
            
            inlet_json[inlet] = inlet_data
            outlet_json[outlet] = outlet_data
            test_json[test] = test_data
        missing_inlet = [f"inlet_{i}" for i in range(1, 456) if inlet_json.get(f"inlet_{i}") is None]
        missing_outlet = [f"outlet_{i}" for i in range(1, 456) if outlet_json.get(f"outlet_{i}") is None]
        missing_test = [f"test_{i}" for i in range(1, 456) if test_json.get(f"test_{i}") is None]

        print("Missing inlets:", missing_inlet)
        print("Missing outlets:", missing_outlet)
        print("Missing tests:", missing_test)
        
        detox_create = Detox(
                            location=location,
                            city_location=city_location,
                            lab_report_no=lab_report_no,
                            invoice_bill_no=invoice_bill_no,
                            reporting_date=reporting_date,
                            report_1=report_1,
                            report_2=report_2,
                            attention_1=attention_1,
                            attention_2=attention_2,
                            sample_id_1=sample_id_1,
                            sample_id_2=sample_id_2,
                            sample_col_date=sample_col_date,
                            sample_des_1=sample_des_1,
                            sample_des_2=sample_des_2,
                            sample_method_1=sample_method_1,
                            sample_method_2=sample_method_2,
                            sample_type_1=sample_type_1,
                            sample_type_2=sample_type_2,
                            sample_tech_1=sample_tech_1,
                            sample_tech_2=sample_tech_2,
                            sample_col_by=sample_col_by,
                            date_analysis=date_analysis,
                            date_analysis_to=date_analysis_to,
                            test_desc=test_desc,
                            raw_water_1=raw_water_1,
                            wastewater_1=wastewater_1,
                            sludge_1=sludge_1,
                            raw_water_2=raw_water_2,
                            wastewater_2=wastewater_2,
                            sludge_2=sludge_2,
                            raw_water_3=raw_water_3,
                            wastewater_3=wastewater_3,
                            sludge_3=sludge_3,
                            extra_field=extra_field,
                            extra_field_2=extra_field_2,
                            extra_field_3=extra_field_3,
                            extra_field_3_1=extra_field_3_1,
                            extra_field_4=extra_field_4,
                            extra_field_4_1=extra_field_4_1,
                            extra_field_5=extra_field_5,
                            extra_field_6=extra_field_6,
                            extra_field_7=extra_field_7,
                            extra_field_8=extra_field_8,
                            extra_field_8_1=extra_field_8_1,
                            extra_field_9=extra_field_9,
                            extra_field_10=extra_field_10,
                            extra_field_11=extra_field_11,
                            extra_field_12=extra_field_12,
                            extra_field_13=extra_field_13,
                            extra_field_14=extra_field_14,
                            extra_field_15=extra_field_15,
                            extra_field_16=extra_field_16,
                            extra_field_17=extra_field_17,
                            inlet=inlet_json,
                            outlet=outlet_json,
                            test=test_json,
                            analyst_signature=analyst_sign,
                            assistant_manager_signature=review_sign,
                            lab_manager_signature=approved_sign,
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
                            edit_note=edit_note,
                            doc_1=doc_1,
                            doc_2=doc_2,
                            doc_3=doc_3,**image_data,pdf_heading=pdf_heading
                            )

        detox_create.save()
        id = (Detox.objects.last()).id
        if "submit_and_view" in request.POST:
             url = f"/detox/create_view_detox/{str(id)}/"
             return redirect(to=url)
        if "submit_and_new" in request.POST:
             
             return render(request, "detox.html")
    else:
        return render(request,'detox.html', {'signs':signs})
    
def detoxList(request):
     from EnviTechAlApp.listfilter import _by_date_desc, _list_filter
     detoxList, _srch = _list_filter(request, Detox)
     context = {'list':detoxList, 'searched':_srch}

     return render(request,"detoxList.html",context)  
 
def detox_edit(request,pk):
    detox = Detox.objects.get(id=pk)
    detox.extra_field = safe_load(detox.extra_field)
    detox.extra_field_2 = safe_load(detox.extra_field_2)
    detox.extra_field_3 = safe_load(detox.extra_field_3)
    detox.extra_field_3_1 = safe_load(detox.extra_field_3_1)
    detox.extra_field_4 = safe_load(detox.extra_field_4)
    detox.extra_field_4_1 = safe_load(detox.extra_field_4_1)
    detox.extra_field_5 = safe_load(detox.extra_field_5)
    detox.extra_field_6 = safe_load(detox.extra_field_6)
    detox.extra_field_7 = safe_load(detox.extra_field_7)
    detox.extra_field_8 = safe_load(detox.extra_field_8)
    detox.extra_field_8_1 = safe_load(detox.extra_field_8_1)
    detox.extra_field_9 = safe_load(detox.extra_field_9)
    detox.extra_field_10 = safe_load(detox.extra_field_10)
    detox.extra_field_11 = safe_load(detox.extra_field_11)
    detox.extra_field_12 = safe_load(detox.extra_field_12)
    detox.extra_field_13 = safe_load(detox.extra_field_13)
    detox.extra_field_14 = safe_load(detox.extra_field_14)
    detox.extra_field_15 = safe_load(detox.extra_field_15)
    detox.extra_field_16 = safe_load(detox.extra_field_16)
    detox.extra_field_17 = safe_load(detox.extra_field_17)
    image_previews = {}
    for i in range(1, 7):
        image_key = f'pdf_image_{i}'
        image_data = getattr(detox, image_key)
        if image_data:
            image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
    context = {
        'detox': detox,
        'inlets': detox.inlet if detox.inlet else {},
        'outlets': detox.outlet if detox.outlet else {},
        'tests': detox.test if detox.test else {},
        'extra_field': detox.extra_field or {},
        'extra_field_2': detox.extra_field_2 or {},
        'extra_field_3': detox.extra_field_3 or {},
        'extra_field_3_1': detox.extra_field_3_1 or {},
        'extra_field_4': detox.extra_field_4 or {},
        'extra_field_4_1': detox.extra_field_4_1 or {},
        'extra_field_5': detox.extra_field_5 or {},
        'extra_field_6': detox.extra_field_6 or {},
        'extra_field_7': detox.extra_field_7 or {},
        'extra_field_8': detox.extra_field_8 or {},
        'extra_field_8_1': detox.extra_field_8_1 or {},
        'extra_field_9': detox.extra_field_9 or {},
        'extra_field_10': detox.extra_field_10 or {},
        'extra_field_11': detox.extra_field_11 or {},
        'extra_field_12': detox.extra_field_12 or {},
        'extra_field_13': detox.extra_field_13 or {},
        'extra_field_14': detox.extra_field_14 or {},
        'extra_field_15': detox.extra_field_15 or {},
        'extra_field_16': detox.extra_field_16 or {},
        'extra_field_17': detox.extra_field_17 or {},
        'logo':logo,
        'signs':signs,
        'pdf_image_1': image_previews.get('pdf_image_1'),
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),
        
    }
    return render(request,"detox_edit.html",context)


def detox_edit_update(request,pk):
    detox = Detox.objects.get(id=pk)
    if request.method == 'POST':
        detox.location = request.POST.get('location')
        detox.city_location = request.POST.get('city_location')
        detox.lab_report_no = request.POST.get('lab_report_no')
        detox.invoice_bill_no = request.POST.get('invoice_bill_no')
        detox.reporting_date = request.POST.get('reporting_date')
        detox.report_1 = request.POST.get('report_1')
        detox.report_2 = request.POST.get('report_2')
        detox.attention_1 = request.POST.get('attention_1')
        detox.attention_2 = request.POST.get('attention_2')
        detox.sample_id_1 = request.POST.get('sample_id_1')
        detox.sample_id_2 = request.POST.get('sample_id_2')
        detox.sample_col_date = request.POST.get('sample_col_date')
        detox.sample_des_1 = request.POST.get('sample_des_1')
        detox.sample_des_2 = request.POST.get('sample_des_2')
        detox.sample_method_1 = request.POST.get('sample_method_1')
        detox.sample_method_2 = request.POST.get('sample_method_2')
        detox.sample_type_1 = request.POST.get('sample_type_1')
        detox.sample_type_2 = request.POST.get('sample_type_2')
        detox.sample_tech_1 = request.POST.get('sample_tech_1')
        detox.sample_tech_2 = request.POST.get('sample_tech_2')
        detox.sample_col_by = request.POST.get('sample_col_by')
        detox.date_analysis = request.POST.get('date_analysis')
        detox.date_analysis_to = request.POST.get('date_analysis_to')
        detox.test_desc = request.POST.get('test_desc')
        detox.raw_water_1 = request.POST.get('raw_water_1')
        detox.wastewater_1 = request.POST.get('wastewater_1')
        detox.sludge_1 = request.POST.get('sludge_1')
        detox.raw_water_2 = request.POST.get('raw_water_2')
        detox.wastewater_2 = request.POST.get('wastewater_2')
        detox.sludge_2 = request.POST.get('sludge_2')
        detox.raw_water_3 = request.POST.get('raw_water_3')
        detox.wastewater_3 = request.POST.get('wastewater_3')
        detox.sludge_3 = request.POST.get('sludge_3')
        detox.legend_1 = request.POST.get('legend_1')
        detox.legend_2 = request.POST.get('legend_2')
        detox.legend_3 = request.POST.get('legend_3')
        detox.legend_4 = request.POST.get('legend_4')
        detox.legend_5 = request.POST.get('legend_5')
        detox.legend_6 = request.POST.get('legend_6')
        detox.legend_7 = request.POST.get('legend_7')
        detox.legend_8 = request.POST.get('legend_8')
        detox.legend_9 = request.POST.get('legend_9')
        detox.legend_10 = request.POST.get('legend_10')
        detox.legend_11 = request.POST.get('legend_11')
        detox.edit_note = request.POST.get('edit_note')
        detox.doc_1 = request.POST.get('doc_1')
        detox.doc_2 = request.POST.get('doc_2')
        detox.doc_3 = request.POST.get('doc_3')
        
        detox.pdf_heading = request.POST.get('pdf_heading')
        for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)

               print(f"Image {i} remove_requested: {remove_requested}")  # Debug

               if remove_requested == "on":
                    print(f"Removing image {i}")
                    setattr(detox, image_key, '')
                    setattr(detox, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(detox, image_key, base64_encoded)
                         setattr(detox, desc_key, description or '')
                         print(f"Updated image {i}")
                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
               else:
                    if description is not None:
                         setattr(detox, desc_key, description)
                         print(f"Updated description {i}")
        
        analyst_sign_id = request.POST.get('analyst_sign')
        review_sign_id = request.POST.get('review_sign')
        approved_sign_id = request.POST.get('approved_sign')
        analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
        review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
        approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

        # Assign to ambientUpdate if needed
        detox.analyst_signature = analyst_sign
        detox.assistant_manager_signature = review_sign
        detox.lab_manager_signature = approved_sign
        
        
        def process_extra_field(field_name, prefix=''):
            if field_name in request.POST:
                data = json.loads(request.POST[field_name])
                for i in range(len(request.POST.getlist(f'{prefix}sr[]'))):
                    data.append({
                        "sr": request.POST.getlist(f'{prefix}sr[]')[i],
                        "parameters": request.POST.getlist(f'{prefix}parameters[]')[i],
                        "cas": request.POST.getlist(f'{prefix}cas[]')[i],
                        "methods": request.POST.getlist(f'{prefix}method[]')[i],
                        "1rl": request.POST.getlist(f'{prefix}1rl[]')[i],
                        "unit": request.POST.getlist(f'{prefix}unit[]')[i],
                        "inlet": request.POST.getlist(f'{prefix}inlet[]')[i],
                        "outlet": request.POST.getlist(f'{prefix}outlet[]')[i],
                        "1rl2": request.POST.getlist(f'{prefix}1rl2[]')[i],
                        "unit2": request.POST.getlist(f'{prefix}unit2[]')[i],
                        "test": request.POST.getlist(f'{prefix}test[]')[i],
                    })
                setattr(detox, field_name, data)

        # Process each extra field with its unique prefix
        process_extra_field('extra_field')  # Uses default field names (sr[], parameters[], etc.)
        process_extra_field('extra_field_2', 'extra2_')
        process_extra_field('extra_field_3', 'extra3_')
        process_extra_field('extra_field_3_1', 'extra3_1_')
        process_extra_field('extra_field_4', 'extra4_')
        process_extra_field('extra_field_4_1', 'extra4_1_')
        process_extra_field('extra_field_5', 'extra5_')
        process_extra_field('extra_field_6', 'extra6_')
        process_extra_field('extra_field_7', 'extra7_')
        process_extra_field('extra_field_8', 'extra8_')
        process_extra_field('extra_field_8_1', 'extra8_1_')
        process_extra_field('extra_field_9', 'extra9_')
        process_extra_field('extra_field_10', 'extra10_')
        process_extra_field('extra_field_11', 'extra11_')
        process_extra_field('extra_field_12', 'extra12_')
        process_extra_field('extra_field_13', 'extra13_')
        process_extra_field('extra_field_14', 'extra14_')
        process_extra_field('extra_field_15', 'extra15_')
        process_extra_field('extra_field_16', 'extra16_')
        process_extra_field('extra_field_17', 'extra17_')
             
             
    
        
        inlet_json = {}
        outlet_json = {}
        test_json = {}
        for i in range(1,456):
            inlet = f'inlet_{i}'
            outlet = f'outlet_{i}'
            test = f'test_{i}'
            
            inlet_data = request.POST.get(inlet)
            outlet_data = request.POST.get(outlet)
            test_data = request.POST.get(test)
            
            inlet_json[inlet] = inlet_data
            outlet_json[outlet] = outlet_data
            test_json[test] = test_data
        detox.inlet = inlet_json
        detox.outlet = outlet_json
        detox.test = test_json 
        
           
        detox.save()
        id = detox.id
        if "submit_and_view" in request.POST:
             url = f'/detox/create_view_detox/{str(id)}/'
             return redirect(to=url)
        if "submit_and_new" in request.POST:
             return redirect('detox_edit')
        else:
             return HttpResponse('Invalid Request Method',status=400)
     
    return render(request,"detox_edit.html")      



def detox_clone(request,pk):
    detox = Detox.objects.get(id=pk)
    detox.extra_field = safe_load(detox.extra_field)
    detox.extra_field_2 = safe_load(detox.extra_field_2)
    detox.extra_field_3 = safe_load(detox.extra_field_3)
    detox.extra_field_3_1 = safe_load(detox.extra_field_3_1)
    detox.extra_field_4 = safe_load(detox.extra_field_4)
    detox.extra_field_4_1 = safe_load(detox.extra_field_4_1)
    detox.extra_field_5 = safe_load(detox.extra_field_5)
    detox.extra_field_6 = safe_load(detox.extra_field_6)
    detox.extra_field_7 = safe_load(detox.extra_field_7)
    detox.extra_field_8 = safe_load(detox.extra_field_8)
    detox.extra_field_8_1 = safe_load(detox.extra_field_8_1)
    detox.extra_field_9 = safe_load(detox.extra_field_9)
    detox.extra_field_10 = safe_load(detox.extra_field_10)
    detox.extra_field_11 = safe_load(detox.extra_field_11)
    detox.extra_field_12 = safe_load(detox.extra_field_12)
    detox.extra_field_13 = safe_load(detox.extra_field_13)
    detox.extra_field_14 = safe_load(detox.extra_field_14)
    detox.extra_field_15 = safe_load(detox.extra_field_15)
    detox.extra_field_16 = safe_load(detox.extra_field_16)
    detox.extra_field_17 = safe_load(detox.extra_field_17)
    image_previews = {}
    for i in range(1, 7):
        image_key = f'pdf_image_{i}'
        image_data = getattr(detox, image_key)
        if image_data:
            image_previews[image_key] = f"data:image/jpeg;base64,{image_data}"
    context = {
        'detox': detox,
        'inlets': detox.inlet if detox.inlet else {},
        'outlets': detox.outlet if detox.outlet else {},
        'tests': detox.test if detox.test else {},
        'extra_field': detox.extra_field or {},
        'extra_field_2': detox.extra_field_2 or {},
        'extra_field_3': detox.extra_field_3 or {},
        'extra_field_3_1': detox.extra_field_3_1 or {},
        'extra_field_4': detox.extra_field_4 or {},
        'extra_field_4_1': detox.extra_field_4_1 or {},
        'extra_field_5': detox.extra_field_5 or {},
        'extra_field_6': detox.extra_field_6 or {},
        'extra_field_7': detox.extra_field_7 or {},
        'extra_field_8': detox.extra_field_8 or {},
        'extra_field_8_1': detox.extra_field_8_1 or {},
        'extra_field_9': detox.extra_field_9 or {},
        'extra_field_10': detox.extra_field_10 or {},
        'extra_field_11': detox.extra_field_11 or {},
        'extra_field_12': detox.extra_field_12 or {},
        'extra_field_13': detox.extra_field_13 or {},
        'extra_field_14': detox.extra_field_14 or {},
        'extra_field_15': detox.extra_field_15 or {},
        'extra_field_16': detox.extra_field_16 or {},
        'extra_field_17': detox.extra_field_17 or {},
        'logo':logo,
        'signs':signs,
        'pdf_image_1': image_previews.get('pdf_image_1'),
         'pdf_image_2': image_previews.get('pdf_image_2'),
         'pdf_image_3': image_previews.get('pdf_image_3'),
         'pdf_image_4': image_previews.get('pdf_image_4'),
         'pdf_image_5': image_previews.get('pdf_image_5'),
         'pdf_image_6': image_previews.get('pdf_image_6'),
        
    }
    return render(request,"detox_clone.html",context)


def detox_clone_update(request,pk):
    detox = Detox.objects.get(id=pk)
    if request.method == 'POST':
        detox.location = request.POST.get('location')
        detox.city_location = request.POST.get('city_location')
        detox.lab_report_no = request.POST.get('lab_report_no')
        detox.invoice_bill_no = request.POST.get('invoice_bill_no')
        detox.reporting_date = request.POST.get('reporting_date')
        detox.report_1 = request.POST.get('report_1')
        detox.report_2 = request.POST.get('report_2')
        detox.attention_1 = request.POST.get('attention_1')
        detox.attention_2 = request.POST.get('attention_2')
        detox.sample_id_1 = request.POST.get('sample_id_1')
        detox.sample_id_2 = request.POST.get('sample_id_2')
        detox.sample_col_date = request.POST.get('sample_col_date')
        detox.sample_des_1 = request.POST.get('sample_des_1')
        detox.sample_des_2 = request.POST.get('sample_des_2')
        detox.sample_method_1 = request.POST.get('sample_method_1')
        detox.sample_method_2 = request.POST.get('sample_method_2')
        detox.sample_type_1 = request.POST.get('sample_type_1')
        detox.sample_type_2 = request.POST.get('sample_type_2')
        detox.sample_tech_1 = request.POST.get('sample_tech_1')
        detox.sample_tech_2 = request.POST.get('sample_tech_2')
        detox.sample_col_by = request.POST.get('sample_col_by')
        detox.date_analysis = request.POST.get('date_analysis')
        detox.date_analysis_to = request.POST.get('date_analysis_to')
        detox.test_desc = request.POST.get('test_desc')
        detox.raw_water_1 = request.POST.get('raw_water_1')
        detox.wastewater_1 = request.POST.get('wastewater_1')
        detox.sludge_1 = request.POST.get('sludge_1')
        detox.raw_water_2 = request.POST.get('raw_water_2')
        detox.wastewater_2 = request.POST.get('wastewater_2')
        detox.sludge_2 = request.POST.get('sludge_2')
        detox.raw_water_3 = request.POST.get('raw_water_3')
        detox.wastewater_3 = request.POST.get('wastewater_3')
        detox.sludge_3 = request.POST.get('sludge_3')
        detox.legend_1 = request.POST.get('legend_1')
        detox.legend_2 = request.POST.get('legend_2')
        detox.legend_3 = request.POST.get('legend_3')
        detox.legend_4 = request.POST.get('legend_4')
        detox.legend_5 = request.POST.get('legend_5')
        detox.legend_6 = request.POST.get('legend_6')
        detox.legend_7 = request.POST.get('legend_7')
        detox.legend_8 = request.POST.get('legend_8')
        detox.legend_9 = request.POST.get('legend_9')
        detox.legend_10 = request.POST.get('legend_10')
        detox.legend_11 = request.POST.get('legend_11')
        detox.edit_note = request.POST.get('edit_note')
        detox.doc_1 = request.POST.get('doc_1')
        detox.doc_2 = request.POST.get('doc_2')
        detox.doc_3 = request.POST.get('doc_3')
        
        detox.pdf_heading = request.POST.get('pdf_heading')
        for i in range(1, 7):
               image_key = f'pdf_image_{i}'
               desc_key = f'pdf_desc_{i}'
               remove_key = f'remove_image_{i}'

               uploaded_file = request.FILES.get(image_key)
               description = request.POST.get(desc_key)
               remove_requested = request.POST.get(remove_key)

               print(f"Image {i} remove_requested: {remove_requested}")  # Debug

               if remove_requested == "on":
                    print(f"Removing image {i}")
                    setattr(detox, image_key, '')
                    setattr(detox, desc_key, '')
               elif uploaded_file:
                    try:
                         file_bytes = uploaded_file.read()
                         base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
                         setattr(detox, image_key, base64_encoded)
                         setattr(detox, desc_key, description or '')
                         print(f"Updated image {i}")
                    except Exception as e:
                         print(f"Error processing image {i}: {e}")
               else:
                    if description is not None:
                         setattr(detox, desc_key, description)
                         print(f"Updated description {i}")
        
        analyst_sign_id = request.POST.get('analyst_sign')
        review_sign_id = request.POST.get('review_sign')
        approved_sign_id = request.POST.get('approved_sign')
        analyst_sign = get_object_or_404(Signatures, id=analyst_sign_id) if analyst_sign_id else None
        review_sign = get_object_or_404(Signatures, id=review_sign_id) if review_sign_id else None
        approved_sign = get_object_or_404(Signatures, id=approved_sign_id) if approved_sign_id else None

        # Assign to ambientUpdate if needed
        detox.analyst_signature = analyst_sign
        detox.assistant_manager_signature = review_sign
        detox.lab_manager_signature = approved_sign
        
        
        def process_extra_field(field_name, prefix=''):
            if field_name in request.POST:
                data = json.loads(request.POST[field_name])
                for i in range(len(request.POST.getlist(f'{prefix}sr[]'))):
                    data.append({
                        "sr": request.POST.getlist(f'{prefix}sr[]')[i],
                        "parameters": request.POST.getlist(f'{prefix}parameters[]')[i],
                        "cas": request.POST.getlist(f'{prefix}cas[]')[i],
                        "methods": request.POST.getlist(f'{prefix}method[]')[i],
                        "1rl": request.POST.getlist(f'{prefix}1rl[]')[i],
                        "unit": request.POST.getlist(f'{prefix}unit[]')[i],
                        "inlet": request.POST.getlist(f'{prefix}inlet[]')[i],
                        "outlet": request.POST.getlist(f'{prefix}outlet[]')[i],
                        "1rl2": request.POST.getlist(f'{prefix}1rl2[]')[i],
                        "unit2": request.POST.getlist(f'{prefix}unit2[]')[i],
                        "test": request.POST.getlist(f'{prefix}test[]')[i],
                    })
                setattr(detox, field_name, data)

        # Process each extra field with its unique prefix
        process_extra_field('extra_field')  # Uses default field names (sr[], parameters[], etc.)
        process_extra_field('extra_field_2', 'extra2_')
        process_extra_field('extra_field_3', 'extra3_')
        process_extra_field('extra_field_3_1', 'extra3_1_')
        process_extra_field('extra_field_4', 'extra4_')
        process_extra_field('extra_field_4_1', 'extra4_1_')
        process_extra_field('extra_field_5', 'extra5_')
        process_extra_field('extra_field_6', 'extra6_')
        process_extra_field('extra_field_7', 'extra7_')
        process_extra_field('extra_field_8', 'extra8_')
        process_extra_field('extra_field_8_1', 'extra8_1_')
        process_extra_field('extra_field_9', 'extra9_')
        process_extra_field('extra_field_10', 'extra10_')
        process_extra_field('extra_field_11', 'extra11_')
        process_extra_field('extra_field_12', 'extra12_')
        process_extra_field('extra_field_13', 'extra13_')
        process_extra_field('extra_field_14', 'extra14_')
        process_extra_field('extra_field_15', 'extra15_')
        process_extra_field('extra_field_16', 'extra16_')
        process_extra_field('extra_field_17', 'extra17_')
             
             
    
        
        inlet_json = {}
        outlet_json = {}
        test_json = {}
        for i in range(1,456):
            inlet = f'inlet_{i}'
            outlet = f'outlet_{i}'
            test = f'test_{i}'
            
            inlet_data = request.POST.get(inlet)
            outlet_data = request.POST.get(outlet)
            test_data = request.POST.get(test)
            
            inlet_json[inlet] = inlet_data
            outlet_json[outlet] = outlet_data
            test_json[test] = test_data
        detox.inlet = inlet_json
        detox.outlet = outlet_json
        detox.test = test_json 
        
           
        detox.save()
        id = detox.id
        if "submit_and_view" in request.POST:
             url = f'/detox/create_view_detox/{str(id)}/'
             return redirect(to=url)
        if "submit_and_new" in request.POST:
             return redirect('detox_clone')
        else:
             return HttpResponse('Invalid Request Method',status=400)
     
    return render(request,"detox_clone.html")      


def detox_delete(request, pk):
     from django.shortcuts import redirect
     from django.contrib import messages
     n, _ = Detox.objects.filter(id=pk).delete()
     if n:
         messages.success(request, "Detox record deleted successfully.")
     else:
         messages.error(request, "Record not found - nothing was deleted.")
     return redirect("/detox/detoxList") 
    
def create_view_detox(request,pk):
    detox = Detox.objects.get(id=pk)
    # print("detox  ----------------------  ",detox.extra_field)
    # extra_field_data = list(detox.extra_field.items())
    
    # for key,value in extra_field_data:
    #     print(key,value)
    detox.extra_field = safe_load(detox.extra_field)
    detox.extra_field_2 = safe_load(detox.extra_field_2)
    detox.extra_field_3 = safe_load(detox.extra_field_3)
    detox.extra_field_3_1 = safe_load(detox.extra_field_3_1)
    detox.extra_field_4 = safe_load(detox.extra_field_4)
    detox.extra_field_4_1 = safe_load(detox.extra_field_4_1)
    detox.extra_field_5 = safe_load(detox.extra_field_5)
    detox.extra_field_6 = safe_load(detox.extra_field_6)
    detox.extra_field_7 = safe_load(detox.extra_field_7)
    detox.extra_field_8 = safe_load(detox.extra_field_8)
    detox.extra_field_8_1 = safe_load(detox.extra_field_8_1)
    detox.extra_field_9 = safe_load(detox.extra_field_9)
    detox.extra_field_10 = safe_load(detox.extra_field_10)
    detox.extra_field_11 = safe_load(detox.extra_field_11)
    detox.extra_field_12 = safe_load(detox.extra_field_12)
    detox.extra_field_13 = safe_load(detox.extra_field_13)
    detox.extra_field_14 = safe_load(detox.extra_field_14)
    detox.extra_field_15 = safe_load(detox.extra_field_15)
    detox.extra_field_16 = safe_load(detox.extra_field_16)
    detox.extra_field_17 = safe_load(detox.extra_field_17)
    
    
    # Generate a unique file name for the QR code
    current_url = request.build_absolute_uri()
    qr_filename = f"qr_{detox.lab_report_no}.png"
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
    
    
    context = {
        'detox': detox,
        'inlets': detox.inlet if detox.inlet else {},
        'outlets': detox.outlet if detox.outlet else {},
        'tests': detox.test if detox.test else {},
        'extra_field': detox.extra_field or {},
        'extra_field_2': detox.extra_field_2 or {},
        'extra_field_3': detox.extra_field_3 or {},
        'extra_field_3_1': detox.extra_field_3_1 or {},
        'extra_field_4': detox.extra_field_4 or {},
        'extra_field_4_1': detox.extra_field_4_1 or {},
        'extra_field_5': detox.extra_field_5 or {},
        'extra_field_6': detox.extra_field_6 or {},
        'extra_field_7': detox.extra_field_7 or {},
        'extra_field_8': detox.extra_field_8 or {},
        'extra_field_8_1': detox.extra_field_8_1 or {},
        'extra_field_9': detox.extra_field_9 or {},
        'extra_field_10': detox.extra_field_10 or {},
        'extra_field_11': detox.extra_field_11 or {},
        'extra_field_12': detox.extra_field_12 or {},
        'extra_field_13': detox.extra_field_13 or {},
        'extra_field_14': detox.extra_field_14 or {},
        'extra_field_15': detox.extra_field_15 or {},
        'extra_field_16': detox.extra_field_16 or {},
        'extra_field_17': detox.extra_field_17 or {},
        'qr': qr_relative_path,
        'logo':logo
        
    }
    return render(request,"detox_report.html",context)


def detox_pdf(request, pk):
    qr_file_path = ""
    data = Detox.objects.get(id=pk)
    class PDFWithPageNumbers(FPDF):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._table_header_required = False
            self.set_auto_page_break(auto=True, margin=10)
            self.set_top_margin(40)
            
            # Add fonts during initialization
            font_path = "static/fonts/calibri.ttf"
            font_path_bold = "static/fonts/calibrib.ttf"
            font_path_alger = "static/fonts/ALGER.TTF"
            script_font_path = "static/fonts/SCRIPTBL.TTF"
            
            self.add_font("Calibri", "", font_path, uni=True)
            self.add_font("Calibri", "B", font_path_bold, uni=True)
            self.add_font("Algerian", "", font_path_alger)
            self.add_font('ScriptMT', '', script_font_path, uni=True)
        
        def header(self):
            self.set_y(0)
            self.set_x(0)
            self.image("static/assets/Header watermark.jpg", 0, 0, self.w, 30)
            self.image("static/assets/EnviTechAL LOGO.png", 16, 5, 24, 23)
            
            # Header styling
            self.set_line_width(0.5)
            self.set_draw_color(26, 84, 26)
            self.line(0, 30, self.w, 30)
            
            # Company name
            self.set_font("Algerian", "", 16)
            self.set_text_color(13, 46, 145)
            self.text(85, 15, txt="ENVI TECH AL")
            
            # Tagline
            self.set_font("Calibri", "B", 11)
            self.set_text_color(26, 84, 26)
            self.text(55, 23, txt="We strive for Pragmatic approach to achieve quality Excellence")
            self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png', 168, 5, 25, 23)
            
            # Body watermark
            self.image('static/assets/report water mark.png', 0, 30, self.w, self.h-35)
            
            
            
            # QR code generation
            target_url = request.build_absolute_uri(reverse('create_view_detox', kwargs={'pk': pk}))
            qr_filename = f"qr_{pk}.png"
            qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=6,
            )
            qr.add_data(target_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(qr_file_path)
            
            
            pdf.set_text_color(0, 0, 0)
            self.set_draw_color(0, 0, 0)
            
            
            
            self.set_font("Calibri", "B", 11)
            pdf.text(5,43,text='Lab Report No: ')
            self.set_font("Calibri", "", 11)
            pdf.text(31,43,text=data.lab_report_no)
            self.line(31, 45, 31 + self.get_string_width(data.lab_report_no), 45)
            self.image(qr_file_path, "C", y=40, w=20, h=20)
            
            
            # Page number
            self.set_font("Calibri", "B", 11)
            self.text(165, 43, txt="Page No:")
            self.set_font("Calibri", "", 11)
            page_num_text = f"{self.page_no()}"
            self.line(180,45,190+self.get_string_width(page_num_text),45)
            self.set_y(42.5)
            self.cell(self.w - 24, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
            
            self.set_font("Calibri", "B", 11)
            
            pdf.text(5,51,text='Invoice Bill No: ')
            self.set_font("Calibri", "", 11)
            
            pdf.text(31,51,text=data.invoice_bill_no)
            self.line(31, 53, 31 + self.get_string_width(data.invoice_bill_no), 53)
            
            
            
            # Page number
            self.set_font("Calibri", "B", 11)
            self.text(153.5, 51, txt="Reporting Date:")
            self.set_font("Calibri", "", 11)
            
            self.text(180, 51,text=f"{data.reporting_date}")
            self.set_font("Calibri", "", 11)
            self.line(180,53,180+self.get_string_width(data.reporting_date),53)
            
            
            pdf.ln(10)
        
        def _draw_table_header(self):
            """Draw the custom table header at current Y position"""
            
            self.set_fill_color(232, 232, 232)  # Light purple background
            self.set_font("Calibri", "B", 13) # Light purple background
            pdf.set_x(5)
            self.cell(200,8,"TEST RESULTS", border=True, align='C',ln=True,fill=True)
            # Save current Y position
            self.set_font("Calibri", "B", 9)
            # Save current Y position
            current_y = self.get_y()
            
            # First row of table header
            self.set_x(5)
            self.cell(10, 14, "Sr #", 1, align="C",fill=True)
            self.cell(46, 14, "Parameters/Analytes Description", 1, align="C",fill=True)
            self.cell(19, 14, "CAS NO", 1, align="C",fill=True)
            old_header_y = pdf.get_y()
            self.multi_cell(28, 7, "Methods/\nEquipment", 1, align="C",fill=True)
            pdf.set_y(old_header_y)
            
            # Wastewater and Sludge headers (merged cells)
            self.set_x(108)
            self.cell(58, 7, "Wastewater", 1, align="C",fill=True)
            self.cell(39, 7, "Sludge", 1, align="C",fill=True)
            
            # Second row of header (sub-headers)
            self.set_y(current_y + 7)  # Move down 7mm
            self.set_x(108)
            self.cell(12, 7, "¹R.L.", 1, align="C",fill=True)
            self.cell(12, 7, "Unit", 1, align="C",fill=True)
            self.cell(17, 7, "¹R.W./Inlet", 1, align="C",fill=True)
            self.cell(17, 7, "1A.T./Outlet", 1, align="C",fill=True)
            self.cell(10, 7, "¹R.L.", 1, align="C",fill=True)
            self.cell(12, 7, "Unit", 1, align="C",fill=True)
            self.cell(17, 7, "Test results", 1, align="C",fill=True)
            
            # Reset position for data rows
            self.set_y(current_y + 14)
            
            # Reset position for data rows
            self.set_y(current_y + 14)
        
        def check_page_break(self, required_height):
            """Check if we need a new page and add header if needed"""
            if self.get_y() + required_height > self.page_break_trigger:
                self.add_page()
                self.set_y(100)  # Set Y position below header
                self.draw_table_header()
                return True
            return False
        
        def get_multicell_height(self, text, width, line_height):
            """Calculate the height needed for a multicell"""
            lines = self.multi_cell(w=width, h=line_height, txt=text, border=0, align='C', split_only=True)
            return len(lines) * line_height
            
        def add_table_row(self, row_num, desc_text, cas_no, method, ww_rl, ww_unit, inlet, outlet, sludge_rl, sludge_unit, test_result):
            """Add a properly aligned table row with multicell support"""
            # Define cell widths
            pdf.set_font("Calibri", "", 9)
            cell_widths = {
                'row_num': 10,
                'desc': 46,
                'cas_no': 19,
                'method': 28,
                'ww_rl': 12,
                'ww_unit': 12,
                'inlet': 17,
                'outlet': 17,
                'sludge_rl': 10,
                'sludge_unit': 12,
                'test_result': 17
            }
            
            line_height = 6
            
            # Calculate heights for all multicells
            heights = {
                'row_num': self.get_multicell_height(str(row_num), cell_widths['row_num'], line_height),
                'desc': self.get_multicell_height(desc_text, cell_widths['desc'], line_height),
                'cas_no': self.get_multicell_height(cas_no, cell_widths['cas_no'], line_height),
                'method': self.get_multicell_height(method, cell_widths['method'], line_height),
                'ww_rl': self.get_multicell_height(ww_rl, cell_widths['ww_rl'], line_height),
                'ww_unit': self.get_multicell_height(ww_unit, cell_widths['ww_unit'], line_height),
                'inlet': self.get_multicell_height(inlet, cell_widths['inlet'], line_height),
                'outlet': self.get_multicell_height(outlet, cell_widths['outlet'], line_height),
                'sludge_rl': self.get_multicell_height(sludge_rl, cell_widths['sludge_rl'], line_height),
                'sludge_unit': self.get_multicell_height(sludge_unit, cell_widths['sludge_unit'], line_height),
                'test_result': self.get_multicell_height(test_result, cell_widths['test_result'], line_height)
            }
            
            # Find the maximum height
            max_height = max(heights.values())
            
            # Calculate how many lines we need to reach max_height
            lines_needed = max_height // line_height
            
            # Check if we need a new page
            if self.get_y() + max_height > self.page_break_trigger:
                self.add_page()
                self.set_y(66)
                self._draw_table_header()
                self.set_font("Calibri", "", 9)
            
            # Get starting position
            start_x = self.get_x()
            start_y = self.get_y()
             
            # Function to draw a cell with consistent height
            def draw_cell(x, y, width, height, text, align="C"):
                self.set_xy(x, y)
                # First draw the multicell content
                self.multi_cell(width, line_height, text, border=0, align=align)
                # Then draw the border rectangle to enforce consistent height
                self.rect(x, y, width, height)
            
            # Draw all cells with consistent height (max_height)
            draw_cell(start_x - 5, start_y, cell_widths['row_num'], max_height, str(row_num), "C")
            
            # Position for description
            draw_cell(start_x + 5, start_y, cell_widths['desc'], max_height, desc_text, "L")
            
            # Position for remaining cells
            current_x = start_x + 5 + cell_widths['desc']
            draw_cell(current_x, start_y, cell_widths['cas_no'], max_height, cas_no, "C")
            
            current_x += cell_widths['cas_no']
            draw_cell(current_x, start_y, cell_widths['method'], max_height, method, "C")
            
            current_x += cell_widths['method']
            draw_cell(current_x, start_y, cell_widths['ww_rl'], max_height, ww_rl, "C")
            
            current_x += cell_widths['ww_rl']
            draw_cell(current_x, start_y, cell_widths['ww_unit'], max_height, ww_unit, "C")
            
            current_x += cell_widths['ww_unit']
            draw_cell(current_x, start_y, cell_widths['inlet'], max_height, inlet, "C")
            
            current_x += cell_widths['inlet']
            draw_cell(current_x, start_y, cell_widths['outlet'], max_height, outlet, "C")
            
            current_x += cell_widths['outlet']
            draw_cell(current_x, start_y, cell_widths['sludge_rl'], max_height, sludge_rl, "C")
            
            current_x += cell_widths['sludge_rl']
            draw_cell(current_x, start_y, cell_widths['sludge_unit'], max_height, sludge_unit, "C")
            
            current_x += cell_widths['sludge_unit']
            draw_cell(current_x, start_y, cell_widths['test_result'], max_height, test_result, "C")
            
            # Update position
            self.set_y(start_y + max_height)
            
            
        def _draw_cov_table_header(self):
            """Draw the custom table header at current Y position"""
            
            self.set_fill_color(232, 232, 232)  # Light purple background
            self.set_font("Calibri", "B", 13) # Light purple background
            pdf.set_x(5)
            self.cell(200,8,"TEST RESULTS", border=True, align='C',ln=True,fill=True)
            # Save current Y position
            self.set_font("Calibri", "B", 9)
            # Save current Y position
            current_y = self.get_y()
            
            # First row of table header
            self.set_x(5)
            self.cell(10, 14, "Sr #", 1, align="C",fill=True)
            self.cell(46, 14, "Parameters/Analytes Description", 1, align="C",fill=True)
            self.cell(19, 14, "CAS NO", 1, align="C",fill=True)
            old_header_y = pdf.get_y()
            self.multi_cell(28, 7, "Methods/\nEquipment", 1, align="C",fill=True)
            pdf.set_y(old_header_y)
            
            # Wastewater and Sludge headers (merged cells)
            self.set_x(108)
            self.cell(58, 7, "Wastewater", 1, align="C",fill=True)
            self.cell(39, 7, "Sludge", 1, align="C",fill=True)
            
            # Second row of header (sub-headers)
            self.set_y(current_y + 7)  # Move down 7mm
            self.set_x(108)
            self.cell(12, 7, "¹F.L.", 1, align="C",fill=True)
            self.cell(12, 7, "Unit", 1, align="C",fill=True)
            self.cell(17, 7, "¹R.W./Inlet", 1, align="C",fill=True)
            self.cell(17, 7, "¹A.T./Outlet", 1, align="C",fill=True)
            self.cell(10, 7, "¹R.L.", 1, align="C",fill=True)
            self.cell(12, 7, "Unit", 1, align="C",fill=True)
            self.cell(17, 7, "Test results", 1, align="C",fill=True)
            
            # Reset position for data rows
            self.set_y(current_y + 14)
            
            # Reset position for data rows
            self.set_y(current_y + 14)    
            
        def add_cov_table_row(self, row_num, desc_text, cas_no, method, ww_rl, ww_unit, inlet, outlet, sludge_rl, sludge_unit, test_result):
            """Add a properly aligned table row with multicell support"""
            # Define cell widths
            pdf.set_font("Calibri", "", 9)
            cell_widths = {
                'row_num': 10,
                'desc': 46,
                'cas_no': 19,
                'method': 28,
                'ww_rl': 12,
                'ww_unit': 12,
                'inlet': 17,
                'outlet': 17,
                'sludge_rl': 10,
                'sludge_unit': 12,
                'test_result': 17
            }
            
            line_height = 6
            
            # Calculate heights for all multicells
            heights = {
                'row_num': self.get_multicell_height(str(row_num), cell_widths['row_num'], line_height),
                'desc': self.get_multicell_height(desc_text, cell_widths['desc'], line_height),
                'cas_no': self.get_multicell_height(cas_no, cell_widths['cas_no'], line_height),
                'method': self.get_multicell_height(method, cell_widths['method'], line_height),
                'ww_rl': self.get_multicell_height(ww_rl, cell_widths['ww_rl'], line_height),
                'ww_unit': self.get_multicell_height(ww_unit, cell_widths['ww_unit'], line_height),
                'inlet': self.get_multicell_height(inlet, cell_widths['inlet'], line_height),
                'outlet': self.get_multicell_height(outlet, cell_widths['outlet'], line_height),
                'sludge_rl': self.get_multicell_height(sludge_rl, cell_widths['sludge_rl'], line_height),
                'sludge_unit': self.get_multicell_height(sludge_unit, cell_widths['sludge_unit'], line_height),
                'test_result': self.get_multicell_height(test_result, cell_widths['test_result'], line_height)
            }
            
            # Find the maximum height
            max_height = max(heights.values())
            
            # Calculate how many lines we need to reach max_height
            lines_needed = max_height // line_height
            
            # Check if we need a new page
            if self.get_y() + max_height > self.page_break_trigger:
                self.add_page()
                self.set_y(65)
                self._draw_cov_table_header()
                self.set_font("Calibri", "", 9)
            
            # Get starting position
            start_x = self.get_x()
            start_y = self.get_y()
            
            # Function to draw a cell with consistent height
            def draw_cell(x, y, width, height, text, align="C"):
                self.set_xy(x, y)
                # First draw the multicell content
                self.multi_cell(width, line_height, text, border=0, align=align)
                # Then draw the border rectangle to enforce consistent height
                self.rect(x, y, width, height)
            
            # Draw all cells with consistent height (max_height)
            draw_cell(start_x - 5, start_y, cell_widths['row_num'], max_height, str(row_num), "C")
            
            # Position for description
            draw_cell(start_x + 5, start_y, cell_widths['desc'], max_height, desc_text, "L")
            
            # Position for remaining cells
            current_x = start_x + 5 + cell_widths['desc']
            draw_cell(current_x, start_y, cell_widths['cas_no'], max_height, cas_no, "C")
            
            current_x += cell_widths['cas_no']
            draw_cell(current_x, start_y, cell_widths['method'], max_height, method, "C")
            
            current_x += cell_widths['method']
            draw_cell(current_x, start_y, cell_widths['ww_rl'], max_height, ww_rl, "C")
            
            current_x += cell_widths['ww_rl']
            draw_cell(current_x, start_y, cell_widths['ww_unit'], max_height, ww_unit, "C")
            
            current_x += cell_widths['ww_unit']
            draw_cell(current_x, start_y, cell_widths['inlet'], max_height, inlet, "C")
            
            current_x += cell_widths['inlet']
            draw_cell(current_x, start_y, cell_widths['outlet'], max_height, outlet, "C")
            
            current_x += cell_widths['outlet']
            draw_cell(current_x, start_y, cell_widths['sludge_rl'], max_height, sludge_rl, "C")
            
            current_x += cell_widths['sludge_rl']
            draw_cell(current_x, start_y, cell_widths['sludge_unit'], max_height, sludge_unit, "C")
            
            current_x += cell_widths['sludge_unit']
            draw_cell(current_x, start_y, cell_widths['test_result'], max_height, test_result, "C")
            
            # Update position
            self.set_y(start_y + max_height)
        
        
        def add_aligned_row(self, texts, widths, aligns, borders, font_styles=None,is_bold_first=False):
            """
            Adds a row where ALL cells match the tallest cell's height automatically.
            Perfectly handles cases like sludge_2 with multiple lines.
            """
            line_height = 6  # Default matching add_table_row()
            
            # 1. Calculate height for EACH cell
            cell_heights = [
                self.get_multicell_height(text, width, line_height)
                for text, width in zip(texts, widths)
            ]
            row_height = max(cell_heights)  # Height for ALL cells in this row
            
            # 2. Save starting position
            x_start = self.get_x()
            y_start = self.get_y()
            
            # 3. Draw each cell with identical height
            for i, (text, width, align, border) in enumerate(zip(texts, widths, aligns, borders)):
                self.set_xy(x_start, y_start)
                
                if i == 0 and is_bold_first:
                    self.set_font("Calibri", "B", 9)
                else:
                    self.set_font("Calibri", "", 9)
                
                # Magic happens here - all cells use the same row_height
                self.multi_cell(
                    w=width, 
                    h=row_height/(self.get_multicell_height(text, width, line_height)/line_height),
                    txt=text, 
                    border=border,
                    align=align
                )
                x_start += width
            
            # 4. Move to next line
            self.set_y(y_start + row_height)
            self.set_x(self.l_margin)
            
        def footer(self):
            self.set_y(-14)
            self.set_fill_color(40, 25, 105)    
            self.rect(0, self.h-14, self.w, 12, "F")
            self.image("static/assets/Picture1.png", 5, self.h-16, 14, 14)
            self.set_text_color(255, 255, 255)
            self.set_font("Calibri", "", 8)
            self.text(18, self.h-6, txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,,+924232296099")
            
            self.text(18, self.h-10, txt="Head Office:345,First Flooer,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
            self.image("static/assets/earth.png", 165, self.h-12, 7, 7)
            self.text(175, self.h-6, txt="info@envitechal.com")
            self.text(175, self.h-10, txt="www.envitechal.com")
            
            
            
            
       
    # Create PDF instance
    pdf = PDFWithPageNumbers()
    pdf.set_auto_page_break(auto=True, margin=16) 
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Calibri", "B", 15)
    pdf.set_y(23)
    pdf.cell(0,25,text="ANALYTICAL TEST REPORT",align="C",ln=True)
    pdf.set_font("Calibri", "B", 15)
    pdf.set_y(60)
    pdf.cell(0,10,text="CUSTOMER DETAILS",border=False,ln=True, align="C")
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,14,text="Report To",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(108,7,text=f"{data.report_1}",ln=True,border=True)
    pdf.set_x(90)
    pdf.cell(108,7,text=f"{data.report_2}",border=True,ln=True)
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,14,text="Attention",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(108,7,text=f"{data.attention_1}",ln=True,border=True)
    pdf.set_x(90)
    pdf.cell(108,7,text=f"{data.attention_2}",border=True,ln=True)
    
    pdf.ln(2)
    pdf.set_font("Calibri", "B", 15)
    pdf.cell(0,10,text="SAMPLE DESCRIPTION ",border=False,ln=True, align="C")
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sample ID",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(54.5,7,text=f"{data.sample_id_1}",border=True)
    
    pdf.cell(54.5,7,text=f"{data.sample_id_2}",border=True,ln=True)
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sample Collection Date ",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(109,7,text=f"{data.sample_col_date}",border=True,ln=True)
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sample Description",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(54.5,7,text=f"{data.sample_des_1}",border=True)
    
    pdf.cell(54.5,7,text=f"{data.sample_des_2}",border=True,ln=True)
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sampling Method",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(54.5,7,text=f"{data.sample_method_1}",border=True)
    
    pdf.cell(54.5,7,text=f"{data.sample_method_2}",border=True,ln=True)
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sample Type",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(54.5,7,text=f"{data.sample_type_1}",border=True)
    
    pdf.cell(54.5,7,text=f"{data.sample_type_2}",border=True,ln=True)
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sampling Technique",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(54.5,7,text=f"{data.sample_tech_1}",border=True)
    
    pdf.cell(54.5,7,text=f"{data.sample_tech_2}",border=True,ln=True)
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Sample Collected by",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(109,7,text=f"{data.sample_col_by}",border=True,ln=True)
    
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Date of Analysis",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(109,7,text=f"{data.date_analysis} to {data.date_analysis_to}",border=True,ln=True)
    
    
    
    pdf.set_font("Calibri", "B", 9)
    pdf.cell(80,7,text="Test Description",border=True)
    
    pdf.set_font("Calibri", "", 9)
    pdf.cell(109,7,text=f"{data.test_desc}",border=True,ln=True)
    
    
    pdf.ln(2)
    pdf.set_font("Calibri", "B", 15)
    pdf.cell(0,10,text="Result Summary",border=False,ln=True, align="C")
    
    pdf.set_font("Calibri", "B", 9)
    
    pdf.cell(40,7,"Test Description",border=True)
    pdf.cell(40,7,"Raw Water/INLET",border=True,align='C')
    pdf.cell(65,7,"Wastewater After Treatment /OUTLET ",border=True,align='C')
    pdf.cell(40,7,"Sludge",border=True,ln=True,align='C')
    
    pdf.add_aligned_row(
        texts=["Conventional Parameters", data.raw_water_1, data.wastewater_1, data.sludge_1],
        widths=[40, 40, 65, 40],
        aligns=["L", "L", "L", "L"],
        borders=[1, 1, 1, 1],
        is_bold_first=True  # This makes first cell bold
    )

    pdf.add_aligned_row(
        texts=["Metals", data.raw_water_2, data.wastewater_2, data.sludge_2],
        widths=[40, 40, 65, 40],
        aligns=["L", "L", "L", "L"],
        borders=[1, 1, 1, 1],
        is_bold_first=True  # Bold for Metals
    )

    pdf.add_aligned_row(
        texts=["MRSL Parameters", data.raw_water_3, data.wastewater_3, data.sludge_3],
        widths=[40, 40, 65, 40],
        aligns=["L", "L", "L", "L"],
        borders=[1, 1, 1, 1],
        is_bold_first=True  # Bold for MRSL
    )
    
    
    pdf.image(data.analyst_signature.signature,30,231,20.32,20.32)
    pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({data.analyst_signature.role})"),250)
    pdf.text(26,253,f"Analyzed By ({data.analyst_signature.role})")
    pdf.image(data.assistant_manager_signature.signature,100,232,20.32,20.32)
    pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({data.assistant_manager_signature.role})"),250)
    pdf.text(87.5,253,f"Reviewed By ({data.assistant_manager_signature.role})")
    pdf.image(envitech_logo,154,228,22,22)
    pdf.image(data.lab_manager_signature.signature,178,233,20.32,20.32)
    pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({data.lab_manager_signature.role})"),250)
    pdf.text(160,253,f"Approved By ({data.lab_manager_signature.role})")


    pdf.set_font("Calibri","B", 9)
    pdf.line(10,257,-10+pdf.w,257)
    pdf.text(10,262,txt="Disclaimer:")
    pdf.set_font("Calibri","", 8)
    pdf.text(10,266,txt="• Report is valid for current batch (sample).")
    pdf.text(10,269,txt="• This report is not valid for any publication or judcial purpose.")
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
    if data.location == "SEQS":
         pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
    if data.location == "PEQS":
         pdf.image('static/assets/EPA_updated.png',155,258,21,17)
    if data.location == "NEQS":
         pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
    if data.location =='PEQS':
         pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
    else:
         pdf.text(152,276,txt="(LAB/L.C/ENVI TECH AL-2/20/93/2024)")
    pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
    pdf.text(128.5,276,txt="(Certificate # 080177324-QMS)")
    
    
    pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

    pdf.set_font("Calibri","", 7)
    pdf.rect(126,277,25,5)
    pdf.text(128,280,txt=data.doc_1)
    pdf.rect(151,277,29,5)
    pdf.text(155,280,txt=data.doc_2)
    pdf.rect(180,277,25,5)
    pdf.text(183.5,280,txt=data.doc_3)
    
    
    def table_header():
        pdf.set_font("Calibri", "B", 9)
        pdf.set_fill_color(232, 232, 232)  # Light purple background
        pdf.set_font("Calibri", "B", 13) # Light purple background
        pdf.set_x(5)
        pdf.cell(200,8,"TEST RESULTS", border=True, align='C',ln=True,fill=True)
        # Save current Y position
        pdf.set_font("Calibri", "B", 9)
        
        # Save current Y position
        current_y = pdf.get_y()
        
        # First row of table header
        pdf.set_x(5)
        pdf.cell(10, 14, "Sr #", 1, align="C",fill=True)
        pdf.cell(46, 14, "Parameters/Analytes Description", 1, align="C",fill=True)
        pdf.cell(19, 14, "CAS NO", 1, align="C",fill=True)
        old_header_y = pdf.get_y()
        pdf.multi_cell(28, 7, "Methods/\nEquipment", 1, align="C",fill=True)
        pdf.set_y(old_header_y)
        
        # Wastewater and Sludge headers (merged cells)
        pdf.set_x(108)
        pdf.cell(58, 7, "Wastewater", 1, align="C",fill=True)
        pdf.cell(39, 7, "Sludge", 1, align="C",fill=True)
        
        # Second row of header (sub-headers)
        pdf.set_y(current_y + 7)  # Move down 7mm
        pdf.set_x(108)
        pdf.cell(12, 7, "¹R.L.", 1, align="C",fill=True)
        pdf.cell(12, 7, "Unit", 1, align="C",fill=True)
        pdf.cell(17, 7, "¹R.W./Inlet", 1, align="C",fill=True)
        pdf.cell(17, 7, "¹A.T./Outlet", 1, align="C",fill=True)
        pdf.cell(10, 7, "¹R.L.", 1, align="C",fill=True)
        pdf.cell(12, 7, "Unit", 1, align="C",fill=True)
        pdf.cell(17, 7, "Test results", 1, align="C",fill=True)
        
        # Reset position for data rows
        pdf.set_y(current_y + 14)
        
        # Reset position for data rows
        pdf.set_y(current_y + 14)
        
        
    pdf.add_page()
    
    pdf.set_font("Calibri","B", 9)
    
    pdf.set_y(65)
    table_header()
    
    
    def check_page_break(pdf, row_height):
        """Check if we need a new page and add one if needed"""
        if pdf.get_y() + row_height > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(65)  # Reset Y position after page break
            pdf._draw_table_header()
            pdf.set_font("Calibri", "", 9)
        return pdf.get_y()  # Return current Y position
    
    
    
    
   
    
    pdf.set_x(5)
    pdf.cell(200,7,"1. Alkylphenols (AP'S) / Alkylphenol ethoxylates (APEO'S)",border=1,ln=True)
    pdf.set_font("Calibri","", 9)
    
    
    pdf.add_table_row(
        "1.1", 
        "Nonylphenol (n-nonyl and Isononyl)", 
        "Various \n11066-49-2 \n25154-52-3 \n104-40-5 \n90481-04-2 \n84852-15-3", 
        "LC/MS", 
        "1", 
        "µg/l", 
        data.inlet['inlet_1'], 
        data.outlet['outlet_1'], 
        "0.4", 
        "mg/kg", 
        data.test['test_1']
    )
    
    pdf.add_table_row(
        "1.2", 
        "Octyl phenol (n-octyl and Isooctyl)", 
        "Various \n140-66-9 \n27193-28-8 \n1806-26-4", 
        "LC/MS", 
        "1", 
        "µg/l", 
        data.inlet['inlet_2'], 
        data.outlet['outlet_2'], 
        "0.4", 
        "mg/kg", 
        data.test['test_2']
    )
    
    pdf.add_table_row(
        "1.3", 
        "Heptyl phenol (branched and linear)", 
        "Various", 
        "LC/MS", 
        "-", 
        "µg/l", 
        data.inlet['inlet_3'], 
        data.outlet['outlet_3'], 
        "-", 
        "mg/kg", 
        data.test['test_3']
    )
    
    pdf.add_table_row(
        "1.4", 
        "Pentylphenol (branched & linear)", 
        "Various", 
        "LC/MS", 
        "-", 
        "µg/l", 
        data.inlet['inlet_4'], 
        data.outlet['outlet_4'], 
        "-", 
        "mg/kg", 
        data.test['test_4']
    )
    
    pdf.add_table_row(
        "1.5", 
        "Nonylphenol ethoxylates", 
        "Various \n9016-45-9 \n26027-38-3 \n68412-54-4 \n127087-87-0 37205-87-1", 
        "LC/MS", 
        "1", 
        "µg/l", 
        data.inlet['inlet_5'], 
        data.outlet['outlet_5'], 
        "0.4", 
        "mg/kg", 
        data.test['test_5']
    )
    
    pdf.add_table_row(
        "1.6", 
        "Octylphenolethoxylates (OPEO) (n-octyl and iso- octyl)", 
        "Various \n9002-93-1 \n9036-19-5 \n68987-90-6", 
        "LC/MS", 
        "1", 
        "µg/l", 
        data.inlet['inlet_6'], 
        data.outlet['outlet_6'], 
        "0.4", 
        "mg/kg", 
        data.test['test_6']
    )
    
    
    extra_field = safe_load(data.extra_field)
    extra_field_2 = safe_load(data.extra_field_2)
    extra_field_3 = safe_load(data.extra_field_3)
    extra_field_3_1 = safe_load(data.extra_field_3_1)
    extra_field_4 = safe_load(data.extra_field_4)
    extra_field_4_1 = safe_load(data.extra_field_4_1)
    extra_field_5 = safe_load(data.extra_field_5)
    extra_field_6 = safe_load(data.extra_field_6)
    extra_field_7 = safe_load(data.extra_field_7)
    extra_field_8 = safe_load(data.extra_field_8)
    extra_field_8_1 = safe_load(data.extra_field_8_1)
    extra_field_9 = safe_load(data.extra_field_9)
    extra_field_10 = safe_load(data.extra_field_10)
    extra_field_11 = safe_load(data.extra_field_11)
    extra_field_12 = safe_load(data.extra_field_12)
    extra_field_13 = safe_load(data.extra_field_13)
    extra_field_14 = safe_load(data.extra_field_14)
    extra_field_15 = safe_load(data.extra_field_15)
    extra_field_16 = safe_load(data.extra_field_16)
    extra_field_17 = safe_load(data.extra_field_17)
    
    if extra_field:
        for i in extra_field:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
            )
        
     # # 2. Phthalates section header
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "2. Phthalates", border=1, ln=True)
    
    pdf.set_font("Calibri", "", 9)
    
    phthalate_data = [
        ("2.1", "Benzyl butyl phthalate (BBP)", "85-68-7", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_7']}", f"{data.outlet['outlet_7']}", "-", "mg/kg", f"{data.test['test_7']}"),
        ("2.2", "Dibutyl phthalate (DBP)", "84-74-2", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_8']}", f"{data.outlet['outlet_8']}", "-", "mg/kg", f"{data.test['test_8']}"),
        ("2.3", "Diethyl Phthalate (DEP)", "84-66-2", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_9']}", f"{data.outlet['outlet_9']}", "-", "mg/kg", f"{data.test['test_9']}"),
        ("2.4", "Dimethyl phthalate (DMP)", "131-11-3", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_10']}", f"{data.outlet['outlet_10']}", "-", "mg/kg", f"{data.test['test_10']}"),
        ("2.5", "Di-(2-ethylhexyl) phthalate (DEHP)", "117-81-7", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_11']}", f"{data.outlet['outlet_11']}", "-", "mg/kg", f"{data.test['test_11']}"),
        ("2.6", "Di-(2-methoxy ethyl) phthalate (DMEP)", "117-82-8", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_12']}", f"{data.outlet['outlet_12']}", "-", "mg/kg", f"{data.test['test_12']}"),
        ("2.7", "Di-C6-8-branched alkyl phthalates (DIHP)", "71888-89-6", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_13']}", f"{data.outlet['outlet_13']}", "-", "mg/kg", f"{data.test['test_13']}"),
        ("2.8", "Di-C7-11-branched alkyl phthalates (DHNUP)", "68515-42-4", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_14']}", f"{data.outlet['outlet_14']}", "-", "mg/kg", f"{data.test['test_14']}"),
        ("2.9", "Dicyclo hexyl phthalates (DCHP)", "84-61-7", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_15']}", f"{data.outlet['outlet_15']}", "-", "mg/kg", f"{data.test['test_15']}"),
        ("2.10", "Dihexylphthalates, branched and linear (DHxP)", "68515-50-4", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_16']}", f"{data.outlet['outlet_16']}", "-", "mg/kg", f"{data.test['test_16']}"),
        ("2.11", "Di-iso-butyl phthalate (DIBP)", "84-69-5", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_17']}", f"{data.outlet['outlet_17']}", "-", "mg/kg", f"{data.test['test_17']}"),
        ("2.12", "Di-iso-hexylphthalate (DIHxP)", "71850-09-4", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_18']}", f"{data.outlet['outlet_18']}", "-", "mg/kg", f"{data.test['test_18']}"),
        ("2.13", "Di-iso-octyl phthalate (DIOP)", "27554-26-3", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_19']}", f"{data.outlet['outlet_19']}", "-", "mg/kg", f"{data.test['test_19']}"),
        ("2.14", "Di-iso-nonyl phthalate (DINP)", "28553-12-0 \n68515-48-0", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_20']}", f"{data.outlet['outlet_20']}", "-", "mg/kg", f"{data.test['test_20']}"),
        ("2.15", "Di-iso-decyl phthalate (DIDP)", "26761-40-0 \n68515-49-1", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_21']}", f"{data.outlet['outlet_21']}", "-", "mg/kg", f"{data.test['test_21']}"),
        ("2.16", "Di-n-propyl phthalate (DPP)", "131-16-8", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_22']}", f"{data.outlet['outlet_22']}", "-", "mg/kg", f"{data.test['test_22']}"),
        ("2.17", "Di-n-hexylphthalate (DHP)", "84-75-3", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_23']}", f"{data.outlet['outlet_23']}", "-", "mg/kg", f"{data.test['test_23']}"),
        ("2.18", "Di-n-octylphthalate (DNOP)", "117-84-0", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_24']}", f"{data.outlet['outlet_24']}", "-", "mg/kg", f"{data.test['test_24']}"),
        ("2.19", "Di-n-nonylphthalate (DNP)", "84-76-4", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_25']}", f"{data.outlet['outlet_25']}", "-", "mg/kg", f"{data.test['test_25']}"),
        #("2.20", "Di-n-pentylphthalate (DPP)", "131-18-0", "GC/MS", "2", "µg/l", f"{data.inlet['inlet_26']}", f"{data.outlet['outlet_26']}", "-", "mg/kg", f"{data.test['test_26']}"),
        
    ]
    for row in phthalate_data:
        pdf.add_table_row(*row)
        
    pdf.set_x(5)    
    pdf.cell(10,35,"2.20",border=True,align="C")
    pdf.cell(46,7,"Di-n-pentylphthalate (DPP)",border=True,align="L")
    pdf.cell(19,7,"131-180 ",border=True,align="C")
    pdf.cell(28,7,"GC/MS",border=True,align="C")
    pdf.cell(12,7,"2",border=True,align="C")
    pdf.cell(12,7,"µg/l",border=True,align="C")
    pdf.cell(17,7,f"{data.inlet['inlet_26']}",border=True,align="C")
    pdf.cell(17,7,f"{data.outlet['outlet_26']}",border=True,align="C")
    pdf.cell(10,7,"-",border=True,align="C")
    pdf.cell(12,7,"mg/kg",border=True,align="C")
    pdf.cell(17,7,f"{data.test['test_26']}",border=True,align="C",ln=True)
    
    
    pdf.set_x(15)
    pdf.cell(46,7,"Di-iso-pentylphthalate (DPP)",border=True,align="L")
    pdf.cell(19,7,"605-505",border=True,align="C")
    pdf.cell(28,7,"GC/MS",border=True,align="C")
    pdf.cell(12,7,"2",border=True,align="C")
    pdf.cell(12,7,"µg/l",border=True,align="C")
    pdf.cell(17,7,f"{data.inlet['inlet_27']}",border=True,align="C")
    pdf.cell(17,7,f"{data.outlet['outlet_27']}",border=True,align="C")
    pdf.cell(10,7,"-",border=True,align="C")
    pdf.cell(12,7,"mg/kg",border=True,align="C")
    pdf.cell(17,7,f"{data.test['test_27']}",border=True,align="C",ln=True)
    
    pdf.set_x(15)
    reset_y =pdf.get_y()
    pdf.multi_cell(46,7,"Dipentylphthalate, branched and linear (DPP)",border=True,align="L")
    pdf.set_y(reset_y)
    pdf.set_x(61)
    pdf.cell(19,14,"8477706-0 ",border=True,align="C")
    pdf.cell(28,14,"GC/MS",border=True,align="C")
    pdf.cell(12,14,"2",border=True,align="C")
    pdf.cell(12,14,"µg/l",border=True,align="C")
    pdf.cell(17,14,f"{data.inlet['inlet_28']}",border=True,align="C")
    pdf.cell(17,14,f"{data.outlet['outlet_28']}",border=True,align="C")
    pdf.cell(10,14,"-",border=True,align="C")
    pdf.cell(12,14,"mg/kg",border=True,align="C")
    pdf.cell(17,14,f"{data.test['test_28']}",border=True,align="C",ln=True)
    
    pdf.set_x(15)

    pdf.cell(446,7,"Iso-pentyl-n-pentylphthalate (DPP)",border=True,align="L")
    pdf.cell(19,7,"77629769-9",border=True,align="C")
    pdf.cell(28,7,"GC/MS",border=True,align="C")
    pdf.cell(12,7,"2",border=True,align="C")
    pdf.cell(12,7,"µg/l",border=True,align="C")
    pdf.cell(17,7,f"{data.inlet['inlet_29']}",border=True,align="C")
    pdf.cell(17,7,f"{data.outlet['outlet_29']}",border=True,align="C")
    pdf.cell(10,7,"-",border=True,align="C")
    pdf.cell(12,7,"mg/kg",border=True,align="C")
    pdf.cell(17,7,f"{data.test['test_29']}",border=True,align="C",ln=True)
    
    
    phthalate_2nd =[
        ("2.21", "1,2-benzenedicarboxylic acid, di-C6-10-alkyl esters", "68515-51-5", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_30']}", f"{data.outlet['outlet_30']}", "-", "mg/kg", f"{data.test['test_30']}"),
        ("2.22", "1,2-benzenedicarboxylic acid, mixed decyl-, and hexyl, and octylesters", "68648-93-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_31']}", f"{data.outlet['outlet_31']}", "-", "mg/kg", f"{data.test['test_31']}")
    ]
    for row in phthalate_2nd:
        pdf.add_table_row(*row)
    
    
        
    if extra_field_2:
        for i in extra_field_2:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
            )
            
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "3. Brominated, Chlorinated and Other flame Retardants ", border=1, ln=True)
    
    pdf.set_font("Calibri", "", 9)
    
    flame_retardant_data = [
        ("3.1", "Polybromobiphenyles (PBBs)", "59536-65-1", "GC/MS", "sum 5", "µg/l", f"{data.inlet['inlet_32']}", f"{data.outlet['outlet_32']}", "-", "mg/kg", f"{data.test['test_32']}"),
        ("3.2", "Monobromobiphenyls (MonoBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_33']}", f"{data.outlet['outlet_33']}", "-", "mg/kg", f"{data.test['test_33']}"),
        ("3.3", "Dibromobiphenyls (DiBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_34']}", f"{data.outlet['outlet_34']}", "-", "mg/kg", f"{data.test['test_34']}"),
        ("3.4", "Tribromobiphenyls (TriBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_35']}", f"{data.outlet['outlet_35']}", "-", "mg/kg", f"{data.test['test_35']}"),
        ("3.5", "Tetrabromobiphenyls (TetraBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_36']}", f"{data.outlet['outlet_36']}", "-", "mg/kg", f"{data.test['test_36']}"),
        ("3.6", "Pentabromobiphenyls (PentaBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_37']}", f"{data.outlet['outlet_37']}", "-", "mg/kg", f"{data.test['test_37']}"),
        ("3.7", "Hexabromobiphenyls (HexaBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_38']}", f"{data.outlet['outlet_38']}", "-", "mg/kg", f"{data.test['test_38']}"),
        ("3.8", "Heptabromobiphenyls (HeptaBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_39']}", f"{data.outlet['outlet_39']}", "-", "mg/kg", f"{data.test['test_39']}"),
        ("3.9", "Octabromobiphenyls (OctaBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_40']}", f"{data.outlet['outlet_40']}", "-", "mg/kg", f"{data.test['test_40']}"),
        ("3.10", "Nonabromobiphenyls (NonaBB)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_41']}", f"{data.outlet['outlet_41']}", "-", "mg/kg", f"{data.test['test_41']}"),
        ("3.11", "Decabromobiphenyl (DecaBB)", "13654-09-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_42']}", f"{data.outlet['outlet_42']}", "-", "mg/kg", f"{data.test['test_42']}"),
        ("3.12", "Polybrominated diphenyl ethers (PBDEs)", "Various", "GC/MS", "sum 5", "µg/l", f"{data.inlet['inlet_43']}", f"{data.outlet['outlet_43']}", "-", "mg/kg", f"{data.test['test_43']}"),
        ("3.13", "Monobromodiphenylethers (MonoBDEs)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_44']}", f"{data.outlet['outlet_44']}", "-", "mg/kg", f"{data.test['test_44']}"),
        ("3.14", "Dibromodiphenylethers (DiBDEs)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_45']}", f"{data.outlet['outlet_45']}", "-", "mg/kg", f"{data.test['test_45']}"),
        ("3.15", "Tribromodiphenylethers (TriBDEs)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_46']}", f"{data.outlet['outlet_46']}", "-", "mg/kg", f"{data.test['test_46']}"),
        ("3.16", "Tetabromodiphenylethers (TetraBDEs)", "Various \n40088-47-9", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_47']}", f"{data.outlet['outlet_47']}", "-", "mg/kg", f"{data.test['test_47']}"),
        ("3.17", "Pentabromodiphenylethers (PentaBDEs)", "Various \n32534-81-", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_48']}", f"{data.outlet['outlet_48']}", "-", "mg/kg", f"{data.test['test_48']}"),
        ("3.18", "Hexabromodiphenylethers (HexaBDEs)", "Various \n36483-60-0", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_49']}", f"{data.outlet['outlet_49']}", "-", "mg/kg", f"{data.test['test_49']}"),
        ("3.19", "Heptabromodiphenylethers (HeptaBDEs)", "Various \n68928-80-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_50']}", f"{data.outlet['outlet_50']}", "-", "mg/kg", f"{data.test['test_50']}"),
        ("3.20", "Octabromodiphenylethers (OctaBDEs)", "Various \n32536-52-0", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_51']}", f"{data.outlet['outlet_51']}", "-", "mg/kg", f"{data.test['test_51']}"),
        ("3.21", "Nonabromodiphenylethers (NonaBDEs)", "Various \n63936-56-1", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_52']}", f"{data.outlet['outlet_52']}", "-", "mg/kg", f"{data.test['test_52']}"),
        ("3.22", "Decabromodiphenylether (DecaBDE)", "10043-35-3 \n11113-50-15", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_53']}", f"{data.outlet['outlet_53']}", "-", "mg/kg", f"{data.test['test_53']}"),
        ("3.23", "Tri-(2,3 dibromo propyl) phosphate (TRIS)", "126-72-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_54']}", f"{data.outlet['outlet_54']}", "-", "mg/kg", f"{data.test['test_54']}"),
        ("3.24", "Tris(2-chloroethyl) phosphate (TCEP)", "115-96-8", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_55']}", f"{data.outlet['outlet_55']}", "-", "mg/kg", f"{data.test['test_55']}"),
        ("3.25", "3,5,3',5'-Tetrabromo-bisphenol A (TBBA)", "79-94-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_56']}", f"{data.outlet['outlet_56']}", "-", "mg/kg", f"{data.test['test_56']}"),
        ("3.26", "Hexabromocyclododecane (HBCDD) and all main diastereomeres identified (alpha-, beta-, gamma-)", "Various", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_57']}", f"{data.outlet['outlet_57']}", "-", "mg/kg", f"{data.test['test_57']}"),
        ("3.27", "Bis(2,3-dibromopropyl) phosphate (BIS)", "5412-25-9", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_58']}", f"{data.outlet['outlet_58']}", "-", "mg/kg", f"{data.test['test_58']}"),
        ("3.28", "2,2-Bis(bromomethyl)-1,3-propanediol (BBMP)", "3296-90-0", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_59']}", f"{data.outlet['outlet_59']}", "-", "mg/kg", f"{data.test['test_59']}")
    ]

    for row in flame_retardant_data:
        pdf.add_table_row(*row)   
        
    if extra_field_3:
        for i in extra_field_3:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
            )
    
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "3.Other Flame Retardants ", border=1, ln=True)
    
    pdf.set_font("Calibri", "", 9)
    
    flame_retardant_data_continued = [
        ("3.29", "Tris(1,3-dichlorisopropyl) phosphate (TDCPP)", "13674-87-8", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_60']}", f"{data.outlet['outlet_60']}", "-", "mg/kg", f"{data.test['test_60']}"),
        ("3.30", "Tris(2-chloro-1-methylethyl) phosphate (TCPP)", "13674-84-5", "LC/MS", "25", "µg/l", f"{data.inlet['inlet_61']}", f"{data.outlet['outlet_61']}", "-", "mg/kg", f"{data.test['test_61']}"),
        ("3.31", "Tris-(aziridinyl)-phosphinoxide (TEPA)", "545-55-1", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_62']}", f"{data.outlet['outlet_62']}", "-", "mg/kg", f"{data.test['test_62']}"),
        ("3.32", "Borate, Zinc Salt", "12767-90-7", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_63']}", f"{data.outlet['outlet_63']}", "-", "mg/kg", f"{data.test['test_63']}"),
        ("3.33", "Boric acid", "Various", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_64']}", f"{data.outlet['outlet_64']}", "-", "mg/kg", f"{data.test['test_64']}"),
        ("3.34", "Diboron trioxide", "1303-86-2", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_65']}", f"{data.outlet['outlet_65']}", "-", "mg/kg", f"{data.test['test_65']}"),
        ("3.35", "Disodium tetraborate, anhydrous", "1303-96-4 \n1330-43-4 \n12179-04-3", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_66']}", f"{data.outlet['outlet_66']}", "-", "mg/kg", f"{data.test['test_66']}"),
        ("3.36", "Disodium octaborate", "12008-41-2", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_67']}", f"{data.outlet['outlet_67']}", "-", "mg/kg", f"{data.test['test_67']}"),
        ("3.37", "Tetraboron disodium heptaoxide, hydrate", "12267-73-1", "ICP", "100⁷", "µg/l", f"{data.inlet['inlet_68']}", f"{data.outlet['outlet_68']}", "-", "mg/kg", f"{data.test['test_68']}"),
        ("3.38", "Dibromopropylether", "21850-44-2", "ICP", "25", "µg/l", f"{data.inlet['inlet_69']}", f"{data.outlet['outlet_69']}", "-", "mg/kg", f"{data.test['test_69']}"),
        ("3.39", "Flame retardants which contain toxic metals like antimony or arsenic", "Various", "ICP", "-", "µg/l", f"{data.inlet['inlet_70']}", f"{data.outlet['outlet_70']}", "-", "mg/kg", f"{data.test['test_70']}"),
        ("3.40", "Antimony trioxide", "1309-64-4", "ICP", "-", "µg/l", f"{data.inlet['inlet_71']}", f"{data.outlet['outlet_71']}", "-", "mg/kg", f"{data.test['test_71']}"),
        ("3.41", "Antimony pentoxide", "1314-60-9", "ICP", "-", "µg/l", f"{data.inlet['inlet_72']}", f"{data.outlet['outlet_72']}", "-", "mg/kg", f"{data.test['test_72']}"),
        ("3.42", "Tri-o-cresyl phosphate", "78-30-8", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_73']}", f"{data.outlet['outlet_73']}", "-", "mg/kg", f"{data.test['test_73']}"),
        ("3.43", "Trixylyl phosphate", "25155-23-1", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_74']}", f"{data.outlet['outlet_74']}", "-", "mg/kg", f"{data.test['test_74']}")
    ]

    for row in flame_retardant_data_continued:
        pdf.add_table_row(*row)
    
    
    if extra_field_3_1:
        for i in extra_field_3_1:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
            )
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "4.Hazardous Colorants", border=1, ln=True)
    pdf.set_x(5)
    pdf.cell(200, 7, "Arylamines (Released from Azo colorants or in free manner) ", border=1, ln=True)
    
    pdf.set_font("Calibri", "", 9)       
    aromatic_amines_data = [
        ("4.1", "4-Aminobiphenyl", "92-67-1", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_75']}", f"{data.outlet['outlet_75']}", "-", "mg/kg", f"{data.test['test_75']}"),
            ("4.2", "Benzidine", "92-87-5", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_76']}", f"{data.outlet['outlet_76']}", "-", "mg/kg", f"{data.test['test_76']}"),
            ("4.3", "4-Chloro-o-toluidine", "95-69-2", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_77']}", f"{data.outlet['outlet_77']}", "-", "mg/kg", f"{data.test['test_77']}"),
            ("4.4", "2-Naphthylamine", "91-59-8", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_78']}", f"{data.outlet['outlet_78']}", "-", "mg/kg", f"{data.test['test_78']}"),
            ("4.5", "o-Aminoazotoluene", "97-56-3", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_79']}", f"{data.outlet['outlet_79']}", "-", "mg/kg", f"{data.test['test_79']}"),
            ("4.6", "2-Amino-4-nitrotoluene", "99-55-8", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_80']}", f"{data.outlet['outlet_80']}", "-", "mg/kg", f"{data.test['test_80']}"),
            ("4.7", "4-Chloroaniline", "106-47-8", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_81']}", f"{data.outlet['outlet_81']}", "-", "mg/kg", f"{data.test['test_81']}"),
            ("4.8", "2,4-Diaminoanisole", "615-05-4", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_82']}", f"{data.outlet['outlet_82']}", "-", "mg/kg", f"{data.test['test_82']}"),
            ("4.9", "4,4'-Diaminodiphenylmethane", "101-77-9", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_83']}", f"{data.outlet['outlet_83']}", "-", "mg/kg", f"{data.test['test_83']}"),
            ("4.10", "3,3'-Dichlorobenzidine", "91-94-1", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_84']}", f"{data.outlet['outlet_84']}", "-", "mg/kg", f"{data.test['test_84']}"),
            ("4.11", "3,3'-Dimethoxybenzidine", "119-90-4", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_85']}", f"{data.outlet['outlet_85']}", "-", "mg/kg", f"{data.test['test_85']}"),
            ("4.12", "3,3'-Dimethylbenzidine", "119-93-7", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_86']}", f"{data.outlet['outlet_86']}", "-", "mg/kg", f"{data.test['test_86']}"),
            ("4.13", "4,4'-Methylenedi-o-toluidine", "838-88-0", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_87']}", f"{data.outlet['outlet_87']}", "-", "mg/kg", f"{data.test['test_87']}"),
            ("4.14", "p-Cresidine; 6-Methoxy-m-toluidine", "120-71-8", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_88']}", f"{data.outlet['outlet_88']}", "-", "mg/kg", f"{data.test['test_88']}"),
            ("4.15", "4,4'-Methylene-bis-(2-chloroaniline)", "101-14-4", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_89']}", f"{data.outlet['outlet_89']}", "-", "mg/kg", f"{data.test['test_89']}"),
            ("4.16", "4,4'-Oxydianiline", "101-80-4", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_90']}", f"{data.outlet['outlet_90']}", "-", "mg/kg", f"{data.test['test_90']}"),
            ("4.17", "4,4'-Thiodianiline", "139-65-1", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_91']}", f"{data.outlet['outlet_91']}", "-", "mg/kg", f"{data.test['test_91']}"),
            ("4.18", "o-Toluidine", "95-53-4", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_92']}", f"{data.outlet['outlet_92']}", "-", "mg/kg", f"{data.test['test_92']}"),
            ("4.19", "2,4-Toluylendiamine", "95-80-7", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_93']}", f"{data.outlet['outlet_93']}", "-", "mg/kg", f"{data.test['test_93']}"),
            ("4.20", "2,4,5-Trimethylaniline", "137-17-7", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_94']}", f"{data.outlet['outlet_94']}", "-", "mg/kg", f"{data.test['test_94']}"),
            ("4.21", "o-Anisidine (2-Methoxyaniline)", "90-04-0", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_95']}", f"{data.outlet['outlet_95']}", "-", "mg/kg", f"{data.test['test_95']}"),
            ("4.22", "4-Aminoazobenzene", "60-09-3", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_96']}", f"{data.outlet['outlet_96']}", "-", "mg/kg", f"{data.test['test_96']}"),
            ("4.23", "2,4-Xylidine", "95-68-1", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_97']}", f"{data.outlet['outlet_97']}", "-", "mg/kg", f"{data.test['test_97']}"),
            ("4.24", "2,6-Xylidine", "87-62-7", "GC/MS & HPLC", "0.1", "µg/l", f"{data.inlet['inlet_98']}", f"{data.outlet['outlet_98']}", "-", "mg/kg", f"{data.test['test_98']}"),
            ("4.25", "2,5-Diaminotoluene / 2-Methyl-p-phenylenediamine", "615-50-9", "GC/MS & HPLC", "-", "µg/l", f"{data.inlet['inlet_99']}", f"{data.outlet['outlet_99']}", "-", "mg/kg", f"{data.test['test_99']}"),
            ("4.26", "4-Ethoxyaniline / p-Phenetidine", "156-43-4", "GC/MS & HPLC", "-", "µg/l", f"{data.inlet['inlet_100']}", f"{data.outlet['outlet_100']}", "-", "mg/kg", f"{data.test['test_100']}"),
            ("4.27", "3,3-Diaminobenzidine", "91-95-2", "GC/MS & HPLC", "-", "µg/l", f"{data.inlet['inlet_101']}", f"{data.outlet['outlet_101']}", "-", "mg/kg", f"{data.test['test_101']}"),
            ("4.28", "Aniline", "62-53-3", "GC/MS & HPLC", "-", "µg/l", f"{data.inlet['inlet_102']}", f"{data.outlet['outlet_102']}", "-", "mg/kg", f"{data.test['test_102']}")
        ]

    for row in aromatic_amines_data:
        pdf.add_table_row(*row)
        
        
        
    if extra_field_4:
        for i in extra_field_4:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
    
            )
            
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "4. HazardouS COlorants (Carcinogenic, allergenic, or banned fOr other reasons) ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9)         
            
    hazardous_colorants_data = [
            ("4.29", "C.I. Acid Red 26 (C.I. 16150)", "3761-53-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_103']}", f"{data.outlet['outlet_103']}", "-", "mg/kg", f"{data.test['test_103']}"),
            ("4.30", "C.I. Acid Red 114", "6459-94-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_104']}", f"{data.outlet['outlet_104']}", "-", "mg/kg", f"{data.test['test_104']}"),
            ("4.31", "C.I. Acid Violet 49", "1694-09-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_105']}", f"{data.outlet['outlet_105']}", "-", "mg/kg", f"{data.test['test_105']}"),
            ("4.32", "C.I. Basic Blue 26", "2580-56-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_106']}", f"{data.outlet['outlet_106']}", "-", "mg/kg", f"{data.test['test_106']}"),
            ("4.33", "C.I. Basic Green 4 (Chloride)", "569-64-2", "LC/DAD/MS", "sum 1", "µg/l", f"{data.inlet['inlet_107']}", f"{data.outlet['outlet_107']}", "-", "mg/kg", f"{data.test['test_107']}"),
            ("4.34", "C.I. Basic Green 4 (Free)", "10309-95-2", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_108']}", f"{data.outlet['outlet_108']}", "-", "mg/kg", f"{data.test['test_108']}"),
            ("4.35", "C.I. Basic Green 4 (Oxalate)", "2437-29-8 \n18015-76-4", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_109']}", f"{data.outlet['outlet_109']}", "-", "mg/kg", f"{data.test['test_109']}"),
            ("4.36", "C.I. Basic Red 9 (C.I. 42500)", "569-61-9", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_110']}", f"{data.outlet['outlet_110']}", "-", "mg/kg", f"{data.test['test_110']}"),
            ("4.37", "C.I. Basic Violet 1", "8004-87-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_111']}", f"{data.outlet['outlet_111']}", "-", "mg/kg", f"{data.test['test_111']}"),
            ("4.38", "C.I. Basic Violet 3", "548-62-9", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_112']}", f"{data.outlet['outlet_112']}", "-", "mg/kg", f"{data.test['test_112']}"),
            ("4.39", "C.I. Basic Violet 14 (C.I. 42510)", "632-99-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_113']}", f"{data.outlet['outlet_113']}", "-", "mg/kg", f"{data.test['test_113']}"),
            ("4.40", "C.I. Direct Black 38 (C.I. 30235)", "1937-37-7", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_114']}", f"{data.outlet['outlet_114']}", "-", "mg/kg", f"{data.test['test_114']}"),
            ("4.41", "C.I. Direct Blue 6 (C.I. 22610)", "2602-46-2", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_115']}", f"{data.outlet['outlet_115']}", "-", "mg/kg", f"{data.test['test_115']}"),
            ("4.42", "C.I. Direct Blue 15", "2429-74-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_116']}", f"{data.outlet['outlet_116']}", "-", "mg/kg", f"{data.test['test_116']}"),
            ("4.43", "C.I. Direct Blue 218", "28407-37-6", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_117']}", f"{data.outlet['outlet_117']}", "-", "mg/kg", f"{data.test['test_117']}"),
            ("4.44", "C.I. Direct Brown 95", "16071-86-6", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_118']}", f"{data.outlet['outlet_118']}", "-", "mg/kg", f"{data.test['test_118']}"),
            ("4.45", "C.I. Direct Red 28 (C.I. 22120)", "573-58-0", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_119']}", f"{data.outlet['outlet_119']}", "-", "mg/kg", f"{data.test['test_119']}"),
            ("4.46", "C.I. Disperse Blue 1 (C.I. 64500)", "2475-45-8", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_120']}", f"{data.outlet['outlet_120']}", "-", "mg/kg", f"{data.test['test_120']}"),
            ("4.47", "C.I. Disperse Blue 3 (C.I. 61505)", "2475-46-9", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_121']}", f"{data.outlet['outlet_121']}", "-", "mg/kg", f"{data.test['test_121']}"),
            ("4.48", "C.I. Disperse Blue 7 (C.I. 62500)", "3179-90-6", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_122']}", f"{data.outlet['outlet_122']}", "-", "mg/kg", f"{data.test['test_122']}"),
            ("4.49", "C.I. Disperse Blue 26 (C.I. 63305)", "3860-63-7", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_123']}", f"{data.outlet['outlet_123']}", "-", "mg/kg", f"{data.test['test_123']}"),
            ("4.50", "C.I. Disperse Blue 35 (mixture)", "12222-75-2", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_124']}", f"{data.outlet['outlet_124']}", "-", "mg/kg", f"{data.test['test_124']}"),
            ("4.51", "C.I. Disperse Blue 35 Component 1", "56524-77-7", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_125']}", f"{data.outlet['outlet_125']}", "-", "mg/kg", f"{data.test['test_125']}"),
            ("4.52", "C.I. Disperse Blue 35 Component 2", "56524-76-6", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_126']}", f"{data.outlet['outlet_126']}", "-", "mg/kg", f"{data.test['test_126']}"),
            ("4.53", "C.I. Disperse Blue 102", "12222-97-8 \n(69766-79-6)", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_127']}", f"{data.outlet['outlet_127']}", "-", "mg/kg", f"{data.test['test_127']}"),
            ("4.54", "C.I. Disperse Blue 106", "12223-01-7 \n(68516-81-4)", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_128']}", f"{data.outlet['outlet_128']}", "-", "mg/kg", f"{data.test['test_128']}"),
            ("4.55", "C.I. Disperse Blue 124", "61951-51-7", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_129']}", f"{data.outlet['outlet_129']}", "-", "mg/kg", f"{data.test['test_129']}"),
            ("4.56", "C.I. Disperse Brown 1", "23355-64-8", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_130']}", f"{data.outlet['outlet_130']}", "-", "mg/kg", f"{data.test['test_130']}"),
            ("4.57", "C.I. Disperse Orange 1 (C.I. 11080)", "2581-69-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_131']}", f"{data.outlet['outlet_131']}", "-", "mg/kg", f"{data.test['test_131']}"),
            ("4.58", "C.I. Disperse Orange 3 (C.I. 11005)", "730-40-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_132']}", f"{data.outlet['outlet_132']}", "-", "mg/kg", f"{data.test['test_132']}"),
            ("4.59", "C.I. Disperse Orange 11 (C.I. 60700)", "82-28-0", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_133']}", f"{data.outlet['outlet_133']}", "-", "mg/kg", f"{data.test['test_133']}"),
            ("4.60", "C.I. Disperse Orange 37/59/76 (C.I. 11132)", "13301-61-6", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_134']}", f"{data.outlet['outlet_134']}", "-", "mg/kg", f"{data.test['test_134']}"),
            ("4.61", "C.I. Disperse Orange 149", "85136-74-9", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_135']}", f"{data.outlet['outlet_135']}", "-", "mg/kg", f"{data.test['test_135']}"),
            ("4.62", "C.I. Disperse Red 1 (C.I. 11110)", "2872-52-8", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_136']}", f"{data.outlet['outlet_136']}", "-", "mg/kg", f"{data.test['test_136']}"),
            ("4.63", "C.I. Disperse Red 11 (C.I. 62015)", "2872-48-2", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_137']}", f"{data.outlet['outlet_137']}", "-", "mg/kg", f"{data.test['test_137']}"),
            ("4.64", "C.I. Disperse Red 17 (C.I. 11210)", "3179-89-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_138']}", f"{data.outlet['outlet_138']}", "-", "mg/kg", f"{data.test['test_138']}"),
            ("4.65", "C.I. Disperse Yellow 1 (C.I. 10345)", "119-15-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_139']}", f"{data.outlet['outlet_139']}", "-", "mg/kg", f"{data.test['test_139']}"),
            ("4.66", "C.I. Disperse Yellow 3 (C.I. 11855)", "2832-40-8", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_140']}", f"{data.outlet['outlet_140']}", "-", "mg/kg", f"{data.test['test_140']}"),
            ("4.67", "C.I. Disperse Yellow 9 (C.I. 10375)", "6373-73-5", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_141']}", f"{data.outlet['outlet_141']}", "-", "mg/kg", f"{data.test['test_141']}"),
            ("4.68", "C.I. Disperse Yellow 23 (C.I. 26070)", "6250-23-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_142']}", f"{data.outlet['outlet_142']}", "-", "mg/kg", f"{data.test['test_142']}"),
            ("4.69", "C.I. Disperse Yellow 39", "12236-29-2", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_143']}", f"{data.outlet['outlet_143']}", "-", "mg/kg", f"{data.test['test_143']}"),
            ("4.70", "C.I. Basic Yellow 2 / Solvent Yellow 34", "2465-27-2", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_144']}", f"{data.outlet['outlet_144']}", "-", "mg/kg", f"{data.test['test_144']}"),
            ("4.71", "C.I. Disperse Yellow 49", "54824-37-2", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_145']}", f"{data.outlet['outlet_145']}", "-", "mg/kg", f"{data.test['test_145']}"),
            ("4.72", "C.I. Pigment Red 104 (Lead Chromate molybdate sulphate red; C.I. 77605)", "12656-85-8", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_146']}", f"{data.outlet['outlet_146']}", "-", "mg/kg", f"{data.test['test_146']}"),
            ("4.73", "C.I. Pigment Yellow 34 (Lead sulfochromate yellow; C.I. 77603)", "1344-37-2", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_147']}", f"{data.outlet['outlet_147']}", "-", "mg/kg", f"{data.test['test_147']}"),
            ("4.74", "C.I. Solvent Blue 4", "6786-83-0", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_148']}", f"{data.outlet['outlet_148']}", "-", "mg/kg", f"{data.test['test_148']}"),
            ("4.75", "C.I. Solvent Violet 8", "561-41-1", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_149']}", f"{data.outlet['outlet_149']}", "-", "mg/kg", f"{data.test['test_149']}"),
            ("4.76", "C.I. Solvent Yellow 1 (p-Aminoazo benzene; Aniline yellow)", "60-09-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_150']}", f"{data.outlet['outlet_150']}", "-", "mg/kg", f"{data.test['test_150']}"),
            ("4.77", "C.I. Solvent Yellow 2 (C.I. 11020)", "60-11-7", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_151']}", f"{data.outlet['outlet_151']}", "-", "mg/kg", f"{data.test['test_151']}"),
            ("4.78", "C.I. Solvent Yellow 3 (o-Aminoazo benzene)", "97-56-3", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_152']}", f"{data.outlet['outlet_152']}", "-", "mg/kg", f"{data.test['test_152']}"),
            ("4.79", "C.I. Solvent Yellow 14", "842-07-9", "LC/DAD/MS", "1", "µg/l", f"{data.inlet['inlet_153']}", f"{data.outlet['outlet_153']}", "-", "mg/kg", f"{data.test['test_153']}"),
            ("4.80", "Navy Blue (index no. 611-070-00-2; Component 1 & 2)", "118685-33-9", "LC/DAD/MS", "500", "µg/l", f"{data.inlet['inlet_154']}", f"{data.outlet['outlet_154']}", "-", "mg/kg", f"{data.test['test_154']}"),
            ("4.81", "Colorants containing heavy metals (lead or cadmium)", "Various", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_155']}", f"{data.outlet['outlet_155']}", "-", "mg/kg", f"{data.test['test_155']}"),
            ("4.82", "Colorants with acute toxicity (LD50 < 100 mg/kg)", "Various", "LC/DAD/MS", "-", "µg/l", f"{data.inlet['inlet_156']}", f"{data.outlet['outlet_156']}", "-", "mg/kg", f"{data.test['test_156']}")
        ]

    for row in hazardous_colorants_data:
        pdf.add_table_row(*row)
    
    
    if extra_field_4_1:
        for i in extra_field_4_1:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
    
            )
            
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "5. Organotin Compounds ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9)        
    organotin_data = [
        ("5.1", "Dibutylin (DBT)", "Various \n683-18-1", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_157']}", f"{data.outlet['outlet_157']}", "-", "mg/kg", f"{data.test['test_157']}"),
        ("5.2", "Dibutyltin hydrogen borate", "75113-37-0", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_158']}", f"{data.outlet['outlet_158']}", "-", "mg/kg", f"{data.test['test_158']}"),
        ("5.3", "Dioctyltin(DOT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_159']}", f"{data.outlet['outlet_159']}", "-", "mg/kg", f"{data.test['test_159']}"),
        ("5.4", "Diphenyltin (DPhT)", "Various \n1011-95-6", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_160']}", f"{data.outlet['outlet_160']}", "-", "mg/kg", f"{data.test['test_160']}"),
        ("5.5", "Dipropyltin", "Various \n867-36-7", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_161']}", f"{data.outlet['outlet_161']}", "-", "mg/kg", f"{data.test['test_161']}"),
        ("5.6", "Monobutyltin(MBT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_162']}", f"{data.outlet['outlet_162']}", "-", "mg/kg", f"{data.test['test_162']}"),
        ("5.7", "Monooctyltin(MOT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_163']}", f"{data.outlet['outlet_163']}", "-", "mg/kg", f"{data.test['test_163']}"),
        ("5.8", "Tetrabutyltin(TeBT)", "Various \n1461-25-2", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_164']}", f"{data.outlet['outlet_164']}", "-", "mg/kg", f"{data.test['test_164']}"),
        ("5.9", "Tetraethyltin(TeET)", "597-64-8", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_165']}", f"{data.outlet['outlet_165']}", "-", "mg/kg", f"{data.test['test_165']}"),
        ("5.10", "Tetraoctyltin compounds (TeOT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_166']}", f"{data.outlet['outlet_166']}", "-", "mg/kg", f"{data.test['test_166']}"),
        ("5.11", "Tributyltin (TBT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_167']}", f"{data.outlet['outlet_167']}", "-", "mg/kg", f"{data.test['test_167']}"),
        ("5.12", "Bis(tributyltin) oxide (TBTO)", "56-35-9", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_168']}", f"{data.outlet['outlet_168']}", "-", "mg/kg", f"{data.test['test_168']}"),
        ("5.13", "Tricyclohexyltin (TCyHT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_169']}", f"{data.outlet['outlet_169']}", "-", "mg/kg", f"{data.test['test_169']}"),
        ("5.14", "Trimethyltin (TMT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_170']}", f"{data.outlet['outlet_170']}", "-", "mg/kg", f"{data.test['test_170']}"),
        ("5.15", "Trioctyltin (TOT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_171']}", f"{data.outlet['outlet_171']}", "-", "mg/kg", f"{data.test['test_171']}"),
        ("5.16", "Triphenyltin (TPhT)", "Various \n668-34-8", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_172']}", f"{data.outlet['outlet_172']}", "-", "mg/kg", f"{data.test['test_172']}"),
        ("5.17", "Tripropyltin (TPT)", "Various", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_173']}", f"{data.outlet['outlet_173']}", "-", "mg/kg", f"{data.test['test_173']}"),
        ("5.18", "Dimethyltin", "753-73-1", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_174']}", f"{data.outlet['outlet_174']}", "-", "mg/kg", f"{data.test['test_174']}"),
        ("5.19", "Monophenyltin", "1124-19-2", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_175']}", f"{data.outlet['outlet_175']}", "-", "mg/kg", f"{data.test['test_175']}"),
        ("5.20", "Monomethyltin", "993-16-8", "GC/MS", "0.01", "µg/l", f"{data.inlet['inlet_176']}", f"{data.outlet['outlet_176']}", "-", "mg/kg", f"{data.test['test_176']}")
]

    for row in organotin_data:
        pdf.add_table_row(*row)
        
        
    if extra_field_5:
        for i in extra_field_5:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
    
            )
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "6. PFC’s, Per and polyfluorinated Compounds", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9)              
            
    pfas_data = [
        ("6.1", "PFAS (according to OECD)", "Various", "LC/MS", "-", "µg/l", f"{data.inlet['inlet_177']}", f"{data.outlet['outlet_177']}", "-", "mg/kg", f"{data.test['test_177']}"),
        ("6.2", "Perfluorooctane sulfonic acid and sulfonates (PFOS)", "Various \n1763-23-1", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_178']}", f"{data.outlet['outlet_178']}", "-", "mg/kg", f"{data.test['test_178']}"),
        ("6.3", "Perfluoro-1-octane sulfonamide (PFOSA)", "754-91-6", "LC/MS", "0.1", "µg/l", f"{data.inlet['inlet_179']}", f"{data.outlet['outlet_179']}", "-", "mg/kg", f"{data.test['test_179']}"),
        ("6.4", "Perfluoroectane sulfon flouride (PFOSF/POSF)", "307-35-7", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_180']}", f"{data.outlet['outlet_180']}", "-", "mg/kg", f"{data.test['test_180']}"),
        ("6.5", "N-methylperfluoro-1-octane sulfonamide (N-Me-FOSA)", "31506-32-8", "LC/MS", "0.1", "µg/l", f"{data.inlet['inlet_181']}", f"{data.outlet['outlet_181']}", "-", "mg/kg", f"{data.test['test_181']}"),
        ("6.6", "N-ethylperfluoro-1-octane sulfonamide (N-Et-FOSA)", "4151-50-2", "LC/MS", "0.1", "µg/l", f"{data.inlet['inlet_182']}", f"{data.outlet['outlet_182']}", "-", "mg/kg", f"{data.test['test_182']}"),
        ("6.7", "2-(N-methylperfluoro-1-octane sulfonamide)-ethanol (N-Me-FOSE)", "24448-09-7", "LC/MS", "0.1", "µg/l", f"{data.inlet['inlet_183']}", f"{data.outlet['outlet_183']}", "-", "mg/kg", f"{data.test['test_183']}"),
        ("6.8", "2-(N-ethylperfluoro-1-octane sulfonamide)-ethanol (N-Et-FOSE)", "1691-99-2", "LC/DAD/MS", "0.1", "µg/l", f"{data.inlet['inlet_184']}", f"{data.outlet['outlet_184']}", "-", "mg/kg", f"{data.test['test_184']}"),
        ("6.9", "Perfluoro heptanoicacid (PFHpA) and salts", "Various \n375-85-9", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_185']}", f"{data.outlet['outlet_185']}", "-", "mg/kg", f"{data.test['test_185']}"),
        ("6.10", "Perfluoro octanoicacid (PFOA) and salts", "Various \n335-67-1", "LC/MS", "50", "µg/l", f"{data.inlet['inlet_186']}", f"{data.outlet['outlet_186']}", "-", "mg/kg", f"{data.test['test_186']}"),
        ("6.11", "Perfluoro nonanoicacid (PFNA) and salts", "Various \n375-95-1", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_188']}", f"{data.outlet['outlet_188']}", "-", "mg/kg", f"{data.test['test_188']}"),
        ("6.12", "Perfluoro decanoicacid (PFDA) and salts", "Various \n335-76-2", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_189']}", f"{data.outlet['outlet_189']}", "-", "mg/kg", f"{data.test['test_189']}"),
        ("6.13", "Henicosafluoro decanoicacid (Perfluoroun decanoic acid (PFUdA) and salts", "Various \n2058-94-8", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_190']}", f"{data.outlet['outlet_190']}", "-", "mg/kg", f"{data.test['test_190']}"),
        ("6.14", "Tricosafluoroun decanoicacid (Perfluorodo decanoic acid (PFDoA) and salts", "Various \n307-55-1", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_191']}", f"{data.outlet['outlet_191']}", "-", "mg/kg", f"{data.test['test_191']}"),
        ("6.15", "Pentacosafluoroutri decanoicacid (Perfluorotri decanoic acid (PFTrDA) and salts", "Various \n72629-94-8", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_192']}", f"{data.outlet['outlet_192']}", "-", "mg/kg", f"{data.test['test_192']}"),
        ("6.16", "Heptacosafluoroutetra decanoicacid (Perfluorotetra decanoic acid (PFTeDA) and salts", "Various \n376-06-7", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_193']}", f"{data.outlet['outlet_193']}", "-", "mg/kg", f"{data.test['test_193']}"),
        ("6.17", "Perfluoro butanoicacid (PFBA) and salts", "Various \n375-22-4", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_194']}", f"{data.outlet['outlet_194']}", "-", "mg/kg", f"{data.test['test_194']}"),
        ("6.18", "Perfluoro pentanoicacid (PFPeA) and salts", "Various \n2706-90-3", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_195']}", f"{data.outlet['outlet_195']}", "-", "mg/kg", f"{data.test['test_195']}"),
        ("6.19", "Perfluoro hexanoicacid (PFHxA) and salts", "Various \n307-24-4", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_196']}", f"{data.outlet['outlet_196']}", "-", "mg/kg", f"{data.test['test_196']}"),
        ("6.20", "Perfluoro (3,7-dimethyloctanoic acid) PF-3,7-DMOA and salts", "Various \n172155-07-6", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_197']}", f"{data.outlet['outlet_197']}", "-", "mg/kg", f"{data.test['test_197']}"),
        ("6.21", "Perfluoro butansulfonic acid (PFBS) and salts", "Various \n375-73-5 \n59933-66-3", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_198']}", f"{data.outlet['outlet_198']}", "-", "mg/kg", f"{data.test['test_198']}"),
        ("6.22", "Perfluoro hexansulfonic acid (PFHxS) and salts", "Various \n355-46-4", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_199']}", f"{data.outlet['outlet_199']}", "-", "mg/kg", f"{data.test['test_199']}"),
        ("6.23", "Perfluoro heptansulfonic acid (PFHpS) and salts", "Various \n375-92-8", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_200']}", f"{data.outlet['outlet_200']}", "-", "mg/kg", f"{data.test['test_200']}"),
        ("6.24", "Henicosafluoro Decane sulfonic acid (Perfluorodecane sulfonic acid) (PFDS) and salts", "Various \n335-77-3", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_201']}", f"{data.outlet['outlet_201']}", "-", "mg/kg", f"{data.test['test_201']}"),
        ("6.25", "7H-Perfluorou Heptanoic acid (7HPFHpA) and salts", "Various \n1546-95-8", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_202']}", f"{data.outlet['outlet_202']}", "-", "mg/kg", f"{data.test['test_202']}"),
        ("6.26", "2H,2H,3H,3H-Perfluoroun decanoicacid (44HPFUnA) and salts", "Various \n34598-33-9", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_203']}", f"{data.outlet['outlet_203']}", "-", "mg/kg", f"{data.test['test_203']}"),
        ("6.27", "1H,1H,2H,2 Perfluorooctan Sulfonic acid (1H,1H,2H,2H-PFOS) and salts", "Various \n27619-97-2", "LC/MS", "0.01", "µg/l", f"{data.inlet['inlet_204']}", f"{data.outlet['outlet_204']}", "-", "mg/kg", f"{data.test['test_204']}"),
        ("6.28", "1H,1H,2H,2H-Perfluoro-1-hexanol (4:2 FTOH)", "2043-47-2", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_205']}", f"{data.outlet['outlet_205']}", "-", "mg/kg", f"{data.test['test_205']}"),
        ("6.29", "1H,1H,2H,2H-Perfluoro-1-octanol (6:2 FTOH)", "647-42-7", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_206']}", f"{data.outlet['outlet_206']}", "-", "mg/kg", f"{data.test['test_206']}"),
        ("6.30", "1H,1H,2H,2H-Perfluoro-1-decanol (8:2 FTOH)", "678-39-7", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_207']}", f"{data.outlet['outlet_207']}", "-", "mg/kg", f"{data.test['test_207']}"),
        ("6.31", "1H,1H,2H,2H-Perfluoro-1-dodecanol (10:2 FTOH)", "865-86-1", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_208']}", f"{data.outlet['outlet_208']}", "-", "mg/kg", f"{data.test['test_208']}"),
        ("6.32", "1H,1H,2H,2H-Perfluorooctylacrylate (6:2 FTAC)", "17527-29-6", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_209']}", f"{data.outlet['outlet_209']}", "-", "mg/kg", f"{data.test['test_209']}"),
        ("6.33", "1H,1H,2H,2H-Perfluorodecylacrylate (8:2 FTAC)", "27905-45-9", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_210']}", f"{data.outlet['outlet_210']}", "-", "mg/kg", f"{data.test['test_210']}"),
        ("6.34", "1H,1H,2H,2H-Perfluorododecylacrylate (10:2 FTAC)", "17741-60-5", "LC/MS", "1", "µg/l", f"{data.inlet['inlet_211']}", f"{data.outlet['outlet_211']}", "-", "mg/kg", f"{data.test['test_211']}")
]

    for row in pfas_data:
        pdf.add_table_row(*row)
        
    if extra_field_6:
        for i in extra_field_6:
            pdf.add_table_row(
                str(i.get("sr", "")), 
                str(i.get("parameters", "")), 
                str(i.get("cas", "")), 
                str(i.get("method", "")), 
                str(i.get("1rl", "")), 
                str(i.get("unit", "")), 
                str(i.get('inlet', "")), 
                str(i.get('outlet', "")), 
                str(i.get("1rl2", "")), 
                str(i.get("unit2", "")), 
                str(i.get('test', ""))
    
            )
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "7.Chlorobezenes and Chlorotoluenes ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    chlorinated_data = [
    ("7.1", "Chlorobenzenes", "108-90-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_212']}", f"{data.outlet['outlet_212']}", "-", "mg/kg", f"{data.test['test_212']}"),
    ("7.2", "Dichlorobenzenes", "25321-22-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_213']}", f"{data.outlet['outlet_213']}", "-", "mg/kg", f"{data.test['test_213']}"),
    ("7.3", "1,2-Dichlorobenzenes", "95-50-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_214']}", f"{data.outlet['outlet_214']}", "-", "mg/kg", f"{data.test['test_214']}"),
    ("7.4", "1,3-Dichlorobenzenes", "541-73-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_215']}", f"{data.outlet['outlet_215']}", "-", "mg/kg", f"{data.test['test_215']}"),
    ("7.5", "1,4-Dichlorobenzenes", "106-46-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_216']}", f"{data.outlet['outlet_216']}", "-", "mg/kg", f"{data.test['test_216']}"),
    ("7.6", "Trichlorobenzenes", "12002-48-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_217']}", f"{data.outlet['outlet_217']}", "-", "mg/kg", f"{data.test['test_217']}"),
    ("7.7", "1,2,3-Trichlorobenzenes", "87-61-6", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_218']}", f"{data.outlet['outlet_218']}", "-", "mg/kg", f"{data.test['test_218']}"),
    ("7.8", "1,2,4-Trichlorobenzenes", "120-82-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_219']}", f"{data.outlet['outlet_219']}", "-", "mg/kg", f"{data.test['test_219']}"),
    ("7.9", "1,3,5-Trichlorobenzenes", "108-70-3", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_220']}", f"{data.outlet['outlet_220']}", "-", "mg/kg", f"{data.test['test_220']}"),
    ("7.10", "Tetrachlorobenzenes", "12408-10-5", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_221']}", f"{data.outlet['outlet_221']}", "-", "mg/kg", f"{data.test['test_221']}"),
    ("7.11", "1,2,3,4-Tetrachlorobenzenes", "634-66-2", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_222']}", f"{data.outlet['outlet_222']}", "-", "mg/kg", f"{data.test['test_222']}"),
    ("7.12", "1,2,3,5-Tetrachlorobenzenes", "634-90-2", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_223']}", f"{data.outlet['outlet_223']}", "-", "mg/kg", f"{data.test['test_223']}"),
    ("7.13", "1,2,4,5-Tetrachlorobenzenes", "95-94-3", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_224']}", f"{data.outlet['outlet_224']}", "-", "mg/kg", f"{data.test['test_224']}"),
    ("7.14", "Pentachlorobenzenes", "608-93-5", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_225']}", f"{data.outlet['outlet_225']}", "-", "mg/kg", f"{data.test['test_225']}"),
    ("7.15", "Hexachlorobenzenes", "118-74-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_226']}", f"{data.outlet['outlet_226']}", "-", "mg/kg", f"{data.test['test_226']}"),
    ("7.16", "Chlorotulene", "Various", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_227']}", f"{data.outlet['outlet_227']}", "-", "mg/kg", f"{data.test['test_227']}"),
    ("7.17", "2-Chlorotulene", "95-49-8", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_228']}", f"{data.outlet['outlet_228']}", "0.2", "mg/kg", f"{data.test['test_228']}"),
    ("7.18", "3-Chlorotulene", "108-41-8", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_229']}", f"{data.outlet['outlet_229']}", "0.2", "mg/kg", f"{data.test['test_229']}"),
    ("7.19", "4-Chlorotulene", "106-43-4", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_230']}", f"{data.outlet['outlet_230']}", "0.2", "mg/kg", f"{data.test['test_230']}"),
    ("7.20", "DiChlorotulene", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_231']}", f"{data.outlet['outlet_231']}", "-", "mg/kg", f"{data.test['test_231']}"),
    ("7.21", "2,3-Dichlorotulene", "32768-54-0", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_232']}", f"{data.outlet['outlet_232']}", "0.2", "mg/kg", f"{data.test['test_232']}"),
    ("7.22", "2,4-Dichlorotulene", "95-73-8", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_233']}", f"{data.outlet['outlet_233']}", "0.2", "mg/kg", f"{data.test['test_233']}"),
    ("7.23", "2,5-Dichlorotulene", "19398-61-9", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_234']}", f"{data.outlet['outlet_234']}", "0.2", "mg/kg", f"{data.test['test_234']}"),
    ("7.24", "2,6-Dichlorotulene", "118-69-4", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_235']}", f"{data.outlet['outlet_235']}", "0.2", "mg/kg", f"{data.test['test_235']}"),
    ("7.25", "3,4-Dichlorotulene", "95-75-0", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_236']}", f"{data.outlet['outlet_236']}", "0.2", "mg/kg", f"{data.test['test_236']}"),
    ("7.26", "3,5-Dichlorotulene", "25186-47-4", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_237']}", f"{data.outlet['outlet_237']}", "0.2", "mg/kg", f"{data.test['test_237']}"),
    ("7.27", "Alpha, alpha Dichlorotulene", "98-78-3", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_238']}", f"{data.outlet['outlet_238']}", "-", "mg/kg", f"{data.test['test_238']}"),
    ("7.28", "Trichlorotulene", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_239']}", f"{data.outlet['outlet_239']}", "-", "mg/kg", f"{data.test['test_239']}"),
    ("7.29", "2,3,4-Trichlorotulene", "7359-72-0", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_240']}", f"{data.outlet['outlet_240']}", "0.2", "mg/kg", f"{data.test['test_240']}"),
    ("7.30", "2,3,6-Trichlorotulene", "2077-46-5", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_241']}", f"{data.outlet['outlet_241']}", "0.2", "mg/kg", f"{data.test['test_241']}"),
    ("7.31", "2,4,5-Trichlorotulene", "6639-30-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_242']}", f"{data.outlet['outlet_242']}", "0.2", "mg/kg", f"{data.test['test_242']}"),
    ("7.32", "2,4,6-Trichlorotulene", "23749-65-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_243']}", f"{data.outlet['outlet_243']}", "0.2", "mg/kg", f"{data.test['test_243']}"),
    ("7.33", "3,4,5-Trichlorotulene", "21472-86-6", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_244']}", f"{data.outlet['outlet_244']}", "0.2", "mg/kg", f"{data.test['test_244']}"),
    ("7.34", "Alpha, alpha,alpha Trichlorotulene", "98-07-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_245']}", f"{data.outlet['outlet_245']}", "0.2", "mg/kg", f"{data.test['test_245']}"),
    ("7.35", "Alpha, 2,4-Trichlorotulene", "94-99-5", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_246']}", f"{data.outlet['outlet_246']}", "0.2", "mg/kg", f"{data.test['test_246']}"),
    ("7.36", "Alpha, 2,6-Trichlorotulene", "2014-83-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_247']}", f"{data.outlet['outlet_247']}", "0.2", "mg/kg", f"{data.test['test_247']}"),
    ("7.37", "Alpha, 3,4-Trichlorotulene", "102-47-6", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_248']}", f"{data.outlet['outlet_248']}", "0.2", "mg/kg", f"{data.test['test_248']}"),
    ("7.38", "Tetrachlorotulene", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_249']}", f"{data.outlet['outlet_249']}", "-", "mg/kg", f"{data.test['test_249']}"),
    ("7.39", "Alpha,alpha 2,6 Tetrachlorotulene", "81-19-6", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_250']}", f"{data.outlet['outlet_250']}", "0.2", "mg/kg", f"{data.test['test_250']}"),
    ("7.40", "Alpha,alpha, alpha 2 Tetrachlorotulene", "2136-89-2", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_251']}", f"{data.outlet['outlet_251']}", "0.2", "mg/kg", f"{data.test['test_251']}"),
    ("7.41", "Alpha,alpha, alpha 4 Tetrachlorotulene", "5216-25-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_252']}", f"{data.outlet['outlet_252']}", "0.2", "mg/kg", f"{data.test['test_252']}"),
    ("7.42", "2,3,4,5-Tetrachlorotulene", "76057-12-0", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_253']}", f"{data.outlet['outlet_253']}", "0.2", "mg/kg", f"{data.test['test_253']}"),
    ("7.43", "2,3,5,6-Tetrachlorotulene", "29733-70-8", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_254']}", f"{data.outlet['outlet_254']}", "0.2", "mg/kg", f"{data.test['test_254']}"),
    ("7.44", "2,3,4,6-Tetrachlorotulene", "875-40-1", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_255']}", f"{data.outlet['outlet_255']}", "0.2", "mg/kg", f"{data.test['test_255']}"),
    ("7.45", "2,3,4,5,6-Pentachlorotulene", "877-11-2", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_256']}", f"{data.outlet['outlet_256']}", "0.2", "mg/kg", f"{data.test['test_256']}")
]

    for row in chlorinated_data:
        pdf.add_table_row(*row)
   
   
   
    if extra_field_7:
         for i in extra_field_7:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )

    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "8.Chlorinated and Other Solvents", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    
    chlorinated_data_part2 = [
        ("8.1", "Dichloromethane", "75-09-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_257']}", f"{data.outlet['outlet_257']}", "-", "mg/kg", f"{data.test['test_257']}"),
        ("8.2", "Trichloromethane (Chloroform)", "67-66-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_258']}", f"{data.outlet['outlet_258']}", "-", "mg/kg", f"{data.test['test_258']}"),
        ("8.3", "Tetrachloromethane (Carbon tetrachloride)(C/M,S)", "56-23-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_259']}", f"{data.outlet['outlet_259']}", "-", "mg/kg", f"{data.test['test_259']}"),
        ("8.4", "Chlorinated ethanes and ethenes", "Various", "GC/MS", "1", "-", f"{data.inlet['inlet_260']}", f"{data.outlet['outlet_260']}", "-", "-", f"{data.test['test_260']}"),
        ("8.5", "1,1-Dichloroethane (C/M,S)", "75-34-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_261']}", f"{data.outlet['outlet_261']}", "-", "mg/kg", f"{data.test['test_261']}"),
        ("8.6", "1,2-Dichloroethane (C/M,S)", "107-06-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_262']}", f"{data.outlet['outlet_262']}", "-", "mg/kg", f"{data.test['test_262']}"),
        ("8.7", "1,1,1-Trichloroethane (C/M,S)", "71-55-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_263']}", f"{data.outlet['outlet_263']}", "-", "mg/kg", f"{data.test['test_263']}"),
        ("8.8", "1,1,2-Trichloroethane (C/M,S)", "79-00-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_264']}", f"{data.outlet['outlet_264']}", "-", "mg/kg", f"{data.test['test_264']}"),
        ("8.9", "1,1,1,2-Tetrachloroethane (C/M,S)", "630-20-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_265']}", f"{data.outlet['outlet_265']}", "-", "mg/kg", f"{data.test['test_265']}"),
        ("8.10", "1,1,2,2-Tetrachloroethane (C/M,S)", "79-34-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_266']}", f"{data.outlet['outlet_266']}", "-", "mg/kg", f"{data.test['test_266']}"),
        ("8.11", "Pentachloroethane (C/M,S)", "76-01-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_267']}", f"{data.outlet['outlet_267']}", "-", "mg/kg", f"{data.test['test_267']}"),
        ("8.12", "1,1-Dichloroethylene (C/M,S)", "75-35-4", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_268']}", f"{data.outlet['outlet_268']}", "-", "mg/kg", f"{data.test['test_268']}"),
        ("8.13", "1,2-Dichloroethylene, cis and trans (C/M,S)", "540-59-0, 156-60-5, 156-59-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_269']}", f"{data.outlet['outlet_269']}", "-", "mg/kg", f"{data.test['test_269']}"),
        ("8.14", "Trichloroethylene (C/M,S)", "79-01-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_270']}", f"{data.outlet['outlet_270']}", "-", "mg/kg", f"{data.test['test_270']}"),
        ("8.15", "Tetrachloroethylene (C/M,S)", "127-18-4", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_271']}", f"{data.outlet['outlet_271']}", "-", "mg/kg", f"{data.test['test_271']}"),
        ("8.16", "1,2,3-Trichloropropane (C/M,S)", "96-18-4", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_272']}", f"{data.outlet['outlet_272']}", "-", "mg/kg", f"{data.test['test_272']}"),
        ("8.17", "Hexachlorobutadiene (C/M,S)", "87-68-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_273']}", f"{data.outlet['outlet_273']}", "-", "mg/kg", f"{data.test['test_273']}")
        ]

    for row in chlorinated_data_part2:
        pdf.add_table_row(*row)
    
    if extra_field_8:
         for i in extra_field_8:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "Other VOC’s ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 

    aromatic_data = [
        ("8.18", "N-ethyl-2-pyrrolidone", "2687-91", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_274']}", f"{data.outlet['outlet_274']}", "-", "mg/kg", f"{data.test['test_274']}"),
        ("8.19", "Methyl-ethyl ketone", "78-93-3", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_275']}", f"{data.outlet['outlet_275']}", "-", "mg/kg", f"{data.test['test_275']}"),
        ("8.20", "Ethylbenzene", "100-41-4", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_276']}", f"{data.outlet['outlet_276']}", "-", "mg/kg", f"{data.test['test_276']}"),
        ("8.21", "Xylene", "1330-20-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_277']}", f"{data.outlet['outlet_277']}", "-", "mg/kg", f"{data.test['test_277']}"),
        ("8.22", "o-Xylene", "95-47-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_278']}", f"{data.outlet['outlet_278']}", "-", "mg/kg", f"{data.test['test_278']}"),
        ("8.23", "m-Xylene", "108-38-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_279']}", f"{data.outlet['outlet_279']}", "-", "mg/kg", f"{data.test['test_279']}"),
        ("8.24", "p-Xylene", "106-42-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_280']}", f"{data.outlet['outlet_280']}", "-", "mg/kg", f"{data.test['test_280']}"),
        ("8.25", "Cyclohexanone", "108-94-1", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_281']}", f"{data.outlet['outlet_281']}", "-", "mg/kg", f"{data.test['test_281']}"),
        ("8.26", "2-ethoxyethylacetate", "111-15-9", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_282']}", f"{data.outlet['outlet_282']}", "-", "mg/kg", f"{data.test['test_282']}"),
        ("8.27", "Acetophenone", "98-86-2", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_283']}", f"{data.outlet['outlet_283']}", "-", "mg/kg", f"{data.test['test_283']}"),
        ("8.28", "2-phenyl-2propanol", "617-94-7", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_284']}", f"{data.outlet['outlet_284']}", "-", "mg/kg", f"{data.test['test_284']}"),
        ("8.29", "Bis-(2-methoxyethyl) ether", "111-96-6", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_285']}", f"{data.outlet['outlet_285']}", "-", "mg/kg", f"{data.test['test_285']}"),
        ("8.30", "Stryene", "100-42-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_286']}", f"{data.outlet['outlet_286']}", "-", "mg/kg", f"{data.test['test_286']}"),
        ("8.31", "Benzene", "71-43-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_287']}", f"{data.outlet['outlet_287']}", "-", "mg/kg", f"{data.test['test_287']}"),
        ("8.32", "Toulene", "108-88-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_288']}", f"{data.outlet['outlet_288']}", "-", "mg/kg", f"{data.test['test_288']}"),
        ("8.33", "1-methyl-2-Pyrrolidone (NMP)", "872-50-4", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_289']}", f"{data.outlet['outlet_289']}", "-", "mg/kg", f"{data.test['test_289']}"),
        ("8.34", "N,N-Dimethylacetamide (DMAc)", "127-19-5", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_290']}", f"{data.outlet['outlet_290']}", "-", "mg/kg", f"{data.test['test_290']}"),
        ("8.35", "N,N-Dimethylformamide (DMF)", "68-12-2", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_291']}", f"{data.outlet['outlet_291']}", "-", "mg/kg", f"{data.test['test_291']}"),
        ("8.36", "2-ethoxyethanol", "110-80-5", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_292']}", f"{data.outlet['outlet_292']}", "-", "mg/kg", f"{data.test['test_292']}"),
        ("8.37", "Ethylene glycol dimethyl ether (EGDME)", "110-71-4", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_293']}", f"{data.outlet['outlet_293']}", "-", "mg/kg", f"{data.test['test_293']}"),
        ("8.38", "2-Methoxy ethanol", "109-86-4", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_294']}", f"{data.outlet['outlet_294']}", "-", "mg/kg", f"{data.test['test_294']}"),
        ("8.39", "2-Methoxy ethyl acetate", "110-49-6", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_295']}", f"{data.outlet['outlet_295']}", "-", "mg/kg", f"{data.test['test_295']}"),
        ("8.40", "2-Methoxy propyl acetate", "70657-70-4", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_296']}", f"{data.outlet['outlet_296']}", "-", "mg/kg", f"{data.test['test_296']}"),
        ("8.41", "Triethylene glycol dimethyl ether (TEGDME)", "112-49-2", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_297']}", f"{data.outlet['outlet_297']}", "-", "mg/kg", f"{data.test['test_297']}"),
        ("8.42", "Phenol", "108-95-2", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_298']}", f"{data.outlet['outlet_298']}", "-", "mg/kg", f"{data.test['test_298']}"),
        ("8.43", "Formamide", "75-12-7", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_299']}", f"{data.outlet['outlet_299']}", "-", "mg/kg", f"{data.test['test_299']}"),
        ("8.44", "Other aromatic hydrocarbons", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_300']}", f"{data.outlet['outlet_300']}", "-", "mg/kg", f"{data.test['test_300']}")
    ]
    
    
    for row in aromatic_data:
        pdf.add_table_row(*row)

    if extra_field_8_1:
         for i in extra_field_8_1:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
     
    
    
    
    

    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "9.Chlorophenols ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    chlorinated_data_part3 = [
        ("9.1", "Pentachlorophenol (PCP)", "87-86-5", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_301']}", f"{data.outlet['outlet_301']}", "-", "mg/kg", f"{data.test['test_301']}"),
    ("9.2", "Tetrachlorophenol (TeCP)", "25167-83-3", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_302']}", f"{data.outlet['outlet_302']}", "-", "mg/kg", f"{data.test['test_302']}"),
    ("9.3", "2,3,4,5-Tetrachlorophenol", "4901-51-3", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_303']}", f"{data.outlet['outlet_303']}", "-", "mg/kg", f"{data.test['test_303']}"),
    ("9.4", "2,3,4,6-Tetrachlorophenol", "58-90-2", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_304']}", f"{data.outlet['outlet_304']}", "-", "mg/kg", f"{data.test['test_304']}"),
    ("9.5", "2,3,5,6-Tetrachlorophenol", "935-95-5", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_305']}", f"{data.outlet['outlet_305']}", "-", "mg/kg", f"{data.test['test_305']}"),
    ("9.6", "Trichlorophenol", "25167-82-2", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_306']}", f"{data.outlet['outlet_306']}", "-", "mg/kg", f"{data.test['test_306']}"),
    ("9.7", "2,3,4-Trichlorophenol", "15950-66-0", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_307']}", f"{data.outlet['outlet_307']}", "-", "mg/kg", f"{data.test['test_307']}"),
    ("9.8", "2,3,5-Trichlorophenol", "933-78-8", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_308']}", f"{data.outlet['outlet_308']}", "-", "mg/kg", f"{data.test['test_308']}"),
    ("9.9", "2,3,6-Trichlorophenol", "933-75-5", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_309']}", f"{data.outlet['outlet_309']}", "-", "mg/kg", f"{data.test['test_309']}"),
    ("9.10", "2,4,5-Trichlorophenol", "95-95-4", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_310']}", f"{data.outlet['outlet_310']}", "-", "mg/kg", f"{data.test['test_310']}"),
    ("9.11", "2,4,6-Trichlorophenol", "88-06-2", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_311']}", f"{data.outlet['outlet_311']}", "-", "mg/kg", f"{data.test['test_311']}"),
    ("9.12", "3,4,5-Trichlorophenol", "609-19-8", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_312']}", f"{data.outlet['outlet_312']}", "-", "mg/kg", f"{data.test['test_312']}"),
    ("9.13", "Dichlorophenol (DiCP)", "25167-81-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_313']}", f"{data.outlet['outlet_313']}", "-", "mg/kg", f"{data.test['test_313']}"),
    ("9.14", "2,3-Dichlorophenol", "576-24-9", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_314']}", f"{data.outlet['outlet_314']}", "-", "mg/kg", f"{data.test['test_314']}"),
    ("9.15", "2,4-Dichlorophenol", "120-83-2", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_315']}", f"{data.outlet['outlet_315']}", "-", "mg/kg", f"{data.test['test_315']}"),
    ("9.16", "2,5-Dichlorophenol", "583-78-8", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_316']}", f"{data.outlet['outlet_316']}", "-", "mg/kg", f"{data.test['test_316']}"),
    ("9.17", "2,6-Dichlorophenol", "87-65-0", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_317']}", f"{data.outlet['outlet_317']}", "-", "mg/kg", f"{data.test['test_317']}"),
    ("9.18", "3,4-Dichlorophenol", "95-77-2", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_318']}", f"{data.outlet['outlet_318']}", "-", "mg/kg", f"{data.test['test_318']}"),
    ("9.19", "3,5-Dichlorophenol", "591-35-5", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_319']}", f"{data.outlet['outlet_319']}", "-", "mg/kg", f"{data.test['test_319']}"),
    ("9.20", "Mono Chlorophenols", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_320']}", f"{data.outlet['outlet_320']}", "-", "mg/kg", f"{data.test['test_320']}"),
    ("9.21", "2-Chlorophenol", "95-57-8", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_321']}", f"{data.outlet['outlet_321']}", "-", "mg/kg", f"{data.test['test_321']}"),
    ("9.22", "3-Chlorophenol", "108-43-0", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_322']}", f"{data.outlet['outlet_322']}", "-", "mg/kg", f"{data.test['test_322']}"),
    ("9.23", "4-Chlorophenol", "106-48-9", "GC/MS", "0.5", "µg/l", f"{data.inlet['inlet_323']}", f"{data.outlet['outlet_323']}", "-", "mg/kg", f"{data.test['test_323']}"),
    ("9.24", "Salts and Esters from the above mentioned Chlorophenols", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_324']}", f"{data.outlet['outlet_324']}", "-", "mg/kg", f"{data.test['test_324']}")
    ]

    for row in chlorinated_data_part3:
        pdf.add_table_row(*row)
    
    if extra_field_9:
         for i in extra_field_9:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "10. Chlorinated paraffins ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    
    
    chlorinated_data_part4 = [
        ("10.1", "Short chain chlorinated paraffins (SCCP), C10-13", "85535-84-8", "GC/MS", "5", "µg/l", f"{data.inlet['inlet_325']}", f"{data.outlet['outlet_325']}", "-", "mg/kg", f"{data.test['test_325']}"),
        ("10.2", "Medium chain chlorinated paraffins (MCCP), C14-17", "85535-85-9", "GC/MS", "5", "µg/l", f"{data.inlet['inlet_326']}", f"{data.outlet['outlet_326']}", "-", "mg/kg", f"{data.test['test_326']}")
    ]

    for row in chlorinated_data_part4:
        pdf.add_table_row(*row)
    
    
    
    if extra_field_10:
         for i in extra_field_10:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
             
             
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "11. Heavy metals and their compounds ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    
    metals_data = [
        ("11.1", "Antimony (Sb)", "7440-36-0 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_327']}", f"{data.outlet['outlet_327']}", "2", "mg/kg", f"{data.test['test_327']}"),
        ("11.2", "Arsenic (As)", "7440-38-2 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_328']}", f"{data.outlet['outlet_328']}", "2", "mg/kg", f"{data.test['test_328']}"),
        ("11.3", "Lead (Pb)", "7439-92-1 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_329']}", f"{data.outlet['outlet_329']}", "2", "mg/kg", f"{data.test['test_329']}"),
        ("11.4", "Cadmium (Cd)", "7440-43-9 et al.", "*APHA 3125-B", "0.1", "µg/l", f"{data.inlet['inlet_330']}", f"{data.outlet['outlet_330']}", "2", "mg/kg", f"{data.test['test_330']}"),
        ("11.5", "Chromium (Cr)", "7440-47-3 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_331']}", f"{data.outlet['outlet_331']}", "2", "mg/kg", f"{data.test['test_331']}"),
        ("11.6", "Hexavalent Chromium (Cr VI)", "18540-29-9 et al.", "*APHA 3500 Cr-B", "1", "µg/l", f"{data.inlet['inlet_332']}", f"{data.outlet['outlet_332']}", "2", "mg/kg", f"{data.test['test_332']}"),
        ("11.7", "Cobalt (Co)", "7440-48-4 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_333']}", f"{data.outlet['outlet_333']}", "2", "mg/kg", f"{data.test['test_333']}"),
        ("11.8", "Copper (Cu)", "7440-50-8 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_334']}", f"{data.outlet['outlet_334']}", "2", "mg/kg", f"{data.test['test_334']}"),
        ("11.9", "Nickel (Ni)", "7440-02-0 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_335']}", f"{data.outlet['outlet_335']}", "2", "mg/kg", f"{data.test['test_335']}"),
        ("11.10", "Mercury (Hg)", "7439-97-6 et al.", "*APHA 3112-B", "0.05", "µg/l", f"{data.inlet['inlet_336']}", f"{data.outlet['outlet_336']}", "0.2", "mg/kg", f"{data.test['test_336']}"),
        ("11.11", "Zinc (Zn)", "7440-66-6 et al.", "*APHA 3125-B", "5", "µg/l", f"{data.inlet['inlet_337']}", f"{data.outlet['outlet_337']}", "2", "mg/kg", f"{data.test['test_337']}"),
        ("11.12", "Manganese (Mn)", "7439-96-5 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_338']}", f"{data.outlet['outlet_338']}", "2", "mg/kg", f"{data.test['test_338']}"),
        ("11.13", "Silver (Ag)", "7440-22-4 et al.", "*APHA 3125-B", "1", "µg/l", f"{data.inlet['inlet_339']}", f"{data.outlet['outlet_339']}", "2", "mg/kg", f"{data.test['test_339']}")
    ]

    for row in metals_data:
        pdf.add_table_row(*row)
    
    
    
    
    
    if extra_field_11:
         for i in extra_field_11:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "12.Polycyclic Aromatic Hydrocarbons (PAH’s) ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    pah_data = [
        ("12.1", "Acenaphthene", "83-32-9", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_340']}", f"{data.outlet['outlet_340']}", "0.2", "mg/kg", f"{data.test['test_340']}"),
        ("12.2", "Acenaphthylene", "208-96-8", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_341']}", f"{data.outlet['outlet_341']}", "0.2", "mg/kg", f"{data.test['test_341']}"),
        ("12.3", "Anthracene", "120-12-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_342']}", f"{data.outlet['outlet_342']}", "0.2", "mg/kg", f"{data.test['test_342']}"),
        ("12.4", "Benzo[a]anthracene", "56-55-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_343']}", f"{data.outlet['outlet_343']}", "0.2", "mg/kg", f"{data.test['test_343']}"),
        ("12.5", "Benzo[a]pyrene", "50-32-8", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_344']}", f"{data.outlet['outlet_344']}", "0.2", "mg/kg", f"{data.test['test_344']}"),
        ("12.6", "Benzo[b]fluoranthene", "205-99-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_345']}", f"{data.outlet['outlet_345']}", "0.2", "mg/kg", f"{data.test['test_345']}"),
        ("12.7", "Benzo[e]pyrene", "192-97-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_346']}", f"{data.outlet['outlet_346']}", "0.2", "mg/kg", f"{data.test['test_346']}"),
        ("12.8", "Benzo[ghi]perylene", "191-24-2", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_347']}", f"{data.outlet['outlet_347']}", "0.2", "mg/kg", f"{data.test['test_347']}"),
        ("12.9", "Benzo[j]fluoranthene", "205-82-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_348']}", f"{data.outlet['outlet_348']}", "0.2", "mg/kg", f"{data.test['test_348']}"),
        ("12.10", "Benzo[k]fluoranthene", "207-08-9", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_349']}", f"{data.outlet['outlet_349']}", "0.2", "mg/kg", f"{data.test['test_349']}"),
        ("12.11", "Chrysene", "218-01-9", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_350']}", f"{data.outlet['outlet_350']}", "0.2", "mg/kg", f"{data.test['test_350']}"),
        ("12.12", "Cyclopenta[c,d]pyrene", "27208-37-3", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_351']}", f"{data.outlet['outlet_351']}", "-", "mg/kg", f"{data.test['test_351']}"),
        ("12.13", "Dibenzo[a,h]anthracene", "53-70-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_352']}", f"{data.outlet['outlet_352']}", "0.2", "mg/kg", f"{data.test['test_352']}"),
        ("12.14", "Dibenzo[a,e]pyrene", "192-65-4", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_353']}", f"{data.outlet['outlet_353']}", "-", "mg/kg", f"{data.test['test_353']}"),
        ("12.15", "Dibenzo[a,h]pyrene", "189-64-0", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_354']}", f"{data.outlet['outlet_354']}", "-", "mg/kg", f"{data.test['test_354']}"),
        ("12.16", "Dibenzo[a,i]pyrene", "189-55-9", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_355']}", f"{data.outlet['outlet_355']}", "-", "mg/kg", f"{data.test['test_355']}"),
        ("12.17", "Dibenzo[a,l]pyrene", "191-30-0", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_356']}", f"{data.outlet['outlet_356']}", "-", "mg/kg", f"{data.test['test_356']}"),
        ("12.18", "Fluoranthene", "206-44-0", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_357']}", f"{data.outlet['outlet_357']}", "0.2", "mg/kg", f"{data.test['test_357']}"),
        ("12.19", "Fluorene", "86-73-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_358']}", f"{data.outlet['outlet_358']}", "0.2", "mg/kg", f"{data.test['test_358']}"),
        ("12.20", "Indeno[1,2,3-cd]pyrene", "193-39-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_359']}", f"{data.outlet['outlet_359']}", "0.2", "mg/kg", f"{data.test['test_359']}"),
        ("12.21", "1-Methylpyrene", "2381-21-7", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_360']}", f"{data.outlet['outlet_360']}", "-", "mg/kg", f"{data.test['test_360']}"),
        ("12.22", "Naphthalene", "91-20-3", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_361']}", f"{data.outlet['outlet_361']}", "0.2", "mg/kg", f"{data.test['test_361']}"),
        ("12.23", "Phenanthrene", "85-01-8", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_362']}", f"{data.outlet['outlet_362']}", "0.2", "mg/kg", f"{data.test['test_362']}"),
        ("12.24", "Pyrene", "129-00-0", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_363']}", f"{data.outlet['outlet_363']}", "0.2", "mg/kg", f"{data.test['test_363']}")
    ]

    for row in pah_data:
        pdf.add_table_row(*row)
    
    if extra_field_12:
         for i in extra_field_12:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "13. Surfactants, wetting agents (other than APEOS’s)", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    quaternary_data = [
        ("13.1", "DHTDMAC (di hydrogenated tallow)dimethylammoniumchloride)", "61789-80-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_364']}", f"{data.outlet['outlet_364']}", "-", "mg/kg", f"{data.test['test_364']}"),
        ("13.2", "DSDMAC (distearyldimethylammoniumchloride)", "107-64-2", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_365']}", f"{data.outlet['outlet_365']}", "-", "mg/kg", f"{data.test['test_365']}"),
        ("13.3", "DTDMAC (bis(hydrogenated tallow alkyl)dimethylammoniumchloride)", "68783-78-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_366']}", f"{data.outlet['outlet_366']}", "-", "mg/kg", f"{data.test['test_366']}"),
        ("13.4", "EDTA", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_367']}", f"{data.outlet['outlet_367']}", "-", "mg/kg", f"{data.test['test_367']}"),
        ("13.5", "DTPA", "67-43-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_368']}", f"{data.outlet['outlet_368']}", "-", "mg/kg", f"{data.test['test_368']}"),
        ("13.6", "Tetrapropylenbenzolsulfonat (TPS), sodium salt", "11067-82-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_369']}", f"{data.outlet['outlet_369']}", "-", "mg/kg", f"{data.test['test_369']}")
    ]
    for row in quaternary_data:
        pdf.add_table_row(*row)

    if extra_field_13:
         for i in extra_field_13:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "14. Other substances ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 

    section_14_data = [
        ("14.1", "Aminoethylethanolamine (AEEA)", "111-41-1", "GC/MS", "500", "µg/l", f"{data.inlet['inlet_370']}", f"{data.outlet['outlet_370']}", "-", "mg/kg", f"{data.test['test_370']}"),
        ("14.2", "Aminoethylethanolamine (AEEA) Derivatives", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_371']}", f"{data.outlet['outlet_371']}", "-", "mg/kg", f"{data.test['test_371']}"),
        ("14.3", "Asbestos", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_372']}", f"{data.outlet['outlet_372']}", "-", "mg/kg", f"{data.test['test_372']}"),
        ("14.4", "Asbestos (Fb)", "1332-21-4", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_373']}", f"{data.outlet['outlet_373']}", "-", "mg/kg", f"{data.test['test_373']}"),
        ("14.5", "Bisphenol A (P)", "80-05-7", "GC/MS", "10", "µg/l", f"{data.inlet['inlet_374']}", f"{data.outlet['outlet_374']}", "-", "mg/kg", f"{data.test['test_374']}"),
        ("14.6", "Bisphenol B (P)", "77-40-7", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_375']}", f"{data.outlet['outlet_375']}", "-", "mg/kg", f"{data.test['test_375']}"),
        ("14.7", "Carbon disulfide", "75-15-0", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_376']}", f"{data.outlet['outlet_376']}", "-", "mg/kg", f"{data.test['test_376']}"),
        ("14.8", "C,C’-azodiformamide (ADCA; Diazene-1,2-dicarboxamide)", "123-77-3", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_377']}", f"{data.outlet['outlet_377']}", "-", "mg/kg", f"{data.test['test_377']}"),
        ("14.9", "o-Cresol", "95-48-7", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_378']}", f"{data.outlet['outlet_378']}", "-", "mg/kg", f"{data.test['test_378']}"),
        ("14.10", "m-Cresol", "108-39-4", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_379']}", f"{data.outlet['outlet_379']}", "-", "mg/kg", f"{data.test['test_379']}"),
        ("14.11", "p-Cresol", "106-44-5", "GC/MS", "1", "µg/l", f"{data.inlet['inlet_380']}", f"{data.outlet['outlet_380']}", "-", "mg/kg", f"{data.test['test_380']}"),
        ("14.12", "Dioxins and furanes", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_381']}", f"{data.outlet['outlet_381']}", "-", "mg/kg", f"{data.test['test_381']}"),
        ("14.13", "Dimethylfumarate (DMFu)", "624-49-7", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_382']}", f"{data.outlet['outlet_382']}", "-", "mg/kg", f"{data.test['test_382']}"),
        ("14.14", "6,6’-di-tert-butyl-2,2’-methylenedi-p-cresol", "119-47-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_383']}", f"{data.outlet['outlet_383']}", "-", "mg/kg", f"{data.test['test_383']}"),
        ("14.15", "D4; Octamethylcyclotetrasiloxane", "556-67-2", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_384']}", f"{data.outlet['outlet_384']}", "-", "mg/kg", f"{data.test['test_384']}"),
        ("14.16", "D5; Decamethylcyclopentasiloxane", "541-02-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_385']}", f"{data.outlet['outlet_385']}", "-", "mg/kg", f"{data.test['test_385']}"),
        ("14.17", "D6; Dodecamethylcyclohexasiloxane", "540-97-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_386']}", f"{data.outlet['outlet_386']}", "-", "mg/kg", f"{data.test['test_386']}"),
        ("14.18", "N-(Hydroxymethyl)acrylamide", "924-42-5", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_387']}", f"{data.outlet['outlet_387']}", "-", "mg/kg", f"{data.test['test_387']}"),
        ("14.19", "2-Mercaptobenzothiazole (2-MBT)", "149-30-4", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_388']}", f"{data.outlet['outlet_388']}", "-", "mg/kg", f"{data.test['test_388']}"),
        ("14.20", "N-Methylaniline", "100-61-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_389']}", f"{data.outlet['outlet_389']}", "-", "mg/kg", f"{data.test['test_389']}"),
        ("14.21", "Monomethyldibromodiphenylmethane", "99688-47-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_390']}", f"{data.outlet['outlet_390']}", "-", "mg/kg", f"{data.test['test_390']}"),
        ("14.22", "Monomethyldichlorodiphenylmethane (Ugilec 121)", "81161-70-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_391']}", f"{data.outlet['outlet_391']}", "-", "mg/kg", f"{data.test['test_391']}"),
        ("14.23", "Monomethyltetrachlorodiphenylmethane", "Various \n76253-60-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_392']}", f"{data.outlet['outlet_392']}", "-", "mg/kg", f"{data.test['test_392']}"),
        ("14.24", "Halogenated Naphthalenes", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_393']}", f"{data.outlet['outlet_393']}", "-", "mg/kg", f"{data.test['test_393']}"),
        ("14.25", "5-t-butyl-2,4,6-trinitro-m-xylol (Musk Xylol)", "81-15-2", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_394']}", f"{data.outlet['outlet_394']}", "-", "mg/kg", f"{data.test['test_394']}"),
        ("14.26", "Permethrin", "52645-53-1", "GC/MS", "500", "µg/l", f"{data.inlet['inlet_395']}", f"{data.outlet['outlet_395']}", "-", "mg/kg", f"{data.test['test_395']}"),
        ("14.27", "o-Phenylphenol (OPP)", "90-43-7", "GC/MS", "100", "µg/l", f"{data.inlet['inlet_396']}", f"{data.outlet['outlet_396']}", "-", "mg/kg", f"{data.test['test_396']}"),
        ("14.28", "Pesticides / Fumigants for storage and transport", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_397']}", f"{data.outlet['outlet_397']}", "-", "mg/kg", f"{data.test['test_397']}"),
        ("14.29", "Phthalimide", "85-41-6", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_398']}", f"{data.outlet['outlet_398']}", "-", "mg/kg", f"{data.test['test_398']}"),
        ("14.30", "Potassium Cyanide ⁷", "151-50-8", "GC/MS", "0.2", "mg/l", f"{data.inlet['inlet_399']}", f"{data.outlet['outlet_399']}", "-", "mg/kg", f"{data.test['test_399']}"),
        ("14.31", "Quinoline", "91-22-5", "GC/MS", "50", "µg/l", f"{data.inlet['inlet_400']}", f"{data.outlet['outlet_400']}", "-", "mg/kg", f"{data.test['test_400']}"),
        ("14.32", "Quintozene", "82-68-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_401']}", f"{data.outlet['outlet_401']}", "-", "mg/kg", f"{data.test['test_401']}")
    ]

    
    for row in section_14_data:
        pdf.add_table_row(*row)
    
    
    
    
    row_height = 24.1  # Tallest cell height for this row
    start_y = check_page_break(pdf, row_height)

    pdf.set_x(5)
    pdf.cell(10, row_height , "14.33", border=True, align="C")

    pdf.set_x(15)
    pdf.multi_cell(46, 4, "Rubber,natural Latex, sulphur cured SBR, Accelerators releasing carcinogenic nitrosamines, such as", 
                border=True, align="L")
    pdf.set_y(start_y)  # Reset to row start position
    pdf.set_x(61)
    pdf.cell(19, row_height-8, "99688-478", border=True, align="C")
    pdf.cell(28, row_height-8, "GC/MS", border=True, align="C")
    pdf.cell(12, row_height-8, "-", border=True, align="C")
    pdf.cell(12, row_height-8, "µg/l", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.inlet['inlet_402']}", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.outlet['outlet_402']}", border=True, align="C")
    pdf.cell(10, row_height-8, "-", border=True, align="C")
    pdf.cell(12, row_height-8, "mg/kg", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.test['test_402']}", border=True, align="C", ln=True)
    
    # Second row - Shorter description
    row_height = 16  # Adjusted to match visual balance
    start_y = check_page_break(pdf, row_height)

    pdf.set_x(15)
    pdf.multi_cell(46, 4, "Zinc diethyldithiocarbamate (ZDEC)", border=True, align="L")
    pdf.set_y(start_y)
    pdf.set_x(61)
    pdf.cell(19, row_height-8, "14324-551", border=True, align="C")
    pdf.cell(28, row_height-8, "GC/MS", border=True, align="C")
    pdf.cell(12, row_height-8, "-", border=True, align="C")
    pdf.cell(12, row_height-8, "µg/l", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.inlet['inlet_403']}", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.outlet['outlet_403']}", border=True, align="C")
    pdf.cell(10, row_height-8, "-", border=True, align="C")
    pdf.cell(12, row_height-8, "mg/kg", border=True, align="C")
    pdf.cell(17, row_height-8, f"{data.test['test_403']}", border=True, align="C", ln=True)
    

    
    section_14_2nd = [
        ("14.34", "Silica (particles of respirable size)", "14464-46-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_404']}", f"{data.outlet['outlet_404']}", "-", "mg/kg", f"{data.test['test_404']}"),
        ("14.35", "Sodium Cyanide ⁷", "Various \n143-33-9", "GC/MS", "0.2", "mg/l", f"{data.inlet['inlet_405']}", f"{data.outlet['outlet_405']}", "-", "mg/kg", f"{data.test['test_405']}"),
        ("14.36", "Sodium Sulfide", "1313-82-2", "GC/MS", "0.5", "mg/l", f"{data.inlet['inlet_406']}", f"{data.outlet['outlet_406']}", "-", "mg/kg", f"{data.test['test_406']}"),
        ("14.37", "Sodium sulfide, hydrat", "27610-45-3", "GC/MS", "0.5", "mg/l", f"{data.inlet['inlet_407']}", f"{data.outlet['outlet_407']}", "-", "mg/kg", f"{data.test['test_407']}"),
        ("14.38", "Sodium sulfide, nonahydrat", "1313-84-4", "GC/MS", "0.5", "mg/l", f"{data.inlet['inlet_408']}", f"{data.outlet['outlet_408']}", "-", "mg/kg", f"{data.test['test_408']}"),
        ("14.39", "Sodium sulfide, pentahydrat", "1313-83-3", "GC/MS", "0.5", "mg/l", f"{data.inlet['inlet_409']}", f"{data.outlet['outlet_409']}", "-", "mg/kg", f"{data.test['test_409']}"),
        ("14.40", "Halogenated terphenyles", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_410']}", f"{data.outlet['outlet_410']}", "-", "mg/kg", f"{data.test['test_410']}"),
        ("14.41", "Thiourea", "62-56-6", "GC/MS", "50", "mg/l", f"{data.inlet['inlet_411']}", f"{data.outlet['outlet_411']}", "-", "mg/kg", f"{data.test['test_411']}"),
        ("14.42", "Trialkyltin-, Triaryltin-, arsenic- or arsenic compounds as protective agents for production water", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_412']}", f"{data.outlet['outlet_412']}", "-", "mg/kg", f"{data.test['test_412']}"),
        ("14.43", "Tricholophenoxy fatty acid and derivatives", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_413']}", f"{data.outlet['outlet_413']}", "-", "mg/kg", f"{data.test['test_413']}"),
        ("14.44", "Triclosan", "3380-34-5", "GC/MS", "100", "µg/l", f"{data.inlet['inlet_414']}", f"{data.outlet['outlet_414']}", "-", "mg/kg", f"{data.test['test_414']}"),
        ("14.45", "2-(2,4,5-Trichlorphenoxy)propionic acid salts", "Various", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_415']}", f"{data.outlet['outlet_415']}", "-", "mg/kg", f"{data.test['test_415']}"),
        ("14.46", "2-(2,4,5-Trichlorphenoxy)propionic acid salts (Fenoprop)", "93-72-1", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_416']}", f"{data.outlet['outlet_416']}", "-", "mg/kg", f"{data.test['test_416']}"),
        ("14.47", "2,4,5-Trichlorphenoxyacetic acid (2,4,5-T)", "93-76-5", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_417']}", f"{data.outlet['outlet_417']}", "-", "mg/kg", f"{data.test['test_417']}"),
        ("14.48", "2,4,5-Trichlorphenoxyacetic acid salts", "Various", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_418']}", f"{data.outlet['outlet_418']}", "-", "mg/kg", f"{data.test['test_418']}"),
        ("14.49", "2,4,5-Trimethylaniline hydrochloride", "21436-97-5", "GC/MS", "0.1", "mg/l", f"{data.inlet['inlet_419']}", f"{data.outlet['outlet_419']}", "-", "mg/kg", f"{data.test['test_419']}"),
        ("14.50", "Tris(2-methoxyethoxy)vinylsilane", "1067-53-4", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_420']}", f"{data.outlet['outlet_420']}", "-", "mg/kg", f"{data.test['test_420']}"),
        ("14.51", "Titanium dioxide (particles of respirable size)⁷", "1317-70-0 / 1317-80-2 / 13463-67-7", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_421']}", f"{data.outlet['outlet_421']}", "-", "mg/kg", f"{data.test['test_421']}"),
        ("14.52", "2,4-Diaminoanisole sulphate", "39156-41-7", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_422']}", f"{data.outlet['outlet_422']}", "-", "mg/kg", f"{data.test['test_422']}"),
        ("14.53", "2-Naphthylammonium acetate", "553-00-4", "GC/MS", "0.1", "mg/l", f"{data.inlet['inlet_423']}", f"{data.outlet['outlet_423']}", "-", "mg/kg", f"{data.test['test_423']}"),
        ("14.54", "4-Chlor-o-toluidinium chloride (Azoic Diazo Component 11)", "3165-93-3", "GC/MS", "0.1", "µg/l", f"{data.inlet['inlet_424']}", f"{data.outlet['outlet_424']}", "-", "mg/kg", f"{data.test['test_424']}"),
        ("14.55", "2-Benzotriazol-2-yl-4,6-di-tert-butylphenol (UV-320)", "3846-71-7", "GC/MS", "100", "µg/l", f"{data.inlet['inlet_425']}", f"{data.outlet['outlet_425']}", "-", "mg/kg", f"{data.test['test_425']}"),
        ("14.56", "2,4-Di-tert-butyl-6-(5-chlorobenzotriazol-2-yl)phenol (UV-327)", "3864-99-1", "GC/MS", "100", "µg/l", f"{data.inlet['inlet_426']}", f"{data.outlet['outlet_426']}", "-", "mg/kg", f"{data.test['test_426']}"),
        ("14.57", "2-(2H-Benzotriazol-2-yl)-4,6-ditertpentylphenol (UV-328)", "25973-55-1", "GC/MS", "100", "µg/l", f"{data.inlet['inlet_427']}", f"{data.outlet['outlet_427']}", "-", "mg/kg", f"{data.test['test_427']}"),
        ("14.58", "2-(2H-Benzotriazol-2-yl)-4-(tert-butyl)-6-(sec-butyl)phenol (UV-350)", "36437-37-3", "GC/MS", "100", "mg/l", f"{data.inlet['inlet_428']}", f"{data.outlet['outlet_428']}", "-", "mg/kg", f"{data.test['test_428']}"),
        ("14.59", "4-Phenylcyclohexene", "4994-16-5", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_429']}", f"{data.outlet['outlet_429']}", "-", "mg/kg", f"{data.test['test_429']}"),
        ("14.60", "4-Vinylcyclohexene", "100-40-3", "GC/MS", "-", "mg/l", f"{data.inlet['inlet_430']}", f"{data.outlet['outlet_430']}", "-", "mg/kg", f"{data.test['test_430']}"),
        ("14.61", "Glutaraldehyde", "111-30-8", "GC/MS", "-", "µg/l", f"{data.inlet['inlet_431']}", f"{data.outlet['outlet_431']}", "-", "mg/kg", f"{data.test['test_431']}"),
    ]
    for row in section_14_2nd:
        pdf.add_table_row(*row)
    if extra_field_14:
         for i in extra_field_14:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
     
             )
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "15.Climate relevant gases (Ozone layer depleting substance & fluorinated greenhouse gases) ", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    
    
    section_15_data = [
            ("15.1", "Complete halogenated chlorofluorohydrocarbons (CFC's)", "Various", "GC/MS", "-", "µg/l", data.inlet["inlet_432"], data.outlet["outlet_432"], "-", "mg/kg", data.test["test_432"]),
            ("15.2", "Complete halogenated chlorofluorohydrocarbons containing bromines", "Various", "GC/MS", "-", "µg/l", data.inlet["inlet_433"], data.outlet["outlet_433"], "-", "mg/kg", data.test["test_433"]),
            ("15.3", "Partly halogenated chlorofluorohydrocarbons (HCFC's)", "Various", "GC/MS", "-", "µg/l", data.inlet["inlet_434"], data.outlet["outlet_434"], "-", "mg/kg", data.test["test_434"]),
            ("15.4", "Partly halogenated chlorofluorohydrocarbons containing bromines", "Various", "GC/MS", "-", "µg/l", data.inlet["inlet_435"], data.outlet["outlet_435"], "-", "mg/kg", data.test["test_435"]),
            ("15.5", "Hydrofluorocarbons (HFC's)", "Various", "GC/MS", "-", "µg/l", data.inlet["inlet_436"], data.outlet["outlet_436"], "-", "mg/kg", data.test["test_436"]),
        ]

    for row in section_15_data:
        pdf.add_table_row(*row)
        
    
    if extra_field_15:
         for i in extra_field_15:
             pdf.add_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
             )
    
    
    pdf.set_font("Calibri", "B", 10)
    pdf.set_x(5)
    pdf.cell(200, 7, "Conventional Parameters", border=1, ln=True)     
    pdf.set_font("Calibri", "", 9) 
    
    # pdf.set_font("Calibri", "B", 9)
    pdf.set_fill_color(232, 232, 232)  # Light purple background
    pdf.set_font("Calibri", "B", 13) # Light purple background
    pdf.set_x(5)
    pdf.cell(200,8,"TEST RESULTS", border=True, align='C',ln=True,fill=True)
    # Save current Y position
    pdf.set_font("Calibri", "B", 9)
    
    # Save current Y position
    current_y = pdf.get_y()
    
    # First row of table header
    pdf.set_x(5)
    pdf.cell(10, 14, "Sr #", 1, align="C",fill=True)
    pdf.cell(46, 14, "Parameters/Analytes Description", 1, align="C",fill=True)
    pdf.cell(19, 14, "CAS NO", 1, align="C",fill=True)
    old_header_y = pdf.get_y()
    pdf.multi_cell(28, 7, "Methods/\nEquipment", 1, align="C",fill=True)
    pdf.set_y(old_header_y)
    
    # Wastewater and Sludge headers (merged cells)
    pdf.set_x(108)
    pdf.cell(58, 7, "Wastewater", 1, align="C",fill=True)
    pdf.cell(39, 7, "Sludge", 1, align="C",fill=True)
    
    # Second row of header (sub-headers)
    pdf.set_y(current_y + 7)  # Move down 7mm
    pdf.set_x(108)
    pdf.cell(12, 7, "¹F.L.", 1, align="C",fill=True)
    pdf.cell(12, 7, "Unit", 1, align="C",fill=True)
    pdf.cell(17, 7, "¹R.W./Inlet", 1, align="C",fill=True)
    pdf.cell(17, 7, "¹A.T./Outlet", 1, align="C",fill=True)
    pdf.cell(10, 7, "¹R.L.", 1, align="C",fill=True)
    pdf.cell(12, 7, "Unit", 1, align="C",fill=True)
    pdf.cell(17, 7, "Test results", 1, align="C",fill=True)
    
    # Reset position for data rows
    pdf.set_y(current_y + 14)
    
    # Reset position for data rows
    pdf.set_y(current_y + 14)
    pdf.set_font("Calibri", "", 8)
    section_1_17_data = [
        ("1", "pH value", "-", "APHA 4500 H-B", "6.0 – 9.0", "-", data.inlet["inlet_437"], data.outlet["outlet_437"], "-", "-", data.test["test_437"]),
        ("2", "Max. Effluent Temperature", "-", "-", "Max 35", "°C", data.inlet["inlet_438"], data.outlet["outlet_438"], "-", "-", data.test["test_438"]),
        ("3", "Color/spectral absorption at 436nm", "-", "ISO 7887-B", "7", "m-1", data.inlet["inlet_439"], data.outlet["outlet_439"], "-", "-", data.test["test_439"]),
        ("3", "Color/spectral absorption at 525nm", "-", "ISO 7887-B", "5", "m-1", data.inlet["inlet_440"], data.outlet["outlet_440"], "-", "-", data.test["test_440"]),
        ("3", "Color/spectral absorption at 620nm", "-", "ISO 7887-B", "3", "m-1", data.inlet["inlet_441"], data.outlet["outlet_441"], "-", "-", data.test["test_441"]),
        ("4", "Chemical Oxygen Demand (COD)", "-", "HACH 8000", "150", "mg/l", data.inlet["inlet_442"], data.outlet["outlet_442"], "-", "-", data.test["test_442"]),
        ("5", "Biochemical Oxygen Demand (BOD5)", "-", "HACH 10099", "30", "mg/l", data.inlet["inlet_443"], data.outlet["outlet_443"], "-", "-", data.test["test_443"]),
        ("6", "Absorbable organic halogens AOX as (Cl)", "-", "USEPA 1650", "1.0", "mg/l", data.inlet["inlet_444"], data.outlet["outlet_444"], "-", "-", data.test["test_444"]),
        ("7", "Ammonia as (NH4-N)", "-", "HACH 8038", "10", "mg/l", data.inlet["inlet_445"], data.outlet["outlet_445"], "-", "-", data.test["test_445"]),
        ("8", "Total Nitrogen", "-", "HACH 10072", "20", "mg/l", data.inlet["inlet_446"], data.outlet["outlet_446"], "-", "-", data.test["test_446"]),
        ("9", "Total Phosphorus as (P)", "-", "HACH 8190", "3", "mg/l", data.inlet["inlet_447"], data.outlet["outlet_447"], "-", "-", data.test["test_447"]),
        ("10", "Total Suspended Solids", "-", "APHA 2540 D", "50", "mg/l", data.inlet["inlet_448"], data.outlet["outlet_448"], "-", "-", data.test["test_448"]),
        ("11", "Oil and grease", "-", "USEPA 1664", "10", "mg/l", data.inlet["inlet_449"], data.outlet["outlet_449"], "-", "-", data.test["test_449"]),
        ("12", "Phenol Index", "-", "APHA 5530 C", "0.5", "mg/l", data.inlet["inlet_450"], data.outlet["outlet_450"], "-", "-", data.test["test_450"]),
        ("13", "E - Coli", "-", "USEPA 1604", "126", "CFU/100ml", data.inlet["inlet_451"], data.outlet["outlet_451"], "-", "-", data.test["test_451"]),
        ("14", "Persistent Foam", "-", "N/A", "Not visible", "mg/l", data.inlet["inlet_452"], data.outlet["outlet_452"], "-", "-", data.test["test_452"]),
        ("15", "Cyanide", "-", "HACH 8027", "0.2", "mg/l", data.inlet["inlet_453"], data.outlet["outlet_453"], "-", "-", data.test["test_453"]),
        ("16", "Sulfide (as S2-)", "-", "APHA 4500 S2-D", "0.5", "mg/l", data.inlet["inlet_454"], data.outlet["outlet_454"], "-", "-", data.test["test_454"]),
        ("17", "Sulfite", "-", "APHA 4500 (SO3)2--C", "2", "mg/l", data.inlet["inlet_455"], data.outlet["outlet_455"], "-", "-", data.test["test_455"]),
    ]

    for row in section_1_17_data:
        pdf.add_cov_table_row(*row)
    
    
    if extra_field_16:
         for i in extra_field_16:
             pdf.add_cov_table_row(
                 str(i.get("sr", "")), 
                 str(i.get("parameters", "")), 
                 str(i.get("cas", "")), 
                 str(i.get("method", "")), 
                 str(i.get("1rl", "")), 
                 str(i.get("unit", "")), 
                 str(i.get('inlet', "")), 
                 str(i.get('outlet', "")), 
                 str(i.get("1rl2", "")), 
                 str(i.get("unit2", "")), 
                 str(i.get('test', ""))
             )
    
    
    pdf.ln(5)
    pdf.set_font("Calibri", "B", 7) 
    pdf.set_x(5)
    pdf.cell(4,4,"Note:",border=False,)
    pdf.set_font("Calibri", "", 7)
    pdf.set_x(10)
    if data.edit_note:
        pdf.multi_cell(0,3,f"{data.edit_note}")
        
        
        
    for i in range(1, 13):
        field_name = f"legend_{i}"
        value = getattr(data, field_name, None)
        if value:  # Only add if value is not None or empty
            pdf.set_x(5)
            pdf.multi_cell(0, 3, value)
            
            
            
            
    if extra_field_17:
         for i in extra_field_17:
             pdf.set_x(5)
             pdf.multi_cell(0, 3, f"{i.get('legend','')}", ln=True)
    
    if data.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(data, f'pdf_image_{i}')
               desc = getattr(data, f'pdf_desc_{i}')
               if base64_str:
                    try:
                         image_bytes = base64.b64decode(base64_str)
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                              tmp_file.write(image_bytes)
                              image_path = tmp_file.name
                         images.append({"path": image_path, "desc": desc or ''})
                    except Exception as e:
                         print(f"Failed to decode image {i}:", e)

          count = len(images)
          pdf._table_header_required = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=data.pdf_heading,align="C")
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

     

    # Prepare response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=detox_report_{pk}.pdf'
    
    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())
    
    # Clean up QR code file
    if os.path.exists(qr_file_path):
        os.remove(qr_file_path)
    
    return response