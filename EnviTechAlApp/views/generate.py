# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403




def generate_leq_chart(results, limit_value, method_limit, leq_value, time_labels=None):
    plt.figure(figsize=(8, 4))

    x = range(len(results))
    bar_width = 0.3  # Slightly reduced width to accommodate 3 bars

    # Colors for results (red if above limit)
    colors = ['red' if r > limit_value else 'blue' for r in results]

    # Plot bars
    result_bars = plt.bar(
        [i - bar_width for i in x],  # Adjusted positioning
        results,
        width=bar_width,
        color=colors,
        alpha=0.8,
        label='Result'
    )

    limit_bars = plt.bar(
        x,  # Middle position
        [limit_value]*len(results),
        width=bar_width,
        color='green',
        alpha=0.6,
        label=f'{method_limit} Limit'
    )
    
    # ✅ Add leq_value column
    leq_color = 'orange' if leq_value > limit_value else 'gold'
    leq_bars = plt.bar(
        [i + bar_width for i in x],  # Right position
        [leq_value]*len(results),
        width=bar_width,
        color=leq_color,
        alpha=0.8,
        label='Leq Value'
    )

    # ✅ Add value labels on top of each bar
    for bar in result_bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f'{height:.0f}',
            ha='center',
            va='bottom',
            fontsize=7
        )

    for bar in limit_bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f'{height:.0f}',
            ha='center',
            va='bottom',
            fontsize=7,
            color='darkgreen'
        )
    
    for bar in leq_bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f'{height:.0f}',
            ha='center',
            va='bottom',
            fontsize=7,
            color='darkred' if leq_value > limit_value else 'darkgoldenrod'
        )

    # Labels, title, etc.
    if time_labels:
        plt.xticks(x, time_labels, rotation=45, ha='right', fontsize=8)
    else:
        plt.xticks(x, [str(i+1) for i in x])

    plt.xlabel('Time')
    plt.ylabel('dB(A)')
    plt.title('')
    plt.legend()
    plt.tight_layout()

    # Save chart to memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120)
    plt.close()
    buffer.seek(0)
    return buffer


