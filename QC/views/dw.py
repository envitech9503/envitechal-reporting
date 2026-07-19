# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


@csrf_exempt
def create_dw_qc(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            
           
            for k in body.keys():
                pass

            sample_id = body.get('sample_id')
            data = body.copy()
            if 'sample_id' in data:
                del data['sample_id']

            report = Dw_rds.objects.create(
                sample_id=sample_id,
                rds=data
            )
            return redirect(f"/qc/generate_dw_qc_pdf_response/{report.id}/")
            # return generate_dw_qc_pdf_response(report, data, sample_id)
            # return JsonResponse({
            #     "status": "success",
            #     "id": report.id,
            #     "sample_id": report.sample_id
            # })
            
            
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    sample_ids = Sample_registration.objects.all()
    dw_ids = DrinkingWaterForm.objects.all()
    sample = serializers.serialize('json',sample_ids,fields=('sample_id',))
    dw = serializers.serialize('json',dw_ids,fields=('sample_id',))
    context={'sample':sample,'dw':dw,'signs':signs}
    return render(request,"rds_dw.html",context)









def generate_dw_qc_pdf_response(report, pk):
    """Generate PDF for DW QC report with proper page breaks"""

    pdf = CustomPDF()
    pdf.add_page()

    report = Dw_rds.objects.get(id=pk)
    sample_id = report.sample_id

    font_path = "static/fonts/calibri.ttf"
    font_path_bold = "static/fonts/calibrib.ttf"
    pdf.add_font("Calibri", "", font_path, uni=True)
    pdf.add_font("Calibri", "B", font_path_bold, uni=True)

    data = report.rds or {}
    

    # Margins
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_top_margin(10)

    PAGE_BREAK_THRESHOLD = 255
    CONTENT_START_Y = 35

    def check_page_break(required_height=10):
        if pdf.get_y() + required_height > PAGE_BREAK_THRESHOLD:
            pdf.add_page()
            pdf.set_y(CONTENT_START_Y)
            return True
        return False

    col_widths = [10, 30, 45, 25, 25, 25, 25]

    def add_table_header():
        pdf.set_font("Calibri", 'B', 9)
        pdf.set_x(12)
        headers = ["S.no", "Date", "Parameter", "Results", "Performed By", "Checked By", "Remarks"]
        for i, h in enumerate(headers):
            pdf.cell(col_widths[i], 8, h, 1, 0, 'C')
        pdf.ln()
        pdf.set_font("Calibri", size=9)

    # Header
    pdf.set_y(CONTENT_START_Y)
    pdf.set_font("Calibri", 'B', 10)
    pdf.cell(0, 5, f"Sample ID: {sample_id}", ln=True)
    add_table_header()

    row_height = 8

    # 🔥 COLLECT ALL ROW KEYS (main + CRM sub-rows)
    rows = {}

    for key, val in data.items():
        if key.startswith("date_") and val:
            row_key = key.replace("date_", "")
            rows[row_key] = val

    # Sort rows by date
    sorted_rows = sorted(
        rows.keys(),
        key=lambda rk: data.get(f"date_{rk}") or ""
    )

    if not sorted_rows:
        check_page_break(row_height)
        pdf.set_x(12)
        pdf.cell(sum(col_widths), row_height, "No data available", 1, 1, 'C')
        return pdf

    # 🔢 Sequential S.no
    s_no = 1

    for row_key in sorted_rows:
        check_page_break(row_height)

        pdf.set_x(12)
        pdf.cell(col_widths[0], row_height, str(s_no), 1, 0, 'C')

        pdf.cell(
            col_widths[1],
            row_height,
            str(data.get(f'date_{row_key}', '')),
            1, 0, 'C'
        )

        pdf.cell(
            col_widths[2],
            row_height,
            str(data.get(f'parameter_{row_key}', '')),
            1, 0, 'L'
        )

        pdf.cell(
            col_widths[3],
            row_height,
            str(data.get(f'result_{row_key}', '')),
            1, 0, 'C'
        )

        # Performed By
        performed_id = (
            data.get(f'performed_by_{row_key}')
            or data.get(f'performed_{row_key}')
            or ''
        )
        if performed_id:
            try:
                sign = Signatures.objects.get(id=int(performed_id))
                x, y = pdf.get_x(), pdf.get_y()
                pdf.cell(col_widths[4], row_height, '', 1, 0)
                if sign.signature:
                    pdf.image(sign.signature.path, x + 1, y + 1,
                              w=col_widths[4] - 2, h=row_height - 2)
            except:
                pdf.cell(col_widths[4], row_height, 'N/A', 1, 0)
        else:
            pdf.cell(col_widths[4], row_height, '', 1, 0)

        # Checked By
        checked_id = (
            data.get(f'checked_by_{row_key}')
            or data.get(f'checked_{row_key}')
            or ''
        )
        if checked_id:
            try:
                sign = Signatures.objects.get(id=int(checked_id))
                x, y = pdf.get_x(), pdf.get_y()
                pdf.cell(col_widths[5], row_height, '', 1, 0)
                if sign.signature:
                    pdf.image(sign.signature.path, x + 1, y + 1,
                              w=col_widths[5] - 2, h=row_height - 2)
            except:
                pdf.cell(col_widths[5], row_height, 'N/A', 1, 0)
        else:
            pdf.cell(col_widths[5], row_height, '', 1, 0)

        pdf.cell(
            col_widths[6],
            row_height,
            str(data.get(f'remarks_{row_key}', '')),
            1, 1, 'C'
        )

        s_no += 1

    # CALCULATION SECTIONS WITH SMART PAGE BREAKS
    def add_calculation_header():
        """Add calculation header with page break check"""
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 12)
        pdf.cell(0, 6, "CALCULATION", 0, 1, 'C')
        pdf.ln(2)

    def add_formula_with_line(formula_content, result_text, divisor_text=None, start_x=30):
        """Helper function to add formula with line and optional divisor"""
        old_y = pdf.get_y()
        text_width = pdf.get_string_width(formula_content)
        
        pdf.set_x(start_x)
        pdf.cell(text_width, 6, f"{formula_content} = {result_text}", align='L', ln=True)
        pdf.line(start_x, old_y+5.5, start_x+text_width, old_y+5.5)
        
        if divisor_text:
            divisor_width = pdf.get_string_width(divisor_text)
            center_divisor_x = start_x + (text_width / 2) - (divisor_width / 2)
            pdf.set_x(center_divisor_x)
            pdf.cell(divisor_width, 6, divisor_text, align="C", ln=True)
        else:
            pdf.ln(-4)  # Add some spacing if no divisor
        
        pdf.ln(3)  # Consistent spacing after formula

    def add_simple_formula_section(check_key, section_title, head_key, ans_key, param_key, 
                                  value_suffix="", df_suffix="", div_key=None, start_x=30):
        """Add a simple formula section with page break check"""
        if data.get(check_key):
            check_page_break(10)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, f"{section_title}:", 0, 1, 'L')
            
            if data.get(head_key):
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data[head_key], ln=True)
            
            pdf.cell(0, 6, "Formula:", ln=True)
            pdf.set_font("Calibri", '', 10)
            
            # Build formula content
            formula_parts = []
            
            
            for i in range(1, 4):
                # Try ALL possible patterns
                possible_patterns = []
                
                # Pattern 1: Original pattern
                possible_patterns.append((
                    f"{check_key[:-1]}{i}{value_suffix}",
                    f"{check_key[:-1]}{i}{df_suffix}",
                    "Pattern 1"
                ))
                
                # Pattern 2: With underscore
                possible_patterns.append((
                    f"{check_key}_{i}{value_suffix}",
                    f"{check_key}_{i}{df_suffix}",
                    "Pattern 2"
                ))
                
                # Pattern 3: Remove trailing numbers from check_key
                base_key = check_key.rstrip('0123456789_')
                possible_patterns.append((
                    f"{base_key}{i}{value_suffix}",
                    f"{base_key}{i}{df_suffix}",
                    "Pattern 3"
                ))
                
                # Pattern 4: For beryllium/ammonium specifically for_alum1_df1
                if 'beryllium' in check_key.lower() or 'ammonium' in check_key.lower():
                    possible_patterns.append((
                        f"for_{section_title.lower()}1_{i}",
                        f"for_{section_title.lower()}1_{i}_df",
                        "Pattern 4 (specific)"
                    ))
                
                
                # Pattern 5: Direct numbered
                possible_patterns.append((
                    f"for_{section_title.lower()}{i}",
                    f"for_{section_title.lower()}{i}_df",
                    "Pattern 5"
                ))
                
                # Try all patterns
                found_val = None
                found_df = None
                found_pattern = None
                
                for val_pattern, df_pattern, pattern_name in possible_patterns:
                    val_exists = val_pattern in data
                    df_exists = df_pattern in data
                    
                    if val_exists and df_exists:
                        found_val = data[val_pattern]
                        found_df = data[df_pattern]
                        found_pattern = pattern_name
                        break
                
                if found_val and found_df:
                    formula_parts.append(f"({found_val} X {found_df})")
                else:
                    pass
            
            if formula_parts:
                formula_content = " + ".join(formula_parts)
                result_text = f"{data.get(ans_key, '')} {data.get(param_key, '')}"
                divisor = data.get(div_key) if div_key else None
                add_formula_with_line(formula_content, result_text, divisor, start_x)
            else:
                # Show all keys that might be relevant
                search_terms = [check_key, section_title.lower(), head_key]
                for key in sorted(data.keys()):
                    if any(term in key.lower() for term in search_terms):
                        pass

    def add_average_formula_section_crm(check_key, section_title, head_key, ans_key, param_key, 
                                div_key=None, start_x=30):
            """Add formula section with average calculation"""
            if data.get(check_key):
                check_page_break(30)
                pdf.set_font("Calibri", 'B', 11)
                # pdf.cell(0, 8, f"{section_title}", 0, 1, 'L')
                if data.get(head_key):
                    pdf.cell(0, 6, f"{data.get(head_key)}", ln=True)
                pdf.set_font("Calibri", '', 10)
                for i in range(1, 4):
                    std = data.get(f"{base}_crm_standard_{i}")
                    srm = data.get(f"{base}_crm_srm{i}")

                    if std or srm:
                        pdf.cell(0, 6, f"{std} : {srm}", ln=True)

                pdf.ln(3)
                
                

                # ---------- FIRST PART (Simple Average Formula) ----------
                pdf.cell(0, 6, "Formula:", ln=True)
                pdf.set_font("Calibri", '', 10)

                # Save current Y
                old_y = pdf.get_y()

                # Build formula content like: a + b + c
                avg_values = []
                for i in range(1, 4):
                    val_key = f"{check_key[:-1]}{i}"  # for_color1, for_color2, for_color3
                    if data.get(val_key):
                        avg_values.append(str(data[val_key]))

                if avg_values:
                    formula_content = " + ".join(avg_values)
                    color_text_width = pdf.get_string_width(formula_content)
                    color_line_start_x = start_x
                    color_line_end_x = start_x + color_text_width

                    # Draw formula
                    pdf.set_x(start_x)
                    pdf.cell(color_text_width, 6, f"{formula_content} = {data.get(ans_key)} {data.get(param_key)}", align='L', ln=True)

                    # Draw underline
                    pdf.line(color_line_start_x, old_y + 5.5, color_line_end_x, old_y + 5.5)

                    # Draw divisor centered below line
                    divisor_text = data.get(div_key) if div_key else None
                    divisor_width = pdf.get_string_width(divisor_text)
                    center_divisor_x = color_line_start_x + (color_text_width / 2) - (divisor_width / 2)
                    pdf.set_x(center_divisor_x)
                    pdf.cell(divisor_width, 6, divisor_text, align="C", ln=True)

                # Spacing before next section
                pdf.ln(3)
    
    
    
    
    def add_average_formula_section(check_key, section_title, head_key, ans_key, param_key, 
                               div_key=None, start_x=30):
        """Add formula section with average calculation"""
        if data.get(check_key):
            check_page_break(30)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, f"{section_title}", 0, 1, 'L')
            pdf.set_font("Calibri", 'B', 10)
            
            if data.get(head_key):
                pdf.cell(0, 6, f"{data.get(head_key)}", ln=True)
            

            # ---------- FIRST PART (Simple Average Formula) ----------
            pdf.cell(0, 6, "Formula:", ln=True)
            pdf.set_font("Calibri", '', 10)

            # Save current Y
            old_y = pdf.get_y()

            # Build formula content like: a + b + c
            avg_values = []
            for i in range(1, 4):
                val_key = f"{check_key[:-1]}{i}"  # for_color1, for_color2, for_color3
                if data.get(val_key):
                    avg_values.append(str(data[val_key]))

            if avg_values:
                formula_content = " + ".join(avg_values)
                color_text_width = pdf.get_string_width(formula_content)
                color_line_start_x = start_x
                color_line_end_x = start_x + color_text_width

                # Draw formula
                pdf.set_x(start_x)
                pdf.cell(color_text_width, 6, f"{formula_content} = {data.get(ans_key)} {data.get(param_key)}", align='L', ln=True)

                # Draw underline
                pdf.line(color_line_start_x, old_y + 5.5, color_line_end_x, old_y + 5.5)

                # Draw divisor centered below line
                divisor_text = data.get(div_key) if div_key else None
                divisor_width = pdf.get_string_width(divisor_text)
                center_divisor_x = color_line_start_x + (color_text_width / 2) - (divisor_width / 2)
                pdf.set_x(center_divisor_x)
                pdf.cell(divisor_width, 6, divisor_text, align="C", ln=True)

            # Spacing before next section
            pdf.ln(3)

            # ---------- SECOND PART (Weighted Average Formula) ----------
            head_key_1 = head_key + "_1"
            pdf.set_font("Calibri", 'B', 10)
            if data.get(head_key_1):
                pdf.cell(0, 6, f"{data.get(head_key_1)}", ln=True)

                pdf.cell(0, 6, "Formula:", ln=True)
            pdf.set_font("Calibri", '', 10)

            # Save current Y
            old_y = pdf.get_y()

            # Build weighted formula like: (a × a_df) + (b × b_df) + (c × c_df)
            formula_parts = []
            for i in range(1, 4):
                val_key = f"{check_key[:-1]}1_{1}"
                df_key = f"{check_key[:-1]}1_{i}_df"
                if data.get(val_key) and data.get(df_key):
                    formula_parts.append(f"({data[val_key]} X {data[df_key]})")
                # formula_parts.append(f"()")

            if formula_parts:
                formula_content = " + ".join(formula_parts)
                color_text_width = pdf.get_string_width(formula_content)
                color_line_start_x = start_x
                color_line_end_x = start_x + color_text_width

                # Draw formula
                pdf.set_x(start_x)
                pdf.cell(color_text_width, 6, f"{formula_content} = {data.get(ans_key + '_1')} {data.get(param_key + '_1')}", align='L', ln=True)

                # Draw underline
                pdf.line(color_line_start_x, old_y + 5.5, color_line_end_x, old_y + 5.5)

                # Center divisor below line
                divisor_text = str(data.get(div_key)) if data.get(div_key) else ""
                divisor_width = pdf.get_string_width(divisor_text)
                center_divisor_x = color_line_start_x + (color_text_width / 2) - (divisor_width / 2)
                pdf.set_x(center_divisor_x)
                pdf.cell(divisor_width, 6, divisor_text, align="C")

            pdf.ln(4)

    def add_formula_block(head_text, reading_text, formula_content, result_text, divisor_text=None, start_x=30):
        """Add a formula block with automatic page break check"""
        # Check page break before each formula (estimate 25px needed)
        check_page_break(25)
        
        if head_text:
            pdf.set_font("Calibri", 'B', size=10)
            pdf.cell(0, 6, head_text, ln=True)
        
        if reading_text:
            pdf.cell(0, 6, reading_text, ln=True)
        
        pdf.cell(0, 6, "Formula:", ln=True)
        pdf.set_font("Calibri", '', 10)
        
        # Save current Y position
        old_y = pdf.get_y()
        
        # Get the width of the formula content
        text_width = pdf.get_string_width(formula_content)
        
        # Calculate line position to match text width
        line_start_x = start_x
        line_end_x = start_x + text_width
        
        # Draw the formula text
        pdf.set_x(start_x)
        pdf.cell(text_width, 6, f"{formula_content} = {result_text}", align='L', ln=True)
        
        # Draw the line below the formula
        pdf.line(line_start_x, old_y+5.5, line_end_x, old_y+5.5)
        
        if divisor_text:
            # Center the divisor below the line
            divisor_width = pdf.get_string_width(divisor_text)
            center_divisor_x = line_start_x + (text_width / 2) - (divisor_width / 2)
            pdf.set_x(center_divisor_x)
            pdf.cell(divisor_width, 3, divisor_text, align="C", ln=True)
            


    # Start calculations section
    pdf.add_page()
    pdf.set_y(35)
    add_calculation_header()

    # TDS Calculation Section
    if data.get('tds_final_ans'):
        check_page_break(100)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 4, "Total Dissolved Solids (TDS) Calculation:", 0, 1, 'L')
        pdf.set_font("Calibri", size=10)
        pdf.ln(3)
        
        # Process TDS sections
        tds_sections = [
            ('tds_head_1', 'bw1', 'AW05', 'vs1', 'ans1', 'ans_param', ''),
            ('tds_head_2', 'bw2', 'AW10', 'vs2', 'ans2', 'ans_param_2', 'read_1'),
            ('tds_head_3', 'bw3', 'AW15', 'vs3', 'ans3', 'ans_param_3', 'read_2'),
            ('tds_head_4', 'bw4', 'AW20', 'vs4', 'ans4', 'ans_param_4', 'read_3')
        ]
        
        for head_key, bw_key, aw_key, vs_key, ans_key, param_key, read_key in tds_sections:
            if data.get(head_key):
                check_page_break(25)
                
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data[head_key], border=False, align="L", ln=True)
                
                if data.get(read_key):
                    pdf.cell(0, 6, data[read_key], border=False, align="L", ln=True)
                
                pdf.set_x(30)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(30, 6, "Before Weight   = ", border=False, align="L")
                pdf.cell(0, 6, data.get(bw_key, ''), border=False, align="L", ln=True)
                
                pdf.set_x(30)
                pdf.cell(30, 6, "After Weight   = ", align="L")
                after_weights = [data.get(f'AW{i:02d}', '') for i in range(
                    int(aw_key[-2:])-4, int(aw_key[-2:])+1
                )]
                pdf.cell(0, 6, ", ".join(filter(None, after_weights)), align="L", ln=True)
                
                pdf.set_x(30)
                pdf.cell(36, 6, "Volume of Sample  =  ", border=False, align="L")
                pdf.cell(35, 6, data.get(vs_key, ''), border=False, align="L", ln=True)
                
                pdf.set_x(30)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(35, 6, "Formula :", border=False, align="L", ln=True)
                pdf.set_font("Calibri", '', 10)
                
                formula_text = f"({data.get(aw_key, '')} - {data.get(bw_key, '')}) X 1000000"
                result_text = f"{data.get(ans_key, '')} {data.get(param_key, '')}"
                add_formula_with_line(formula_text, result_text, data.get(vs_key, ''), 40)
       
        # TDS Final Average
        if 'tds_final_ans' in data:
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.ln(2)
            pdf.cell(0, 6, "Average of Total Dissolved Solids:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            
            final_text = f"{data.get('tds_final_ans1', '')} + {data.get('tds_final_ans2', '')} + {data.get('tds_final_ans3', '')}"
            result_text = f"{data['tds_final_ans']} {data.get('tds_final_param', '')}"
            add_formula_with_line(final_text, result_text, data.get('tds_final_divi','3'), 40)

    for key in sorted(data.keys()):

        # Match keys like: tds_crm_36_1_bw
        match = re.match(r'(tds_crm_\d+_\d+)_bw$', key)
        if not match:
            continue

        base = match.group(1)

        bw = data.get(f"{base}_bw")
        vs = data.get(f"{base}_vs")
        ans = data.get(f"{base}_ans")

        # --------- Collect ALL non-empty AW values (for display) ---------
        aw_values = []
        for i in range(1, 6):
            value = data.get(f"{base}_aw_{i}")
            if value:
                aw_values.append(value)

        # --------- Get LAST non-empty AW value (for formula) ---------
        aw_last = None
        for i in range(5, 0, -1):
            value = data.get(f"{base}_aw_{i}")
            if value:
                aw_last = value
                break

        # Skip if required values missing
        if not bw or not aw_last or not vs or not ans:
            continue

        check_page_break(40)

        # ---------- HEADER ----------
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get(f"{base}_head"), ln=True)
        pdf.ln(2)

        pdf.set_font("Calibri", '', 10)

        # ---------- BEFORE WEIGHT ----------
        pdf.set_x(30)
        pdf.cell(45, 6, "Before Weight  = ", ln=False)
        pdf.cell(0, 6, str(bw), ln=True)

        # ---------- AFTER WEIGHT (SHOW ALL VALUES) ----------
        pdf.set_x(30)
        pdf.cell(45, 6, "After Weight   = ", ln=False)
        pdf.cell(0, 6, ", ".join(aw_values), ln=True)

        # ---------- VOLUME ----------
        pdf.set_x(30)
        pdf.cell(45, 6, "Volume of Sample = ", ln=False)
        pdf.cell(0, 6, str(vs), ln=True)

        pdf.ln(3)

        # ---------- FORMULA (USE ONLY LAST VALUE) ----------
        pdf.set_x(30)
        pdf.set_font("Calibri", 'B', 10)
        pdf.cell(0, 6, "Formula :", ln=True)

        pdf.set_font("Calibri", '', 10)

        formula_text = f"({aw_last} − {bw}) × 1000000"
        result_text = f"{ans} mg/L"

        add_formula_with_line(
            formula_text,
            result_text,
            vs,
            40
        )


        pdf.ln(-4)
    
    # pH Calculation Section
    if data.get('for_ph1'):
        check_page_break(80)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 4, "pH Calculation:", 0, 1, 'L')
        
        ph_sections = [
            ('ph_head_1', 'for_ph1', 'for_ph2', 'for_ph3', 'ph_ans_1'),
            ('ph_head_2', 'for2_ph1', 'for2_ph2', 'for2_ph3', 'ph_ans_2'), 
            ('ph_head_3', 'for3_ph1', 'for3_ph2', 'for3_ph3', 'ph_ans_3'),
            ('ph_head_4', 'for4_ph1', 'for4_ph2', 'for4_ph3', 'ph_ans_4')
        ]
        
        for i, (head, val1, val2, val3, ans) in enumerate(ph_sections, start=1):
            if data.get(head):
                check_page_break(15)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data[head], border=False, align="L", ln=True)
                pdf.set_font("Calibri", size=10)

                ph_text = f"{data.get(val1, '')} + {data.get(val2, '')} + {data.get(val3, '')}"
                result_text = f"{data.get(ans, '')}"

                divisor = data.get(f'ph_divi_{i}', '3')  # ✅ CORRECT

                add_formula_with_line(ph_text, result_text, divisor, 30)
    
    pdf.ln(-4)
    for key in data.keys():
        match = re.match(r'(ph_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
    # Add all other calculation sections using helper functions
    # simple_calculations = [
    #     ('for_alum1', 'Aluminium Calculations', 'alum_head', 'alum_ans', 'alum_param', '', '_df', 'alum_divi'),
    #     ('for_anitomny1', 'Antimony Calculations', 'anitomny_head', 'anitomny_ans', 'anitomny_param', '', '_df', 'anitm_divi'),
    #     ('for_arsenic1', 'Arsenic Calculations', 'arsenic_head', 'arsenic_ans', 'arsenic_param', '', '_df', 'arsenic_divi'),
    #     ('for_barium1', 'Barium Calculations', 'barium_head', 'barium_ans', 'barium_param', '', '_df', 'barium_divi'),
    #     ('for_boron1', 'Boron Calculations', 'boron_head', 'boron_ans', 'boron_param', '', '_df', 'boron_divi'),
    #     ('for_cadmium1', 'Cadmium Calculations', 'cadmium_head', 'cadmium_ans', 'cadmium_param', '', '_df', 'cadmium_divi'),
    #     ('for_chromium1', 'Chromium Calculations', 'chromium_head', 'chromium_ans', 'chromium_param', '', '_df', 'chromium_divi'),
    #     ('for_copper1', 'Copper Calculations', 'copper_head', 'copper_ans', 'copper_param', '', '_df', 'copper_divi'),
    #     ('for_lead1', 'Lead Calculations', 'lead_head', 'lead_ans', 'lead_param', '', '_df', 'lead_divi'),
    #     ('for_manganese1', 'Manganese Calculations', 'manganese_head', 'manganese_ans', 'manganese_param', '', '_df', 'manganese_divi'),
    #     ('for_mercury1', 'Mercury Calculations', 'mercury_head', 'mercury_ans', 'mercury_param', '', '_df', 'mercury_divi'),
    #     ('for_nickel1', 'Nickel Calculations', 'nickel_head', 'nickel_ans', 'nickel_param', '', '_df', 'nickel_divi'),
    #     ('for_phenolic1', 'Phenolic Calculations', 'phenolic_head', 'phenolic_ans', 'phenolic_param', '', '_df', 'phenolic_divi'),
    #     ('for_selenium1', 'Selenium Calculations', 'selenium_head', 'selenium_ans', 'selenium_param', '', '_df', 'selenium_divi'),
    #     ('for_zinc1', 'Zinc Calculations', 'zinc_head', 'zinc_ans', 'zinc_param', '', '_df', 'zinc_divi'),
    #     ('for_beryllium1_1', 'Beryllium Calculations', 'beryllium_head_1', 'beryllium_ans_1', 'beryllium_param_1', '_1', '_1_df', 'beryllium_divi'),
    #     ('for_ammonium1_1', 'Ammonium Calculations', 'ammonium_head', 'ammonium_ans_1', 'ammonium_param_1', '_1', '_1_df', 'ammonium_divi'),
    #     ('for_formaldehyde1', 'Formaldehyde Calculations', 'formaldehyde_head', 'formaldehyde_ans', 'formaldehyde_param', '', '_df', 'formaldehyde_divi'),
    #     ('for_iron1', 'Iron Calculations', 'iron_head', 'iron_ans', 'iron_param', '', '_df', 'iron_divi'),
    #     ('for_sodium1', 'Sodium Calculations', 'sodium_head', 'sodium_ans', 'sodium_param', '', '_df', 'sodium_divi'),
    # ]

    # for calc_params in simple_calculations:
    #     add_simple_formula_section(*calc_params)

    add_simple_formula_section('for_alum1', 'Aluminium Calculations', 'alum_head', 'alum_ans', 'alum_param', '', '_df', 'alum_divi'),
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_aluminium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
        
    add_simple_formula_section('for_anitomny1', 'Antimony Calculations', 'anitomny_head', 'anitomny_ans', 'anitomny_param', '', '_df', 'anitm_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_antimony_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_arsenic1', 'Arsenic Calculations', 'arsenic_head', 'arsenic_ans', 'arsenic_param', '', '_df', 'arsenic_divi'),
    
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_arsenic_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_barium1', 'Barium Calculations', 'barium_head', 'barium_ans', 'barium_param', '', '_df', 'barium_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_barium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_boron1', 'Boron Calculations', 'boron_head', 'boron_ans', 'boron_param', '', '_df', 'boron_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_boron_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_cadmium1', 'Cadmium Calculations', 'cadmium_head', 'cadmium_ans', 'cadmium_param', '', '_df', 'cadmium_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_cadmium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_chromium1', 'Chromium Calculations', 'chromium_head', 'chromium_ans', 'chromium_param', '', '_df', 'chrom_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_chromium_(?:vi|iv)_crm_\d+_\d+)_1$', key, re.IGNORECASE)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_copper1', 'Copper Calculations', 'copper_head', 'copper_ans', 'copper_param', '', '_df', 'copper_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_copper_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_lead1', 'Lead Calculations', 'lead_head', 'lead_ans', 'lead_param', '', '_df', 'lead_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_lead_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_manganese1', 'Manganese Calculations', 'manganese_head', 'manganese_ans', 'manganese_param', '', '_df', 'manganese_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_manganese_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_mercury1', 'Mercury Calculations', 'mercury_head', 'mercury_ans', 'mercury_param', '', '_df', 'mercury_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_mercury_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_nickel1', 'Nickel Calculations', 'nickel_head', 'nickel_ans', 'nickel_param', '', '_df', 'nickel_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_nickel_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_phenolic1', 'Phenolic Calculations', 'phenolic_head', 'phenolic_ans', 'phenolic_param', '', '_df', 'phenolic_divi'),
    
    for key in data.keys():
        match = re.match(r'(phenol_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
    add_simple_formula_section('for_selenium1', 'Selenium Calculations', 'selenium_head', 'selenium_ans', 'selenium_param', '', '_df', 'selenium_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_selenium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_zinc1', 'Zinc Calculations', 'zinc_head', 'zinc_ans', 'zinc_param', '', '_df', 'zinc_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_zinc_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_beryllium1_1', 'Beryllium Calculations', 'beryllium_head_1', 'beryllium_ans_1', 'beryllium_param_1', '_1', '_1_df', 'beryllium_divi'),
    add_simple_formula_section('for_ammonium1_1', 'Ammonium Calculations', 'ammonium_head', 'ammonium_ans_1', 'ammonium_param_1', '_1', '_1_df', 'ammonium_divi'),
    add_simple_formula_section('for_formaldehyde1', 'Formaldehyde Calculations', 'formaldehyde_head', 'formaldehyde_ans', 'formaldehyde_param', '', '_df', 'formaldehyde_divi'),
    add_simple_formula_section('for_iron1', 'Iron Calculations', 'iron_head', 'iron_ans', 'iron_param', '', '_df', 'iron_divi'),
    
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_iron_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
        
    add_simple_formula_section('for_sodium1', 'Sodium Calculations', 'sodium_head', 'sodium_ans', 'sodium_param', '', '_df', 'sodium_divi'),
    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_sodium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
    
    
    
    # Average calculations
    # average_calculations = [
    #     ('for_color1', 'Color Calculation', 'color_head', 'color_ans', 'color_param', 'color_divi'),
    #     ('color_crm_1_1_1', 'Color CRM Calculation', 'color_crm_1_1_head', 'color_crm_1_1_ans', 'color_crm_1_1_param', 'color_crm_1_1_divi'),
    #     ('for_cyanide1', 'Cyanide Calculation', 'cyanide_head', 'cyanide_ans', 'cyanide_param', 'cyanide_divi'),
    #     ('for_fluoride1', 'Fluoride Calculation', 'fluoride_head', 'fluoride_ans', 'fluoride_param', 'fluoride_divi'),
    #     ('for_nitrate1', 'Nitrate Calculation', 'nitrate_head', 'nitrate_ans', 'nitrate_param', 'nitrate_divi'),
    #     ('for_nitrite1', 'Nitrite Calculation', 'nitrite_head', 'nitrite_ans', 'nitrite_param', 'nitrite_divi'),
    #     ('for_residual1', 'Residual Calculation', 'residual_head', 'residual_ans', 'residual_param', 'residual_divi'),
    #     ('for_trubidity1', 'Turbidity Calculation', 'trubidity_head', 'trubidity_ans', 'trubidity_param', 'trubidity_divi'),
    #     ('for_ammonia1', 'Ammonia Calculation', 'ammonia_head', 'ammonia_ans', 'ammonia_param', 'ammonia_divi'),
    #     ('for_ionic_det1', 'Ionic Detergent Calculation', 'ionic_det_head', 'ionic_det_ans', 'ionic_det_param', 'ionic_det_divi'),
    #     ('for_freechlorine1', 'Freechlorine Calculation', 'freechlorine_head', 'freechlorine_ans', 'freechlorine_param', 'freechlorine_divi'),
    #     ('for_sulphate1', 'sulphate Calculation', 'sulphate_head', 'sulphate_ans', 'sulphate_param', 'sulphate_divi'),
    # ]

    # for calc_params in average_calculations:
    #     add_average_formula_section(*calc_params)
    
    # add_average_formula_section('for_color1', 'Color Calculation', 'color_head', 'color_ans', 'color_param', 'color_divi')
    if(data.get('color_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Color Calculations", ln=True)
        pdf.cell(0,6,data.get('color_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_color1')} + {data.get('for_color2')} + {data.get('for_color3')}",
                f"{data['color_ans']} {data.get('color_param')}",
                data.get('color_divi1', "3")
            )
            
    if(data.get('color_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('color_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_color1_1')} X {data.get('for_color1_1_df')}) + ({data.get('for_color1_2')} X {data.get('for_color1_2_df')}) + ({data.get('for_color1_3')} X {data.get('for_color1_3_df')})",
                f"{data['color_ans_1']} {data.get('color_param_1')}",
                data.get('color_divi')
            )
    
    for key in data.keys():
        match = re.match(r'(color_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )

    # add_average_formula_section('for_cyanide1', 'Cyanide Calculation', 'cyanide_head', 'cyanide_ans', 'cyanide_param', 'cyanide_divi')
    
    if(data.get('cyanide_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Cyanide Calculations", ln=True)
        pdf.cell(0,6,data.get('cyanide_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_cyanide1')} + {data.get('for_cyanide2')} + {data.get('for_cyanide3')}",
                f"{data['cyanide_ans']} {data.get('cyanide_param')}",
                data.get('cyanide_divi1', "3")
            )
            
    if(data.get('cyanide_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('cyanide_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_cyanide1_1')} X {data.get('for_cyanide1_1_df')}) + ({data.get('for_cyanide1_2')} X {data.get('for_cyanide1_2_df')}) + ({data.get('for_cyanide1_3')} X {data.get('for_cyanide1_3_df')})",
                f"{data['cyanide_ans_1']} {data.get('cyanide_param_1')}",
                data.get('cyanide_divi')
            )
    
    for key in data.keys():
        match = re.match(r'(cyanide_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
    
    
    # add_average_formula_section('for_fluoride1', 'Fluoride Calculation', 'fluoride_head', 'fluoride_ans', 'fluoride_param', 'fluoride_divi')
    if(data.get('fluoride_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Fluoride Calculations", ln=True)
        pdf.cell(0,6,data.get('fluoride_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_fluoride1')} + {data.get('for_fluoride2')} + {data.get('for_fluoride3')}",
                f"{data['fluoride_ans']} {data.get('fluoride_param')}",
                data.get('fluoride_divi1', "3")
            )
            
    if(data.get('fluoride_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('fluoride_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_fluoride1_1')} X {data.get('for_fluoride1_1_df')}) + ({data.get('for_fluoride1_2')} X {data.get('for_fluoride1_2_df')}) + ({data.get('for_fluoride1_3')} X {data.get('for_fluoride1_3_df')})",
                f"{data['fluoride_ans_1']} {data.get('fluoride_param_1')}",
                data.get('fluoride_divi')
            )
    
    for key in data.keys():
        match = re.match(r'(fluoride_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
    
    
    # add_average_formula_section('for_nitrate1', 'Nitrate Calculation', 'nitrate_head', 'nitrate_ans', 'nitrate_param', 'nitrate_divi')
    
    if(data.get('nitrate_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Nitrate Calculations", ln=True)
        pdf.cell(0,6,data.get('nitrate_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_nitrate1')} + {data.get('for_nitrate2')} + {data.get('for_nitrate3')}",
                f"{data['nitrate_ans']} {data.get('nitrate_param')}",
                data.get('nitrate_divi1', "3")
            )
            
    if(data.get('nitrate_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('nitrate_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_nitrate1_1')} X {data.get('for_nitrate1_1_df')}) + ({data.get('for_nitrate1_2')} X {data.get('for_nitrate1_2_df')}) + ({data.get('for_nitrate1_3')} X {data.get('for_nitrate1_3_df')})",
                f"{data['nitrate_ans_1']} {data.get('nitrate_param_1')}",
                data.get('nitrate_divi')
            )
    
    
    for key in data.keys():
        match = re.match(r'(nitrate_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
        
    # add_average_formula_section('for_nitrite1', 'Nitrite Calculation', 'nitrite_head', 'nitrite_ans', 'nitrite_param', 'nitrite_divi')
    
    if(data.get('nitrite_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Nitrite Calculations", ln=True)
        pdf.cell(0,6,data.get('nitrite_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_nitrite1')} + {data.get('for_nitrite2')} + {data.get('for_nitrite3')}",
                f"{data['nitrite_ans']} {data.get('nitrite_param')}",
                data.get('nitrite_divi1', "3")
            )
            
    if(data.get('nitrite_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('nitrite_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_nitrite1_1')} X {data.get('for_nitrite1_1_df')}) + ({data.get('for_nitrite1_2')} X {data.get('for_nitrite1_2_df')}) + ({data.get('for_nitrite1_3')} X {data.get('for_nitrite1_3_df')})",
                f"{data['nitrite_ans_1']} {data.get('nitrite_param_1')}",
                data.get('nitrite_divi')
            )
    
    for key in data.keys():
        match = re.match(r'(nitrite_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
        
    # add_average_formula_section('for_residual1', 'Residual Calculation', 'residual_head', 'residual_ans', 'residual_param', 'residual_divi')
    
    if(data.get('residual_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Residual Chlorine Calculations", ln=True)
        pdf.cell(0,6,data.get('residual_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_residual1')} + {data.get('for_residual2')} + {data.get('for_residual3')}",
                f"{data['residual_ans']} {data.get('residual_param')}",
                data.get('residual_divi1', "3")
            )
            
    if(data.get('residual_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('residual_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_residual1_1')} X {data.get('for_residual1_1_df')}) + ({data.get('for_residual1_2')} X {data.get('for_residual1_2_df')}) + ({data.get('for_residual1_3')} X {data.get('for_residual1_3_df')})",
                f"{data['residual_ans_1']} {data.get('residual_param_1')}",
                data.get('residual_divi')
            )
    
    
    for key in data.keys():
        match = re.match(r'(residual_chlorine_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
    # add_average_formula_section('for_trubidity1', 'Turbidity Calculation', 'trubidity_head', 'trubidity_ans', 'trubidity_param', 'trubidity_divi')
    if(data.get('trubidity_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Trubidity Calculations", ln=True)
        pdf.cell(0,6,data.get('trubidity_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_trubidity1')} + {data.get('for_trubidity2')} + {data.get('for_trubidity3')}",
                f"{data['trubidity_ans']} {data.get('trubidity_param')}",
                data.get('trubidity_divi1', "3")
            )
            
    if(data.get('trubidity_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('trubidity_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_trubidity1_1')} X {data.get('for_trubidity1_1_df')}) + ({data.get('for_trubidity1_2')} X {data.get('for_trubidity1_2_df')}) + ({data.get('for_trubidity1_3')} X {data.get('for_trubidity1_3_df')})",
                f"{data['trubidity_ans_1']} {data.get('trubidity_param_1')}",
                data.get('trubidity_divi')
            )
        
        
    for key in data.keys():
        match = re.match(r'(turbidity_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
    add_average_formula_section('for_ammonia1', 'Ammonia Calculation', 'ammonia_head', 'ammonia_ans', 'ammonia_param', 'ammonia_divi')  
    add_average_formula_section('for_ionic_det1', 'Ionic Detergent Calculation', 'ionic_det_head', 'ionic_det_ans', 'ionic_det_param', 'ionic_det_divi')   
    add_average_formula_section('for_freechlorine1', 'Freechlorine Calculation', 'freechlorine_head', 'freechlorine_ans', 'freechlorine_param', 'freechlorine_divi')
    # add_average_formula_section('for_sulphate1', 'sulphate Calculation', 'sulphate_head', 'sulphate_ans', 'sulphate_param', 'sulphate_divi')
    if(data.get('sulphate_ans')):
        
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "sulphate Calculations", ln=True)
        pdf.cell(0,6,data.get('sulphate_head'),ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"{data.get('for_sulphate1')} + {data.get('for_sulphate2')} + {data.get('for_sulphate3')}",
                f"{data['sulphate_ans']} {data.get('sulphate_param')}",
                data.get('sulphate_divi1', "3")
            )
            
    if(data.get('sulphate_ans_1')):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 6, data.get('sulphate_head_1'), ln=True)
        pdf.set_font("Calibri", '', 10)
        add_formula_block(
                None,
                None,
                f"({data.get('for_sulphate1_1')} X {data.get('for_sulphate1_1_df')}) + ({data.get('for_sulphate1_2')} X {data.get('for_sulphate1_2_df')}) + ({data.get('for_sulphate1_3')} X {data.get('for_sulphate1_3_df')})",
                f"{data['sulphate_ans_1']} {data.get('sulphate_param_1')}",
                data.get('sulphate_divi')
            )
    
    
    for key in data.keys():
        match = re.match(r'(sulphate_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # render only if checkbox/value is true
        if not data.get(f"{base}_1"):
            continue

        add_average_formula_section(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        
        
        
    # Specialized sections with proper page breaks
    specialized_sections = [
        'chloride_1_1', 'hardness_2_1', 'acidity_1_1', 'alkalinity_1_1',
        'ecoli_ans', 'fecal_ans'
    ]

    # Helper function for formula blocks
    
    def add_formula_block_2(head_text, reading_text, formula_content, result_text, divisor_text=None, start_x=30):
        """Add a formula block with automatic page break check"""
        # Check page break before each formula (estimate 25px needed)
        check_page_break(25)
        
        if head_text:
            pdf.set_font("Calibri", 'B', size=10)
            pdf.cell(0, 6, head_text, ln=True)
        
        if reading_text:
            pdf.cell(0, 6, reading_text, ln=True)
        
        pdf.cell(0, 6, "Formula:", ln=True)
        pdf.set_font("Calibri", '', 10)
        
        # Save current Y position
        old_y = pdf.get_y()
        
        # Get the width of the formula content
        text_width = pdf.get_string_width(formula_content)
        
        # Calculate line position to match text width
        line_start_x = start_x
        line_end_x = start_x + text_width
        
        # Draw the formula text
        pdf.set_x(start_x)
        pdf.cell(text_width, 6, f"{formula_content} X {result_text}", align='L', ln=True)
        
        # Draw the line below the formula
        pdf.line(line_start_x, old_y+5.5, line_end_x, old_y+5.5)
        
        if divisor_text:
            # Center the divisor below the line
            divisor_width = pdf.get_string_width(divisor_text)
            center_divisor_x = line_start_x + (text_width / 2) - (divisor_width / 2)
            pdf.set_x(center_divisor_x)
            pdf.cell(divisor_width, 3, divisor_text, align="C", ln=True)

    # HARDNESS CALCULATION
    if data.get('hardness_2_1'):
        # check_page_break(100)  # Reserve space for entire hardness section
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Hardness Calculation:", 0, 1, 'L')
        
        # Hardness Reading 1
        if data.get('hardness_reading_1'):
            add_formula_block(
                data.get('hardness_head_2'),
                data.get('hardness_reading_1'),
                f"({data.get('hardness_2_1')} - {data.get('hardness_2_2')}) X 1000",
                f"{data['hardness_ans2']} {data.get('hardness_param2')}",
                data.get('hardness_2_3')
            )
        
        # Hardness Reading 2
        pdf.set_font("Calibri", 'B', 11)
        if data.get('hardness_reading_2'):
            add_formula_block(
                None,  # No head for subsequent readings
                data.get('hardness_reading_2'),
                f"({data.get('hardness_3_1')} - {data.get('hardness_3_2')}) X 1000",
                f"{data['hardness_ans3']} {data.get('hardness_param3')}",
                data.get('hardness_3_3')
            )
        
        # Hardness Reading 3
        pdf.set_font("Calibri", 'B', 11)
        if data.get('hardness_readinng_3'):
            add_formula_block(
                None,  # No head for subsequent readings
                data.get('hardness_readinng_3'),
                f"({data.get('hardness_4_1')} - {data.get('hardness_4_2')}) X 1000",
                f"{data['hardness_ans4']} {data.get('hardness_param4')}",
                data.get('hardness_4_3')
            )
            
        formula_parts = []

        if data.get('hardness_reading_1'):
            formula_parts.append(
                f"({data.get('for_hardness1')} X {data.get('for_hardness1_df')})"
            )

        if data.get('hardness_reading_2'):
            formula_parts.append(
                f"({data.get('for_hardness2')} X {data.get('for_hardness2_df')})"
            )

        if data.get('hardness_readinng_3'):
            formula_parts.append(
                f"({data.get('for_hardness3')} X {data.get('for_hardness3_df')})"
            )
        
        average_formula = " + ".join(formula_parts)
        # Hardness Average
        if formula_parts:
            add_formula_block(
                data.get('hardness_avg_head'),
                None,
                average_formula,
                f"{data['for_hardness_ans']} {data.get('for_hardness_param')}",
                data.get('hardness_divi')
            )

    
    for key in sorted(data.keys()):
        # Match keys like 'alkalinity_crm_36_1_1'
        match = re.match(r'(total_hardness_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # Check if value exists for this base first element
        if not data.get(f"{base}_1"):
            continue
        pdf.set_font("Calibri", 'B', size=10)
        pdf.cell(0,5,"Total Hardness CRM Calculations",ln=True)
        pdf.set_font("Calibri", '', size=10)
        head = data.get(f"{base}_head")                  # e.g. "Alkalinity:"
        reading = data.get(f"{base}_reading_1")          # if you have reading keys for CRM, else None
        val_1 = data.get(f"{base}_1")                     # e.g. "10.4"
        val_2 = data.get(f"{base}_2")                     # e.g. "0.1"
        val_3 = data.get(f"{base}_3")                     # e.g. "0.02"
        val_4 = data.get(f"{base}_4")                     # e.g. "0.02"
        divisor = data.get(f"{base}_divi") or "1"         # e.g. "100"
        ans = data.get(f"{base}_ans")                      # e.g. "103.000"
        param = data.get(f"{base}_param")                  # e.g. "mg/L"

        # Compose formula string like: "(val_1 + val_2 + val_3) / divisor"
        

        # Call add_formula_block dynamically
        add_formula_block(
            head,
            reading,
            f"({val_1} - {val_2}) X 1000",
            f"{ans} {param}",
            divisor
        )
    
    # ACIDITY CALCULATION
    if data.get('acidity_1_1'):
        check_page_break(120)  # Reserve space for entire acidity section
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Acidity Calculation:", 0, 1, 'L')  # Fixed title from "Hardness"
        
        # Acidity Reading 1
        add_formula_block(
            data.get('acidity_head_1'),
            data.get('acidity_reading_1'),
            f"({data.get('acidity_1_1')} - {data.get('acidity_1_2')}) X {data.get('acidity_1_3')} X 5000",
            f"{data['acidity_ans1']} {data.get('acidity_param1')}",
            data.get('acidity_1_4')
        )
        
        # Acidity Reading 2
        add_formula_block(
            None,
            data.get('acidity_reading_2'),
            f"({data.get('acidity_2_1')} - {data.get('acidity_2_2')}) X {data.get('acidity_2_3')} X 5000",
            f"{data['acidity_ans2']} {data.get('acidity_param2')}",
            data.get('acidity_2_4')
        )
        
        # Acidity Reading 3
        add_formula_block(
            None,
            data.get('acidity_reading_3'),
            f"({data.get('acidity_3_1')} - {data.get('acidity_3_2')}) X {data.get('acidity_3_3')} X 5000",
            f"{data['acidity_ans3']} {data.get('acidity_param3')}",
            data.get('acidity_3_4')
        )
        
        # Acidity Average
        if data.get('for_acidity1'):
            add_formula_block(
                data.get('acidity_avg_head'),
                None,
                f"({data.get('for_acidity1')} X {data.get('for_acidity1_df')}) + ({data.get('for_acidity2')} X {data.get('for_acidity2_df')}) + ({data.get('for_acidity3')} X {data.get('for_acidity3_df')})",
                f"{data['for_acidity_ans']} {data.get('for_acidity_param')}",
                data.get('acidity_divi')
            )

    # ALKALINITY CALCULATION
    if data.get('alkalinity_1_1'):
        check_page_break(120)  # Reserve space for entire alkalinity section
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Alkalinity Calculation:", 0, 1, 'L')
        
        # Alkalinity Reading 1
        add_formula_block(
            data.get('alkalinity_head_1'),
            data.get('alkalinity_reading_1'),
            f"({data.get('alkalinity_1_1')} - {data.get('alkalinity_1_2')}) X {data.get('alkalinity_1_3')} X 5000",
            f"{data['alkalinity_ans1']} {data.get('alkalinity_param1')}",
            data.get('alkalinity_1_4')
        )
        
        # Alkalinity Reading 2
        add_formula_block(
            None,
            data.get('alkalinity_reading_2'),
            f"({data.get('alkalinity_2_1')} - {data.get('alkalinity_2_2')}) X {data.get('alkalinity_2_3')} X 5000",
            f"{data['alkalinity_ans2']} {data.get('alkalinity_param2')}",
            data.get('alkalinity_2_4')
        )
        
        # Alkalinity Reading 3
        add_formula_block(
            None,
            data.get('alkalinity_reading_3'),
            f"({data.get('alkalinity_3_1')} - {data.get('alkalinity_3_2')}) X {data.get('alkalinity_3_3')} X 5000",
            f"{data['alkalinity_ans3']} {data.get('alkalinity_param3')}",
            data.get('alkalinity_3_4')
        )
        
        # Alkalinity Average
        if data.get('for_alkalinity1'):
            add_formula_block(
                data.get('alkalinity_avg_head'),
                None,
                f"({data.get('for_alkalinity1')} X {data.get('for_alkalinity1_df')}) + ({data.get('for_alkalinity2')} X {data.get('for_alkalinity2_df')}) + ({data.get('for_alkalinity3')} X {data.get('for_alkalinity3_df')})",
                f"{data['for_alkalinity_ans']} {data.get('for_alkalinity_param')}",
                data.get('alkalinity_divi')
            )
        pdf.set_font("Calibri", 'B', size=10)
        pdf.cell(0,5,"Alkalinity CRM Calculations",ln=True)
        pdf.set_font("Calibri", '', size=10)
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(alkalinity_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # Check if value exists for this base first element
            if not data.get(f"{base}_1"):
                continue

            head = data.get(f"{base}_head")                  # e.g. "Alkalinity:"
            reading = data.get(f"{base}_reading_1")          # if you have reading keys for CRM, else None
            val_1 = data.get(f"{base}_1")                     # e.g. "10.4"
            val_2 = data.get(f"{base}_2")                     # e.g. "0.1"
            val_3 = data.get(f"{base}_3")                     # e.g. "0.02"
            divisor = data.get(f"{base}_divi") or "1"         # e.g. "100"
            ans = data.get(f"{base}_ans")                      # e.g. "103.000"
            param = data.get(f"{base}_param")                  # e.g. "mg/L"

            # Compose formula string like: "(val_1 + val_2 + val_3) / divisor"
            

            # Call add_formula_block dynamically
            add_formula_block(
                head,
                reading,
                f"({val_1} - {val_2}) X {val_3} X 5000",
                f"{ans} {param}",
                divisor
            )

    # CHLORIDE CALCULATION (if you have this data)
    if data.get('chloride_ans1'):
    
        check_page_break(120)  # Reserve space for entire chloride section
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Chloride Calculation:", 0, 1, 'L')
        
        # Chloride Reading 1
        add_formula_block(
            data.get('chloride_head_1'),
            None,
            f"({data.get('chloride_1_1')} - {data.get('chloride_1_2')}) - ({data.get('chloride_1_3')} - {data.get('chloride_1_4')}) X {data.get('chloride_1_5')} X 35450",
            f"{data['chloride_ans1']} {data.get('chloride_param1')}",
            data.get('chloride_1_6')
        )
        
        # Chloride Reading 2
        pdf.set_font("Calibri", 'B', 11)
        if data.get('chloride_reading_1'):
            add_formula_block(
                data.get('chloride_head_2'),
                data.get('chloride_reading_1'),
                f"({data.get('chloride_2_1')} - {data.get('chloride_2_2')}) - ({data.get('chloride_2_3')} - {data.get('chloride_2_4')}) X {data.get('chloride_2_5')} X 35450",
                f"{data.get('chloride_ans2', data.get('chloride_ans1', ''))} {data.get('chloride_param2', data.get('chloride_param1', ''))}",
                data.get('chloride_2_6')
            )
        
        # Chloride Reading 3
        pdf.set_font("Calibri", 'B', 11)
        if data.get('chloride_reading_2'):
            add_formula_block(
                data.get('chloride_head_3'),
                data.get('chloride_reading_2'),
                f"({data.get('chloride_3_1')} - {data.get('chloride_3_2')}) - ({data.get('chloride_3_3')} - {data.get('chloride_3_4')}) X {data.get('chloride_3_5')} X 35450",
                f"{data.get('chloride_ans3', data.get('chloride_ans1', ''))} {data.get('chloride_param3', data.get('chloride_param1', ''))}",
                data.get('chloride_3_6')
            )
        
        # Chloride Reading 4
        pdf.set_font("Calibri", 'B', 11)
        if data.get('chloride_reading_3'):
            add_formula_block(
                data.get('chloride_head_4'),
                data.get('chloride_reading_3'),
                f"({data.get('chloride_4_1')} - {data.get('chloride_4_2')}) - ({data.get('chloride_4_3')} - {data.get('chloride_4_4')}) X {data.get('chloride_4_5')} X 35450",
                f"{data.get('chloride_ans4', data.get('chloride_ans1', ''))} {data.get('chloride_param4', data.get('chloride_param1', ''))}",
                data.get('chloride_4_6')
            )
        
        chloride_formula_parts = []
        if data.get('chloride_reading_1'):
            chloride_formula_parts.append(
                f"({data.get('for_chloride1')} X {data.get('for_chloride1_df')})"
            )
        
        # Chloride Reading 3
        if data.get('chloride_reading_2'):
            chloride_formula_parts.append(
                f"({data.get('for_chloride2')} X {data.get('for_chloride2_df')})"
            )
        
        # Chloride Reading 4
        if data.get('chloride_reading_3'):
            chloride_formula_parts.append(
                f"({data.get('for_chloride3')} X {data.get('for_chloride3_df')})"
            )
        # Chloride Average (if available)
        chloride_avg_formula = " + ".join(chloride_formula_parts)
        if data.get('for_chloride1'):
            add_formula_block(
                data.get('chloride_avg_head', "Chloride Average"),
                None,
                chloride_avg_formula,
                f"{data.get('for_chloride_ans', '')} {data.get('for_chloride_param', '')}",
                data.get('chloride_divi')
            )
        
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(chloride_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # Check if value exists for this base first element
            if not data.get(f"{base}_1"):
                continue
            pdf.set_font("Calibri", 'B', size=10)
            pdf.cell(0,5,"Chloride CRM Calculations",ln=True)
            pdf.set_font("Calibri", '', size=10)
            head = data.get(f"{base}_head")                  # e.g. "Alkalinity:"
            reading = data.get(f"{base}_reading_1")          # if you have reading keys for CRM, else None
            val_1 = data.get(f"{base}_1")                     # e.g. "10.4"
            val_2 = data.get(f"{base}_2")                     # e.g. "0.1"
            val_3 = data.get(f"{base}_3")                     # e.g. "0.02"
            val_4 = data.get(f"{base}_4")                     # e.g. "0.02"
            val_5 = data.get(f"{base}_5")                     # e.g. "0.02"
            divisor = data.get(f"{base}_divi") or "1"         # e.g. "100"
            ans = data.get(f"{base}_ans")                      # e.g. "103.000"
            param = data.get(f"{base}_param")                  # e.g. "mg/L"

            # Compose formula string like: "(val_1 + val_2 + val_3) / divisor"
            

            # Call add_formula_block dynamically
            add_formula_block(
                head,
                None,
                f"({val_1} - {val_2}) - ({val_3} - {val_4}) X {val_5} X 35450",
                f"{ans} {param}",
                divisor
            )

    # SIMPLE CALCULATIONS (E.coli, Fecal)
    if data.get('ecoli_ans'):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "E.Coli Calculation:", 0, 1, 'L')
        pdf.set_font("Calibri", '', 10)
        pdf.cell(0, 6, f"Result: {data['ecoli_ans']} {data.get('ecoli_param', '')}", ln=True)

    if data.get('fecal_ans'):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Faecal Coliform Calculation:", 0, 1, 'L')
        pdf.set_font("Calibri", '', 10)
        pdf.cell(0, 6, f"Result: {data['fecal_ans']} {data.get('fecal_param', '')}", ln=True)
        
    if data.get('hetrobacteria_ans'):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Heterotrophic Bacteria calculations:", 0, 1, 'L')
        pdf.set_font("Calibri", '', 10)
        pdf.cell(0, 6, f"Result: {data['hetrobacteria_ans']} {data.get('hetrobacteria_param', '')}", ln=True)
        
    if data.get('total_coliform_ans'):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Coliform:", 0, 1, 'L')
        pdf.set_font("Calibri", '', 10)
        pdf.cell(0, 6, f"Result: {data['total_coliform_ans']} {data.get('total_coliform_param', '')}", ln=True)
        
    
    if data.get('bacteria_ans'):
        check_page_break(20)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Total Bacteria Count:", 0, 1, 'L')
        pdf.set_font("Calibri", '', 10)
        pdf.cell(0, 6, f"Result: {data['bacteria_ans']} {data.get('bacteria_param', '')}", ln=True)
        
    
    
    if data.get('carbonates_1_1'):
        check_page_break(120)  # Reserve space for entire carbonates section
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 8, "Carbonates Calculation:", 0, 1, 'L')
        
        # Alkalinity Reading 1
        add_formula_block(
            data.get('carbonates_head_1'),
            data.get('carbonates_reading_1'),
            f"({data.get('carbonates_1_1')} - {data.get('carbonates_1_2')}) X {data.get('carbonates_1_3')} X 5000",
            f"{data['carbonates_ans1']} {data.get('carbonates_param1')}",
            data.get('carbonates_1_4')
        )
        
        # carbonates Reading 2
        add_formula_block(
            None,
            data.get('carbonates_reading_2'),
            f"({data.get('carbonates_2_1')} - {data.get('carbonates_2_2')}) X {data.get('carbonates_2_3')} X 5000",
            f"{data['carbonates_ans2']} {data.get('carbonates_param2')}",
            data.get('carbonates_2_4')
        )
        
        # carbonates Reading 3
        add_formula_block(
            None,
            data.get('carbonates_reading_3'),
            f"({data.get('carbonates_3_1')} - {data.get('carbonates_3_2')}) X {data.get('carbonates_3_3')} X 5000",
            f"{data['carbonates_ans3']} {data.get('carbonates_param3')}",
            data.get('carbonates_3_4')
        )
        
        # carbonates Average
        if data.get('for_carbonates1'):
            add_formula_block(
                data.get('carbonates_avg_head'),
                None,
                f"({data.get('for_carbonates1')} X {data.get('for_carbonates1_df')}) + ({data.get('for_carbonates2')} X {data.get('for_carbonates2_df')}) + ({data.get('for_carbonates3')} X {data.get('for_carbonates3_df')})",
                f"{data['for_carbonates_ans']} {data.get('for_carbonates_param')}",
                data.get('carbonates_divi')
            )
    

        
    # MAGNESIUM CALCULATION
    if data.get('for_magnesium1_1') or data.get('r1_final'):
        # check_page_break(100)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 4, "Magnesium Calculation:", 0, 1, 'L')
        pdf.set_font("Calibri", size=10)
        pdf.ln(3)
        
        # Method 1: Direct Magnesium Calculation
        if data.get('for_magnesium1_1'):
            check_page_break(25)
            
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('magnesium_head', 'Magnesium: (APHA 3111-B):'), border=False, align="L", ln=True)
            
            pdf.set_x(10)
            pdf.set_font("Calibri", '', 10)
            pdf.cell(30, 6, "Formula = ", border=False, align="L")
            
            # Build formula content
            formula_parts = []
            for i in range(1, 4):
                val = data.get(f'for_magnesium1_{i}', '')
                df = data.get(f'for_magnesium1_{i}_df', '')
                if val and df:
                    formula_parts.append(f"({val} X {df})")
            
            if formula_parts:
                formula_content = " + ".join(formula_parts)
                result_text = f"{data.get('magnesium_ans_1', '')} {data.get('magnesium_param_1', 'mg/L')}"
                divisor = data.get('magnesium_divi', '3')
                add_formula_with_line(formula_content, result_text, divisor, 25)
        
        # Method 2: APHA 3500-Mg B Calculation Method
        if data.get('r1_final'):
            check_page_break(25)
            
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('magnesium_head_1', 'Magnesium: (APHA 3500-Mg B- Calculation Method):'), border=False, align="L", ln=True)
            
            # Process each reading
            magnesium_sections = [
                ('r1', 'r1_th_as_caco', 'r1_final', 'r1_initial', 'r1_multiply', 'r1_divi', 'r1_ans', 'r1_param', 
                'r1_th', 'r1_df', 'r1_th1', 'r1_th_param',
                'r1_ch', 'r1_1_final', 'r1_1_initial', 'r1_1_multiply', 'r1_1_divi', 'r1_1_ans', 'r1_1_param',
                'r1_1_th', 'r1_1_df', 'r1_1_CaH1', 'r1_1_th_param',
                'r1_mg', 'r1_th1_final', 'r1_cah1_final', 'r1_final_multiply', 'r1_final_ans', 'r1_final_param'),
                
                ('r2', 'r2_th_as_caco', 'r2_final', 'r2_initial', 'r2_multiply', 'r2_divi', 'r2_ans', 'r2_param',
                'r2_th', 'r2_df', 'r2_th1', 'r2_th_param',
                'r2_ch', 'r2_1_final', 'r2_1_initial', 'r2_1_multiply', 'r2_1_divi', 'r2_1_ans', 'r2_1_param',
                'r2_1_th', 'r2_1_df', 'r2_1_CaH1', 'r2_1_th_param',
                'r2_mg', 'r2_th1_final', 'r2_cah1_final', 'r2_final_multiply', 'r2_final_ans', 'r2_final_param'),
                
                ('r3', 'r3_th_as_caco', 'r3_final', 'r3_initial', 'r3_multiply', 'r3_divi', 'r3_ans', 'r3_param',
                'r3_th', 'r3_df', 'r3_th1', 'r3_th_param',
                'r3_ch', 'r3_1_final', 'r3_1_initial', 'r3_1_multiply', 'r3_1_divi', 'r3_1_ans', 'r3_1_param',
                'r3_1_th', 'r3_1_df', 'r3_1_CaH1', 'r3_1_th_param',
                'r3_mg', 'r3_th1_final', 'r3_cah1_final', 'r3_final_multiply', 'r3_final_ans', 'r3_final_param')
            ]
            
            for section in magnesium_sections:
                (reading_key, th_head, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                th_key, df_key, th1_key, th_param_key,
                ch_head, ch_final_key, ch_initial_key, ch_multiply_key, ch_divi_key, ch_ans_key, ch_param_key,
                ch_th_key, ch_df_key, ch_cah1_key, ch_th_param_key,
                mg_head, mg_th_final_key, mg_cah_final_key, mg_multiply_key, mg_ans_key, mg_param_key) = section
                
                if data.get(final_key):
                    check_page_break(40)
                    
                    # Reading Header
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.ln(3)
                    pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[1]}'), border=False, align="L", ln=True)
                    
                    # Total Hardness as CaCO3
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(40, 6, f"{data.get(th_head, 'Total Hardness as CaCO3')} = ", border=False, align="L")
                    
                    pdf.set_font("Calibri", '', 10)
                    
                    formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                    result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                    divisor = data.get(divi_key, '50')
                    
                    add_formula_with_line(formula_text, result_text, divisor, 50)
                    
                    # TH Calculation
                    if data.get(th_key) and data.get(df_key):
                        pdf.ln(-2)
                        pdf.set_x(50)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(0, 3, f"{data.get(th_key, '')} X {data.get(df_key, '')} = {data.get(th1_key, '')} {data.get(th_param_key, 'mg/L')}", align="L", ln=True)
                    pdf.ln(3)
                    # Calcium Hardness
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(40, 6, f"{data.get(ch_head, 'Calcium Hardness')} = ", border=False, align="L")
                    
                    formula_text = f"({data.get(ch_final_key, '')} - {data.get(ch_initial_key, '')}) X {data.get(ch_multiply_key, '1000')}"
                    result_text = f"{data.get(ch_ans_key, '')} {data.get(ch_param_key, 'mg/L')}"
                    divisor = data.get(ch_divi_key, '50')
                    add_formula_with_line(formula_text, result_text, divisor, 40)
                    
                    # CaH Calculation
                    if data.get(ch_th_key) and data.get(ch_df_key):
                        pdf.ln(-2)
                        pdf.set_x(40)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(0, 6, f"{data.get(ch_th_key, '')} X {data.get(ch_df_key, '')} = {data.get(ch_cah1_key, '')} {data.get(ch_th_param_key, 'mg/L')}", align="L", ln=True)
                    pdf.ln(3)
                    # Final Magnesium Calculation
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(40, 6, f"{data.get(mg_head, 'Magnesium')} = ({data.get(mg_th_final_key, '')} - {data.get(mg_cah_final_key, '')}) X {data.get(mg_multiply_key, '0.243')} = {data.get(mg_ans_key, '')} {data.get(mg_param_key, 'mg/L')}", border=False, align="L")
                    
                    # formula_text = f""
                    # result_text = f"{data.get(mg_ans_key, '')} {data.get(mg_param_key, 'mg/L')}"
                    # add_formula_with_line(formula_text, result_text, None, 40)
                    
                    pdf.ln(4)
            
            # Magnesium Average
            if data.get('avg_ans1'):
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('avg_head', 'Average of Magnesium:'), border=False, align="L", ln=True)
                pdf.set_font("Calibri", size=10)
                
                formula_text = f"{data.get('avg_ans1', '')} + {data.get('avg_ans2', '')} + {data.get('avg_ans3', '')}"
                result_text = f"{data.get('avg_final_ans', '')} {data.get('avg_param', 'mg/L')}"
                divisor = data.get('avg_divi', '3')
                add_formula_with_line(formula_text, result_text, divisor, 40)

    for key in sorted(data.keys()):
        
        match = re.match(r'(crm_magnesium_crm_\d+_\d+)_1$', key)
        
        if not match:
            
            continue

        base = match.group(1)
        

        if not data.get(f"{base}_1"):
            continue

        
        # ---------- CRM HEADER ----------
        if data.get(f"{base}_crm_head"):
            check_page_break(20)
            # pdf.set_font("Calibri", 'B', 11)
            # pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

        # ---------- CRM STANDARDS ----------
        pdf.set_font("Calibri", '', 10)

        # for i in range(1, 4):
        #     std = data.get(f"{base}_crm_standard_{i}")
        #     srm = data.get(f"{base}_crm_srm{i}")

        #     if std or srm:
        #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

        # pdf.ln(3)

        # ---------- AVERAGE FORMULA ----------
        add_average_formula_section_crm(
            check_key=f"{base}_1",
            section_title="",
            head_key=f"{base}_head",
            ans_key=f"{base}_ans",
            param_key=f"{base}_param",
            div_key=f"{base}_divi"
        )
        pdf.ln(-4)
            
    # Calcium Calculation Section
    if data.get('for_calcium1_1') or data.get('cal_r1_final') or data.get('ch_r1_final'):
        check_page_break(100)
        pdf.set_font("Calibri", 'B', 11)
        pdf.cell(0, 4, "Calcium Calculation:", 0, 1, 'L')
        pdf.set_font("Calibri", size=10)
        pdf.ln(3)
        
        # Method 1: Direct Calcium Calculation
        if data.get('for_calcium1_1'):
            check_page_break(25)
            
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('calcium_head', 'Calcium: (APHA 3111-B)'), border=False, align="L", ln=True)
            
            pdf.set_x(10)
            pdf.set_font("Calibri", '', 10)
            pdf.cell(30, 6, "Formula = ", border=False, align="L")
            
            # Build formula content
            formula_parts = []
            for i in range(1, 4):
                val = data.get(f'for_calcium1_{i}', '')
                df = data.get(f'for_calcium1_{i}_df', '')
                if val and df:
                    formula_parts.append(f"({val} X {df})")
            
            if formula_parts:
                formula_content = " + ".join(formula_parts)
                result_text = f"{data.get('calcium_ans_1', '')} {data.get('calcium_param_1', 'mg/L')}"
                divisor = data.get('calcium_divi', '3')
                add_formula_with_line(formula_content, result_text, divisor, 25)
        
        # Method 2: ASTM D 1126
        if data.get('cal_r1_final'):
            check_page_break(25)
            
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('calcium_head_1', 'Calcium: (ASTM D 1126)'), border=False, align="L", ln=True)
            
            # Process each reading for Method 2
            calcium_sections_1 = [
                ('cal_r1', 'cal_r1_final', 'cal_r1_initial', 'cal_r1_multiply', 'cal_r1_divi', 'cal_r1_ans', 'cal_r1_param',
                'cal_r1_cah', 'cal_r1_df', 'cal_r1_cah1', 'cal_r1_cah_param'),
                
                ('cal_r2', 'cal_r2_final', 'cal_r2_initial', 'cal_r2_multiply', 'cal_r2_divi', 'cal_r2_ans', 'cal_r2_param',
                'cal_r2_cah', 'cal_r2_df', 'cal_r2_cah1', 'cal_r2_cah_param'),
                
                ('cal_r3', 'cal_r3_final', 'cal_r3_initial', 'cal_r3_multiply', 'cal_r3_divi', 'cal_r3_ans', 'cal_r3_param',
                'cal_r3_cah', 'cal_r3_df', 'cal_r3_cah1', 'cal_r3_cah_param')
            ]
            
            for section in calcium_sections_1:
                (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                cah_key, df_key, cah1_key, cah_param_key) = section
                
                if data.get(final_key):
                    check_page_break(40)
                    
                    # Reading Header
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'), border=False, align="L", ln=True)
                    
                    # Formula Header
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(20, 6, "Formula:", border=False, align="L")
                    pdf.cell(0, 6, "", border=False, align="L", ln=True)
                    
                    # Main formula
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    
                    formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                    result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                    divisor = data.get(divi_key, '50')
                    add_formula_with_line(formula_text, result_text, divisor, 25)
                    
                    # CaH Calculation
                    if data.get(cah_key) and data.get(df_key):
                        pdf.set_x(25)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(0, 6, f"{data.get(cah_key, '')} X {data.get(df_key, '')} = {data.get(cah1_key, '')} {data.get(cah_param_key, 'mg/L')}", align="L", ln=True)
                    
                    pdf.ln(4)
            
            # Calcium Average for Method 2
            if data.get('cal_avg_ans1'):
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('cal_avg_head', 'Average of Calcium:'), border=False, align="L", ln=True)
                pdf.set_font("Calibri", size=10)
                
                formula_text = f"{data.get('cal_avg_ans1', '')} + {data.get('cal_avg_ans2', '')} + {data.get('cal_avg_ans3', '')}"
                result_text = f"{data.get('cal_avg_final_ans', '')} {data.get('cal_avg_param', 'mg/L')}"
                divisor = data.get('cal_avg_divi', '3')
                add_formula_with_line(formula_text, result_text, divisor, 40)
        
        # Method 3: APHA 3500 Ca-B Calculation Method
        if data.get('ch_r1_final'):
            check_page_break(25)
            
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('calcium_head_2', 'Calcium: (APHA 3500 Ca-B) Calculation Method'), border=False, align="L", ln=True)
            
            # Process each reading for Method 3
            calcium_sections_2 = [
                ('ch_r1', 'ch_r1_final', 'ch_r1_initial', 'ch_r1_multiply', 'ch_r1_divi', 'ch_r1_ans', 'ch_r1_param',
                'ch_r1_cah', 'ch_r1_df', 'ch_r1_cah1', 'ch_r1_cah_param',
                'ch_c1_ans1', 'ch_c1_divi', 'ch_c1_multiply', 'ch_c1_ans', 'ch_c1_param'),
                
                ('ch_r2', 'ch_r2_final', 'ch_r2_initial', 'ch_r2_multiply', 'ch_r2_divi', 'ch_r2_ans', 'ch_r2_param',
                'ch_r2_cah', 'ch_r2_df', 'ch_r2_cah1', 'ch_r2_cah_param',
                'ch_c2_ans1', 'ch_c2_divi', 'ch_c2_multiply', 'ch_c2_ans', 'ch_c2_param'),
                
                ('ch_r3', 'ch_r3_final', 'ch_r3_initial', 'ch_r3_multiply', 'ch_r3_divi', 'ch_r3_ans', 'ch_r3_param',
                'ch_r3_cah', 'ch_r3_df', 'ch_r3_cah1', 'ch_r3_cah_param',
                'ch_c3_ans1', 'ch_c3_divi', 'ch_c3_multiply', 'ch_c3_ans', 'ch_c3_param')
            ]
            
            for section in calcium_sections_2:
                (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                cah_key, df_key, cah1_key, cah_param_key,
                cal_ans1_key, cal_divi_key, cal_multiply_key, cal_ans_key, cal_param_key) = section
                
                if data.get(final_key):
                    check_page_break(40)
                    
                    # Reading Header
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'), border=False, align="L", ln=True)
                    
                    # Calcium Hardness
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.ln(4)
                    pdf.cell(40, 6, f"{data.get(f'ch_{reading_key[-1]}', 'Calcium Hardness')} = ", border=False, align="L")
                    
                    formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                    result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                    divisor = data.get(divi_key, '50')
                    add_formula_with_line(formula_text, result_text, divisor, 45)
                    
                    # CaH Calculation
                    if data.get(cah_key) and data.get(df_key):
                        pdf.ln(-3)
                        pdf.set_x(40)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(0, 6, f"{data.get(cah_key, '')} X {data.get(df_key, '')} = {data.get(cah1_key, '')} {data.get(cah_param_key, 'mg/L')}", align="L", ln=True)
                    pdf.ln(3)
                    # Calcium
                    # Calcium
                    pdf.set_x(10)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(40, 6, f"{data.get(f'cal_{reading_key[-1]}', 'Calcium')} = ", border=False, align="L")

                    # Get values
                    answer_value = data.get(cal_ans1_key, 'Answer')
                    divisor_value = data.get(cal_divi_key, '1000')
                    multiply_value = data.get(cal_multiply_key, '400.8')
                    result_value = data.get(cal_ans_key, 'Ca1')
                    param_unit = data.get(cal_param_key, 'mg/L')

                    # Create the fraction with horizontal line
                    pdf.set_x(30)
                    pdf.cell(10, 6, f"{answer_value}", align="C")
                    pdf.ln(-4)  # Move to next line for the fraction line

                    # Draw the horizontal line (vinculum)
                    pdf.set_x(30)  # Adjust X position based on where the fraction should be
                    old_x=pdf.get_x()
                    line_y = pdf.get_y()
                    pdf.line(30, line_y, 40, line_y)  # Adjust coordinates as needed
                    pdf.ln(2)  # Small space after the line

                    # Continue with the rest of the formula
                    pdf.set_x(30)
                    
                    pdf.cell(10, 2, f"{divisor_value}", align="C")
                    pdf.set_y(line_y-5)
                    pdf.set_x(old_x+10)
                    pdf.cell(5, 6, f" × {multiply_value} = {result_value} {param_unit}", align="L", ln=True)

                    pdf.ln(4)
            pdf.ln(4)
            # Calcium Average for Method 3
            if data.get('ch_avg_ans1'):
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('ch_avg_head', 'Average of Calcium:'), border=False, align="L", ln=True)
                pdf.set_font("Calibri", size=10)
                
                formula_text = f"{data.get('ch_avg_ans1', '')} + {data.get('ch_avg_ans2', '')} + {data.get('ch_avg_ans3', '')}"
                result_text = f"{data.get('ch_avg_final_ans', '')} {data.get('ch_avg_param', 'mg/L')}"
                divisor = data.get('ch_avg_divi', '3')
                add_formula_with_line(formula_text, result_text, divisor, 40)
            
            
    
    
    pdf.set_font("Calibri", '', size=10)
    for key in sorted(data.keys()):
        # Match keys like 'alkalinity_crm_36_1_1'
        match = re.match(r'(calcium_crm_\d+_\d+)_1$', key)
        if not match:
            continue

        base = match.group(1)

        # Check if value exists for this base first element
        if not data.get(f"{base}_1"):
            continue

        head = data.get(f"{base}_head")                  # e.g. "Alkalinity:"
        reading = data.get(f"{base}_reading_1")          # if you have reading keys for CRM, else None
        val_1 = data.get(f"{base}_1")                     # e.g. "10.4"
        val_2 = data.get(f"{base}_2")                     # e.g. "0.1"
        val_3 = data.get(f"{base}_3")                     # e.g. "0.02"
        val_4 = data.get(f"{base}_4")                     # e.g. "0.02"
        divisor = data.get(f"{base}_divi") or "1"         # e.g. "100"
        ans = data.get(f"{base}_ans")                      # e.g. "103.000"
        param = data.get(f"{base}_param")                  # e.g. "mg/L"

        # Compose formula string like: "(val_1 + val_2 + val_3) / divisor"
        

        # Call add_formula_block dynamically
        add_formula_block_2(
            head,
            reading,
            f"({val_1} - {val_2}) X {val_3} X 1000",
            f"{val_4}  =  {ans} {param}",
            divisor
        )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={sample_id}.pdf'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())

    return response

@csrf_exempt
def get_dw(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sample_id = data.get('sample_id')
            if not sample_id:
                return JsonResponse({'error': 'sample_id is required'}, status=400)

            sample = Sample_registration.objects.filter(sample_id=sample_id).first()
            dw_report = DrinkingWaterForm.objects.filter(sample_id=sample_id).first()
            
            if not sample or not dw_report:
                return JsonResponse({'error': 'Data not found'}, status=404)

            qc_results = []
            processed_parameters = set()
            
            # STEP 1: Parse extra_field JSON if it exists
            extra_field_data = {}
            if dw_report.extra_field:
                try:
                    extra_field_data = ast.literal_eval(dw_report.extra_field) if dw_report.extra_field else {}
                    # Convert to dictionary for easy lookup: {parameter_name: result}
                    extra_field_dict = {item.get('parameters', '').strip().lower(): item.get('result', 'N/A') 
                                      for item in extra_field_data if item.get('parameters')}
                except:
                    extra_field_dict = {}
            else:
                extra_field_dict = {}

            # STEP 2: Process checked parameters from sample registration
            for checkinp_field, param_data in PARAMETER_MAPPING.items():
                if getattr(sample, checkinp_field, False) is True:
                    parameter_name = param_data["name"]
                    normalized_name = parameter_name.rstrip('*').strip().lower()
                    
                    # Only process if not already added
                    if normalized_name not in processed_parameters:
                        # Check if this parameter maps to a direct database field (water_sr1 to water_sr32)
                        if param_data["field"].startswith('water_sr') and hasattr(dw_report, param_data["field"]):
                            # Get result from direct database field
                            test_result = getattr(dw_report, param_data["field"], "N/A")
                        else:
                            # Get result from extra_field JSON
                            test_result = extra_field_dict.get(normalized_name, "N/A")
                        
                        qc_results.append({
                            'parameter': parameter_name,
                            'test_result': test_result if test_result not in [None, ""] else "N/A",
                            'type': 'standard',
                            'source_field': checkinp_field
                        })
                        processed_parameters.add(normalized_name)

            # STEP 3: Add any remaining parameters from extra_field that weren't in the standard mapping
            for param in extra_field_data:
                parameter_name = param.get('parameters', 'Unknown')
                result_value = param.get('result', 'N/A')
                normalized_name = parameter_name.strip().lower()
                
                if normalized_name not in processed_parameters:
                    qc_results.append({
                        'parameter': parameter_name,
                        'test_result': result_value,
                        'type': 'other', 
                        'source_field': 'extra_field'
                    })
                    processed_parameters.add(normalized_name)

            signatures_data = [{
                'id': sign.id,
                'name': f"{sign.user.username} ({sign.role})"
            } for sign in signs]
            
            return JsonResponse({
                'status': 'success',
                'sample_id': sample_id,
                'qc_data': qc_results,
                'start_date': dw_report.date_of_analysis_from if dw_report.date_of_analysis_from else None,
                'signatures': signatures_data
            })

        except Exception as e:
            logger.error(f"Error processing sample {sample_id}: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)



def dw_rds_list(request):
    dw_list = Dw_rds.objects.all().order_by('-created_at')
    return render(request,'dw_rds_list.html',context={'list':dw_list})



@csrf_exempt
def create_dw_qc_manual(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            
           
            for k in body.keys():
                pass

            sample_id = body.get('sample_id')
            data = body.copy()
            if 'sample_id' in data:
                del data['sample_id']

            report = Dw_rds.objects.create(
                sample_id=sample_id,
                rds=data
            )
            return redirect(f"/qc/generate_dw_qc_pdf_response/{report.id}/")
            # return generate_dw_qc_pdf_response(report, data, sample_id)
            # return JsonResponse({
            #     "status": "success",
            #     "id": report.id,
            #     "sample_id": report.sample_id
            # })
            
            
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    sample_ids = Sample_registration.objects.all()
    dw_ids = DrinkingWaterForm.objects.all()
    sample = serializers.serialize('json',sample_ids,fields=('sample_id',))
    dw = serializers.serialize('json',dw_ids,fields=('sample_id',))
    signs_list = []
    for sign in signs:
        signs_list.append({
            'id': sign.id,
            'name': sign.user.get_full_name() or sign.user.username,
            'user_id': sign.user.id,
            
        })

    user_signs = json.dumps(signs_list)
    context={'sample':sample,'dw':dw,'signs':user_signs}
    return render(request,'rds_dw_manual.html',context)


def dw_testing_results_sample(request):
    if request.method == 'POST':
        sample_id = request.POST.get('sample_id')
        
        if not sample_id:
            return JsonResponse({'error': 'sample_id is required'}, status=400)
        
        try:
            dw_data = Dw_rds.objects.get(sample_id=sample_id)
            
            # Convert model to dictionary
            dw_data_dict = {
                'sample_id': dw_data.sample_id,
                'created_at': dw_data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'rds': dw_data.rds  # This is already a dict if JSONField
            }
            
            return JsonResponse({
                'success': True,
                'dw_data': dw_data_dict,
                'sample_id': sample_id
            })
            
        except Dw_rds.DoesNotExist:
            return JsonResponse({'error': f'Sample ID {sample_id} not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # For GET requests
    all_sample_ids = Dw_rds.objects.values_list('sample_id', flat=True)
    return render(request, 'rds_testing_results_dw.html', {'all_sample_ids': all_sample_ids})




@csrf_exempt
def dw_testing_results_sample_save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        results = {
            'legend': data.get('legend', ''),
            # Store editable header values
            'headers': {
                'crm_head_1': data.get('crm_head_1', 'RM/CRM Certified Value'),
                'crm_head_2': data.get('crm_head_2', 'RM/CRM Acceptance Limit'),
                'crm_head_3': data.get('crm_head_3', 'RM/CRM Test Results')
            }
        }
        # Get all parameter indices dynamically from the data
        row_indices = []
        for key in data.keys():
            if key.startswith('parameter_'):
                # Extract index from parameter_1, parameter_2, etc.
                try:
                    idx = int(key.split('_')[1])
                    row_indices.append(idx)
                except (ValueError, IndexError):
                    continue
        
        row_indices.sort()  # Will give [1,2,3,...,31,33,34,35,36,37,38]
        
        def get_value(name, default="-"):
            v = data.get(name)
            return v if v not in [None, "", "null"] else default
        
        for idx in row_indices:
            # Get CRM result - it could be a string or a list
            crm_value = data.get(f'crm_result_{idx}', '-')
            
            # Handle the case where CRM result is a list (for multiple CRM values per parameter)
            if isinstance(crm_value, list):
                crm_text = ', '.join([str(c) for c in crm_value if c and c != '-'])
                crm_list = crm_value
            else:
                crm_text = str(crm_value) if crm_value and crm_value != '-' else '-'
                crm_list = [crm_text] if crm_text != '-' else []
            
            results[f'row_{idx}'] = {
                "date": get_value(f'date_{idx}'),
                "parameter": get_value(f'parameter_{idx}'),
                "equipment": get_value(f'equipment_{idx}'),
                "method": get_value(f'method_{idx}'),
                "certified": get_value(f'certified_{idx}'),
                "acceptance": get_value(f'acceptance_{idx}'),
                "crm_results": crm_text,  # Store as string for easy PDF rendering
                "crm_list": crm_list,     # Store original list if needed
                "sample_result": get_value(f'sample_result_{idx}'),
                "performed_by": get_value(f'performed_by_{idx}'),
                "reviewed_by": get_value(f'reviewed_by_{idx}'),
                "status": get_value(f'status_{idx}'),
            }
            

        # Get title and sample_id
        sample_id = data.get('sample_id', 'N/A')
        title = data.get('title', 'QC Report')
        
        obj = TestingResultsOfDWSamples.objects.create(
            sample_id=sample_id,
            title=title,
            results=results,
            location=data.get('location','N/A')
        )

        return generate_pdf_for_dw_testing_results(obj)


def generate_pdf_for_dw_testing_results(obj):
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
                pass

        def get_signature_image(self, sign_id):
            """Get signature image path from signature ID"""
            if not sign_id or sign_id == '-' or sign_id == '' or sign_id is None:
                return None
            try:
                sign = Signatures.objects.get(id=int(sign_id))
                if sign.signature and sign.signature.path:
                    return sign.signature.path
                return None
            except (Signatures.DoesNotExist, ValueError, Exception) as e:
                return None

        def draw_signature_in_cell(self, x, y, w, h, signature_id):
            """Draw signature image inside a cell, centered and scaled"""
            signature_path = self.get_signature_image(signature_id)
            if signature_path and os.path.exists(signature_path):
                try:
                    img_w = w - 4
                    img_h = h - 4
                    
                    from PIL import Image as PILImage
                    with PILImage.open(signature_path) as img:
                        img_ratio = img.width / img.height
                        cell_ratio = img_w / img_h
                        
                        if img_ratio > cell_ratio:
                            final_w = img_w
                            final_h = img_w / img_ratio
                        else:
                            final_h = img_h
                            final_w = img_h * img_ratio
                    
                    x_pos = x + (w - final_w) / 2
                    y_pos = y + (h - final_h) / 2
                    
                    self.image(signature_path, x_pos, y_pos, final_w, final_h)
                    return True
                except Exception as e:
                    pass
            return False

        def draw_text_centered(self, x, y, w, h, text, font_size=8, font_style=""):
            """Draw text centered both horizontally and vertically with wrapping"""
            self.set_font("Calibri", font_style, font_size)
            
            # Calculate how many lines are needed
            lines = self.multi_cell(w - 4, 4, str(text), split_only=True)
            num_lines = len(lines) if lines else 1
            text_height = num_lines * 4
            
            # Calculate Y position to center vertically
            y_pos = y + (h - text_height) / 2
            
            # Draw the text centered
            self.set_xy(x + 2, y_pos)
            self.multi_cell(w - 4, 4, str(text), border=0, align='C')
            
            return num_lines

        def header(self):
            self.set_y(0)
            self.set_x(0)
            
            try:
                self.image("static/assets/EnviTechAL LOGO.png", 16, 5, 22, 24)
            except:
                pass
                
            self.set_line_width(0.5)
            self.set_draw_color(26, 84, 26)
            self.line(0, 31, self.w, 31)
            
            self.set_font("Algerian", "", 16)
            self.set_text_color(13, 46, 145)
            self.text(140, 15, txt="ENVI TECH AL")
            
            self.set_font("Calibri", "B", 15)
            self.set_text_color(25, 27, 28)
            self.text(96, 23, txt="Testing Results of Sample (For Quality Control Activities)")
            x = 250
            y = 0
            width = 64
            height = 6
            skew_width = 7
            skew_angle = 50
            color = (12, 168, 74)
            
            # Draw the main rectangle
            self.set_fill_color(*color)
            self.rect(x, y, width, height, 'F',)

            # Draw the sloped side
            self.set_draw_color(12, 168, 74)
            self.polygon([(x - skew_width, y), (x, y), (x, y + height)], 'DF')
        
            self.set_font("Calibri", "B", 10)
            self.set_draw_color(25, 27, 28)
            self.rect(250, 8, 40, 20, "D")
            
            self.location = obj.location.lower() if obj.location else ''
            if self.location == 'lahore':
                self.text(252, 13, txt="ETAL-LAB-704-FF-07")
                self.text(252, 17, txt="Issue Date: 05-01-2023")
                self.text(252, 21, txt="Issue No. 01 Rev. No. 00")
            elif self.location == 'karachi':
                self.text(252, 13, txt="ETAL-LAB-704-FF-07")
                self.text(252, 17, txt="Issue Date: 01-08-2022")
                self.text(252, 21, txt="Issue No. 01 Rev. No. 00")
            else:
                self.text(252, 13, txt="ETAL-LAB-704-FF-05")
                self.text(252, 17, txt="Issue Date: 22-12-2025")
                self.text(252, 21, txt="Issue No. 02 Rev. No. 01")
            
            self.set_text_color(0, 0, 0)
            self.alias_nb_pages()
            
            self.set_font("Calibri", "B", 10)
            self.text(252, 25.5, txt="Page No:")
            self.cell(self.w - 17, 48, f'{self.page_no()} of {{nb}}', border=False, align='R')
            
            self.set_text_color(10, 10, 10)
            self.set_font("Calibri", "", 9)
        
        def draw_table_header(self):
            """Draw the table header using multi_cell for centering"""
            col_widths = [10, 27, 33, 25, 25, 25, 25, 25, 25, 19, 19, 20]
            headers_dict = obj.results.get('headers', {})
            crm_head_1 = headers_dict.get('crm_head_1', 'RM/CRM Certified Value')
            crm_head_2 = headers_dict.get('crm_head_2', 'RM/CRM Acceptance Limit')
            crm_head_3 = headers_dict.get('crm_head_3', 'RM/CRM Test Results')
            headers = [
                "S.no", "Date", "Parameter", "Equipment ID", "Test Method",
                crm_head_1, crm_head_2, crm_head_3,
                "Sample Results", "Performed By Initials", "Reviewed By Initials", "Conformance Status (By Reviewer)"
            ]
            
            self.col_widths = col_widths
            
            start_x = self.get_x()
            start_y = self.get_y()
            
            self.set_fill_color(220, 220, 220)
            self.set_font("Calibri", "B", 7)
            
            # Calculate header height based on content
            max_header_lines = 1
            header_line_counts = []
            
            for width, header in zip(col_widths, headers):
                lines = self.multi_cell(width - 2, 4, header, split_only=True)
                num_lines = len(lines) if lines else 1
                header_line_counts.append(num_lines)
                if num_lines > max_header_lines:
                    max_header_lines = num_lines
            
            header_height = max_header_lines * 5
            
            # Draw all cells with borders and fill
            current_x = start_x
            for width in col_widths:
                self.set_xy(current_x, start_y)
                self.cell(width, header_height, "", border=1, align='C', fill=True)
                current_x += width
            
            # Write header text centered using multi_cell
            current_x = start_x
            for i, (width, header) in enumerate(zip(col_widths, headers)):
                self.set_xy(current_x, start_y)
                self.set_font("Calibri", "B", 7)
                
                num_lines = header_line_counts[i]
                text_height = num_lines * 4
                y_pos = start_y + (header_height - text_height) / 2
                
                self.set_xy(current_x + 1, y_pos)
                self.multi_cell(width - 2, 4, header, border=0, align='C')
                
                current_x += width
            
            self.set_y(start_y + header_height)
            self.set_x(start_x)
        
        def check_page_break(self, row_height):
            if self.get_y() + row_height > self.h - 20:
                self.add_page()
                self.set_y(36)
                self.draw_table_header()
                return True
            return False
        
        def footer(self):
            color = (12, 168, 74)
            self.set_text_color(10, 10, 10)
            self.set_font("Calibri","", 9)
               
            self.set_y(-10)
            self.set_x(0)

            self.image('static/assets/phone.PNG',10,self.h-17,7,7)
            self.image('static/assets/office.PNG',50,self.h-18,9,9)
            self.set_font("Calibri","", 10)
            if self.location == 'karachi':
                self.text(18,self.h-13,txt="+92 310 2288801")
                self.text(60,self.h-15,txt="Head Office:345,First Floor, Street-15,Block-3")
                self.text(60,self.h-11,txt="Bahadurabad, Karachi, 75900, Pakistan")
                     
            elif self.location == 'lahore':
                self.text(18,self.h-13,txt="+92 42 32296099")
                self.text(60,self.h-15,txt="Lahore Office: 87-E Madina Height, Office # A/30 & ")
                self.text(60,self.h-11,txt=" A/31 8th Floor,Johar Town, Lahore")
            
            self.image('static/assets/polyPNG-removebg-preview.png',202,185,90,22)

            self.set_draw_color(12, 168, 74)
            self.set_fill_color(*color)
            self.ln(1.7)
            self.set_x(0)
            self.set_text_color(255,255,255)
            self.cell(300,8,"Head Office: First Floor, Street-15,Block-3 Bahadurabad, Karachi, 75900, Pakistan",align="C",fill=True)
            self.set_text_color(0,0,0)

    def parse_date(date_str):
        """Parse date string to datetime object for sorting"""
        if not date_str or date_str == '-':
            return None
        try:
            # Try to parse date in format like "13-February-2026"
            from datetime import datetime
            return datetime.strptime(date_str, "%d-%B-%Y")
        except:
            try:
                # Try alternative format
                return datetime.strptime(date_str, "%d-%b-%Y")
            except:
                return None

    pdf = CustomPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("Calibri", "B", 10)
    pdf.ln(4)
    pdf.cell(160, 6, f"Sample ID : {obj.sample_id}")
    pdf.cell(100, 6, f"Title : {obj.title}", ln=True, align="R")
    pdf.draw_table_header()

    pdf.set_font("Calibri", "", 8)
    serial = 1

    # Get all rows
    rows = [(k, v) for k, v in obj.results.items() if k.startswith("row_")]
    
    # Sort by date (parse date string to datetime for comparison)
    rows_with_dates = []
    for row_key, row in rows:
        date_str = row.get("date", "")
        date_obj = parse_date(date_str)
        rows_with_dates.append((row_key, row, date_obj, date_str))
    
    # Sort by date (None values go to the end)
    rows_with_dates.sort(key=lambda x: (x[2] is None, x[2]))
    
    # Process sorted rows
    for row_key, row, date_obj, date_str in rows_with_dates:
        
        # Get CRM result
        crm_text = str(row.get("crm_results", "-"))
        if crm_text == "-" or not crm_text:
            crm_text = "-"
        
        # Get signature IDs
        performed_id = row.get("performed_by", "-")
        reviewed_id = row.get("reviewed_by", "-")
        
        row_data = [
            str(serial),
            date_str,  # Use the original date string
            row.get("parameter", "-"),
            row.get("equipment", "-"),
            row.get("method", "-"),
            row.get("certified", "-"),
            row.get("acceptance", "-"),
            crm_text,
            row.get("sample_result", "-"),
            performed_id,
            reviewed_id,
            row.get("status", "-")
        ]
        
        signature_col_indices = [9, 10]  # Indices for Performed and Reviewed columns
        
        # Calculate row height
        line_counts = []
        for i, text in enumerate(row_data):
            if i in signature_col_indices and text != '-' and text != '':
                line_counts.append(3)  # Signature needs 3 lines height
            else:
                lines = pdf.multi_cell(pdf.col_widths[i] - 4, 4, str(text), split_only=True)
                line_counts.append(len(lines) if lines else 1)
        
        max_lines = max(line_counts) if line_counts else 1
        row_height = max(max_lines * 4, 15)  # Minimum 15mm for signatures
        
        pdf.check_page_break(row_height)
        
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # Draw each cell
        for i, text in enumerate(row_data):
            x_current = pdf.get_x()
            y_current = pdf.get_y()
            
            # Draw border
            pdf.rect(x_current, y_current, pdf.col_widths[i], row_height)
            
            if i in signature_col_indices and text != '-' and text != '':
                # Draw signature image centered
                pdf.draw_signature_in_cell(x_current, y_current, pdf.col_widths[i], row_height, text)
            else:
                # Draw text centered using draw_text_centered method
                pdf.draw_text_centered(x_current, y_current, pdf.col_widths[i], row_height, text)
            
            # Move cursor to the right of the cell
            pdf.set_xy(x_current + pdf.col_widths[i], y_current)
        
        pdf.set_xy(x_start, y_start + row_height)
        serial += 1

    pdf.ln(2)
    if obj.results.get('legend'):
        pdf.cell(0, 6, obj.results.get('legend', ''))

    

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={obj.id}.pdf'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())

    return response


def dw_testing_results_sample_list(request):
    data = TestingResultsOfDWSamples.objects.all().order_by('-created_at')
    return render(request, 'dw_testing_results_sample_list.html', {'list': data})
    
def dw_testing_results_sample_pdf_from_list(request, pk=None):
    if pk:  # PDF generation for specific ID
        obj = get_object_or_404(TestingResultsOfDWSamples, id=pk)
        return generate_pdf_for_dw_testing_results(obj)
    else:  # List view
        data = TestingResultsOfDWSamples.objects.all().order_by('-created_at')
        return render(request, 'dw_testing_results_sample_list.html', {'list': data})

__all__ = [
    'create_dw_qc',
    'generate_dw_qc_pdf_response',
    'get_dw',
    'dw_rds_list',
    'create_dw_qc_manual',
    'dw_testing_results_sample',
    'dw_testing_results_sample_save',
    'generate_pdf_for_dw_testing_results',
    'dw_testing_results_sample_list',
    'dw_testing_results_sample_pdf_from_list',
]
