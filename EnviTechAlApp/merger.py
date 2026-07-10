# from .models import *
# import os
# def merge_pdfs(selected_reports):
#      from PyPDF2 import PdfReader, PdfWriter
#      merged_pdf = PdfWriter()

#     # Iterate through selected reports and add their pages to the merged PDF
#      for report_id in selected_reports:
#          pdf_path = get_pdf_path_for_report(report_id)
#          if pdf_path:  # Ensure that a valid path is returned
#              with open(pdf_path, 'rb') as pdf_file:
#                  reader = PdfReader(pdf_file)
#                  for page in reader.pages:
#                      merged_pdf.add_page(page)
 
#      # Prepare the output folder and file path
#      filename = f"{'-'.join(selected_reports)}.pdf"
#      folder = "/home/django/EnviTechAlApp/merge_pdf"
#      if not os.path.exists(folder):
#          os.makedirs(folder)
#      output_path = os.path.join(folder, filename)
 
#      # Write the merged PDF to a file
#      with open(output_path, 'wb') as output_file:
#          merged_pdf.write(output_file)
 
#      return output_path

# def get_pdf_path_for_report(report_id):

#     report_mapping = {
#        'dw': (DrinkingWaterForm, '/home/django/EnviTechAlApp/dw_pdf/{}.pdf'),
#        'gae': (GaseousEmissionForm, '/home/django/EnviTechAlApp/gae_pdf/{}.pdf'),
#        # ... add other mappings here ...
#     }
#     for report_type, (model,path_template) in report_mapping.items():
#         try:
#             report = model.objects.get(id=report_id, report_type=report_type)
#             return path_template.formate(report.lab_report_no)
#         except model.DoesNotExist:
#             continue
#     return ""        
    
    
    
    
    


     # try:
     #      dw = DrinkingWaterForm.objects.get(id=report_id, report_type='dw')
     #      return f'/home/django/EnviTechAlApp/dw_pdf/{dw.lab_report_no}.pdf'
     # except DrinkingWaterForm.DoesNotExist:
     #      return ""

     # try:
     #      gae = GaseousEmissionForm.objects.get(id=report_id, report_type='gae')
     #      return f'/home/django/EnviTechAlApp/gae_pdf/{gae.lab_report_no}.pdf'
     # except GaseousEmissionForm.DoesNotExist:
     #      return ""

     # try:
     #      aa = AmbientAirForm.objects.get(id=report_id, report_type='aa')
     #      return f'/home/django/EnviTechAlApp/aa_pdf/{aa.lab_report_no}.pdf'
     # except AmbientAirForm.DoesNotExist:
     #      return ""

     # try:
     #      ww = WasteWaterSludge.objects.get(id=report_id, report_type='ww')
     #      return f'/home/django/EnviTechAlApp/ww_pdf/{ww.lab_report_no}.pdf'
     # except WasteWaterSludge.DoesNotExist:
     #      return ""

     # try:
     #      vem = VehiculEmissionForm.objects.get(id=report_id, report_type='ve')
     #      return f'/home/django/EnviTechAlApp/vem_pdf/{vem.lab_report_no}.pdf'
     # except VehiculEmissionForm.DoesNotExist:
     #      return ""    
     # try:
     #      la = LuxAnalysisForm.objects.get(id=report_id, report_type='la')
     #      return f'/home/django/EnviTechAlApp/la_pdf/{la.lab_report_no}.pdf'
     # except LuxAnalysisForm.DoesNotExist:
     #      return ""    
     # try:
     #      pp = PackingPolyBagForm.objects.get(id=report_id, report_type='pp')
     #      return f'/home/django/EnviTechAlApp/pp_pdf/{pp.lab_report_no}.pdf'
     # except PackingPolyBagForm.DoesNotExist:
     #      return ""    
     # try:
     #      na = NoiseAnalysis.objects.get(id=report_id, report_type='na')
     #      return f'/home/django/EnviTechAlApp/na_pdf/{na.lab_report_no}.pdf'
     # except NoiseAnalysis.DoesNotExist:
     #      return ""    
     # try:
     #      mo = MachineOilForm.objects.get(id=report_id, report_type='mo')
     #      return f'/home/django/EnviTechAlApp/mo_pdf/{mo.lab_report_no}.pdf'
     # except MachineOilForm.DoesNotExist:
     #      return ""
    
     # try:
     #      ma = MicrobialAnalysis.objects.get(id=report_id, report_type='ma')
     #      return f'/home/django/EnviTechAlApp/mba_pdf/{ma.lab_report_no}.pdf'
     # except MicrobialAnalysis.DoesNotExist:
     #      return ""
    
     # try:
     #      vl = ViscousLiquid.objects.get(id=report_id, report_type='vl')
     #      return f'/home/django/EnviTechAlApp/vl_pdf/{vl.lab_report_no}.pdf'
     # except ViscousLiquid.DoesNotExist:
     #      return ""
    
     # try:
     #      aa2 = AmbientAir2.objects.get(id=report_id, report_type='aa2')
     #      return f'/home/django/EnviTechAlApp/aa2_pdf/{aa2.lab_report_no}.pdf'
     # except AmbientAir2.DoesNotExist:
     #      return ""
    
     # try:
     #      ww2 = WasteWaterForm2.objects.get(id=report_id, report_type='ww2')
     #      return f'/home/django/EnviTechAlApp/ww2_pdf/{ww2.lab_report_no}.pdf'
     # except WasteWaterForm2.DoesNotExist:
     #      return ""     
  