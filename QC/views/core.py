# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403

def filter_sign(sign):
    signs = Signatures.objects.filter(user__in=active_users)
    return sign

# Create your views here.
def qc_main(request):
    config = QCAuditConfig.objects.first()

    context = {
        "dw_audit_url": config.use_manual_dw if config else False,
        "ww_audit_url": config.use_manual_ww if config else False,
    }

    return render(request, "qc_main.html", context)



class CustomPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Register custom fonts here ONCE
        font_path = "static/fonts/calibri.ttf"
        font_path_bold = "static/fonts/calibrib.ttf"
        font_path_alger = "static/fonts/ALGER.TTF"

        self.add_font("Calibri", "", font_path, uni=True)
        self.add_font("Calibri", "B", font_path_bold, uni=True)
        self.add_font("Algerian", "", font_path_alger, uni=True)

    def header(self):
        
        self.set_y(0)
        self.set_x(0)
        # self.image("static/assets/header.PNG",0,0,self.w,22.5)

        
        self.image("static/assets/EnviTechAL LOGO.png",16,5,22,24)
        self.set_line_width(0.5)
        self.set_draw_color(26, 84, 26)
        self.line(0,31,self.w,31)
        font_path_alger = "static/fonts/ALGER.TTF"
        self.add_font("Algerian","",font_path_alger)
        self.set_font("Algerian","", 16)
        self.set_text_color(13, 46, 145)
        self.text(85,15,txt="ENVI TECH AL")
        font_path = "static/fonts/calibri.ttf"
        font_path_bold = "static/fonts/calibrib.ttf"
        self.add_font("Calibri","B",font_path_bold,uni=True)
        self.set_font("Calibri","B", 19)
        self.set_text_color(25, 27, 28)
        self.text(80,23,txt="Raw Data Sheet")

        x = 148
        y = 0
        width = 64
        height = 4
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
        self.rect(158,8,40,20,"D")
        self.text(160,13,txt="ETAL-LAB-704-FF-05")
        self.text(160,17,txt="Issue Date: 22-12-2025")
        self.text(160,21,txt="Issue No. 02 Rev. No. 01")
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
        self.text(160,25.5,txt="Page No:")
        self.set_font("Calibri","B", 10)
        # self.line(175,41,178+self.get_string_width(page_number),41)
        self.ln(-3.5)
        self.cell(self.w - 29, 0, f'{self.page_no()} of {{nb}}',border=False, align='R')
        self.set_x(old_x)
        self.set_y(old_y)


        # self.image('static/assets/report water mark.png',0,35,self.w,self.h)
        

        self.set_line_width(0.2)
        self.set_draw_color(0,0,0)
        
        


         
        self.set_text_color(10, 10, 10)
        self.add_font("Calibri","",font_path,uni=True)
        self.add_font("Calibri","B",font_path_bold,uni=True)
        self.set_font("Calibri","", 9)

__all__ = [
    'filter_sign',
    'qc_main',
    'CustomPDF',
]
