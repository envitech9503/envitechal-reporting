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