def generate_leq_line_chart(results, limit_value, leq_result, method_limit, time_labels=None):
    plt.figure(figsize=(10, 5))
    x = range(len(results))

    # Draw colored line segments
    for i in range(1, len(results)):
        if results[i] > limit_value and results[i-1] > limit_value:
            color = 'red'  # Both above limit
        elif results[i] > limit_value or results[i-1] > limit_value:
            color = 'red'  # Crossing limit
        else:
            color = 'blue'  # Within limit

        plt.plot([x[i-1], x[i]], [results[i-1], results[i]], color=color, linewidth=1.8)

    # Scatter points
    colors = ['red' if r > limit_value else 'blue' for r in results]
    plt.scatter(x, results, color=colors, s=15, label='Results')

    # Data labels above points
    for i, r in enumerate(results):
        plt.text(x[i], r + 0.3, f"{r:.1f}", ha='left', va='bottom', fontsize=5)

    # Limit line (Green solid)
    plt.plot(x, [limit_value]*len(results), color='green', linestyle='-', linewidth=1.2,
             label=f'{method_limit} Limit ({limit_value} dB)')

    # Leq line (Red if above limit, Yellow if within)
    leq_color = 'red' if leq_result > limit_value else 'gold'
    plt.axhline(y=leq_result, color=leq_color, linestyle='-', linewidth=1.5,
                label=f'Leq ({leq_result:.1f} dB)')

    # Axes labels and title
    if time_labels:
        plt.xticks(x, time_labels, rotation=45, ha='right', fontsize=6)
    else:
        plt.xticks(x, [str(i+1) for i in x])

    plt.xlabel('Time')
    plt.ylabel('Noise Level (dB)')
    plt.title('')
    plt.legend(fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    # Save to memory buffer (for embedding in PDF)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120)
    plt.close()
    buffer.seek(0)
    return buffer
     
@login_required(login_url="/login")
def generate_merged_pdf(request):
     
     if request.method == 'POST':
          selected_reports = json.loads(request.POST['selected_reports'])
          print('Selected lab_report_nos:', selected_reports)
          selected_reports = [r for r in selected_reports if r]

          if selected_reports:
               from ..merger_pdf import merge_pdfs

               merged_buffer = merge_pdfs(selected_reports, request)

               response = HttpResponse(merged_buffer.read(), content_type='application/pdf')
               filename = "merged_report.pdf"
               response['Content-Disposition'] = f'attachment; filename="{filename}"'
               return response

     return render(request, 'index.html', context={})


@login_required(login_url="/login")
def generate_merged_pdf_certificate(request):
    if request.method == 'POST':
        selected_cert = json.loads(request.POST['selected_reports'])
        
        # Filter out empty strings from selected_reports
        selected_cert = [cert_id for cert_id in selected_cert if cert_id]
        print("SELECTED REPORTS", selected_cert)
        
        if selected_cert:
            # Merge selected PDFs
            from ..merger_cert import merge_pdfs_cert
            merged_pdf_cert = merge_pdfs_cert(selected_cert, request)  # Pass request if needed
            
            response = HttpResponse(merged_pdf_cert.read(), content_type='application/pdf')
            filename = "merged_certificate.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    
    return render(request, 'certificate.html', context={})




def generatePDF(request,pk):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_generatePDF as PDFWithPageNumbers

     # def add_table_with_page_breaks(pdf, table_data, col_widths, line_height=6):
     #    """Helper function to add table with proper page break handling"""
     #    rows_per_page = calculate_rows_per_page(pdf, line_height)
        
     #    for i in range(0, len(table_data), rows_per_page):
     #        if i > 0:  # Not the first chunk
     #            pdf.add_page()
     #            pdf.show_full_header = False  # Don't show full header on subsequent pages
            
     #        chunk = table_data[i:i + rows_per_page]
            
     #        with pdf.table(col_widths=col_widths, line_height=line_height, 
     #                     text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:
     #            for data_row in chunk:
     #                row = table.row()
     #                for datum in data_row:
     #                    row.cell(datum)

     # def calculate_rows_per_page(pdf, line_height):
     #     """Calculate how many rows can fit on a page"""
     #     # Starting Y position after header
     #     start_y = pdf.get_y()
     #     # Available height (page height - top margin - bottom margin - footer space)
     #     available_height = pdf.h - start_y - 30  # 30 for footer and bottom margin
     #     # Rows that can fit
     #     return max(1, math.floor(available_height / line_height))

     # def add_notes_and_legends(pdf, waterForm):
     #     """Add notes and legends with proper page break checking"""
     #     # Check if we need a new page for notes
     #     if pdf.get_y() > pdf.h - 50:  # If too close to bottom
     #         pdf.add_page()
     #         pdf.show_full_header = False


     waterForm = DrinkingWaterForm.objects.get(id=pk)
     waterForm.extra_field = waterForm.extra_field.replace("'", "\"")
     waterForm.extra_field = json.loads(waterForm.extra_field)

     if waterForm.in_out == 'customLimits':
          TABLE_DATA = [
               ["Sr.#","Parameter/Analytes Description","Methods","Unit","Test Result",waterForm.custominput],
          ]
          sr_no = 1
          if waterForm.water_sr1:
               a = [str(sr_no),"pH @ 25°C",waterForm.method_1,"-",waterForm.water_sr1,waterForm.custominput1]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr2:
               a = [str(sr_no),"Total Dissolved Solids (TDS)",waterForm.method_2,"mg/L",waterForm.water_sr2,waterForm.custominput2]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr3:
               a = [str(sr_no),"Total Hardness as CaCO₃",waterForm.method_3,"mg/L",waterForm.water_sr3,waterForm.custominput3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr4:
               a = [str(sr_no),"Color",waterForm.method_4,"TCU",waterForm.water_sr4,waterForm.custominput4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr5:
               a = [str(sr_no),"Turbidity",waterForm.method_5,"NTU",waterForm.water_sr5,waterForm.custominput5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr6:
               a = [str(sr_no),"Nitrite",waterForm.method_6,"mg/L",waterForm.water_sr6,waterForm.custominput6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr7:
               a = [str(sr_no),"Nitrate (NO₃)",waterForm.method_7,"mg/L",waterForm.water_sr7,waterForm.custominput7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr8:
               a = [str(sr_no),"Taste",waterForm.method_8,"-",waterForm.water_sr8,waterForm.custominput8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr9:
               a = [str(sr_no),"Odor",waterForm.method_9,"-",waterForm.water_sr9,waterForm.custominput9]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr10:
               a = [str(sr_no),"Chloride (Cl)",waterForm.method_10,"mg/L",waterForm.water_sr10,waterForm.custominput10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr11:
               a = [str(sr_no),"Fluoride (F)",waterForm.method_11,"mg/L",waterForm.water_sr11,waterForm.custominput11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr12:
               a = [str(sr_no),"Aluminum (Al)",waterForm.method_12,"mg/L",waterForm.water_sr12,waterForm.custominput12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr13:
               a = [str(sr_no),"Nickel (Ni)",waterForm.method_13,"mg/L",waterForm.water_sr13,waterForm.custominput13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr14:
               a = [str(sr_no),"Lead (Pb)",waterForm.method_14,"mg/L",waterForm.water_sr14,waterForm.custominput14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr15:
               a = [str(sr_no),"Barium (Ba)",waterForm.method_15,"mg/L",waterForm.water_sr15,waterForm.custominput15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr16:
               a = [str(sr_no),"Antimony (Sb)",waterForm.method_16,"mg/L",waterForm.water_sr16,waterForm.custominput16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr17:
               a = [str(sr_no),"Arsenic (As)",waterForm.method_17,"mg/L",waterForm.water_sr17,waterForm.custominput17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr18:
               a = [str(sr_no),"Boron (B)",waterForm.method_18,"mg/L",waterForm.water_sr18,waterForm.custominput18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr19:
               a = [str(sr_no),"Cadmium (Cd)",waterForm.method_19,"mg/L",waterForm.water_sr19,waterForm.custominput19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr20:
               a = [str(sr_no),"Chromium (Cr)",waterForm.method_20,"mg/L",waterForm.water_sr20,waterForm.custominput20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr21:
               a = [str(sr_no),"Selenium (Se)",waterForm.method_21,"mg/L",waterForm.water_sr21,waterForm.custominput21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr22:
               a = [str(sr_no),"Copper (Cu)",waterForm.method_22,"mg/L",waterForm.water_sr22,waterForm.custominput22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr23:
               a = [str(sr_no),"Cyanide (CN)",waterForm.method_23,"mg/L",waterForm.water_sr23,waterForm.custominput23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr24:
               a = [str(sr_no),"Mercury (Hg)",waterForm.method_24,"mg/L",waterForm.water_sr24,waterForm.custominput24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr25:
               a = [str(sr_no),"Manganese (Mn)",waterForm.method_25,"mg/L",waterForm.water_sr25,waterForm.custominput25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr26:
               a = [str(sr_no),"Zinc (Zn)",waterForm.method_26,"mg/L",waterForm.water_sr26,waterForm.custominput26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr27:
               a = [str(sr_no),"Residual Chlorine",waterForm.method_27,"mg/L",waterForm.water_sr27,waterForm.custominput27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr28:
               a = [str(sr_no),"Phenolic Compounds as Phenols",waterForm.method_28,"mg/L",waterForm.water_sr28,waterForm.custominput28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr29:
               a = [str(sr_no),"Fecal Coliform",waterForm.method_29,"CFU/100 ml",waterForm.water_sr29,waterForm.custominput29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr30:
               a = [str(sr_no),"Total Coliform",waterForm.method_30,"CFU/100 ml",waterForm.water_sr30,waterForm.custominput30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr31:
               a = [str(sr_no),"E-Coli",waterForm.method_31,"CFU/100 ml",waterForm.water_sr31,waterForm.custominput31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr32:
               a = [str(sr_no),"Pesticides",waterForm.method_32,"mg/L",waterForm.water_sr32,waterForm.custominput32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          for extra_field in waterForm.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)




          pdf = PDFWithPageNumbers(report_number=waterForm.lab_report_no,invoice=waterForm.invoice_bill_no,reporting_date=waterForm.reporting_date,report_to=waterForm.report_to,
                                   address=waterForm.address,attention=waterForm.attention,email=waterForm.email,sample_id=waterForm.sample_id,sample_collection_date=waterForm.sample_collection_date,
                                   sample_description=waterForm.sample_description,sample_type=waterForm.sample_type,sample_collected_by=waterForm.sample_collected_by,
                                   date_of_analysis_to=waterForm.date_of_analysis_to, date_of_analysis_from=waterForm.date_of_analysis_from,test_description=waterForm.test_description,
                                   )
          pdf._rq_request, pdf._rq_pk = request, pk
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True, margin=12)









          #report data table
          num_rows = 0
          with pdf.table(col_widths=(6, 35, 20, 15,18,18),line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows = num_rows + 1
                    # if k == 0:
                    #      data_row[5] = waterForm.select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)     


     else:
          TABLE_DATA = [
          ["Sr.#","Parameter/Analytes Description","Methods","Unit","Test Result",""],
          ]
          sr_no = 1
          if waterForm.water_sr1:
               a = [str(sr_no),"pH @ 25°C",waterForm.method_1 or "*APHA 4500 H","-",waterForm.water_sr1,"6.5 - 8.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr2:
               a = [str(sr_no),"Total Dissolved Solids (TDS)",waterForm.method_2 or "*APHA 2540-C","mg/L",waterForm.water_sr2,"<1000"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr3:
               a = [str(sr_no),"Total Hardness as CaCO₃",waterForm.method_3 or "ASTM D 1126","mg/L",waterForm.water_sr3,"< 500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr4:
               a = [str(sr_no),"Color",waterForm.method_4 or "HACH 8025","TCU",waterForm.water_sr4,"≤ 15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr5:
               a = [str(sr_no),"Turbidity",waterForm.method_5 or "*APHA 2130","NTU",waterForm.water_sr5,"≤ 5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr6:
               a = [str(sr_no),"Nitrite",waterForm.method_6 or "HACH 8507","mg/L",waterForm.water_sr6,"≤ 3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr7:
               a = [str(sr_no),"Nitrate (NO₃)",waterForm.method_7 or "HACH 8039","mg/L",waterForm.water_sr7,"≤ 50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr8:
               a = [str(sr_no),"Taste",waterForm.method_8 or "*APHA 2160","-",waterForm.water_sr8,"Non-Objectionable"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr9:
               a = [str(sr_no),"Odor",waterForm.method_9 or "*APHA 2150","-",waterForm.water_sr9,"Non-Objectionable"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr10:
               a = [str(sr_no),"Chloride (Cl)",waterForm.method_10 or "*APHA 4500 Cl","mg/L",waterForm.water_sr10,"≤ 250"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr11:
               a = [str(sr_no),"Fluoride (F)",waterForm.method_11 or "HACH 8029","mg/L",waterForm.water_sr11,"≤ 1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr12:
               a = [str(sr_no),"Aluminum (Al)",waterForm.method_12 or "*APHA 3111-D","mg/L",waterForm.water_sr12,"≤ 0.2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr13:
               a = [str(sr_no),"Nickel (Ni)",waterForm.method_13 or "*APHA 3111-B","mg/L",waterForm.water_sr13,"≤ 0.02"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr14:
               a = [str(sr_no),"Lead (Pb)",waterForm.method_14 or "*APHA 3111-B","mg/L",waterForm.water_sr14,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr15:
               a = [str(sr_no),"Barium (Ba)",waterForm.method_15 or "HACH 8014","mg/L",waterForm.water_sr15," 0.7"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr16:
               a = [str(sr_no),"Antimony (Sb)",waterForm.method_16 or "*APHA 3111-B","mg/L",waterForm.water_sr16,"≤ 0.005"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr17:
               a = [str(sr_no),"Arsenic (As)",waterForm.method_17 or "*APHA 3114-B","mg/L",waterForm.water_sr17,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr18:
               a = [str(sr_no),"Boron (B)",waterForm.method_18 or "HACH 8015","mg/L",waterForm.water_sr18,"0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr19:
               a = [str(sr_no),"Cadmium (Cd)",waterForm.method_19 or "*APHA 3111-B","mg/L",waterForm.water_sr19,"0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr20:
               a = [str(sr_no),"Chromium (Cr)",waterForm.method_20 or "*APHA 3111-B","mg/L",waterForm.water_sr20,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr21:
               a = [str(sr_no),"Selenium (Se)",waterForm.method_21 or "*APHA 3114-B","mg/L",waterForm.water_sr21,"0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr22:
               a = [str(sr_no),"Copper (Cu)",waterForm.method_22 or "*APHA 3111-B","mg/L",waterForm.water_sr22,"2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr23:
               a = [str(sr_no),"Cyanide (CN)",waterForm.method_23 or "HACH 8027","mg/L",waterForm.water_sr23,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr24:
               a = [str(sr_no),"Mercury (Hg)",waterForm.method_24 or "*APHA 3112-B","mg/L",waterForm.water_sr24,"≤ 0.001"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr25:
               a = [str(sr_no),"Manganese (Mn)",waterForm.method_25 or "*APHA 3111-B","mg/L",waterForm.water_sr25,"≤ 0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr26:
               a = [str(sr_no),"Zinc (Zn)",waterForm.method_26 or "*APHA 3111-B","mg/L",waterForm.water_sr26,"≤ 5.0"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr27:
               a = [str(sr_no),"Residual Chlorine",waterForm.method_27 or "HACH 10069","mg/L",waterForm.water_sr27,"0.2 - 0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr28:
               a = [str(sr_no),"Phenolic Compounds as Phenols",waterForm.method_28 or "ASTM-D-1783","mg/L",waterForm.water_sr28,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr29:
               a = [str(sr_no),"Fecal Coliform",waterForm.method_29 or "USEPA 1604","CFU/100 ml",waterForm.water_sr29,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr30:
               a = [str(sr_no),"Total Coliform",waterForm.method_30 or "*APHA 922 B","CFU/100 ml",waterForm.water_sr30,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr31:
               a = [str(sr_no),"E-Coli",waterForm.method_31 or "USEPA 1604","CFU/100 ml",waterForm.water_sr31,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr32:
               a = [str(sr_no),"Pesticides",waterForm.method_32 or "USEPA-614.1","mg/L",waterForm.water_sr32,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          for extra_field in waterForm.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)




          pdf = PDFWithPageNumbers(report_number=waterForm.lab_report_no,invoice=waterForm.invoice_bill_no,reporting_date=waterForm.reporting_date,report_to=waterForm.report_to,
                                   address=waterForm.address,attention=waterForm.attention,email=waterForm.email,sample_id=waterForm.sample_id,sample_collection_date=waterForm.sample_collection_date,
                                   sample_description=waterForm.sample_description,sample_type=waterForm.sample_type,sample_collected_by=waterForm.sample_collected_by,
                                   date_of_analysis_to=waterForm.date_of_analysis_to, date_of_analysis_from=waterForm.date_of_analysis_from,test_description=waterForm.test_description,
                                   )
          pdf._rq_request, pdf._rq_pk = request, pk

                                   
          pdf.add_page()
          font_path = "static/fonts/calibri.ttf"
          font_path_bold = "static/fonts/calibrib.ttf"
          pdf.add_font("Calibri","",font_path,uni=True)
          pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True, margin=12)









          #report data table
          num_rows = 0
          with pdf.table(col_widths=(6, 35, 20, 15,18,18),line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows = num_rows + 1
                    if k == 0:
                         data_row[5] = waterForm.select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)     
     
     
     # add_table_with_page_breaks(pdf, TABLE_DATA, col_widths=(6, 35, 20, 15, 18, 18))
     # add_notes_and_legends(pdf, waterForm)
     # # Calculate the table height based on the number of rows and row height
     number_of_rows = len(TABLE_DATA)  # Replace with the actual number of rows
     row_height = 6  # Replace with the actual row height in your table
     table_height = (number_of_rows) * row_height   
     
     if pdf.y + number_of_rows * row_height >= pdf.h:
          pdf.add_page()             
     
     
          
          

     
     Table_Data1 = [
          
     ]
     if waterForm.edit_note:
          a=["Note: "+ waterForm.edit_note] 
          Table_Data1.append(a)
          
          
     
     # with pdf.table(col_widths=(190),width=190,line_height=6,text_align=("LEFT")) as table:
         
          for k in range(0,len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if waterForm.legend_1:
          a = [waterForm.legend_1]
          Table_data_legend.append(a)
          
     if waterForm.legend_2:
          a = [waterForm.legend_2]
          Table_data_legend.append(a)
          
     if waterForm.legend_3:
          a = [waterForm.legend_3]
          Table_data_legend.append(a)
          
     if waterForm.legend_4:
          a = [waterForm.legend_4]
          Table_data_legend.append(a)
          
     if waterForm.legend_5:
          a = [waterForm.legend_5]
          Table_data_legend.append(a)
          
     if waterForm.legend_6:
          a = [waterForm.legend_6]
          Table_data_legend.append(a)
          
     if waterForm.legend_7:
          a = [waterForm.legend_7]
          Table_data_legend.append(a)
          
     if waterForm.legend_8:
          a = [waterForm.legend_8]
          Table_data_legend.append(a)
          
     if waterForm.legend_9:
          a = [waterForm.legend_9]
          Table_data_legend.append(a)
          
     if waterForm.legend_10:
          a = [waterForm.legend_10]
          Table_data_legend.append(a)
          
     if waterForm.legend_11:
          a = [waterForm.legend_11]
          Table_data_legend.append(a)
          
     pdf.set_auto_page_break(auto=True, margin=15)
     
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     
     

     
     # if waterForm.city_location.strip().lower().startswith('karachi'):
     #      pdf.image(karachi_analyst.signature,30,231,20.32,20.32)
     #      pdf.line(19,250,36+pdf.get_string_width("Analyzed By (Analyst)"),250)
     #      pdf.text(26,253,"Analyzed By (Analyst)")
     #      pdf.image(karachi_assistant_manager.signature,100,232,20.32,20.32)
     #      pdf.line(126,250,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),250)
     #      pdf.text(87.5,253,"Reviewed By (Assistant Manager)")
     #      pdf.image(waterForm.approved_by,154,228,22,22)
     #      pdf.image(karachi_lab_manager.signature,178,233,20.32,20.32)
     #      pdf.line(155,250,165+pdf.get_string_width("Approved By (Lab Manager)"),250)
     #      pdf.text(160,253,"Approved By (Lab Manager)")
     
     # elif waterForm.city_location == 'Lahore':
     #      pdf.image(lahore_analyst.signature,30,231,20.32,20.32)
     #      pdf.line(19,250,36+pdf.get_string_width("Analyzed By (Analyst)"),250)
     #      pdf.text(26,253,"Analyzed By (Analyst)")
     #      pdf.image(lahore_assistant_manager.signature,100,232,20.32,20.32)
     #      pdf.line(126,250,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),250)
     #      pdf.text(87.5,253,"Reviewed By (Assistant Manager)")
     #      pdf.image(waterForm.approved_by,154,228,22,22)
     #      pdf.image(lahore_lab_manager.signature,178,233,20.32,20.32)
     #      pdf.line(155,250,165+pdf.get_string_width("Approved By (Lab Manager)"),250)
     #      pdf.text(160,253,"Approved By (Lab Manager)")  
     
     if waterForm.analyst_signature:
         pdf.image(waterForm.analyst_signature.signature,30,231,20.32,20.32)
     
     if waterForm.assistant_manager_signature:
         pdf.image(waterForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     
     pdf.image(envitech_logo,154,228,22,22)
     if waterForm.lab_manager_signature:
         pdf.image(waterForm.lab_manager_signature.signature,176,228,20.32,20.32)
     
     
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(waterForm.analyst_signature.role if waterForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(waterForm.analyst_signature.role if waterForm.analyst_signature else '')})")
     pdf.line(126,250,47.5+pdf.get_string_width(f"Reviewed By ({(waterForm.assistant_manager_signature.role if waterForm.assistant_manager_signature else '')})"),250)
     pdf.text(87.5,253,f"Reviewed By ({(waterForm.assistant_manager_signature.role if waterForm.assistant_manager_signature else '')})")
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(waterForm.lab_manager_signature.role if waterForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(waterForm.lab_manager_signature.role if waterForm.lab_manager_signature else '')})")


     
     pdf.line(10,255,-10+pdf.w,255)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,266,txt="• Report is valid for current batch (sample).")
     pdf.text(10,269,txt="• This report is not valid for any publication or judicial purpose.")
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
     
     if waterForm.location == "NEQS" and waterForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif waterForm.location == "NEQS" and waterForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 258.9, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")

     elif waterForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif waterForm.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png', 153, 258.9, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:     
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=waterForm.doc_controll_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=waterForm.doc_controll_2)
     pdf.rect(180,277,25,5)
     pdf.text(183,280,txt=waterForm.doc_controll_3)
     
     
     if waterForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(waterForm, f'pdf_image_{i}')
               desc = getattr(waterForm, f'pdf_desc_{i}')
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
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=waterForm.pdf_heading,align="C")
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

     





     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
)
     # file_path = '/home/django/EnviTechAlApp/drinkingWater/'
     # pdf.output(file_path + waterForm.lab_report_no +'.pdf')
     # pdf = open(file_path + waterForm.lab_report_no +'.pdf', 'rb')

     # response = FileResponse(pdf)
     # return response
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={waterForm.lab_report_no}.pdf'

          # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

def generatePDF_report(request,pk,return_bytes=False):
     from fpdf import FPDF
     from EnviTechAlApp.pdf_common import PDF_generatePDF_report as PDFWithPageNumbers

     # def add_table_with_page_breaks(pdf, table_data, col_widths, line_height=6):
     #    """Helper function to add table with proper page break handling"""
     #    rows_per_page = calculate_rows_per_page(pdf, line_height)
        
     #    for i in range(0, len(table_data), rows_per_page):
     #        if i > 0:  # Not the first chunk
     #            pdf.add_page()
     #            pdf.show_full_header = False  # Don't show full header on subsequent pages
            
     #        chunk = table_data[i:i + rows_per_page]
            
     #        with pdf.table(col_widths=col_widths, line_height=line_height, 
     #                     text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:
     #            for data_row in chunk:
     #                row = table.row()
     #                for datum in data_row:
     #                    row.cell(datum)

     # def calculate_rows_per_page(pdf, line_height):
     #     """Calculate how many rows can fit on a page"""
     #     # Starting Y position after header
     #     start_y = pdf.get_y()
     #     # Available height (page height - top margin - bottom margin - footer space)
     #     available_height = pdf.h - start_y - 30  # 30 for footer and bottom margin
     #     # Rows that can fit
     #     return max(1, math.floor(available_height / line_height))

     # def add_notes_and_legends(pdf, waterForm):
     #     """Add notes and legends with proper page break checking"""
     #     # Check if we need a new page for notes
     #     if pdf.get_y() > pdf.h - 50:  # If too close to bottom
     #         pdf.add_page()
     #         pdf.show_full_header = False


     waterForm = DrinkingWaterForm.objects.get(id=pk)
     waterForm.extra_field = waterForm.extra_field.replace("'", "\"")
     waterForm.extra_field = json.loads(waterForm.extra_field)

     if waterForm.in_out == 'customLimits':
          TABLE_DATA = [
               ["Sr.#","Parameter/Analytes Description","Methods","Unit","Test Result",waterForm.custominput],
          ]
          sr_no = 1
          if waterForm.water_sr1:
               a = [str(sr_no),"pH @ 25°C",waterForm.method_1,"-",waterForm.water_sr1,waterForm.custominput1]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr2:
               a = [str(sr_no),"Total Dissolved Solids (TDS)",waterForm.method_2,"mg/L",waterForm.water_sr2,waterForm.custominput2]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr3:
               a = [str(sr_no),"Total Hardness as CaCO₃",waterForm.method_3,"mg/L",waterForm.water_sr3,waterForm.custominput3]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr4:
               a = [str(sr_no),"Color",waterForm.method_4,"TCU",waterForm.water_sr4,waterForm.custominput4]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr5:
               a = [str(sr_no),"Turbidity",waterForm.method_5,"NTU",waterForm.water_sr5,waterForm.custominput5]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr6:
               a = [str(sr_no),"Nitrite",waterForm.method_6,"mg/L",waterForm.water_sr6,waterForm.custominput6]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr7:
               a = [str(sr_no),"Nitrate (NO₃)",waterForm.method_7,"mg/L",waterForm.water_sr7,waterForm.custominput7]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr8:
               a = [str(sr_no),"Taste",waterForm.method_8,"-",waterForm.water_sr8,waterForm.custominput8]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr9:
               a = [str(sr_no),"Odor",waterForm.method_9,"-",waterForm.water_sr9,waterForm.custominput9]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr10:
               a = [str(sr_no),"Chloride (Cl)",waterForm.method_10,"mg/L",waterForm.water_sr10,waterForm.custominput10]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr11:
               a = [str(sr_no),"Fluoride (F)",waterForm.method_11,"mg/L",waterForm.water_sr11,waterForm.custominput11]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr12:
               a = [str(sr_no),"Aluminum (Al)",waterForm.method_12,"mg/L",waterForm.water_sr12,waterForm.custominput12]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr13:
               a = [str(sr_no),"Nickel (Ni)",waterForm.method_13,"mg/L",waterForm.water_sr13,waterForm.custominput13]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr14:
               a = [str(sr_no),"Lead (Pb)",waterForm.method_14,"mg/L",waterForm.water_sr14,waterForm.custominput14]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr15:
               a = [str(sr_no),"Barium (Ba)",waterForm.method_15,"mg/L",waterForm.water_sr15,waterForm.custominput15]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr16:
               a = [str(sr_no),"Antimony (Sb)",waterForm.method_16,"mg/L",waterForm.water_sr16,waterForm.custominput16]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr17:
               a = [str(sr_no),"Arsenic (As)",waterForm.method_17,"mg/L",waterForm.water_sr17,waterForm.custominput17]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr18:
               a = [str(sr_no),"Boron (B)",waterForm.method_18,"mg/L",waterForm.water_sr18,waterForm.custominput18]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr19:
               a = [str(sr_no),"Cadmium (Cd)",waterForm.method_19,"mg/L",waterForm.water_sr19,waterForm.custominput19]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr20:
               a = [str(sr_no),"Chromium (Cr)",waterForm.method_20,"mg/L",waterForm.water_sr20,waterForm.custominput20]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr21:
               a = [str(sr_no),"Selenium (Se)",waterForm.method_21,"mg/L",waterForm.water_sr21,waterForm.custominput21]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr22:
               a = [str(sr_no),"Copper (Cu)",waterForm.method_22,"mg/L",waterForm.water_sr22,waterForm.custominput22]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr23:
               a = [str(sr_no),"Cyanide (CN)",waterForm.method_23,"mg/L",waterForm.water_sr23,waterForm.custominput23]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr24:
               a = [str(sr_no),"Mercury (Hg)",waterForm.method_24,"mg/L",waterForm.water_sr24,waterForm.custominput24]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr25:
               a = [str(sr_no),"Manganese (Mn)",waterForm.method_25,"mg/L",waterForm.water_sr25,waterForm.custominput25]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr26:
               a = [str(sr_no),"Zinc (Zn)",waterForm.method_26,"mg/L",waterForm.water_sr26,waterForm.custominput26]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr27:
               a = [str(sr_no),"Residual Chlorine",waterForm.method_27,"mg/L",waterForm.water_sr27,waterForm.custominput27]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr28:
               a = [str(sr_no),"Phenolic Compounds as Phenols",waterForm.method_28,"mg/L",waterForm.water_sr28,waterForm.custominput28]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr29:
               a = [str(sr_no),"Fecal Coliform",waterForm.method_29,"CFU/100 ml",waterForm.water_sr29,waterForm.custominput29]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr30:
               a = [str(sr_no),"Total Coliform",waterForm.method_30,"CFU/100 ml",waterForm.water_sr30,waterForm.custominput30]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr31:
               a = [str(sr_no),"E-Coli",waterForm.method_31,"CFU/100 ml",waterForm.water_sr31,waterForm.custominput31]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr32:
               a = [str(sr_no),"Pesticides",waterForm.method_32,"mg/L",waterForm.water_sr32,waterForm.custominput32]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          for extra_field in waterForm.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)




          pdf = PDFWithPageNumbers(report_number=waterForm.lab_report_no,invoice=waterForm.invoice_bill_no,reporting_date=waterForm.reporting_date,report_to=waterForm.report_to,
                                   address=waterForm.address,attention=waterForm.attention,email=waterForm.email,sample_id=waterForm.sample_id,sample_collection_date=waterForm.sample_collection_date,
                                   sample_description=waterForm.sample_description,sample_type=waterForm.sample_type,sample_collected_by=waterForm.sample_collected_by,
                                   date_of_analysis_to=waterForm.date_of_analysis_to, date_of_analysis_from=waterForm.date_of_analysis_from,test_description=waterForm.test_description,
                                   )
          pdf._rq_request, pdf._rq_pk = request, pk
          pdf.add_page(orientation="portrait", format="A4")
          # font_path = "static/fonts/calibri.ttf"
          # font_path_bold = "static/fonts/calibrib.ttf"
          # pdf.add_font("Calibri","",font_path,uni=True)
          # pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True, margin=15)









          #report data table
          num_rows = 0
          with pdf.table(col_widths=(6, 35, 20, 15,18,18),line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows = num_rows + 1
                    # if k == 0:
                    #      data_row[5] = waterForm.select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)     


     else:
          TABLE_DATA = [
          ["Sr.#","Parameter/Analytes Description","Methods","Unit","Test Result",""],
          ]
          sr_no = 1
          if waterForm.water_sr1:
               a = [str(sr_no),"pH @ 25°C",waterForm.method_1 or "*APHA 4500 H","-",waterForm.water_sr1,"6.5 - 8.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr2:
               a = [str(sr_no),"Total Dissolved Solids (TDS)",waterForm.method_2 or "*APHA 2540-C","mg/L",waterForm.water_sr2,"<1000"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr3:
               a = [str(sr_no),"Total Hardness as CaCO₃",waterForm.method_3 or "ASTM D 1126","mg/L",waterForm.water_sr3,"< 500"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr4:
               a = [str(sr_no),"Color",waterForm.method_4 or "HACH 8025","TCU",waterForm.water_sr4,"≤ 15"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr5:
               a = [str(sr_no),"Turbidity",waterForm.method_5 or "*APHA 2130","NTU",waterForm.water_sr5,"≤ 5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr6:
               a = [str(sr_no),"Nitrite",waterForm.method_6 or "HACH 8507","mg/L",waterForm.water_sr6,"≤ 3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr7:
               a = [str(sr_no),"Nitrate (NO₃)",waterForm.method_7 or "HACH 8039","mg/L",waterForm.water_sr7,"≤ 50"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr8:
               a = [str(sr_no),"Taste",waterForm.method_8 or "*APHA 2160","-",waterForm.water_sr8,"Non-Objectionable"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr9:
               a = [str(sr_no),"Odor",waterForm.method_9 or "*APHA 2150","-",waterForm.water_sr9,"Non-Objectionable"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr10:
               a = [str(sr_no),"Chloride (Cl)",waterForm.method_10 or "*APHA 4500 Cl","mg/L",waterForm.water_sr10,"≤ 250"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr11:
               a = [str(sr_no),"Fluoride (F)",waterForm.method_11 or "HACH 8029","mg/L",waterForm.water_sr11,"≤ 1.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr12:
               a = [str(sr_no),"Aluminum (Al)",waterForm.method_12 or "*APHA 3111-D","mg/L",waterForm.water_sr12,"≤ 0.2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr13:
               a = [str(sr_no),"Nickel (Ni)",waterForm.method_13 or "*APHA 3111-B","mg/L",waterForm.water_sr13,"≤ 0.02"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr14:
               a = [str(sr_no),"Lead (Pb)",waterForm.method_14 or "*APHA 3111-B","mg/L",waterForm.water_sr14,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr15:
               a = [str(sr_no),"Barium (Ba)",waterForm.method_15 or "HACH 8014","mg/L",waterForm.water_sr15," 0.7"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr16:
               a = [str(sr_no),"Antimony (Sb)",waterForm.method_16 or "*APHA 3111-B","mg/L",waterForm.water_sr16,"≤ 0.005"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr17:
               a = [str(sr_no),"Arsenic (As)",waterForm.method_17 or "*APHA 3114-B","mg/L",waterForm.water_sr17,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr18:
               a = [str(sr_no),"Boron (B)",waterForm.method_18 or "HACH 8015","mg/L",waterForm.water_sr18,"0.3"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr19:
               a = [str(sr_no),"Cadmium (Cd)",waterForm.method_19 or "*APHA 3111-B","mg/L",waterForm.water_sr19,"0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr20:
               a = [str(sr_no),"Chromium (Cr)",waterForm.method_20 or "*APHA 3111-B","mg/L",waterForm.water_sr20,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr21:
               a = [str(sr_no),"Selenium (Se)",waterForm.method_21 or "*APHA 3114-B","mg/L",waterForm.water_sr21,"0.01"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr22:
               a = [str(sr_no),"Copper (Cu)",waterForm.method_22 or "*APHA 3111-B","mg/L",waterForm.water_sr22,"2"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr23:
               a = [str(sr_no),"Cyanide (CN)",waterForm.method_23 or "HACH 8027","mg/L",waterForm.water_sr23,"≤ 0.05"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr24:
               a = [str(sr_no),"Mercury (Hg)",waterForm.method_24 or "*APHA 3112-B","mg/L",waterForm.water_sr24,"≤ 0.001"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr25:
               a = [str(sr_no),"Manganese (Mn)",waterForm.method_25 or "*APHA 3111-B","mg/L",waterForm.water_sr25,"≤ 0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr26:
               a = [str(sr_no),"Zinc (Zn)",waterForm.method_26 or "*APHA 3111-B","mg/L",waterForm.water_sr26,"≤ 5.0"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr27:
               a = [str(sr_no),"Residual Chlorine",waterForm.method_27 or "HACH 10069","mg/L",waterForm.water_sr27,"0.2 - 0.5"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr28:
               a = [str(sr_no),"Phenolic Compounds as Phenols",waterForm.method_28 or "ASTM-D-1783","mg/L",waterForm.water_sr28,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr29:
               a = [str(sr_no),"Fecal Coliform",waterForm.method_29 or "USEPA 1604","CFU/100 ml",waterForm.water_sr29,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr30:
               a = [str(sr_no),"Total Coliform",waterForm.method_30 or "*APHA 922 B","CFU/100 ml",waterForm.water_sr30,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr31:
               a = [str(sr_no),"E-Coli",waterForm.method_31 or "USEPA 1604","CFU/100 ml",waterForm.water_sr31,"0 CFU/100 ml"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)
          if waterForm.water_sr32:
               a = [str(sr_no),"Pesticides",waterForm.method_32 or "USEPA-614.1","mg/L",waterForm.water_sr32,"-"]
               sr_no = sr_no+1
               TABLE_DATA.append(a)

          for extra_field in waterForm.extra_field:
               parameters = extra_field.get("parameters")
               methods = extra_field.get("methods")
               unit = extra_field.get("unit")
               result = extra_field.get("result")
               limit = extra_field.get("limit")
               # Check if the "parameters" field is not empty before adding the row
               if parameters:
                    a = [str(sr_no), parameters, methods, unit, result, limit]
                    sr_no += 1
                    TABLE_DATA.append(a)




          pdf = PDFWithPageNumbers(report_number=waterForm.lab_report_no,invoice=waterForm.invoice_bill_no,reporting_date=waterForm.reporting_date,report_to=waterForm.report_to,
                                   address=waterForm.address,attention=waterForm.attention,email=waterForm.email,sample_id=waterForm.sample_id,sample_collection_date=waterForm.sample_collection_date,
                                   sample_description=waterForm.sample_description,sample_type=waterForm.sample_type,sample_collected_by=waterForm.sample_collected_by,
                                   date_of_analysis_to=waterForm.date_of_analysis_to, date_of_analysis_from=waterForm.date_of_analysis_from,test_description=waterForm.test_description,
                                   )
          pdf._rq_request, pdf._rq_pk = request, pk
          pdf.add_page(orientation="portrait", format="A4")
          # font_path = "static/fonts/calibri.ttf"
          # font_path_bold = "static/fonts/calibrib.ttf"
          # pdf.add_font("Calibri","",font_path,uni=True)
          # pdf.add_font("Calibri","B",font_path_bold,uni=True)
          pdf.set_font("Calibri","", 9)
          pdf.set_auto_page_break(auto=True, margin=15)









          #report data table
          num_rows = 0
          with pdf.table(col_widths=(6, 35, 20, 15,18,18),line_height=6,text_align=("CENTER","LEFT","CENTER","CENTER",'CENTER','CENTER')) as table:




               for k in range(0,len(TABLE_DATA)):
                    data_row = TABLE_DATA[k]
                    num_rows = num_rows + 1
                    if k == 0:
                         data_row[5] = waterForm.select + " Limits"

                    # watwer mark
                    # pdf.set_page_background("static/assets/Capture.PNG")
                    row = table.row()
                    for i in range(0,len(data_row)):
                         datum = data_row[i]

                         row.cell(datum)     

     
     # add_table_with_page_breaks(pdf, TABLE_DATA, col_widths=(6, 35, 20, 15, 18, 18))
     # add_notes_and_legends(pdf, waterForm)
     # # Calculate the table height based on the number of rows and row height
     number_of_rows = len(TABLE_DATA)  # Replace with the actual number of rows
     row_height = 6  # Replace with the actual row height in your table
     table_height = (number_of_rows) * row_height  
     
     if pdf.y + number_of_rows * row_height >= pdf.h:
          pdf.add_page()             
     
     
          
          

     
     Table_Data1 = [
          
     ]
     if waterForm.edit_note:
          a=["Note: "+ waterForm.edit_note] 
          Table_Data1.append(a)
          
          
     
     # with pdf.table(col_widths=(190),width=190,line_height=6,text_align=("LEFT")) as table:
         
          for k in range(0,len(Table_Data1)):
               data_row = Table_Data1[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.multi_cell(190, 4, datum, border=0, ln=True, align='L')

     Table_data_legend = [

     ]     
     pdf.set_font_size(8)
     if waterForm.legend_1:
          a = [waterForm.legend_1]
          Table_data_legend.append(a)
          
     if waterForm.legend_2:
          a = [waterForm.legend_2]
          Table_data_legend.append(a)
          
     if waterForm.legend_3:
          a = [waterForm.legend_3]
          Table_data_legend.append(a)
          
     if waterForm.legend_4:
          a = [waterForm.legend_4]
          Table_data_legend.append(a)
          
     if waterForm.legend_5:
          a = [waterForm.legend_5]
          Table_data_legend.append(a)
          
     if waterForm.legend_6:
          a = [waterForm.legend_6]
          Table_data_legend.append(a)
          
     if waterForm.legend_7:
          a = [waterForm.legend_7]
          Table_data_legend.append(a)
          
     if waterForm.legend_8:
          a = [waterForm.legend_8]
          Table_data_legend.append(a)
          
     if waterForm.legend_9:
          a = [waterForm.legend_9]
          Table_data_legend.append(a)
          
     if waterForm.legend_10:
          a = [waterForm.legend_10]
          Table_data_legend.append(a)
          
     if waterForm.legend_11:
          a = [waterForm.legend_11]
          Table_data_legend.append(a)
          
     pdf.set_auto_page_break(auto=True, margin=15)
     
     for k in range(0,len(Table_data_legend)):
               data_row = Table_data_legend[k]
               row = table.row()
               for i in range(0,len(data_row)):
                    datum = data_row[i]
                    row.cell(datum)
                    pdf.cell(190, 4, datum, border=0, ln=True, align='L')
     
     

     if waterForm.analyst_signature:
         pdf.image(waterForm.analyst_signature.signature,30,231,20.32,20.32)
     pdf.line(19,250,36+pdf.get_string_width(f"Analyzed By ({(waterForm.analyst_signature.role if waterForm.analyst_signature else '')})"),250)
     pdf.text(26,253,f"Analyzed By ({(waterForm.analyst_signature.role if waterForm.analyst_signature else '')})")
     if waterForm.assistant_manager_signature:
         pdf.image(waterForm.assistant_manager_signature.signature,100,232,20.32,20.32)
     pdf.line(126,250,47.5+pdf.get_string_width("Reviewed By (Assistant Manager)"),250)
     pdf.text(87.5,253,f"Reviewed By ({(waterForm.assistant_manager_signature.role if waterForm.assistant_manager_signature else '')})")
     pdf.image(envitech_logo,154,228,22,22)
     if waterForm.lab_manager_signature:
         pdf.image(waterForm.lab_manager_signature.signature,176,228,20.32,20.32)
     pdf.line(155,250,165+pdf.get_string_width(f"Approved By ({(waterForm.lab_manager_signature.role if waterForm.lab_manager_signature else '')})"),250)
     pdf.text(160,253,f"Approved By ({(waterForm.lab_manager_signature.role if waterForm.lab_manager_signature else '')})")


     
     pdf.line(10,255,-10+pdf.w,255)
     
     pdf.set_font("Calibri","", 8)
     pdf.text(10,266,txt="• Report is valid for current batch (sample).")
     pdf.text(10,269,txt="• This report is not valid for any publication or judicial purpose.")
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
     if waterForm.location == "NEQS" and waterForm.city_location.lower() == "karachi":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png', 156, 259, 19, 15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")

     elif waterForm.location == "NEQS" and waterForm.city_location.lower() == "lahore":
          pdf.image('static/assets/EPA_updated.png', 153, 259, 25, 16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
          
     elif waterForm.location == "SEQS":
          pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)
          pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,262,txt="Disclaimer:")
          
          
     elif waterForm.location == "PEQS":
          pdf.image('static/assets/EPA_updated.png',153,259,25,16)
          pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
          pdf.set_font("Calibri","B", 9)
          pdf.text(10,259,txt="Disclaimer:")
          pdf.set_font("Calibri","", 8)
          pdf.text(10,263,txt="• Regulated by EPA Punjab under Certificate No. 82/Dir/(ML&I)/EPA/03/2025.")
          
          
     # if waterForm.location == "NEQS":
     #      pdf.image('static/assets/SEPA-Sindh-LOGO.png',156,259,19,15)          
     pdf.image('static/assets/ISO-14001_2015 LOGO.png',182,259,19,15)
     pdf.set_font("Calibri","B", 5)
     # if waterForm.location == 'PEQS':
     #      pdf.text(155,276,txt="(82/Dir/(ML&I)/EPA/03/2025)")
     # else:
     #      pdf.text(149,276,txt="(LAB/L.C/ENVI TECH AL-2/20/2020/580/26)")
               
     pdf.text(126,276,txt="(Certificate # 080177324-QMS)")
     
     
     pdf.text(182,276,txt="(Certificate # 080177424-EMS)")

     pdf.set_font("Calibri","", 7)
     pdf.rect(126,277,25,5)
     pdf.text(128,280,txt=waterForm.doc_controll_1)
     pdf.rect(151,277,29,5)
     pdf.text(155,280,txt=waterForm.doc_controll_2)
     pdf.rect(180,277,25,5)
     pdf.text(183,280,txt=waterForm.doc_controll_3)

     if waterForm.pdf_image_1:

          images = []
          for i in range(1, 7):
               base64_str = getattr(waterForm, f'pdf_image_{i}')
               desc = getattr(waterForm, f'pdf_desc_{i}')
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
          pdf.show_full_header = False
          pdf.set_font("Arial", size=13)
          pdf.add_page()
          pdf.set_y(65)
          
          
          pdf.multi_cell(190,10,txt=waterForm.pdf_heading,align="C")
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


     
     pdf.set_encryption(
     owner_password="karachi123",  # Replace with a strong owner password
     user_password="1234",    # Replace with a user password
     encryption_method=fpdf.enums.EncryptionMethod.AES_256,
     permissions=fpdf.enums.AccessPermission.PRINT_LOW_RES | fpdf.enums.AccessPermission.PRINT_HIGH_RES
     )

     #pdf = fpdf.FPDF(orientation="portrait", format="A4")
     
     # file_path = '/home/django/EnviTechAlApp/dw_pdf/'
     # pdf.output(file_path + waterForm.lab_report_no +'.pdf')

     # pdf = open(file_path + waterForm.lab_report_no +'.pdf', 'rb')
     # response = FileResponse(pdf)
     # return response

     
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     pdf_output.seek(0)

     if return_bytes:
          return pdf_output  # ← return raw bytes for merging

     # Original HTTP response path (unchanged)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={waterForm.lab_report_no}.pdf'
     response.write(pdf_output.getvalue())
     return response
    
    
def generate_job_completion_pdf(job):
     class CustomPDF(FPDF):
          def __init__(self, *args, **kwargs):
               super().__init__(*args, **kwargs)
               self.location = ''
               # Register custom fonts
               try:
                    font_path = "static/fonts/calibri.ttf"
                    font_path_bold = "static/fonts/calibrib.ttf"
                    font_path_alger = "static/fonts/ALGER.TTF"
                    
                    self.add_font("Calibri", "", font_path, uni=True)
                    self.add_font("Calibri", "B", font_path_bold, uni=True)
                    self.add_font("Algerian", "", font_path_alger, uni=True)
               except Exception as e:
                    print(f"Font loading error: {e}")
                    pass

          def header(self):
               self.set_y(0)
               self.set_x(0)
               
               try:
                    self.image("static/assets/EnviTechAL LOGO.png", 16, 5, 22, 24)
               except Exception:
                    pass
                    
               self.set_line_width(0.5)
               self.set_draw_color(26, 84, 26)
               self.line(0, 31, self.w, 31)
               
               self.set_font("Algerian", "", 16)
               self.set_text_color(13, 46, 145)
               self.text(90, 15, txt="ENVI TECH AL")
               
               self.set_font("Calibri", "B", 15)
               self.set_text_color(25, 27, 28)
               self.text(83, 23, txt="Work Completion Form")
               
               x = 160
               y = 0
               width = 64
               height = 6
               skew_width = 7
               color = (12, 168, 74)
               
               self.set_fill_color(*color)
               self.rect(x, y, width, height, 'F')
               self.set_draw_color(12, 168, 74)
               self.polygon([(x - skew_width, y), (x, y), (x, y + height)], 'DF')
               
               self.set_font("Calibri", "B", 10)
               self.set_draw_color(25, 27, 28)
               self.rect(160, 8, 40, 20, "D")
               
               self.location = job.location.lower() if job.location else ''
               if self.location == 'lahore':
                    self.text(162, 13, txt="ETAL-LAB-704-FF-08")
                    self.text(162, 17, txt="Issue Date: 15-05-2026")
                    self.text(162, 21, txt="Issue No. 01 Rev. No. 00")
               elif self.location == 'karachi':
                    self.text(162, 13, txt="ETAL-LAB-704-FF-08")
                    self.text(162, 17, txt="Issue Date: 15-05-2026")
                    self.text(162, 21, txt="Issue No. 01 Rev. No. 00")
               else:
                    self.text(162, 13, txt="ETAL-LAB-704-FF-08")
                    self.text(162, 17, txt="Issue Date: 15-05-2026")
                    self.text(162, 21, txt="Issue No. 01 Rev. No. 01")
               
               self.set_text_color(0, 0, 0)
               self.alias_nb_pages()
               self.set_font("Calibri", "B", 10)
               self.text(162, 25.5, txt="Page No:")
               self.cell(self.w - 17, 49, f'{self.page_no()} of {{nb}}', border=False, align='R')
               self.set_text_color(10, 10, 10)
               self.set_font("Calibri", "", 9)
          
          def draw_job_details(self, job):
               self.set_font("Calibri", "", 11)
               self.set_text_color(0, 0, 0)
               self.set_fill_color(237, 243, 255)
               # Job Information
               self.set_y(35)
               # self.set_x(15)
               self.set_font("Calibri", "B", 8)
               url = "https://hrm.envitechal.com/customer_feed_back"

               qr = qrcode.QRCode(
               version=1,
               box_size=10,
               border=2
               )

               qr.add_data(url)
               qr.make(fit=True)

               img = qr.make_image(fill_color="black", back_color="white")

               # Save image to memory instead of file
               buffer = BytesIO()
               img.save(buffer, format="PNG")
               buffer.seek(0)

               # Use directly in FPDF
               self.image(buffer, x=100, y=32, w=12, h=12)
               
               self.text(99.5,47,"SCAN HERE")
               self.text(90,50,"YOUR FEEDBACK MATTERS")
               self.set_font("Calibri", "B", 10)
               
               self.cell(0,6,f"WCF: {job.job_number}",ln=True,align='R')
               self.ln(12)
               # self.cell(0, 7, f"Job ID: JOB-{job.id:06d}", ln=True)
               self.cell(40.9, 7, f"Company Name:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               self.cell(149, 7, f"{job.company.company_name}", border=True,ln=True)
               self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"Address:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.company.address or 'N/A'}", border=True, ln=True)
               self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"Invoice Reference:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.invoice_ref or 'N/A'}", ln=True, border=True)
               self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"PO Reference:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.po_reference or 'N/A'}", ln=True, border=True)
               self.set_font("Calibri", "B", 10)
               
               # Custom PO Fields (NEW - Added here)
               custom_po_fields = job.custom_po_fields if isinstance(job.custom_po_fields, list) else json.loads(job.custom_po_fields) if job.custom_po_fields else []
               
               if custom_po_fields:
                    for po_field in custom_po_fields:
                         label = po_field.get('label', '')
                         value = po_field.get('value', '')
                         
                         self.cell(40.9, 7, f"{label}:", border=True, fill=True)
                         self.set_font("Calibri", "", 10)
                         self.cell(149, 7, f"{value or 'N/A'}", ln=True, border=True)
                         self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"Contact Person:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.company.contact_person or 'N/A'}", ln=True, border=True)
               self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"Contact Number:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.company.contact_number or 'N/A'}", ln=True, border=True)
               self.set_font("Calibri", "B", 10)
               
               self.cell(40.9, 7, f"Email:", border=True,fill=True)
               self.set_font("Calibri", "", 10)
               
               self.cell(149, 7, f"{job.company.email or 'N/A'}", ln=True, border=True)
               
               self.set_font("Calibri", "B", 11)
               
               self.cell(190,7, "Service Description", border=True, ln=True, align="C", fill=True)
               
               
               self.set_font("Calibri", "B", 10)
               
               
               
               
               service_details = job.service_details if isinstance(job.service_details, list) else json.loads(job.service_details)

               TABLE_DATA = [
               ["Sr.#", "Type of Services", "Site Location", "QTY", "Date"],
               ]

               # Add service rows
               for service in service_details:
                    # Format the date
                    date_value = service.get('date', '')
                    formatted_date = ''
                    
                    if date_value:
                         try:
                              # Try to parse the date if it's in YYYY-MM-DD format (from input)
                              date_obj = datetime.strptime(date_value, '%Y-%m-%d')
                              formatted_date = date_obj.strftime('%d-%m-%Y')
                         except Exception:
                              # If already in different format or error, keep original
                              formatted_date = date_value
                    
                    row = [
                         str(service.get('sr_no', '')),
                         service.get('service', ''),
                         service.get('site_location', ''),
                         str(service.get('qty', '')),
                         formatted_date  # Use formatted date
                    ]
                    TABLE_DATA.append(row)

               # Column widths (in mm)
               col_widths = (10, 55, 55, 12, 20)

               # Text alignment
               text_align = ("CENTER", "CENTER", "CENTER", "CENTER", "CENTER")

               with self.table(
               col_widths=col_widths,
               width=190,
               line_height=6,
               text_align=text_align,
               first_row_as_headings=True,
               ) as table:

                    for i, row_data in enumerate(TABLE_DATA):

                         # Set gray only for heading row
                         if i == 0:
                              self.set_fill_color(237, 243, 255)
                         else:
                              self.set_font("Calibri", "", 10)
                              self.set_fill_color(255, 255, 255)

                         row = table.row()

                         for cell_data in row_data:
                              row.cell(str(cell_data))
                              
                              
               self.set_y(240)
               self.set_fill_color(237, 243, 255)
               sign = Signatures.objects.get(id=job.representative_sign)   # if ForeignKey
               self.cell(190, 7, "ACKNOWLEDGMENT", border=True, ln=True, align="C", fill=True)
               self.set_font("Calibri", "B", 8)

               self.cell(47.5, 10, "Name of Envi Tech AL Representative", border=True, align="C")
               self.set_font("Calibri", "", 8)
               
               self.cell(47.5, 10, f"{sign.user.get_full_name() or sign.user.username}", border=True, align="C")
               self.set_font("Calibri", "B", 8)
               
               self.cell(49, 10, "Signature of Envi Tech AL Representative", border=True, align="C")

               
               print(sign,"===========>>>>")
               current_y = self.get_y()

               self.cell(46, 10, "", border=True, ln=True)

               if sign and sign.signature:
                    self.image(
                         sign.signature.path,
                         x=158,
                         y=current_y + 2,
                         w=25,
                         h=8
                    )
               self.cell(47.5, 10, "Name of Service Receiver", border=True, align="C")
               self.set_font("Calibri", "", 8)
               
               self.cell(47.5, 10, f"{job.service_receiver}", border=True, align="C")
               self.set_font("Calibri", "B", 8)
               
               self.cell(49, 10, "Signature of Service Receiver", border=True, align="C")
               self.cell(46, 10, "", border=True, ln=True)

               
               # Acknowledgment Section
               # self.set_y(self.get_y() + 10)
               # self.set_font("Calibri", "B", 11)
               # self.cell(0, 10, "ACKNOWLEDGMENT", ln=True)
               # self.set_font("Calibri", "", 10)
               # self.cell(0, 7, f"Envi Tech AL Representative: {job.representative_name or 'N/A'}", ln=True)
               # self.cell(0, 7, f"Service Receiver: {job.service_receiver or 'N/A'}", ln=True)
          
          def footer(self):
               
               color = (12, 168, 74)
               self.set_text_color(10, 10, 10)
               self.set_font("Calibri","B", 9)
               self.set_y(-26)
               
               self.cell(0,6,"Disclaimer: This form is system-generated; therefore, no stamp is required.",ln=True, align="C")
               self.set_y(-10)
               self.set_x(0)
               self.set_font("Calibri","", 9)

               self.image('static/assets/phone.PNG',10,self.h-17,7,7)
               self.image('static/assets/office.PNG',50,self.h-18,9,9)
               self.set_font("Calibri","", 10)
               if self.location == 'karachi':
                    self.text(18,self.h-13,txt="+92 310 2288801")
                    self.text(60,self.h-15,txt="Head Office:345,First Floor, Street-15,Block-3")
                    self.text(60,self.h-11,txt="Bahadurabad, Karachi, 75900, Pakistan")
                    self.set_draw_color(12, 168, 74)
                    self.set_fill_color(*color)
                    self.ln(1.7)
                    self.set_x(0)
                    self.set_text_color(255,255,255)
                    self.cell(220,8,"",align="C",fill=True)
                    self.set_text_color(0,0,0)
                         
               elif self.location == 'lahore':
                    self.text(18,self.h-13,txt="+92 42 32296099")
                    self.text(60,self.h-15,txt="Lahore Office: 87-E Madina Height, Office # A/30 & ")
                    self.text(60,self.h-11,txt=" A/31 8th Floor,Johar Town, Lahore")
                    self.ln(1.7)
                    self.set_x(0)
                    self.set_draw_color(12, 168, 74)
                    self.set_fill_color(*color)
                    self.set_text_color(255,255,255)
                    self.cell(220,8,"Head Office: First Floor, Street-15,Block-3 Bahadurabad, Karachi, 75900, Pakistan",align="C",fill=True)
               else:
                    self.text(18,self.h-13,txt="+92 310 2288801")
                    self.text(60,self.h-15,txt="Head Office:345,First Floor, Street-15,Block-3")
                    self.text(60,self.h-11,txt="Bahadurabad, Karachi, 75900, Pakistan")

               self.image('static/assets/polyPNG-removebg-preview.png',130,271,90,23)

               
    
     # Create PDF
     pdf = CustomPDF('P', 'mm', 'A4')
     pdf.add_page()
     pdf.set_y(35)
     pdf.draw_job_details(job)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = f'inline; filename={job.job_number}.pdf'

     # Output the PDF to the response
     pdf_output = BytesIO()
     pdf_output.write(pdf.output(dest='S'))
     response.write(pdf_output.getvalue())

     return response

__all__ = [
    'generate_leq_chart',
    'generate_leq_line_chart',
    'generate_merged_pdf',
    'generate_merged_pdf_certificate',
    'generatePDF',
    'generatePDF_report',
    'generate_job_completion_pdf',
]
