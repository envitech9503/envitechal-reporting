import logging
from django.conf import settings
from django.urls import reverse
import qrcode
import os
from fpdf import FPDF


class EtalReportPDF(FPDF):
     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)
          

          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)
          # if self.pages_count == 1:     
          #      page_number = f" {self.page_no()}"+" of "+ f"{self.page_no()}"
          # elif self.pages_count > 1:
          #      page_number = f" {self.page_no() -1 }"+" of "+ f"{self.page_no() }"
          # self.set_text_color(255, 255, 255)
          # self.text(165,270,txt="Page Number"+page_number)

          
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 9)
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          # self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")

     # def add_page(self):
     #      super().add_page()
     #      self.set_top_margin(40)     

     # def add_page(self):
     #      super().add_page()
     #      self.set_top_margin(40)    
     def add_page(self):
          super().add_page()
          self.set_top_margin(40) 


class PDF_samplePdf1(FPDF):





     def header(self):
          self.set_y(0)
          self.set_x(0)

class PDF_verif_pdf1(FPDF):
     def header(self):
          self.set_y(0)
          self.set_x(0)

     def add_page(self):
          super().add_page()
          self.set_top_margin(40) 


class PDF_generatePDF(FPDF):
     def __init__(self,report_number,invoice,reporting_date,report_to,address,attention,email,sample_id,sample_collection_date,
                  sample_description,sample_type,sample_collected_by,date_of_analysis_from,date_of_analysis_to,test_description,*args, **kwargs):

          super().__init__(*args, **kwargs)
          self.show_full_header = True  # default: render everything
          self.report_number = report_number
          self.invoice_number = invoice
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_collection_Date = sample_collection_date
          self.sample_description = sample_description
          self.sample_type = sample_type
          self.sample_collected_by = sample_collected_by
          self.date_of_analysis = (date_of_analysis_from +" to "+ date_of_analysis_to)
          self.test_description = test_description




     def header(self):

          self.set_y(0)
          self.set_x(0)

          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.report_number)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_number)



          target_url = self._rq_request.build_absolute_uri(reverse('DrinkingWaterform-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self.report_number}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,45,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,46,178+self.get_string_width(page_number +"of"+ page_number),46)
          # self.text(175,45,txt=page_number)

          if self.show_full_header:
               self.rect(10,55,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,60, txt="Report to:")
               self.line(30,55,30,68)
               self.text(31,60,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(44,60,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,65,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(44,65,txt=self.address)

               self.rect(10,70,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,75, txt="Attention:")
               self.line(30,70,30,83)
               self.text(31,75,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(43,75,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,80,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(43,80,txt=self.email)


               self.rect(10,85,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,90,txt="Sample ID:")
               self.text(110,90,txt=self.sample_id)

               self.rect(10,91,190,6)
               self.set_font("Calibri","B", 10)
               self.text(67,95,txt="Sample Collection Date:")
               self.text(110,95,txt=self.sample_collection_Date)

               self.rect(10,97,190,6)
               self.set_font("Calibri","B", 10)
               self.text(73,101,txt="Sample Description:")
               self.text(110,101,f"{self.sample_description}")

               self.rect(10,103.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(82,107,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,107,txt=self.sample_type)

               self.line(105,85,105,127)

               self.rect(10,109,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53,113,txt="Sample Collected / Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,113,txt=self.sample_collected_by)

               self.rect(10,115,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,119,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,119,txt=self.date_of_analysis)

               self.rect(10,121.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,125,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,125,txt=self.test_description)


               self.rect(10,130.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,134.5,txt="Analytical Test Report")
               #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 200,self.report_number)

               self.rotate(0)
          #  with pdf.local_context(fill_opacity=0.5):
          #      self.set_font("Arial", "B", 15)
          #      self.set_text_color(192, 192, 180) # Light gray text
          #      # self.set_xy(50, 260)
          #      self.rotate(45)
          #      #self.text(-250, 250,self.lab_rep_no)
          #      for x in range(0, int(self.w), 70):  # Adjust the interval as needed
          #           for y in range(0, int(self.h), 70):  # Adjust the interval as needed
          #                self.text(x-120, y, self.report_number)

          #      self.rotate(0)                    

          self.set_y(137)

class PDF_generatePDF_report(FPDF):
     def __init__(self,report_number,invoice,reporting_date,report_to,address,attention,email,sample_id,sample_collection_date,
                  sample_description,sample_type,sample_collected_by,date_of_analysis_from,date_of_analysis_to,test_description,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.report_number = report_number
          self.invoice_number = invoice
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_collection_Date = sample_collection_date
          self.sample_description = sample_description
          self.sample_type = sample_type
          self.sample_collected_by = sample_collected_by
          self.date_of_analysis = (date_of_analysis_from +" to "+ date_of_analysis_to)
          self.test_description = test_description




     def header(self):

          #header
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,32)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          # pdf.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.report_number)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_number)



          target_url = self._rq_request.build_absolute_uri(reverse('DrinkingWaterform-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self.report_number}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,45,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,46,178+self.get_string_width(page_number +"of"+ page_number),46)
          # self.text(175,45,txt=page_number)

          if self.show_full_header:
               self.rect(10,55,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,60, txt="Report to:")
               self.line(30,55,30,68)
               self.text(31,60,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(44,60,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,65,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(44,65,txt=self.address)

               self.rect(10,70,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,75, txt="Attention:")
               self.line(30,70,30,83)
               self.text(31,75,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(43,75,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,80,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(43,80,txt=self.email)


               self.rect(10,85,190,6)
               self.set_font("Calibri","B", 10)
               self.text(85,90,txt="Sample ID:")
               self.text(110,90,txt=self.sample_id)

               self.rect(10,91,190,6)
               self.set_font("Calibri","B", 10)
               self.text(67,95,txt="Sample Collection Date:")
               self.text(110,95,txt=self.sample_collection_Date)

               self.rect(10,97,190,6)
               self.set_font("Calibri","B", 10)
               self.text(73,101,txt="Sample Description:")
               self.text(110,101,f"{self.sample_description}")

               self.rect(10,103.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(82,107,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,107,txt=self.sample_type)

               self.line(105,85,105,127)

               self.rect(10,109,190,6)
               self.set_font("Calibri","B", 10)
               self.text(54,113,txt="Sample Collected / Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,113,txt=self.sample_collected_by)

               self.rect(10,115,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,119,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,119,txt=self.date_of_analysis)

               self.rect(10,121.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,125,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,125,txt=self.test_description)


               self.rect(10,130.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,134.5,txt="Analytical Test Report")
               #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 200,self.report_number)

               self.rotate(0)

          #footer
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")


          self.set_y(137)

class PDF_gaseousReportgeneratePDF(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,GaseEm_test_perf_date,
                  GasEm_test_desc,GaseEm_test_type,GaseEm_test_perf_by,GaseEm_types,GasEm_test_type_extra,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.GaseEm_test_perf_date = GaseEm_test_perf_date
          self.GasEm_test_desc = GasEm_test_desc
          self.GaseEm_test_type = GaseEm_test_type
          self.GasEm_test_type_extra = GasEm_test_type_extra
          self.GaseEm_test_perf_by = GaseEm_test_perf_by
          self.GaseEm_types = GaseEm_types


     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(40)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,41,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,42,178+self.get_string_width(page_number),42)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,42,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,43,60,43)
          self.text(34,42,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,49,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,50,60,50)
          self.text(34,49,txt=self.invoice_bill_no_number)



          target_url = self._rq_request.build_absolute_uri(reverse('GaseousForm-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self.lab_report_no}.png"
          qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
          print("qr path-------->>>>",qr_file_path)

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

          self.image(qr_file_path,"C",y=34,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,49,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,50,199,50)
          self.text(175,49,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,42,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,43,178+self.get_string_width(page_number +"of"+ page_number),43)
          # self.text(175,42,txt=page_number)

          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=str(self.attention))
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(91,86,txt="Test ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71,92,txt="Test Performed Date:")
               self.text(110,92,txt=self.GaseEm_test_perf_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(87.2,98,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.GaseEm_test_type)

               self.line(105,82,105,118)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74.5,104,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.GaseEm_test_perf_by)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(78,110,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.GasEm_test_desc)

               self.rect(10,112.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,116,txt="Fuel Types:")
               self.set_font("Calibri","B", 10)
               if self.GaseEm_types == 'oil_fired':
                    self.text(110,116,txt='Oil Fired')
               elif self.GaseEm_types == 'gas_fired':
                    self.text(110,116,txt='Gas Fired')
               elif self.GaseEm_types == 'coal_fired':
                    self.text(110,116,txt='Coal Fired')
               if self.GasEm_test_type_extra:
                    self.text(125,116,txt="("+self.GasEm_test_type_extra +")")


               # self.text(110,116,txt=self.GaseEm_types)

               #table header
               self.rect(10,120.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,124.5,txt="Test Report")

           #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(127)

class PDF_gaseousReportgeneratePDF1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,GaseEm_test_perf_date,
                  GasEm_test_desc,GaseEm_test_type,GaseEm_test_perf_by,GaseEm_types,GasEm_test_type_extra,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.GaseEm_test_perf_date = GaseEm_test_perf_date
          self.GasEm_test_desc = GasEm_test_desc
          self.GaseEm_test_type = GaseEm_test_type
          self.GasEm_test_type_extra = GasEm_test_type_extra
          self.GaseEm_test_perf_by = GaseEm_test_perf_by
          self.GaseEm_types = GaseEm_types


     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(45)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,46,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,47,178+self.get_string_width(page_number),47)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,46,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,47,60,47)
          self.text(34,46,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,53,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,54,60,54)
          self.text(34,53,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('GaseousForm-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self.lab_report_no}.png"
          qr_file_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
          print("qr path-------->>>>",qr_file_path)

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

          self.image(qr_file_path,"C",y=36.5,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,53,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,54,199,54)
          self.text(175,53,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,46,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,47,178+self.get_string_width(page_number +"of"+ page_number),47)
          # self.text(175,46,txt=page_number)

          if self.show_full_header:
               self.rect(10,56,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,61, txt="Report to:")
               self.line(30,56,30,69)
               self.text(31,61,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,61,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,66,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,66,txt=self.address)

               self.rect(10,71,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,76, txt="Attention:")
               self.line(30,71,30,84)
               self.text(31,76,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,76,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,81,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,81,txt=self.email)


               self.rect(10,86,190,6)
               self.set_font("Calibri","B", 10)
               self.text(91,90,txt="Test ID:")
               self.text(110,90,txt=self.sample_id)

               self.rect(10,92,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71,96,txt="Test Performed Date:")
               self.text(110,96,txt=self.GaseEm_test_perf_date)


               self.rect(10,98.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(87.2,102,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,102,txt=self.GaseEm_test_type)

               self.line(105,86,105,122)

               self.rect(10,104,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74.5,108,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,108,txt=self.GaseEm_test_perf_by)

               self.rect(10,110,190,6)
               self.set_font("Calibri","B", 10)
               self.text(78,114,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,114,txt=self.GasEm_test_desc)

               self.rect(10,116.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,120,txt="Fuel Types:")
               self.set_font("Calibri","B", 10)
               if self.GaseEm_types == 'oil_fired':
                    self.text(110,120,txt='Oil Fired')
               elif self.GaseEm_types == 'gas_fired':
                    self.text(110,120,txt='Gas Fired')
               elif self.GaseEm_types == 'coal_fired':
                    self.text(110,120,txt='Coal Fired')

               if self.GasEm_test_type_extra:
                    self.text(125,120,txt="("+self.GasEm_test_type_extra +")")

               #table header
               self.rect(10,124.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,128.5,txt="Test Report")

           #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")


          self.set_y(131)

class PDF_ambientAirGeneratePDF(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,ambientAir_test_perf_date,
                  ambientAir_test_perf_by,ambientAir_test_type_location,ambienAir_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.ambientAir_test_perf_date = ambientAir_test_perf_date
          self.ambientAir_test_perf_by = ambientAir_test_perf_by
          self.ambientAir_test_type_location = ambientAir_test_type_location
          self.ambientAir_test_perf_by = ambientAir_test_perf_by
          self.ambienAir_test_desc = ambienAir_test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('ambientAir-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,40,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,41,178+self.get_string_width(page_number +"of"+ page_number),41)
          # self.text(175,40,txt=page_number)

          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65 )
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               if self.email:
                    self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(91,86,txt="Test ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71,92,txt="Test Performed Date:")
               self.text(110,92,txt=self.ambientAir_test_perf_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77.8,98,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.ambienAir_test_desc)

               self.line(105,82,105,112)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(70.5,104,txt="Test Type & Location:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.ambientAir_test_type_location)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74,110,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.ambientAir_test_perf_by)

               #table header
               self.rect(10,114.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,118.5,txt="Test Report")

          #water mark

          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)





          self.set_y(121)

class PDF_ambientAirGeneratePDF1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,ambientAir_test_perf_date,
                  ambientAir_test_perf_by,ambientAir_test_type_location,ambienAir_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.ambientAir_test_perf_date = ambientAir_test_perf_date
          self.ambientAir_test_perf_by = ambientAir_test_perf_by
          self.ambientAir_test_type_location = ambientAir_test_type_location
          self.ambientAir_test_perf_by = ambientAir_test_perf_by
          self.ambienAir_test_desc = ambienAir_test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,44,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,45,178+self.get_string_width(page_number),45)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,44,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,45,60,45)
          self.text(34,44,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,51,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,52,60,52)
          self.text(34,51,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('ambientAir-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,51,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,52,199,52)
          self.text(175,51,txt=self.reporting_date)

          # self.set_font("Calibri","B", 10)
          # self.text(159.5,44,txt="Page No:")
          # self.set_font("Calibri","", 10)
          # self.line(175,45,178+self.get_string_width(page_number +"of"+ page_number),45)
          # self.text(175,44,txt=page_number)

          if self.show_full_header:
               self.rect(10,56,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,61, txt="Report to:")
               self.line(30,56,30,69 )
               self.text(31,61,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,61,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,66,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,66,txt=self.address)

               self.rect(10,71,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,76, txt="Attention:")
               self.line(30,71,30,84)
               self.text(31,76,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,76,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,81,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,81,txt=self.email)


               self.rect(10,86,190,6)
               self.set_font("Calibri","B", 10)
               self.text(91,90,txt="Test ID:")
               self.text(110,90,txt=self.sample_id)

               self.rect(10,92,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71,96,txt="Test Performed Date:")
               self.text(110,96,txt=self.ambientAir_test_perf_date)


               self.rect(10,98.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77.8,102,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,102,txt=self.ambienAir_test_desc)

               self.line(105,86,105,116)

               self.rect(10,104,190,6)
               self.set_font("Calibri","B", 10)
               self.text(70.5,108,txt="Test Type & Location:")
               self.set_font("Calibri","", 10)
               self.text(110,108,txt=self.ambientAir_test_type_location)

               self.rect(10,110,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74,114,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,114,txt=self.ambientAir_test_perf_by)

               #table header
               self.rect(10,118.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,122.5,txt="Test Report")

          #water mark

          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")                    


          self.set_y(125)

class PDF_wasteWaterPdf0(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,ww_sample_colec_Date,
                  ww_sample_colec_by,ww_sample_type,ww_sample_desc,ww_date_of_analy_from,ww_date_of_analy_to,ww_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.ww_sample_colec_Date = ww_sample_colec_Date
          self.ww_sample_colec_by = ww_sample_colec_by
          self.ww_sample_type = ww_sample_type
          self.ww_sample_desc = ww_sample_desc
          self.ww_test_desc = ww_test_desc
          self.ww_date_of_analysis = (ww_date_of_analy_from or "") + " to " + (ww_date_of_analy_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          if self.pages_count == 1:     
               page_number = f" {self.page_no()}"+" of "+ f"{self.page_no()}"
          elif self.pages_count > 1:
               page_number = f" {self.page_no() -1 }"+" of "+ f"{self.page_no() }"


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('wastewater-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          # self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)

          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number +"of"+ page_number),41)
          self.text(175,40,txt=page_number)

          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,76,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,76,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(87,86,txt="Sample ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(67.7,92,txt="Sample Collection Date:")
               self.text(110,92,txt=self.ww_sample_colec_Date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(73.2,98,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.ww_sample_desc)

               self.line(105,82,105,124)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(82.8,104,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.ww_sample_type)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(55,110,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.ww_sample_colec_by)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,116,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.ww_date_of_analysis)

               self.rect(10,118,190,6)
               self.set_font("Calibri","B", 10)
               self.text(78,122,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,122,txt=self.ww_test_desc)

               #table header
               self.rect(10,126.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,130.5,txt="Analytical Test Report")

          #water mark

          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)



          self.set_y(132.9)

class PDF_wasteWaterPdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,report_to,address,attention,email,sample_id,ww_sample_colec_Date,
                  ww_sample_colec_by,ww_sample_type,ww_sample_desc,ww_date_of_analy_from,ww_date_of_analy_to,ww_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.report_to = report_to
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.ww_sample_colec_Date = ww_sample_colec_Date
          self.ww_sample_colec_by = ww_sample_colec_by
          self.ww_sample_type = ww_sample_type
          self.ww_sample_desc = ww_sample_desc
          self.ww_test_desc = ww_test_desc
          self.ww_date_of_analysis = (ww_date_of_analy_from or "") + " to " + (ww_date_of_analy_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(43)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,44,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,45,178+self.get_string_width(page_number),45)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,44,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,45,60,45)
          self.text(34,44,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,51,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,52,60,52)
          self.text(34,51,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('wastewater-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,51,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,52,199,52)
          self.text(175,51,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,56,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,61, txt="Report to:")
               self.line(30,56,30,69)
               self.text(31,61,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,61,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,66,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,66,txt=self.address)

               self.rect(10,71,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,76, txt="Attention:")
               self.line(30,71,30,84)
               self.text(31,76,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,76,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,80,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,80,txt=self.email)


               self.rect(10,86,190,6)
               self.set_font("Calibri","B", 10)
               self.text(87,90,txt="Sample ID:")
               self.text(110,90,txt=self.sample_id)

               self.rect(10,92,190,6)
               self.set_font("Calibri","B", 10)
               self.text(67.7,96,txt="Sample Collection Date:")
               self.text(110,96,txt=self.ww_sample_colec_Date)


               self.rect(10,98.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(73.2,102,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,102,txt=self.ww_sample_desc)

               self.line(105,86,105,128)

               self.rect(10,104,190,6)
               self.set_font("Calibri","B", 10)
               self.text(82.8,108,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,108,txt=self.ww_sample_type)

               self.rect(10,110,190,6)
               self.set_font("Calibri","B", 10)
               self.text(55,114,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,114,txt=self.ww_sample_colec_by)

               self.rect(10,116,190,6)
               self.set_font("Calibri","B", 10)
               self.text(77,120,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,120,txt=self.ww_date_of_analysis)

               self.rect(10,122,190,6)
               self.set_font("Calibri","B", 10)
               self.text(78,126,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,126,txt=self.ww_test_desc)

               #table header
               self.rect(10,130.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,134.5,txt="Analytical Test Report")

          #water mark

          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-10,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-11.5,12,12)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 8)
          self.text(18,self.h-2,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-5,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-8.2,7,7)
          self.text(175,self.h-2.8,txt="info@envitechal.com")
          self.text(175,self.h-5.4,txt="www.envitechal.com")

          self.set_y(136.9)

class PDF_vehicularEmissionReport(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,vehEm_test_perf_date,
                  vehEm_test_perfBy,vehEm_test_type,vehEm_test_desc,report_to,vehEm_test_type_extra,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.vehEm_test_perf_date = vehEm_test_perf_date
          self.vehEm_test_perfBy = vehEm_test_perfBy
          self.vehEm_test_type = vehEm_test_type
          self.vehEm_test_type_extra = vehEm_test_type_extra
          self.vehEm_test_desc = vehEm_test_desc
          self.report_to = report_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('vehicularEmission-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,86,txt="Test ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,92,txt="Test Performed Date:")
               self.text(110,92,txt=self.vehEm_test_perf_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.2,98,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.vehEm_test_desc)

               self.line(105,82,105,112)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,104,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.vehEm_test_type)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,110,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.vehEm_test_perfBy)

               #table header
               self.rect(10,114.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,118.5,txt="Test Report")

           #water mark

          with self.local_context(fill_opacity=0.4):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(121)

class PDF_vehicularEmissionReport1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,vehEm_test_perf_date,
                  vehEm_test_perfBy,vehEm_test_type,vehEm_test_desc,report_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.vehEm_test_perf_date = vehEm_test_perf_date
          self.vehEm_test_perfBy = vehEm_test_perfBy
          self.vehEm_test_type = vehEm_test_type
          self.vehEm_test_desc = vehEm_test_desc
          self.report_to = report_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('vehicularEmission-view', kwargs={'pk': self._rq_pk}))
          print('request url------------->>>>>>',target_url)
          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,70)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,85)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,91,txt="Test ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,97,txt="Test Performed Date:")
               self.text(110,97,txt=self.vehEm_test_perf_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.2,103,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.vehEm_test_desc)

               self.line(105,87,105,117)

               self.rect(10,105,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,109,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.vehEm_test_type)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,115,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.vehEm_test_perfBy)

               #table header
               self.rect(10,119.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,123.5,txt="Test Report")

           #water mark

          with self.local_context(fill_opacity=0.4):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

               #footer
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")     


          self.set_y(126)

class PDF_luxAnalysisReportPdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,lux_test_perf_date,
                  lux_test_perfBy,lux_test_type,lux_test_desc,report_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.lux_test_perf_date = lux_test_perf_date
          self.lux_test_perfBy = lux_test_perfBy
          self.lux_test_type = lux_test_type
          self.lux_test_desc = lux_test_desc
          self.report_to = report_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(41)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,42,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,43,178+self.get_string_width(page_number),43)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,42,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,43,60,43)
          self.text(34,42,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,49,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,50,60,50)
          self.text(34,49,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('luxAnalysis-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=34,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,49,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,50,199,50)
          self.text(175,49,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,54,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,59, txt="Report to:")
               self.line(30,54,30,67)
               self.text(31,59,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,59,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,64,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,64,txt=self.address)

               self.rect(10,69,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,74, txt="Attention:")
               self.line(30,69,30,82)
               self.text(31,74,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,74,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,79,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,79,txt=self.email)


               self.rect(10,84,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,88,txt="Test ID:")
               self.text(110,88,txt=self.sample_id)

               self.rect(10,90,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,94,txt="Test Performed Date:")
               self.text(110,94,txt=self.lux_test_perf_date)


               self.rect(10,96.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.2,100,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,100,txt=self.lux_test_desc)

               self.line(105,84,105,114)

               self.rect(10,102,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,106,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,106,txt=self.lux_test_type)

               self.rect(10,108,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,112,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,112,txt=self.lux_test_perfBy)

               #table header
               self.rect(10,116.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,120.5,txt="Test Report")

          with self.local_context(fill_opacity=0.4):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(123)

class PDF_luxAnalysisReportPdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,lux_test_perf_date,
                  lux_test_perfBy,lux_test_type,lux_test_desc,report_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.lux_test_perf_date = lux_test_perf_date
          self.lux_test_perfBy = lux_test_perfBy
          self.lux_test_type = lux_test_type
          self.lux_test_desc = lux_test_desc
          self.report_to = report_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(46)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,47,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,48,178+self.get_string_width(page_number),48)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,54,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,55,60,55)
          self.text(34,54,txt=self.invoice_bill_no_number)


          target_url = self._rq_request.build_absolute_uri(reverse('luxAnalysis-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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


          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,54,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,55,199,55)
          self.text(175,54,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,59,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,64, txt="Report to:")
               self.line(30,59,30,67)
               self.text(31,64,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,64,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,69,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,69,txt=self.address)

               self.rect(10,74,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,79, txt="Attention:")
               self.line(30,74,30,82)
               self.text(31,79,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,79,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,84,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,84,txt=self.email)


               self.rect(10,89,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,93,txt="Test ID:")
               self.text(110,93,txt=self.sample_id)

               self.rect(10,95,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,99,txt="Test Performed Date:")
               self.text(110,99,txt=self.lux_test_perf_date)


               self.rect(10,101.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.2,105,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,105,txt=self.lux_test_desc)

               self.line(105,89,105,119)

               self.rect(10,107,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,111,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,111,txt=self.lux_test_type)

               self.rect(10,113,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,117,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,117,txt=self.lux_test_perfBy)

               #table header
               self.rect(10,121.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,125.5,txt="Test Report")

          with self.local_context(fill_opacity=0.4):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")

          self.set_y(128)

class PDF_packingPolyBagReport(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,pack_sample_colc_date,
                  pack_sample_colc_by,pack_sample_type,pack_test_desc,report_to,pack_sample_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.pack_sample_colc_date = pack_sample_colc_date
          self.pack_sample_colc_by = pack_sample_colc_by
          self.pack_sample_type = pack_sample_type
          self.pack_test_desc = pack_test_desc
          self.report_to = report_to
          self.pack_sample_desc = pack_sample_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('packingpolybag-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(85,86,txt="Sample ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(52,92,txt="Sample Collected/Received Date:")
               self.text(110,92,txt=self.pack_sample_colc_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71.2,98,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.pack_sample_desc)

               self.line(105,82,105,118)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(80.8,104,txt="sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.pack_sample_type)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53,110,txt="Sample Received/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.pack_sample_colc_by)


               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75,116,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.pack_test_desc)

               #table header
               self.rect(10,122.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,126.5,txt="Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(129.2)

class PDF_packingPolyBagReport1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,pack_sample_colc_date,
                  pack_sample_colc_by,pack_sample_type,pack_test_desc,report_to,pack_sample_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.pack_sample_colc_date = pack_sample_colc_date
          self.pack_sample_colc_by = pack_sample_colc_by
          self.pack_sample_type = pack_sample_type
          self.pack_test_desc = pack_test_desc
          self.report_to = report_to
          self.pack_sample_desc = pack_sample_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no_number)


          target_url = self._rq_request.build_absolute_uri(reverse('packingpolybag-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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


          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,70)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,85)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(85,91,txt="Sample ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(52,97,txt="Sample Collected/Received Date:")
               self.text(110,97,txt=self.pack_sample_colc_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(71.2,103,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.pack_sample_desc)

               self.line(105,87,105,123)

               self.rect(10,105,190,6)
               self.set_font("Calibri","B", 10)
               self.text(80.8,109,txt="sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.pack_sample_type)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53,115,txt="Sample Received/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.pack_sample_colc_by)


               self.rect(10,117,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75,121,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,121,txt=self.pack_test_desc)

               #table header
               self.rect(10,127.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,131.5,txt="Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")

          self.set_y(134.2)

class PDF_noiseAnalysisReport(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,
                  test_perf_by,test_type,test_desc,report_to,select1,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_perf_by = test_perf_by
          self.test_type = test_type
          self.test_desc = test_desc
          self.report_to = report_to
          self.select1 = select1



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('noiseAnalysis-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,86,txt="Test ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,92,txt="Test Performed Date:")
               self.text(110,92,txt=self.test_perf_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,98,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.test_type)

               self.line(105,82,105,112)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,104,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.test_perf_by)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.5,110,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.test_desc)

               #table header
               self.rect(10,114.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,118.5,txt="Test Report")

          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)



          self.set_y(121)

class PDF_noiseAnalysisReport1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,
                  test_perf_by,test_type,test_desc,report_to,select1,*args,**kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_perf_by = test_perf_by
          self.test_type = test_type
          self.test_desc = test_desc
          self.report_to = report_to
          self.select1 = select1



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('noiseAnalysis-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,65)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,80)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,91,txt="Test ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,97,txt="Test Performed Date:")
               self.text(110,97,txt=self.test_perf_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,103,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.test_type)

               self.line(105,87,105,117)

               self.rect(10,105,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,109,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.test_perf_by)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.5,115,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.test_desc)

               #table header
               self.rect(10,119.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,123.5,txt="Test Report")

          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")



          self.set_y(126)

class PDF_machineOilReportPdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,machine_sample_col_date,
                  machine_sample_col_by,machine_sample_type,machine_sample_desc,report_to,machine_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.machine_sample_col_date = machine_sample_col_date
          self.machine_sample_col_by = machine_sample_col_by
          self.machine_sample_type = machine_sample_type
          self.machine_sample_desc = machine_sample_desc
          self.report_to = report_to
          self.machine_test_desc = machine_test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('machineOil-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,86,txt="Sample ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(50.7,92,txt="Sample Collected/Received Date:")
               self.text(110,92,txt=self.machine_sample_col_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,98,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.machine_sample_desc)

               self.line(105,82,105,118)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,104,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.machine_sample_type)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(54.5,110,txt="Sample submitted/Received By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.machine_sample_col_by)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,116,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.machine_test_desc)
               #table header
               self.rect(10,120,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,125,txt="Analytical Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(127)

class PDF_machineOilReportPdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,machine_sample_col_date,
                  machine_sample_col_by,machine_sample_type,machine_sample_desc,report_to,machine_test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.machine_sample_col_date = machine_sample_col_date
          self.machine_sample_col_by = machine_sample_col_by
          self.machine_sample_type = machine_sample_type
          self.machine_sample_desc = machine_sample_desc
          self.report_to = report_to
          self.machine_test_desc = machine_test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('machineOil-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,70)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,85)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,91,txt="Sample ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(50.7,97,txt="Sample Collected/Received Date:")
               self.text(110,97,txt=self.machine_sample_col_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,103,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.machine_sample_desc)

               self.line(105,87,105,123)

               self.rect(10,105,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,109,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.machine_sample_type)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(54.5,115,txt="Sample submitted/Received By:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.machine_sample_col_by)

               self.rect(10,117,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,121,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,121,txt=self.machine_test_desc)
               #table header
               self.rect(10,125,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,130,txt="Analytical Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")

          self.set_y(133)

class PDF_microbialAnalysisPdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,micro_sample_col_date,
                  micro_sample_col_by,micro_sample_type,micro_sample_desc,report_to,micro_test_desc,micro_date_analysis_from,micro_date_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.micro_sample_col_date = micro_sample_col_date
          self.micro_sample_col_by = micro_sample_col_by
          self.micro_sample_type = micro_sample_type
          self.micro_sample_desc = micro_sample_desc
          self.report_to = report_to
          self.micro_test_desc = micro_test_desc
          self.micro_date_analysis_from = micro_date_analysis_from
          self.micro_date_analysis_to = micro_date_analysis_to
          self.date_of_analysis = micro_date_analysis_from +" to "+ micro_date_analysis_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('microbial-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,86,txt="Sample ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68,92,txt="Sample collected Date:")
               self.text(110,92,txt=self.micro_sample_col_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,98,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.micro_sample_desc)

               self.line(105,82,105,124)

               self.rect(10,100,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,104,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.micro_sample_type)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53.8,110,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.micro_sample_col_by)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,116,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.date_of_analysis)

               self.rect(10,118,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,122,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,122,txt=self.micro_test_desc)
               #table header
               self.rect(10,126,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,130,txt="Test Report")

          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(133)

class PDF_microbialAnalysisPdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,micro_sample_col_date,
                  micro_sample_col_by,micro_sample_type,micro_sample_desc,report_to,micro_test_desc,micro_date_analysis_from,micro_date_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no_number = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.micro_sample_col_date = micro_sample_col_date
          self.micro_sample_col_by = micro_sample_col_by
          self.micro_sample_type = micro_sample_type
          self.micro_sample_desc = micro_sample_desc
          self.report_to = report_to
          self.micro_test_desc = micro_test_desc
          self.micro_date_analysis_from = micro_date_analysis_from
          self.micro_date_analysis_to = micro_date_analysis_to
          self.date_of_analysis = micro_date_analysis_from +" to "+ micro_date_analysis_to



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)



          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no_number)

          target_url = self._rq_request.build_absolute_uri(reverse('microbial-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)


          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,70)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,85)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,91,txt="Sample ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68,97,txt="Sample collected Date:")
               self.text(110,97,txt=self.micro_sample_col_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,103,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.micro_sample_desc)

               self.line(105,87,105,129)

               self.rect(10,105,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,109,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.micro_sample_type)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53.8,115,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.micro_sample_col_by)

               self.rect(10,117,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,121,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,121,txt=self.date_of_analysis)

               self.rect(10,123,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,127,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,127,txt=self.micro_test_desc)
               #table header
               self.rect(10,131,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,136,txt="Test Report")

          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")


          self.set_y(138)

class PDF_viscousLiquidPdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,sample_Col_date,
                  sample_col_by,sample_type,sample_Desc,report_to,test_desc,date_of_analysis_from,date_of_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_Col_date = sample_Col_date
          self.sample_col_by = sample_col_by
          self.sample_type = sample_type
          self.sample_Desc = sample_Desc
          self.report_to = report_to
          self.test_desc = test_desc
          self.date_of_analysis_from = date_of_analysis_from
          self.date_of_analysis_to = date_of_analysis_to
          self.date_of_analysis = (date_of_analysis_from or "") +" to "+ (date_of_analysis_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(35)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,36,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,37,178+self.get_string_width(page_number),37)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,36,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,37,60,37)
          self.text(34,36,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,43,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,44,60,44)
          self.text(34,43,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('viscousLiquid-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=28,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,43,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,44,199,44)
          self.text(175,43,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,48,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,53, txt="Report to:")
               self.line(30,48,30,61)
               self.text(31,53,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,53,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,58,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,58,txt=self.address)

               self.rect(10,63,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,68, txt="Attention:")
               self.line(30,63,30,76)
               self.text(31,68,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,68,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,73,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,73,txt=self.email)


               self.rect(10,78,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,82,txt="Sample ID:")
               self.text(110,82,txt=self.sample_id)

               self.rect(10,84,190,6)
               self.set_font("Calibri","B", 10)
               self.text(66.5,88,txt="Sample Collection Date:")
               self.text(110,88,txt=self.sample_Col_date)


               self.rect(10,90.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,94,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,94,txt=self.sample_Desc)

               self.line(105,78,105,120)

               self.rect(10,96,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,100,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,100,txt=self.sample_type)

               self.rect(10,102,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53.5,106,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,106,txt=self.sample_col_by)

               self.rect(10,108,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,112,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,112,txt=self.date_of_analysis)

               self.rect(10,114,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,118,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,118,txt=self.test_desc)
               #table header
               self.rect(10,123.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,127,txt="Analytical Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-90, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(130)

class PDF_viscousLiquidPdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,sample_Col_date,
                  sample_col_by,sample_type,sample_Desc,report_to,test_desc,date_of_analysis_from,date_of_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_Col_date = sample_Col_date
          self.sample_col_by = sample_col_by
          self.sample_type = sample_type
          self.sample_Desc = sample_Desc
          self.report_to = report_to
          self.test_desc = test_desc
          self.date_of_analysis_from = date_of_analysis_from
          self.date_of_analysis_to = date_of_analysis_to
          self.date_of_analysis = (date_of_analysis_from or "") +" to "+ (date_of_analysis_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)



          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(45)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,46,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,47,178+self.get_string_width(page_number),47)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,47,60,47)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,53,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,54,60,54)
          self.text(34,53,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('viscousLiquid-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,53,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,54,199,54)
          self.text(175,53,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,58,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,63, txt="Report to:")
               self.line(30,58,30,66)
               self.text(31,63,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,63,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,68,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,68,txt=self.address)

               self.rect(10,73,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,78, txt="Attention:")
               self.line(30,73,30,81)
               self.text(31,78,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,78,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,83,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,83,txt=self.email)


               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,92,txt="Sample ID:")
               self.text(110,92,txt=self.sample_id)

               self.rect(10,94,190,6)
               self.set_font("Calibri","B", 10)
               self.text(66.5,98,txt="Sample Collection Date:")
               self.text(110,98,txt=self.sample_Col_date)


               self.rect(10,100.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.2,104,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.sample_Desc)

               self.line(105,88,105,130)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.8,110,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.sample_type)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(53.5,116,txt="Sample Collected/Submitted By:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.sample_col_by)

               self.rect(10,118,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,123,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,123,txt=self.date_of_analysis)

               self.rect(10,124,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,128,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,128,txt=self.test_desc)
               #table header
               self.rect(10,133.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,138,txt="Analytical Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-90, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")



          self.set_y(140)

class PDF_ambientAir2Pdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,
                  test_test_perf_by,test_type,report_to,test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_test_perf_by = test_test_perf_by
          self.test_type = test_type
          self.report_to = report_to
          self.test_desc = test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(43)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,44,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,45,178+self.get_string_width(page_number),45)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,44,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,45,60,45)
          self.text(34,44,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,51,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,52,60,52)
          self.text(34,51,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('ambientAir2-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=35,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,51,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,52,199,52)
          self.text(175,51,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,58,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,63, txt="Report to:")
               self.line(30,58,30,69)
               self.text(31,63,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,63,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,68,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,68,txt=self.address)

               self.rect(10,73,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,78, txt="Attention:")
               self.line(30,73,30,84)
               self.text(31,78,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,78,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,83,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,83,txt=self.email)


               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(90,92,txt="Test ID:")
               self.text(110,92,txt=self.sample_id)

               self.rect(10,94,190,6)
               self.set_font("Calibri","B", 10)
               self.text(69.7,98,txt="Test Performed Date:")
               self.text(110,98,txt=self.test_perf_date)


               self.rect(10,100.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.5,104,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.test_test_perf_by)

               self.line(105,88,105,118)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(85.5,110,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.test_type)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.8,116,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.test_desc)


               #table header
               self.rect(10,123.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(87,127.5,txt="Ambient Air Quality Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)



          self.set_y(130)

class PDF_ambientAir2Pdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,
                  test_test_perf_by,test_type,report_to,test_desc,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_test_perf_by = test_test_perf_by
          self.test_type = test_type
          self.report_to = report_to
          self.test_desc = test_desc



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)



          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(43)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,44,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,45,178+self.get_string_width(page_number),45)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,44,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,45,60,45)
          self.text(34,44,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,51,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,52,60,52)
          self.text(34,51,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('ambientAir2-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=36,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,51,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,52,199,52)
          self.text(175,51,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,58,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,63, txt="Report to:")
               self.line(30,58,30,69)
               self.text(31,63,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,63,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,68,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,68,txt=self.address)

               self.rect(10,73,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,78, txt="Attention:")
               self.line(30,73,30,84)
               self.text(31,78,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,78,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,83,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,83,txt=self.email)


               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(90,92,txt="Test ID:")
               self.text(110,92,txt=self.sample_id)

               self.rect(10,94,190,6)
               self.set_font("Calibri","B", 10)
               self.text(69.7,98,txt="Test Performed Date:")
               self.text(110,98,txt=self.test_perf_date)


               self.rect(10,100.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72.5,104,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.test_test_perf_by)

               self.line(105,88,105,118)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(85.5,110,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.test_type)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.8,116,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.test_desc)


               #table header
               self.rect(10,123.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(87,127.5,txt="Ambient Air Quality Test Report")


          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)

          #footer
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")


          self.set_y(130)

class PDF_wasteWater2Pdf(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,sample_Col_date,sampling_method,
                  sample_collected_by,sample_type,sample_desc,report_to,test_description,date_of_analysis_from,date_of_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_Col_date = sample_Col_date
          self.sample_collected_by = sample_collected_by
          self.sample_type = sample_type
          self.sample_desc = sample_desc
          self.sampling_method = sampling_method
          self.report_to = report_to
          self.test_description = test_description
          self.date_of_analysis = (date_of_analysis_from or "") +" to "+ (date_of_analysis_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('wasteWater2-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,86,txt="Sample ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(66,92,txt="Sample Collection Date:")
               self.text(110,92,txt=self.sample_Col_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74,98,txt="Sampling Method:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.sampling_method)

               self.rect(10,100.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,104,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.sample_desc)

               self.line(105,82,105,130)

               self.rect(10,106,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.3,110,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.sample_type)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(70.5,116,txt="Sample Collected By:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.sample_collected_by)

               self.rect(10,118,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,122,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,122,txt=self.date_of_analysis)

               self.rect(10,124,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,128,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,128,txt=self.test_description)
               #table header
               self.rect(10,132.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,136.5,txt="Analytical Test Report")



          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-150, 200,self.lab_report_no)

               self.rotate(0)


          self.set_y(139)

class PDF_wasteWater2Pdf1(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,sample_Col_date,sampling_method,
                  sample_collected_by,sample_type,sample_desc,report_to,test_description,date_of_analysis_from,date_of_analysis_to,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.sample_Col_date = sample_Col_date
          self.sample_collected_by = sample_collected_by
          self.sample_type = sample_type
          self.sample_desc = sample_desc
          self.sampling_method = sampling_method
          self.report_to = report_to
          self.test_description = test_description
          self.date_of_analysis = (date_of_analysis_from or "") +" to "+ (date_of_analysis_to or "")



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)



          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)



          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('wasteWater2-view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,70)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,85)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,91,txt="Sample ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(66,97,txt="Sample Collection Date:")
               self.text(110,97,txt=self.sample_Col_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(74,103,txt="Sampling Method:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.sampling_method)

               self.rect(10,105.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,109,txt="Sample Description:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.sample_desc)

               self.line(105,87,105,135)

               self.rect(10,111,190,6)
               self.set_font("Calibri","B", 10)
               self.text(81.3,115,txt="Sample Type:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.sample_type)

               self.rect(10,117,190,6)
               self.set_font("Calibri","B", 10)
               self.text(70.5,121,txt="Sample Collected By:")
               self.set_font("Calibri","", 10)
               self.text(110,121,txt=self.sample_collected_by)

               self.rect(10,123,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76,127,txt="Date Of Analysis:")
               self.set_font("Calibri","", 10)
               self.text(110,127,txt=self.date_of_analysis)

               self.rect(10,129,190,6)
               self.set_font("Calibri","B", 10)
               self.text(76.5,133,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,133,txt=self.test_description)
               #table header
               self.rect(10,137.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,141.5,txt="Analytical Test Report")



          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 200,self.lab_report_no)

               self.rotate(0)


          #footer
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")


          self.set_y(144)

class PDF_noiseMonitoring_print(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,test_method,test_location,
                  test_perf_by,test_type,test_desc,report_to,select1,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_perf_by = test_perf_by
          self.test_type = test_type
          self.test_desc = test_desc
          self.report_to = report_to
          self.select1 = select1
          self.test_method = test_method
          self.test_location = test_location



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(39)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,40,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          #header table
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,40,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,41,60,41)
          self.text(34,40,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,47,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,48,60,48)
          self.text(34,47,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('noiseMonitoring_view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=33,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,47,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,48,199,48)
          self.text(175,47,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,52,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,57, txt="Report to:")
               self.line(30,52,30,65)
               self.text(31,57,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,57,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,62,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.address)

               self.rect(10,67,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,72, txt="Attention:")
               self.line(30,67,30,80)
               self.text(31,72,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,72,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,77,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.email)


               self.rect(10,82,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,86,txt="Test ID:")
               self.text(110,86,txt=self.sample_id)

               self.rect(10,88,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,92,txt="Test Performed Date:")
               self.text(110,92,txt=self.test_perf_date)


               self.rect(10,94.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,98,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,98,txt=self.test_type)

               self.rect(10,100.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(80.8,104,txt="Test Method:")
               self.set_font("Calibri","", 10)
               self.text(110,104,txt=self.test_method)

               self.rect(10,106.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,110,txt="Location:")
               self.set_font("Calibri","", 10)
               self.text(110,110,txt=self.test_location)

               self.line(105,82,105,124)

               self.rect(10,112,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,116,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,116,txt=self.test_perf_by)

               self.rect(10,118,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.5,122,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,122,txt=self.test_desc)

               #table header
               self.rect(10,126.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,130.5,txt="Test Report")

          #water mark

          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.rotate(0)
               self.set_text_color(192, 192, 180) # Light gray text
               # pdf.set_xy(50, 260)

               self.text(70, 220,self.lab_report_no)

               self.rotate(0)


          self.set_y(133)

class PDF_noiseMonitoring_report(FPDF):
     def __init__(self,lab_report_no,invoice_bill_no,reporting_date,address,attention,email,sample_id,test_perf_date,test_method,test_location,
                  test_perf_by,test_type,test_desc,report_to,select1,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.show_full_header = True
          self.lab_report_no = lab_report_no
          self.invoice_bill_no = invoice_bill_no
          self.reporting_date = reporting_date
          self.address = address
          self.attention = attention
          self.email = email
          self.sample_id = sample_id
          self.test_perf_date = test_perf_date
          self.test_perf_by = test_perf_by
          self.test_type = test_type
          self.test_desc = test_desc
          self.report_to = report_to
          self.select1 = select1
          self.test_method = test_method
          self.test_location = test_location



     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)
          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)


          #
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(130)
          self.set_y(44)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(159.5,45,txt="Page No:")
          self.set_font("Calibri","", 10)
          self.line(175,46,178+self.get_string_width(page_number),46)
          self.cell(self.w - 25, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)

          #header table
          self.set_text_color(0, 0, 0)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 10)

          self.set_font("Calibri","B", 10)
          self.text(10,45,txt="Lab Report No:")
          self.set_font("Calibri","", 10)
          self.line(34,46,60,46)
          self.text(34,45,txt=self.lab_report_no)

          self.set_font("Calibri","B", 10)
          self.text(10,52,txt="Invoice Bill No:")
          self.set_font("Calibri","", 10)
          self.line(34,53,60,53)
          self.text(34,52,txt=self.invoice_bill_no)

          target_url = self._rq_request.build_absolute_uri(reverse('noiseMonitoring_view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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

          self.image(qr_file_path,"C",y=37,w=20,h=20)

          self.set_font("Calibri","B", 10)
          self.text(150,52,txt="Reporting Date:")
          self.set_font("Calibri","", 10)
          self.line(175,53,199,53)
          self.text(175,52,txt=self.reporting_date)



          if self.show_full_header:
               self.rect(10,57,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,62, txt="Report to:")
               self.line(30,57,30,65)
               self.text(31,62,txt='M/s.')
               self.set_font("Calibri","", 10)
               self.text(46,62,txt=self.report_to)
               self.set_font("Calibri","B", 10)
               self.text(31,67,txt='Address')
               self.set_font("Calibri","", 10)
               self.text(46,67,txt=self.address)

               self.rect(10,72,190,13)
               self.set_font("Calibri","B", 10)
               self.text(12,77, txt="Attention:")
               self.line(30,72,30,80)
               self.text(31,77,txt='Mr/Ms.')
               self.set_font("Calibri","", 10)
               self.text(46,77,txt=self.attention)
               self.set_font("Calibri","B", 10)
               self.text(31,82,txt='Email')
               self.set_font("Calibri","", 10)
               self.text(46,82,txt=self.email)


               self.rect(10,87,190,6)
               self.set_font("Calibri","B", 10)
               self.text(89,91,txt="Test ID:")
               self.text(110,91,txt=self.sample_id)

               self.rect(10,93,190,6)
               self.set_font("Calibri","B", 10)
               self.text(68.7,97,txt="Test Performed Date:")
               self.text(110,97,txt=self.test_perf_date)


               self.rect(10,99.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(84.8,103,txt="Test Type:")
               self.set_font("Calibri","", 10)
               self.text(110,103,txt=self.test_type)

               self.rect(10,105.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(80.8,109,txt="Test Method:")
               self.set_font("Calibri","", 10)
               self.text(110,109,txt=self.test_method)

               self.rect(10,111.1,190,6)
               self.set_font("Calibri","B", 10)
               self.text(86,115,txt="Location:")
               self.set_font("Calibri","", 10)
               self.text(110,115,txt=self.test_location)


               self.line(105,87,105,129)

               self.rect(10,117,190,6)
               self.set_font("Calibri","B", 10)
               self.text(72,121,txt="Test Performed By:")
               self.set_font("Calibri","", 10)
               self.text(110,121,txt=self.test_perf_by)

               self.rect(10,123,190,6)
               self.set_font("Calibri","B", 10)
               self.text(75.5,127,txt="Test Description:")
               self.set_font("Calibri","", 10)
               self.text(110,127,txt=self.test_desc)

               #table header
               self.rect(10,134.1,190,7)
               self.set_font("Calibri","B", 12)
               self.text(89,139.5,txt="Test Report")

          #water mark
          with self.local_context(fill_opacity=0.5):
               self.set_font("Arial", "B", 50)
               self.set_text_color(192, 192, 180) # Light gray text
               # self.set_xy(50, 260)
               self.rotate(45)
               self.text(-120, 180,self.lab_report_no)

               self.rotate(0)


          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")



          self.set_y(141)


class PDF_samplePdf(FPDF):

     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)


          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 19)
          self.set_text_color(25, 27, 28)
          self.text(70,28,txt="Sample Registration Form")

          x = 148
          y = 0
          width = 64
          height = 8
          skew_width = 7  # Adjusted width for the sloped side
          skew_angle = 50
          color = (12, 168, 74)  # RGB color for #0CA84A


          # Draw the main rectangle
          self.set_fill_color(*color)
          self.rect(x, y, width, height, 'F',)

          # Draw the sloped side
          self.set_draw_color(12, 168, 74)
          self.polygon([(x - skew_width, y), (x, y), (x, y + height)], 'DF')

          self.set_font("Calibri","B", 10)
          self.set_draw_color(25, 27, 2)
          self.rect(158,12,40,20,"D")
          self.text(160,17,txt=self._rq_sample.lab_no)
          self.text(160,21,txt=self._rq_sample.issue_date)
          self.text(160,25,txt=self._rq_sample.issue_no)
          self.set_text_color(0, 0, 0)
          self.alias_nb_pages()
          old_x = self.get_x()
          old_y = self.get_y()
          self.set_x(100)
          self.set_y(28)
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          page_number = f"{self.page_no()}s: of {{nb}}"
          self.set_font("Calibri","B", 10)
          self.text(160,29,txt="Page No:")
          self.set_font("Calibri","B", 10)
          # self.line(175,41,178+self.get_string_width(page_number),41)
          self.cell(self.w - 33, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
          self.set_x(old_x)
          self.set_y(old_y)


          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)





          self.set_text_color(10, 10, 10)
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 9)


          self.set_y(-10)
          self.set_x(0)

          self.image('static/assets/phone.PNG',10,self.h-15,7,7)
          self.image('static/assets/office.PNG',50,self.h-16,9,9)
          self.set_font("Calibri","", 10)
          if self._rq_sample.city_location == 'Karachi':
                self.text(18,self.h-10,txt="+92 310 2288801")
                self.text(60,self.h-12,txt="Head Office:345,First Floor, Street-15,Block-3")
                self.text(60,self.h-8,txt="Bahadurabad, Karachi, 75900, Pakistan")

          if self._rq_sample.city_location == 'Lahore':
                self.text(18,self.h-10,txt="+92 42 32296099")
                self.text(60,self.h-12,txt="Lahore Office: 87-E Madina Height, Office # A/30 & ")
                self.text(60,self.h-8,txt=" A/31 8th Floor,Johar Town, Lahore")

          self.image('static/assets/polyPNG-removebg-preview.png',130,275,90,23)

          self.set_draw_color(12, 168, 74)
          self.set_fill_color(*color)
          self.rect(0,self.h-4,self.w,5,'DF')

class PDF_calib_pdf(FPDF):




     def header(self):
          self.set_y(0)
          self.set_x(0)
          # self.image("static/assets/header.PNG",0,0,self.w,22.5)

          self.image("static/assets/Header watermark.jpg",0,0,self.w,35)
          self.image("static/assets/EnviTechAL LOGO.png",16,5,26,28)
          self.set_line_width(0.5)
          self.set_draw_color(26, 84, 26)
          self.line(0,35,self.w,35)
          font_path_alger = "static/fonts/ALGER.TTF"
          self.add_font("Algerian","",font_path_alger)
          self.set_font("Algerian","", 16)
          self.set_text_color(13, 46, 145)
          self.text(85,20,txt="ENVI TECH AL")
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","B", 11)
          self.set_text_color(26, 84, 26)
          self.text(55,28,txt="We strive for Pragmatic approach to achieve quality Excellence")
          self.image('static/assets/GreenLab-Gold-LOGO-S-e1578648052937-removebg-preview.png',168,5,27,28)


          #body watermark

          self.image('static/assets/report water mark.png',0,35,self.w,self.h)


          self.set_line_width(0.2)
          self.set_draw_color(0,0,0)




           #water mark
          # with pdf.local_context(fill_opacity=0.5):
          #      self.set_font("Arial", "B", 50)
          #      self.set_text_color(192, 192, 180) # Light gray text
          #      # self.set_xy(50, 260)
          #      self.rotate(45)
          #      self.text(-120, 180,txt="test")

          #      self.rotate(0)
          self.set_text_color(10, 10, 10)
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.set_font("Calibri","", 9)
          self.add_font('ScriptMT', '', 'static/fonts/SCRIPTBL.TTF', uni=True)
          self.set_font('ScriptMT', '', 25)
          self.text(56,43,txt='Certificate of Calibration')
          self.set_font("Calibri","B", 11)
          self.text(10,52,txt='Certificate Number:')
          self.line(42,53.5,60,53.5)
          self.set_font("Calibri","", 11)
          self.text(43,52,txt=self._rq_calib.cert_num)


          target_url = self._rq_request.build_absolute_uri(reverse('calib_view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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


          self.image(qr_file_path,"R",y=36,w=20,h=20)
          self.set_y(-10)
          self.set_x(0)
          # self.image("static/assets/footer.PNG", 0, self.h - 10, self.w, 10)  # Add the footer image 
          self.set_fill_color(40, 25, 105)    
          self.rect(0,self.h-14,self.w,12,"F")
          self.image("static/assets/Picture1.png",5,self.h-16,14,14)
          self.set_text_color(255, 255, 255)
          self.set_font("Calibri","", 9)
          self.text(18,self.h-7,txt="Lahore Office: 87-E Madina Height,Office # A/30 & A/31, 8th Floor, Maulana Shaukat Ali Road,+924232296099")
          self.text(18,self.h-10,txt="Head Office:345,First floor,Street-15,Block-3,Bahadurabad,Karachi,75900,Pakistan. 03102288801")
          self.set_fill_color(255, 255, 255)   
          self.image("static/assets/earth.png",165,self.h-12,7,7)
          self.text(175,self.h-7,txt="info@envitechal.com")
          self.text(175,self.h-10,txt="www.envitechal.com")

     def add_page(self, *args, **kwargs):
          super().add_page(*args, **kwargs)
          self.set_top_margin(40)

class PDF_calib_pdf1(FPDF):




     def header(self):
          self.set_y(0)
          self.set_x(0)

          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          self.add_font("Calibri","",font_path,uni=True)
          self.add_font("Calibri","B",font_path_bold,uni=True)
          self.add_font('ScriptMT', '', 'static/fonts/SCRIPTBL.TTF', uni=True)
          self.set_font('ScriptMT', '', 25)
          self.text(56,43,txt='Certificate of Calibration')
          self.set_font("Calibri","B", 11)
          self.text(10,52,txt='Certificate Number:')
          self.line(42,53.5,60,53.5)
          self.set_font("Calibri","", 11)
          self.text(43,52,txt=self._rq_calib.cert_num)

          target_url = self._rq_request.build_absolute_uri(reverse('calib_view', kwargs={'pk': self._rq_pk}))

          # Generate the QR code for the target URL
          qr_filename = f"qr_{self._rq_pk}.png"
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
          self.image(qr_file_path,"R",y=34,w=20,h=20)


     def add_page(self):
          super().add_page()
          self.set_top_margin(40)     
