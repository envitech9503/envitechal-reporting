# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403

    
        
@csrf_exempt
def create_ww_qc(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            
           
            for k in body.keys():
                pass

            sample_id = body.get('sample_id')
            data = body.copy()
            if 'sample_id' in data:
                del data['sample_id']

            report = Ww_rds.objects.create(
                sample_id=sample_id,
                rds=data
            )
            return redirect(f"/qc/generate_ww_qc_pdf_response/{report.id}/")
            # return generate_dw_qc_pdf_response(report, data, sample_id)
            # return JsonResponse({
            #     "status": "success",
            #     "id": report.id,
            #     "sample_id": report.sample_id
            # })
            
            
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    sample_ids = Sample_registration.objects.all()
    ww_ids = WasteWaterForm2.objects.all()
    sample = serializers.serialize('json',sample_ids,fields=('sample_id',))
    ww = serializers.serialize('json',ww_ids,fields=('sample_id',))
    context={'sample':sample,'ww':ww,'signs':signs}
    return render(request,"rds_ww.html",context)


# WASTEWATER_PARAMETER_MAPPING = {
#     # Standard parameters mapping - adjust field names based on your actual model
#     "checkinp103": {"name": "pH*", "field": "waste_water_sr1"},
#     "checkinp104": {"name": "Color", "field": "waste_water_sr2"},
#     "checkinp105": {"name": "Odor", "field": "waste_water_sr3"},
#     "checkinp106": {"name": "TSS*", "field": "waste_water_sr4"},
#     "checkinp107": {"name": "TDS*", "field": "waste_water_sr5"},
#     "checkinp108": {"name": "BOD*", "field": "waste_water_sr6"},
#     "checkinp109": {"name": "COD*", "field": "waste_water_sr7"},
#     "checkinp110": {"name": "Oil & Grease", "field": "waste_water_sr8"},
#     "checkinp111": {"name": "Total Nitrogen*", "field": "waste_water_sr9"},
#     "checkinp112": {"name": "Ammonical Nitrogen*", "field": "waste_water_sr10"},
#     "checkinp113": {"name": "TKN", "field": "waste_water_sr11"},
#     "checkinp114": {"name": "Phosphate", "field": "waste_water_sr12"},
#     "checkinp115": {"name": "Sulphate", "field": "waste_water_sr13"},
#     "checkinp116": {"name": "Sulphide", "field": "waste_water_sr14"},
#     "checkinp117": {"name": "Fluoride", "field": "waste_water_sr15"},
#     "checkinp118": {"name": "Chloride*", "field": "waste_water_sr16"},
#     "checkinp119": {"name": "Cyanide", "field": "waste_water_sr17"},
#     "checkinp120": {"name": "Phenol", "field": "waste_water_sr18"},
#     "checkinp121": {"name": "Anionic Detergents (MBAS)", "field": "waste_water_sr19"},
#     "checkinp122": {"name": "Arsenic", "field": "waste_water_sr20"},
#     "checkinp123": {"name": "Mercury", "field": "waste_water_sr21"},
#     "checkinp124": {"name": "Cadmium", "field": "waste_water_sr22"},
#     "checkinp125": {"name": "Lead", "field": "waste_water_sr23"},
#     "checkinp126": {"name": "Zinc", "field": "waste_water_sr24"},
#     "checkinp127": {"name": "Chromium (Total)", "field": "waste_water_sr25"},
#     "checkinp128": {"name": "Copper", "field": "waste_water_sr26"},
#     "checkinp129": {"name": "Nickel", "field": "waste_water_sr27"},
#     "checkinp130": {"name": "Iron", "field": "waste_water_sr28"},
#     "checkinp131": {"name": "Manganese", "field": "waste_water_sr29"},
#     "checkinp132": {"name": "Selenium", "field": "waste_water_sr30"},
#     "checkinp133": {"name": "Aluminium", "field": "waste_water_sr31"},
#     "checkinp134": {"name": "Boron", "field": "waste_water_sr32"},
#     "checkinp135": {"name": "Total Coliform", "field": "waste_water_sr33"},
#     "checkinp136": {"name": "Faecal Coliform", "field": "waste_water_sr34"},
#     "checkinp137": {"name": "E.coli", "field": "waste_water_sr35"},
#     "checkinp142": {"name": "Silver", "field": "waste_water_sr36"},
#     "checkinp143": {"name": "Barium", "field": "waste_water_sr37"},
#     "checkinp144": {"name": "Antimony", "field": "waste_water_sr38"},
# }



@csrf_exempt
def get_ww(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sample_id = data.get('sample_id')
            
            if not sample_id:
                return JsonResponse({'error': 'sample_id is required'}, status=400)

            ww_report = WasteWaterForm2.objects.filter(sample_id=sample_id).first()
            
            if not ww_report:
                return JsonResponse({'error': 'Report not found for this sample'}, status=404)

            report_type = ww_report.in_out or 'in-out'
            qc_data = []  # Changed from qc_results to qc_data
            
            # STEP 1: Try to get data from structured_data field FIRST
            structured_data = {}
            if ww_report.structured_data and ww_report.structured_data != '[]':
                try:
                    structured_data = json.loads(ww_report.structured_data)
                except:
                    try:
                        structured_data = ast.literal_eval(ww_report.structured_data)
                    except:
                        structured_data = {}
            
            if isinstance(structured_data, dict) and 'standard_parameters' in structured_data:
                
                # Process standard parameters from structured_data
                for param in structured_data.get('standard_parameters', []):
                    sr_no = param.get('sr_no', 0)
                    parameter = param.get('parameter', f'Parameter {sr_no}')
                    
                    # Create data object matching frontend expectations
                    # Note: We're mapping your backend field names to frontend expected field names
                    data_obj = {
                        'sr_no': sr_no,
                        'parameter': parameter,
                        'reporting_data': ww_report.reporting_date or '',  # This will be used as 'date' field
                        'date': ww_report.reporting_date or '',  # Add this for consistency with frontend
                    }
                    
                    if report_type == 'in':
                        result = param.get('inlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            qc_data.append(data_obj)
                    
                    elif report_type == 'out':
                        result = param.get('outlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            qc_data.append(data_obj)
                    
                    elif report_type == 'in-out':
                        inlet_val = param.get('inlet_result', 'N/A')
                        outlet_val = param.get('outlet_result', 'N/A')
                        data_obj['inlet_result'] = str(inlet_val)
                        data_obj['outlet_result'] = str(outlet_val)
                        qc_data.append(data_obj)
                    
                    elif report_type == 'inlet_customlimits':
                        result = param.get('inlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            data_obj['custom_limit'] = str(param.get('custom_limit', 'N/A'))
                            qc_data.append(data_obj)
                    
                    elif report_type == 'outlet_customLimits':
                        result = param.get('outlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            data_obj['custom_limit'] = str(param.get('custom_limit', 'N/A'))
                            qc_data.append(data_obj)
                
                # Process extra parameters from structured_data
                for extra_param in structured_data.get('extra_parameters', []):
                    sr_no = extra_param.get('sr_no', len(qc_data) + 1)
                    parameter = extra_param.get('parameter', f'Extra Parameter {sr_no}')
                    
                    data_obj = {
                        'sr_no': sr_no,
                        'parameter': parameter,
                        'reporting_data': ww_report.reporting_date or '',
                        'date': ww_report.reporting_date or '',  # Add this for consistency
                    }
                    
                    if report_type == 'in':
                        result = extra_param.get('inlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            qc_data.append(data_obj)
                    
                    elif report_type == 'out':
                        result = extra_param.get('outlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            qc_data.append(data_obj)
                    
                    elif report_type == 'in-out':
                        inlet_val = extra_param.get('inlet_result', 'N/A')
                        outlet_val = extra_param.get('outlet_result', 'N/A')
                        data_obj['inlet_result'] = str(inlet_val)
                        data_obj['outlet_result'] = str(outlet_val)
                        qc_data.append(data_obj)
                    
                    elif report_type == 'inlet_customlimits':
                        result = extra_param.get('inlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            data_obj['custom_limit'] = str(extra_param.get('custom_limit', 'N/A'))
                            qc_data.append(data_obj)
                    
                    elif report_type == 'outlet_customLimits':
                        result = extra_param.get('outlet_result')
                        if result and str(result).strip() and str(result).lower() != 'n/a':
                            data_obj['test_result'] = str(result)
                            data_obj['custom_limit'] = str(extra_param.get('custom_limit', 'N/A'))
                            qc_data.append(data_obj)
            
            else:
                # STEP 2: Fallback to extra_field if structured_data is not available
                extra_field_data = []
                if ww_report.extra_field and ww_report.extra_field != '[]':
                    try:
                        extra_field_data = json.loads(ww_report.extra_field)
                    except:
                        try:
                            extra_field_data = ast.literal_eval(ww_report.extra_field)
                        except:
                            extra_field_data = []
                
                if isinstance(extra_field_data, list):
                    # Process standard parameters (1-32) with default names
                    default_names = [
                        "Temperature 40 °C", "pH*", "Sulphide", "Biological Oxygen Demand(BOD)5",
                        "Chemical Oxygen Demand(COD)", "Total Dissolved Solids (TDS)", 
                        "Total Suspended Solids (TSS)", "Oil & Grease", "Cadmium", "Copper",
                        "Iron", "Lead", "Manganese", "Mercury", "Nickel", "Selenium",
                        "Chromium", "Zinc", "Arsenic", "Chlorine", "Chloride", "Cyanide",
                        "Fluoride", "Ammonia", "Total Toxic Metals", "Sulphate",
                        "An Ionic Detergent As MBAs", "Pesticides", "Phenolic Compounds(as Phenol)",
                        "Boron", "Barium", "Silver"
                    ]
                    
                    # First, get standard parameters from database fields
                    for i in range(1, 33):
                        param_name = default_names[i-1] if i-1 < len(default_names) else f"Parameter {i}"
                        inlet_val = getattr(ww_report, f'result_{i}', '')
                        outlet_val = getattr(ww_report, f'result_{i}_{i}', '')
                        
                        data_obj = {
                            'sr_no': i,
                            'parameter': param_name,
                            'reporting_data': ww_report.reporting_date or '',
                            'date': ww_report.reporting_date or '',  # Add this for consistency
                        }
                        
                        if report_type == 'in' and inlet_val and str(inlet_val).strip() and str(inlet_val).lower() != 'n/a':
                            data_obj['test_result'] = str(inlet_val)
                            qc_data.append(data_obj)
                        
                        elif report_type == 'out' and outlet_val and str(outlet_val).strip() and str(outlet_val).lower() != 'n/a':
                            data_obj['test_result'] = str(outlet_val)
                            qc_data.append(data_obj)
                        
                        elif report_type == 'in-out':
                            data_obj['inlet_result'] = str(inlet_val) if inlet_val and str(inlet_val).strip() else 'N/A'
                            data_obj['outlet_result'] = str(outlet_val) if outlet_val and str(outlet_val).strip() else 'N/A'
                            qc_data.append(data_obj)
                    
                    # Then, process extra parameters from extra_field
                    sr_counter = 33
                    for item in extra_field_data:
                        if isinstance(item, dict):
                            parameter = item.get('parameters', f'Extra Parameter {sr_counter}')
                            
                            data_obj = {
                                'sr_no': sr_counter,
                                'parameter': parameter,
                                'reporting_data': ww_report.reporting_date or '',
                                'date': ww_report.reporting_date or '',  # Add this for consistency
                            }
                            
                            if report_type == 'in':
                                result = item.get('result')
                                if result and str(result).strip() and str(result).lower() != 'n/a':
                                    data_obj['test_result'] = str(result)
                                    qc_data.append(data_obj)
                                    sr_counter += 1
                            
                            elif report_type == 'out':
                                result = item.get('outlet')
                                if result and str(result).strip() and str(result).lower() != 'n/a':
                                    data_obj['test_result'] = str(result)
                                    qc_data.append(data_obj)
                                    sr_counter += 1
                            
                            elif report_type == 'in-out':
                                data_obj['inlet_result'] = str(item.get('result', 'N/A'))
                                data_obj['outlet_result'] = str(item.get('outlet', 'N/A'))
                                qc_data.append(data_obj)
                                sr_counter += 1
            
            # Sort by sr_no
            qc_data.sort(key=lambda x: x['sr_no'])
            
            # Get signatures
            signatures_data = []
            signatures = []
            
            if ww_report.analyst_signature:
                signatures.append(ww_report.analyst_signature)
            if ww_report.assistant_manager_signature:
                signatures.append(ww_report.assistant_manager_signature)
            if ww_report.lab_manager_signature:
                signatures.append(ww_report.lab_manager_signature)
            
            for sign in signatures:
                signatures_data.append({
                    'id': sign.id if hasattr(sign, 'id') else 0,
                    'name': f"{sign.user.username if hasattr(sign, 'user') else 'Unknown'} ({getattr(sign, 'role', 'Unknown')})"
                })
            
            # Add report information
            report_info = {
                'lab_report_no': ww_report.lab_report_no,
                'sample_id': ww_report.sample_id,
                'sample_collection_date': ww_report.sample_Col_date,
                'date_of_analysis_from': ww_report.date_of_analysis_from,
                'date_of_analysis_to': ww_report.date_of_analysis_to,
                'report_type': report_type
            }
            return JsonResponse({
                'status': 'success',
                'sample_id': sample_id,
                'report_type': report_type,
                'report_info': report_info,
                'qc_data': qc_data,  # Changed from qc_results to qc_data
                'signatures': signatures_data,  # Added signatures
                'start_date': ww_report.date_of_analysis_from,
                'total_parameters': len(qc_data),
                'data_source': 'structured_data' if 'standard_parameters' in structured_data else 'extra_field'
            })

        except Exception as e:
            import traceback
            return JsonResponse({'error': str(e)}, status=500)
        
        
        
def generate_ww_qc_pdf_response(report, pk):
    """Generate PDF for DW QC report with proper page breaks"""

    pdf = CustomPDF()
    pdf.add_page()

    report = Ww_rds.objects.get(id=pk)
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

    
    if data.get('report_type') == 'in-out':
    
        # Column widths with Parameter at 55mm
        col_widths = [10, 25, 55, 18, 18, 20, 20, 18]  # Total: 184mm

        def add_table_header():
            pdf.set_font("Calibri", 'B', 9)
            pdf.set_x(13)  # Start position (centered)
            headers = ["S.no", "Date", "Parameter", "Inlet", "Outlet", "Performed By", "Checked By", "Remarks"]
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
            pdf.set_x(13)
            pdf.cell(sum(col_widths), row_height, "No data available", 1, 1, 'C')
            return pdf

        # 🔢 Sequential S.no
        s_no = 1

        for row_key in sorted_rows:
            check_page_break(row_height)

            pdf.set_x(13)
            pdf.cell(col_widths[0], row_height, str(s_no), 1, 0, 'C')

            pdf.cell(
                col_widths[1],
                row_height,
                str(data.get(f'date_{row_key}', '')),
                1, 0, 'C'
            )

            parameter = str(data.get(f'parameter_{row_key}', ''))
            if parameter:
                # Check if this is a CRM parameter (contains "CRM")
                is_crm = "CRM" in parameter.upper()
                
                pdf.cell(
                    col_widths[2],
                    row_height,
                    parameter,
                    1, 0, 'L'
                )
                
                if is_crm:
                    # For CRM: colspan=2 for inlet column, leave outlet empty
                    inlet_value = str(data.get(f'inlet_{row_key}', ''))
                    # Draw a single cell spanning both inlet and outlet columns
                    pdf.cell(
                        col_widths[3] + col_widths[4],  # Combined width of inlet + outlet
                        row_height,
                        inlet_value if inlet_value.strip() != '' else '---',
                        1, 0, 'C'
                    )
                else:
                    # For non-CRM: separate inlet and outlet cells
                    inlet_value = str(data.get(f'inlet_{row_key}', ''))
                    pdf.cell(
                        col_widths[3],
                        row_height,
                        inlet_value if inlet_value.strip() != '' else '---',
                        1, 0, 'C'
                    )
                    
                    outlet_value = str(data.get(f'outlet_{row_key}', ''))
                    pdf.cell(
                        col_widths[4],
                        row_height,
                        outlet_value if outlet_value.strip() != '' else '---',
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
                        pdf.cell(col_widths[5], row_height, '', 1, 0, 'C')
                        if sign.signature:
                            pdf.image(sign.signature.path, x + 1, y + 1,
                                    w=col_widths[5] - 2, h=row_height - 2)
                    except:
                        pdf.cell(col_widths[5], row_height, 'N/A', 1, 0, 'C')
                else:
                    pdf.cell(col_widths[5], row_height, '', 1, 0, 'C')

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
                        pdf.cell(col_widths[6], row_height, '', 1, 0, 'C')
                        if sign.signature:
                            pdf.image(sign.signature.path, x + 1, y + 1,
                                    w=col_widths[6] - 2, h=row_height - 2)
                    except:
                        pdf.cell(col_widths[6], row_height, 'N/A', 1, 0, 'C')
                else:
                    pdf.cell(col_widths[6], row_height, '', 1, 0, 'C')

                pdf.cell(
                    col_widths[7],
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
                pdf.cell(0, 8, f"{section_title}", 0, 1, 'L')
                
                if data.get(head_key):
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data[head_key], ln=True)
                
                pdf.cell(0, 6, "Formula:", ln=True)
                pdf.set_font("Calibri", '', 10)
                
                # Build formula content
                formula_parts = []
                
                
                # Extract parameter name from check_key
                param_name = 'arsenic'
                if 'arsenic' in check_key.lower():
                    param_name = 'arsenic'
                elif 'beryllium' in check_key.lower():
                    param_name = 'beryllium'
                elif 'ammonium' in check_key.lower():
                    param_name = 'ammonium'
                else:
                    # Extract from section_title
                    param_name = section_title.lower().split()[0]
                
                # Determine if this is inlet or outlet
                is_inlet = '_inlet' in check_key.lower() or 'inlet' in section_title.lower()
                is_outlet = '_outlet' in check_key.lower() or 'outlet' in section_title.lower()
                
                for i in range(1, 4):
                    # Try ALL possible patterns
                    possible_patterns = []
                    
                    # Pattern that should work based on debug output: for_arsenic1 + for_arsenic1_df_outlet
                    if is_outlet:
                        possible_patterns.append((
                            f"for_{param_name}{i}",
                            f"for_{param_name}{i}_df_outlet",
                            "Pattern 1 (outlet)"
                        ))
                    elif is_inlet:
                        possible_patterns.append((
                            f"for_{param_name}{i}",
                            f"for_{param_name}{i}_df_inlet",
                            "Pattern 1 (inlet)"
                        ))
                    
                    # Pattern 2: Alternative with just number
                    possible_patterns.append((
                        f"for_{param_name}{i}",
                        f"for_{param_name}{i}_df",
                        "Pattern 2 (simple)"
                    ))
                    
                    # Pattern 3: With inlet/outlet in value key
                    if is_outlet:
                        possible_patterns.append((
                            f"for_{param_name}{i}_outlet",
                            f"for_{param_name}{i}_df_outlet",
                            "Pattern 3 (outlet full)"
                        ))
                    elif is_inlet:
                        possible_patterns.append((
                            f"for_{param_name}{i}_inlet",
                            f"for_{param_name}{i}_df_inlet",
                            "Pattern 3 (inlet full)"
                        ))
                    
                    # Pattern 4: Check the actual keys from your debug output
                    # From your data: for_arsenic1_outlet exists, for_arsenic1_df_outlet exists
                    possible_patterns.append((
                        f"for_{param_name}{i}_outlet" if is_outlet else f"for_{param_name}{i}_inlet",
                        f"for_{param_name}{i}_df_outlet" if is_outlet else f"for_{param_name}{i}_df_inlet",
                        "Pattern 4 (exact match)"
                    ))
                    
                    # Try all patterns
                    found_val = None
                    found_df = None
                    found_pattern = None
                    
                    for val_pattern, df_pattern, pattern_name in possible_patterns:
                        val_exists = val_pattern in data and data[val_pattern] not in ['', None]
                        df_exists = df_pattern in data and data[df_pattern] not in ['', None]
                        
                        if val_exists and df_exists:
                            found_val = data[val_pattern]
                            found_df = data[df_pattern]
                            found_pattern = pattern_name
                            break
                        elif val_pattern in data and df_pattern in data:
                            # Even if empty, let's see what's there
                            pass
                    
                    if found_val is not None and found_df is not None:
                        formula_parts.append(f"({found_val} X {found_df})")
                    else:
                        # Try to manually find matching keys
                        for key in data.keys():
                            if f"for_{param_name}{i}" in key and not key.endswith('_df'):
                                # Look for matching df key
                                for df_key in data.keys():
                                    if f"for_{param_name}{i}" in df_key and '_df' in df_key:
                                        if data[key] and data[df_key]:
                                            found_val = data[key]
                                            found_df = data[df_key]
                                            formula_parts.append(f"({found_val} X {found_df})")
                                            break
                                if found_val:
                                    break
                
                if formula_parts:
                    formula_content = " + ".join(formula_parts)
                    result_text = f"{data.get(ans_key, '')} {data.get(param_key, '')}"
                    divisor = data.get(div_key) if div_key else None
                    add_formula_with_line(formula_content, result_text, divisor, start_x)
                else:
                    # Show all keys that might be relevant
                    search_terms = [param_name, 'inlet' if is_inlet else 'outlet' if is_outlet else '']
                    for key in sorted(data.keys()):
                        if any(term in key.lower() for term in search_terms if term):
                            pass

       
        
       
       
       
        def add_average_formula_section(check_key, section_title, head_key, ans_key, param_key,
                                div_key=None, start_x=30):

            if not data.get(check_key):
                return

            # detect inlet / outlet
            io = "inlet" if check_key.endswith("_inlet") else "outlet"

            # extract parameter name (cyanide, ammonia, bod, etc.)
            # from: for_cyanide1_inlet → cyanide
            param = check_key.replace("for_", "").replace("1_" + io, "")

            check_page_break(30)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, section_title, ln=True)

            # ================= SIMPLE AVERAGE =================
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get(f"{head_key}_1"), ln=True)
            # pdf.cell(0, 6, "Formula:", ln=True)

            pdf.set_font("Calibri", '', 10)
            old_y = pdf.get_y()

            values = []
            for i in range(1, 4):
                key = f"for_{param}{i}_{io}"
                if data.get(key) is not None:
                    values.append(str(data[key]))

            if values:
                formula = " + ".join(values)
                width = pdf.get_string_width(formula)

                pdf.set_x(start_x)
                pdf.cell(
                    width, 6,
                    f"{formula} = {data.get(ans_key + '_simple')} {data.get(param_key + '_simple')}",
                    ln=True
                )

                pdf.line(start_x, old_y + 5.5, start_x + width, old_y + 5.5)

                pdf.set_x(start_x + width / 2 - 2)
                pdf.cell(4, 6, "3", align="C", ln=True)

            pdf.ln(3)

            # ================= WEIGHTED AVERAGE =================
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get(f"{head_key}_2"), ln=True)
            # pdf.cell(0, 6, "Formula:", ln=True)

            pdf.set_font("Calibri", '', 10)
            old_y = pdf.get_y()

            parts = []
            for i in range(1, 4):
                val_key = f"for_{param}1_{i}_{io}"
                df_key  = f"for_{param}1_{i}_df_{io}"

                if data.get(val_key) is not None and data.get(df_key) is not None:
                    parts.append(f"({data[val_key]} X {data[df_key]})")

            if parts:
                formula = " + ".join(parts)
                width = pdf.get_string_width(formula)

                pdf.set_x(start_x)
                pdf.cell(
                    width, 6,
                    f"{formula} = {data.get(ans_key + '_weighted')} {data.get(param_key + '_weighted')}",
                    ln=True
                )

                pdf.line(start_x, old_y + 5.5, start_x + width, old_y + 5.5)

                divisor = str(data.get(div_key)) if data.get(div_key) else ""
                pdf.set_x(start_x + width / 2 - pdf.get_string_width(divisor) / 2)
                pdf.cell(pdf.get_string_width(divisor), 6, divisor, align="C")


                pdf.ln(4)
                
                
        def add_average_formula_section_2(check_key, section_title, head_key, ans_key, param_key,
                                div_key=None, start_x=30):
            
            if not data.get(check_key):
                return
            
            # detect inlet / outlet
            io = "inlet" if check_key.endswith("_inlet") else "outlet"
            
            # extract parameter name (ammonia, ionic_det, freechlorine, etc.)
            # from: for_ammonia1_inlet → ammonia
            # Remove "for_" prefix, then remove "1_inlet" or "1_outlet" suffix
            param_base = check_key.replace("for_", "").replace(f"1_{io}", "")
            
            check_page_break(30)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, section_title, ln=True)
            
            # ================= SIMPLE AVERAGE =================
            # Note: Your data shows head_key is like "ammonia_head_inlet"
            # and the second header is "ammonia_head_1_inlet" (with _1)
            simple_head_key = head_key.replace("_1","")  # e.g., "ammonia_head_inlet"
            pdf.set_font("Calibri", 'B', 10)
            
            # Try to get the header for simple average
            # Your data shows it's actually "ammonia_head_inlet" (not "_1")
            simple_header = data.get(simple_head_key)
            if simple_header:
                pdf.cell(0, 6, simple_header, ln=True)
            
            pdf.set_font("Calibri", '', 10)
            old_y = pdf.get_y()
            
            # Get the 3 values for simple average
            # Your data has keys: for_ammonia1_inlet, for_ammonia2_inlet, for_ammonia3_inlet
            values = []
            for i in range(1, 4):
                key = f"for_{param_base}{i}_{io}"
                if data.get(key) is not None:
                    values.append(str(data[key]))
            
            if values:
                formula = " + ".join(values)
                width = pdf.get_string_width(formula)
                
                pdf.set_x(start_x)
                
                # Your data has answer key like "ammonia_ans_inlet" for simple average
                simple_answer = data.get(f"{ans_key}")
                simple_param = data.get(f"{param_key}")
                
                pdf.cell(
                    width, 6,
                    f"{formula} = {simple_answer} {simple_param}",
                    ln=True
                )
                
                pdf.line(start_x, old_y + 5.5, start_x + width, old_y + 5.5)
                
                # Simple average always divided by 3
                pdf.set_x(start_x + width / 2 - 2)
                pdf.cell(4, 6, "3", align="C", ln=True)
            
            pdf.ln(3)
            
            # ================= WEIGHTED AVERAGE =================
            # For weighted average header, your data shows it's "ammonia_head_1_inlet"
            weighted_head_key = f"{head_key}"  # e.g., "ammonia_head_1_inlet"
            pdf.set_font("Calibri", 'B', 10)
            
            weighted_header = data.get(weighted_head_key)
            if weighted_header:
                pdf.cell(0, 6, weighted_header, ln=True)
            
            pdf.set_font("Calibri", '', 10)
            old_y = pdf.get_y()
            
            # For weighted average, your data has different keys:
            # for_ammonia1_1_inlet, for_ammonia1_2_inlet, for_ammonia1_3_inlet
            # and df keys: for_ammonia1_1_df_inlet, for_ammonia1_2_df_inlet, for_ammonia1_3_df_inlet
            
            parts = []
            for i in range(1, 4):
                val_key = f"for_{param_base}1_{i}_{io}"
                df_key = f"for_{param_base}1_{i}_df_{io}"
                
                if data.get(val_key) is not None and data.get(df_key) is not None:
                    parts.append(f"({data[val_key]} X {data[df_key]})")
            
            if parts:
                formula = " + ".join(parts)
                width = pdf.get_string_width(formula)
                
                pdf.set_x(start_x)
                
                # Your data has weighted answer key like "ammonia_ans_1_inlet"
                weighted_answer_key = f"{ans_key}"  # e.g., "ammonia_ans_1_inlet"
                weighted_param_key = f"{param_key}"  # e.g., "ammonia_param_1_inlet"
                
                weighted_answer = data.get(weighted_answer_key)
                weighted_param = data.get(weighted_param_key)
                
                pdf.cell(
                    width, 6,
                    f"{formula} = {weighted_answer} {weighted_param}",
                    ln=True
                )
                
                pdf.line(start_x, old_y + 5.5, start_x + width, old_y + 5.5)
                
                # Your data has divisor like "ammonia_divi_inlet"
                divisor = str(data.get(div_key)) if data.get(div_key) else ""
                pdf.set_x(start_x + width / 2 - pdf.get_string_width(divisor) / 2)
                pdf.cell(pdf.get_string_width(divisor), 6, divisor, align="C", ln=True)
    
   


                pdf.ln(4)
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
        # INLET TDS Calculations Block
        if data.get('tds_final_ans_inlet'):
            check_page_break(100)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Total Dissolved Solids Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)
            
            # Process INLET TDS sections
            inlet_tds_sections = [
                ('tds_head_1_inlet', 'bw1_inlet', 'AW05_inlet', 'vs1_inlet', 'ans1_inlet', 'ans_param_inlet', ''),
                ('tds_head_2_inlet', 'bw2_inlet', 'AW10_inlet', 'vs2_inlet', 'ans2_inlet', 'ans_param_2_inlet', 'read_1_inlet'),
                ('tds_head_3_inlet', 'bw3_inlet', 'AW15_inlet', 'vs3_inlet', 'ans3_inlet', 'ans_param_3_inlet', 'read_2_inlet'),
                ('tds_head_4_inlet', 'bw4_inlet', 'AW20_inlet', 'vs4_inlet', 'ans4_inlet', 'ans_param_4_inlet', 'read_3_inlet')
            ]
            
            for head_key, bw_key, aw_key, vs_key, ans_key, param_key, read_key in inlet_tds_sections:
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
                    # Extract number from AW key (e.g., '05' from 'AW05_inlet')
                    aw_number = aw_key.split('_')[0][2:]  # Gets '05' from 'AW05_inlet'
                    after_weights = [data.get(f'AW{i:02d}_inlet', '') for i in range(
                        int(aw_number)-4, int(aw_number)+1
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
            
            # INLET TDS Final Average
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.ln(2)
            pdf.cell(0, 6, "Average of Total Dissolved Solids (Inlet):", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            
            final_text = f"{data.get('tds_final_ans1_inlet', '')} + {data.get('tds_final_ans2_inlet', '')} + {data.get('tds_final_ans3_inlet', '')}"
            result_text = f"{data['tds_final_ans_inlet']} {data.get('tds_final_param_inlet', '')}"
            add_formula_with_line(final_text, result_text, data.get('tds_final_divi_inlet','3'), 40)

        # OUTLET TDS Calculations Block
        if data.get('tds_final_ans_outlet'):
            check_page_break(30)
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)
            
            # Process OUTLET TDS sections
            outlet_tds_sections = [
                ('tds_head_1_outlet', 'bw1_outlet', 'AW05_outlet', 'vs1_outlet', 'ans1_outlet', 'ans_param_outlet', ''),
                ('tds_head_2_outlet', 'bw2_outlet', 'AW10_outlet', 'vs2_outlet', 'ans2_outlet', 'ans_param_2_outlet', 'read_1_outlet'),
                ('tds_head_3_outlet', 'bw3_outlet', 'AW15_outlet', 'vs3_outlet', 'ans3_outlet', 'ans_param_3_outlet', 'read_2_outlet'),
                ('tds_head_4_outlet', 'bw4_outlet', 'AW20_outlet', 'vs4_outlet', 'ans4_outlet', 'ans_param_4_outlet', 'read_3_outlet')
            ]
            
            for head_key, bw_key, aw_key, vs_key, ans_key, param_key, read_key in outlet_tds_sections:
                if data.get(head_key):
                    check_page_break(25)
                    
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, "TDS Outlet Calculations", border=False, align="L", ln=True)
                    pdf.cell(0, 6, data[head_key], border=False, align="L", ln=True)
                    
                    if data.get(read_key):
                        pdf.cell(0, 6, data[read_key], border=False, align="L", ln=True)
                    
                    pdf.set_x(30)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(30, 6, "Before Weight   = ", border=False, align="L")
                    pdf.cell(0, 6, data.get(bw_key, ''), border=False, align="L", ln=True)
                    
                    pdf.set_x(30)
                    pdf.cell(30, 6, "After Weight   = ", align="L")
                    # Extract number from AW key (e.g., '05' from 'AW05_outlet')
                    aw_number = aw_key.split('_')[0][2:]  # Gets '05' from 'AW05_outlet'
                    after_weights = [data.get(f'AW{i:02d}_outlet', '') for i in range(
                        int(aw_number)-4, int(aw_number)+1
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
            
            # OUTLET TDS Final Average
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.ln(2)
            pdf.cell(0, 6, "Average of Total Dissolved Solids (Outlet):", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            
            final_text = f"{data.get('tds_final_ans1_outlet', '')} + {data.get('tds_final_ans2_outlet', '')} + {data.get('tds_final_ans3_outlet', '')}"
            result_text = f"{data['tds_final_ans_outlet']} {data.get('tds_final_param_outlet', '')}"
            add_formula_with_line(final_text, result_text, data.get('tds_final_divi_outlet','3'), 40)

        for key in sorted(data.keys()):

            # Match keys like: tds_crm_36_1_bw
            match = re.match(r'(total_dissolved_solids_crm_\d+_\d+)_bw$', key)
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
            
            
            
        # tss calculations
        
        # =========================
        # TSS inlet CALCULATIONS
        # =========================
        if data.get('tss_final_ans_inlet'):
            check_page_break(100)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Total Suspended Solids (TSS) Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            inlet_tss_sections = [
                ('tss_head_1_inlet', 'iw1_inlet', 'FW05_inlet', 'tss_vs1_inlet', 'tss_ans1_inlet', 'tss_ans_param_inlet', ''),
                ('tss_head_2_inlet', 'iw2_inlet', 'FW10_inlet', 'tss_vs2_inlet', 'tss_ans2_inlet', 'tss_ans_param_2_inlet', 'tss_read_1_inlet'),
                ('tss_head_3_inlet', 'iw3_inlet', 'FW15_inlet', 'tss_vs3_inlet', 'tss_ans3_inlet', 'tss_ans_param_3_inlet', 'tss_read_2_inlet'),
                ('tss_head_4_inlet', 'iw4_inlet', 'FW20_inlet', 'tss_vs4_inlet', 'tss_ans4_inlet', 'tss_ans_param_4_inlet', 'tss_read_3_inlet'),
            ]

            for head, iw, fw, vs, ans, param, read in inlet_tss_sections:
                if data.get(head):
                    check_page_break(25)

                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data[head], ln=True)

                    if read and data.get(read):
                        pdf.cell(0, 6, data[read], ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(35, 6, "Initial Weight  = ")
                    pdf.cell(0, 6, data.get(iw, ''), ln=True)

                    fw_num = int(fw[2:4])
                    fw_values = [
                        data.get(f'FW{i:02d}_inlet', '')
                        for i in range(fw_num - 4, fw_num + 1)
                        if data.get(f'FW{i:02d}_inlet')
                    ]

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Final Weight   = ")
                    pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Value of Sample = ")
                    pdf.cell(0, 6, data.get(vs, ''), ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(35, 6, "Formula :", ln=True)

                    pdf.set_font("Calibri", '', 10)
                    formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                    result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                    add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)

            # ---------- FINAL AVERAGE ----------
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, "Average of Total Suspended Solids (inlet):", ln=True)
            pdf.set_font("Calibri", '', 10)

            final_text = (
                f"{data.get('tss_final_ans1_inlet','')} + "
                f"{data.get('tss_final_ans2_inlet','')} + "
                f"{data.get('tss_final_ans3_inlet','')}"
            )
            result_text = f"{data.get('tss_final_ans_inlet')} {data.get('tss_final_param_inlet','')}"

            add_formula_with_line(
                final_text,
                result_text,
                data.get('tss_final_divi_inlet', '3'),
                40
            )


        # =========================
        # TSS outlet CALCULATIONS
        # =========================
        if data.get('tss_final_ans_outlet'):
            check_page_break(100)
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            outlet_tss_sections = [
                ('tss_head_1_outlet', 'iw1_outlet', 'FW05_outlet', 'tss_vs1_outlet', 'tss_ans1_outlet', 'tss_ans_param_outlet', ''),
                ('tss_head_2_outlet', 'iw2_outlet', 'FW10_outlet', 'tss_vs2_outlet', 'tss_ans2_outlet', 'tss_ans_param_2_outlet', 'tss_read_1_outlet'),
                ('tss_head_3_outlet', 'iw3_outlet', 'FW15_outlet', 'tss_vs3_outlet', 'tss_ans3_outlet', 'tss_ans_param_3_outlet', 'tss_read_2_outlet'),
                ('tss_head_4_outlet', 'iw4_outlet', 'FW20_outlet', 'tss_vs4_outlet', 'tss_ans4_outlet', 'tss_ans_param_4_outlet', 'tss_read_3_outlet'),
            ]

            for head, iw, fw, vs, ans, param, read in outlet_tss_sections:
                if data.get(head):
                    check_page_break(40)

                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, "TSS Outlet Calculation", ln=True)
                    pdf.cell(0, 6, data[head], ln=True)

                    if read and data.get(read):
                        pdf.cell(0, 6, data[read], ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(35, 6, "Initial Weight  = ")
                    pdf.cell(0, 6, data.get(iw, ''), ln=True)

                    fw_num = int(fw[2:4])
                    fw_values = [
                        data.get(f'FW{i:02d}_outlet', '')
                        for i in range(fw_num - 4, fw_num + 1)
                        if data.get(f'FW{i:02d}_outlet')
                    ]

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Final Weight   = ")
                    pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Value of Sample = ")
                    pdf.cell(0, 6, data.get(vs, ''), ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(35, 6, "Formula :", ln=True)

                    pdf.set_font("Calibri", '', 10)
                    formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                    result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                    add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)
                    
            # ---------- FINAL AVERAGE ----------
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, "Average of Total Suspended Solids (Outlet):", ln=True)
            pdf.set_font("Calibri", '', 10)

            final_text = (
                f"{data.get('tss_final_ans1_outlet','')} + "
                f"{data.get('tss_final_ans2_outlet','')} + "
                f"{data.get('tss_final_ans3_outlet','')}"
            )
            result_text = f"{data.get('tss_final_ans_outlet')} {data.get('tss_final_param_outlet','')}"

            add_formula_with_line(
                final_text,
                result_text,
                data.get('tss_final_divi_outlet', '3'),
                40
            )

        
        for key in sorted(data.keys()):

            # Match keys like: tds_crm_36_1_bw
            match = re.match(r'(total_suspended_solids_tss_crm_\d+_\d+)_bw$', key)
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

            # ---------- FORMULA (USE ONLY LAST AW) ----------
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
            
            
            
            if data.get('oil_final_ans_inlet'):
                check_page_break(100)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 4, "Oil & Grease Calculation:", 0, 1, 'L')
                pdf.set_font("Calibri", size=10)
                pdf.ln(3)

                inlet_oil_sections = [
                    ('oil_head_1_inlet', 'oil_iw1_inlet', 'oil_FW05_inlet', 'oil_vs1_inlet', 'oil_ans1_inlet', 'oil_ans_param_inlet', 'oil_read_1_inlet'),
                    ('',                 'oil_iw2_inlet', 'oil_FW10_inlet', 'oil_vs2_inlet', 'oil_ans2_inlet', 'oil_ans_param_2_inlet', 'oil_read_2_inlet'),
                    ('',                 'oil_iw3_inlet', 'oil_FW15_inlet', 'oil_vs3_inlet', 'oil_ans3_inlet', 'oil_ans_param_3_inlet', 'oil_read_3_inlet'),
                ]

                for head, iw, fw, vs, ans, param, read in inlet_oil_sections:
                    if data.get(iw):
                        check_page_break(25)

                        if head and data.get(head):
                            pdf.set_font("Calibri", 'B', 10)
                            pdf.cell(0, 6, f"{data[head]}", ln=True)

                        if read and data.get(read):
                            pdf.set_font("Calibri", 'B', 10)
                            pdf.cell(0, 6, data[read], ln=True)
                            pdf.set_font("Calibri", '', 10)

                        pdf.set_x(30)
                        pdf.cell(35, 6, "Initial Weight  = ")
                        pdf.cell(0, 6, data.get(iw, ''), ln=True)

                        fw_num = int(fw[6:8])
                        fw_values = [
                            data.get(f'oil_FW{i:02d}_inlet', '')
                            for i in range(fw_num - 4, fw_num + 1)
                            if data.get(f'oil_FW{i:02d}_inlet')
                        ]

                        pdf.set_x(30)
                        pdf.cell(35, 6, "Final Weight   = ")
                        pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                        pdf.set_x(30)
                        pdf.cell(35, 6, "Value of Sample = ")
                        pdf.cell(0, 6, data.get(vs, ''), ln=True)

                        pdf.set_x(30)
                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(35, 6, "Formula :", ln=True)

                        pdf.set_font("Calibri", '', 10)
                        formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                        result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                        add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)

                # ---------- FINAL AVERAGE ----------
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 6, "Average of Oil & Grease (Inlet):", ln=True)
                pdf.set_font("Calibri", '', 10)

                final_text = (
                    f"{data.get('oil_final_ans1_inlet','')} + "
                    f"{data.get('oil_final_ans2_inlet','')} + "
                    f"{data.get('oil_final_ans3_inlet','')}"
                )
                result_text = f"{data.get('oil_final_ans_inlet')} {data.get('oil_final_param_inlet','')}"

                add_formula_with_line(
                    final_text,
                    result_text,
                    data.get('oil_final_divi_inlet', '3'),
                    40
                )
                
        if data.get('oil_final_ans_outlet'):
            check_page_break(100)
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            outlet_oil_sections = [
                ('oil_head_1_outlet', 'oil_iw1_outlet', 'oil_FW05_outlet', 'oil_vs1_outlet', 'oil_ans1_outlet', 'oil_ans_param_outlet', 'oil_read_1_outlet'),
                ('',                  'oil_iw2_outlet', 'oil_FW10_outlet', 'oil_vs2_outlet', 'oil_ans2_outlet', 'oil_ans_param_2_outlet', 'oil_read_2_outlet'),
                ('',                  'oil_iw3_outlet', 'oil_FW15_outlet', 'oil_vs3_outlet', 'oil_ans3_outlet', 'oil_ans_param_3_outlet', 'oil_read_3_outlet'),
            ]
            
            for head, iw, fw, vs, ans, param, read in outlet_oil_sections:
                if data.get(iw):
                    check_page_break(20)

                    if head and data.get(head):
                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data[head], ln=True)

                    if read and data.get(read):
                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data[read], ln=True)
                        pdf.set_font("Calibri", '', 10)
                        

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Initial Weight  = ")
                    pdf.cell(0, 6, data.get(iw, ''), ln=True)

                    fw_num = int(fw[6:8])
                    fw_values = [
                        data.get(f'oil_FW{i:02d}_outlet', '')
                        for i in range(fw_num - 4, fw_num + 1)
                        if data.get(f'oil_FW{i:02d}_outlet')
                    ]

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Final Weight   = ")
                    pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Value of Sample = ")
                    pdf.cell(0, 6, data.get(vs, ''), ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(35, 6, "Formula :", ln=True)

                    pdf.set_font("Calibri", '', 10)
                    formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                    result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                    add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)

            # ---------- FINAL AVERAGE ----------
            check_page_break(10)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,6,"Average of Oil & Grease (Outlet):",ln=True)
            pdf.set_font("Calibri", '', 10)

            final_text = (
                f"{data.get('oil_final_ans1_outlet','')} + "
                f"{data.get('oil_final_ans2_outlet','')} + "
                f"{data.get('oil_final_ans3_outlet','')}"
            )
            result_text = f"{data.get('oil_final_ans_outlet')} {data.get('oil_final_param_outlet','')}"

            add_formula_with_line(
                final_text,
                result_text,
                data.get('oil_final_divi_outlet', '3'),
                40
            )

        
        for key in sorted(data.keys()):

            # Match keys like: tds_crm_36_1_bw
            match = re.match(r'(oil_grease_crm_\d+_\d+)_bw$', key)
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

            # ---------- FORMULA (USE ONLY LAST AW) ----------
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
        # Check for pH calculations
        if data.get('for_ph1_inlet_4') or data.get('for_ph1_outlet_4'):
            check_page_break(80)
            
            # INLET pH Calculations
            if data.get('for_ph1_inlet_4'):
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 4, "pH Calculations:", 0, 1, 'L')
                
                inlet_ph_sections = [
                    ('ph_head_1_inlet', 'for_ph1_inlet_4', 'for_ph2_inlet_4', 'for_ph3_inlet_4', 'ph_ans_1_inlet'),
                    ('ph_head_2_inlet', 'for_ph1_inlet_7', 'for_ph2_inlet_7', 'for_ph3_inlet_7', 'ph_ans_2_inlet'), 
                    ('ph_head_3_inlet', 'for_ph1_inlet_10', 'for_ph2_inlet_10', 'for_ph3_inlet_10', 'ph_ans_3_inlet'),
                    ('ph_head_4_inlet', 'for_ph1_inlet_sample', 'for_ph2_inlet_sample', 'for_ph3_inlet_sample', 'ph_ans_4_inlet')
                ]
                
                for i, (head, val1, val2, val3, ans) in enumerate(inlet_ph_sections, start=1):
                    if data.get(head):
                        check_page_break(15)
                        pdf.set_font("Calibri", 'B', 11)
                        pdf.cell(0, 6, data[head], border=False, align="L", ln=True)
                        pdf.set_font("Calibri", size=10)

                        ph_text = f"{data.get(val1, '')} + {data.get(val2, '')} + {data.get(val3, '')}"
                        result_text = f"{data.get(ans, '')}"

                        divisor = data.get(f'ph_divi_{i}_inlet', '3')  # Get the divisor for inlet

                        add_formula_with_line(ph_text, result_text, divisor, 30)
                
                pdf.ln(5)  # Add some space between inlet and outlet sections
            
            # OUTLET pH Calculations
            # if data.get('for_ph1_outlet_4'):
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 4, "pH Outlet Calculation:", 0, 1, 'L')
                
            #     outlet_ph_sections = [
            #         ('ph_head_1_outlet', 'for_ph1_outlet_4', 'for_ph2_outlet_4', 'for_ph3_outlet_4', 'ph_ans_1_outlet'),
            #         ('ph_head_2_outlet', 'for_ph1_outlet_7', 'for_ph2_outlet_7', 'for_ph3_outlet_7', 'ph_ans_2_outlet'), 
            #         ('ph_head_3_outlet', 'for_ph1_outlet_10', 'for_ph2_outlet_10', 'for_ph3_outlet_10', 'ph_ans_3_outlet'),
            #         ('ph_head_4_outlet', 'for_ph1_outlet_sample', 'for_ph2_outlet_sample', 'for_ph3_outlet_sample', 'ph_ans_4_outlet')
            #     ]
                
            #     for i, (head, val1, val2, val3, ans) in enumerate(outlet_ph_sections, start=1):
            #         if data.get(head):
            #             check_page_break(15)
            #             pdf.set_font("Calibri", 'B', 10)
            #             pdf.cell(0, 6, data[head], border=False, align="L", ln=True)
            #             pdf.set_font("Calibri", size=10)

            #             ph_text = f"{data.get(val1, '')} + {data.get(val2, '')} + {data.get(val3, '')}"
            #             result_text = f"{data.get(ans, '')}"

            #             divisor = data.get(f'ph_divi_{i}_outlet', '3')  # Get the divisor for outlet

            #             add_formula_with_line(ph_text, result_text, divisor, 30)
            if(data.get('ph_head_4_outlet')):
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get('ph_head_4_outlet'), 0, 1, 'L')
                add_formula_block(
                    None,
                    None,
                    f"{data.get('for_ph1_outlet_sample')} + {data.get('for_ph2_outlet_sample')} + {data.get('for_ph1_outlet_sample')}",
                    f"{data['ph_ans_4_outlet']}",
                    data.get('ph_divi_4_outlet')
                )
        
       
        for key in data.keys():
            match = re.match(r'(ph_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if value exists
            if data.get(f"{base}_1"):

                check_page_break(20)
                pdf.ln(5)

                # fetch actual values
                v1 = data.get(f"{base}_1", "")
                v2 = data.get(f"{base}_2", "")
                v3 = data.get(f"{base}_3", "")
                ans = data.get(f"{base}_ans", "")
                divi = data.get(f"{base}_divi", "")
                head = data.get(f"{base}_head", "")
                param = data.get(f"{base}_param", "")

                add_formula_block(
                    head_text=head,
                    reading_text=None,
                    formula_content=f"{v1} + {v2} + {v3}",
                    result_text=f"{ans}",
                    divisor_text=divi
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

        add_simple_formula_section('for_alum1_inlet', 'Aluminium Calculations', 'alum_head_inlet', 'alum_ans_inlet', 'alum_param_inlet', '', '_df_inlet', 'alum_divi_inlet'),
        add_simple_formula_section('for_alum1_outlet', '', 'alum_head_outlet', 'alum_ans_outlet', 'alum_param_outlet', '', '_df_outlet', 'alum_divi_outlet'),
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

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
            
            
        add_simple_formula_section('for_anitomny1_inlet', 'Antimony Inlet Calculations', 'anitomny_head_inlet', 'anitomny_ans_inlet', 'anitomny_param_inlet', '', '_df_inlet', 'anitm_divi_inlet'),
        add_simple_formula_section('for_anitomny1_outlet', 'Antimony Outlet Calculations', 'anitomny_head_outlet', 'anitomny_ans_outlet', 'anitomny_param_outlet', '', '_df_outlet', 'anitm_divi_outlet'),
        
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

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
            
        add_simple_formula_section('for_arsenic1_inlet', 'Arsenic Calculations', 'arsenic_head_inlet', 'arsenic_ans_inlet', 'arsenic_param_inlet', '', '_df_inlet', 'arsenic_divi_inlet'),
        add_simple_formula_section('for_arsenic1_outlet', '', 'arsenic_head_outlet', 'arsenic_ans_outlet', 'arsenic_param_outlet', '', '_df_outlet', 'arsenic_divi_outlet'),
        
        
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
            
        add_simple_formula_section('for_barium1_inlet', 'Barium Calculations', 'barium_head_inlet', 'barium_ans_inlet', 'barium_param_inlet', '', '_df_inlet', 'barium_divi_inlet'),
        # add_simple_formula_section('for_barium1_outlet', '', 'barium_head_outlet', 'barium_ans_outlet', 'barium_param_outlet', '', '_df_outlet', 'barium_divi_outlet'),
        if(data.get('barium_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    None,
                    data.get('barium_head_outlet'),
                    f"({data.get('for_barium1_outlet')} X {data.get('for_barium1_df_outlet')}) + ({data.get('for_barium2_outlet')} X {data.get('for_barium2_df_outlet')}) + ({data.get('for_barium3_outlet')} X {data.get('for_barium3_df_outlet')})",
                    f"{data['barium_ans_outlet']} {data.get('barium_param_outlet')}",
                    data.get('barium_divi_outlet')
                )
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
            
        add_simple_formula_section('for_boron1_inlet', 'Boron Calculations', 'boron_head_inlet', 'boron_ans_inlet', 'boron_param_inlet', '', '_df_inlet', 'boron_divi_inlet'),
        # add_simple_formula_section('for_boron1_outlet', '', 'boron_head_outlet', 'boron_ans_outlet', 'boron_param_outlet', '', '_df_outlet', 'boron_divi_outlet'),
        if(data.get('boron_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('boron_head_outlet'),
                    None,
                    f"({data.get('for_boron1_outlet')} X {data.get('for_boron1_df_outlet')}) + ({data.get('for_boron2_outlet')} X {data.get('for_boron2_df_outlet')}) + ({data.get('for_boron3_outlet')} X {data.get('for_boron3_df_outlet')})",
                    f"{data['boron_ans_outlet']} {data.get('boron_param_outlet')}",
                    data.get('boron_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_cadmium1_inlet', 'Cadmium Calculations', 'cadmium_head_inlet', 'cadmium_ans_inlet', 'cadmium_param_inlet', '', '_df_inlet', 'cadmium_divi_inlet'),
        # add_simple_formula_section('for_cadmium1_outlet', '', 'cadmium_head_outlet', 'cadmium_ans_outlet', 'cadmium_param_outlet', '', '_df_outlet', 'cadmium_divi_outlet'),
        if(data.get('cadmium_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('cadmium_head_outlet'),
                    None,
                    f"({data.get('for_cadmium1_outlet')} X {data.get('for_cadmium1_df_outlet')}) + ({data.get('for_cadmium2_outlet')} X {data.get('for_cadmium2_df_outlet')}) + ({data.get('for_cadmium3_outlet')} X {data.get('for_cadmium3_df_outlet')})",
                    f"{data['cadmium_ans_outlet']} {data.get('cadmium_param_outlet')}",
                    data.get('cadmium_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_chromium1_inlet', 'Chromium Calculations', 'chromium_head_inlet', 'chromium_ans_inlet', 'chromium_param_inlet', '', '_df_inlet', 'chrom_divi_inlet'),
        # add_simple_formula_section('for_chromium1_outlet', '', 'chromium_head_outlet', 'chromium_ans_outlet', 'chromium_param_outlet', '', '_df_outlet', 'chrom_divi_outlet'),
        if(data.get('chromium_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('chromium_head_outlet'),
                    None,
                    f"({data.get('for_chromium1_outlet')} X {data.get('for_chromium1_df_outlet')}) + ({data.get('for_chromium2_outlet')} X {data.get('for_chromium2_df_outlet')}) + ({data.get('for_chromium3_outlet')} X {data.get('for_chromium3_df_outlet')})",
                    f"{data['chromium_ans_outlet']} {data.get('chromium_param_outlet')}",
                    data.get('chrom_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_copper1_inlet', 'Copper Calculations', 'copper_head_inlet', 'copper_ans_inlet', 'copper_param_inlet', '', '_df_inlet', 'copper_divi_inlet'),
        # add_simple_formula_section('for_copper1_outlet', '', 'copper_head_outlet', 'copper_ans_outlet', 'copper_param_outlet', '', '_df_outlet', 'copper_divi_outlet'),
        if(data.get('copper_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('copper_head_outlet'),
                    None,
                    f"({data.get('for_copper1_outlet')} X {data.get('for_copper1_df_outlet')}) + ({data.get('for_copper2_outlet')} X {data.get('for_copper2_df_outlet')}) + ({data.get('for_copper3_outlet')} X {data.get('for_copper3_df_outlet')})",
                    f"{data['copper_ans_outlet']} {data.get('copper_param_outlet')}",
                    data.get('copper_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_lead1_inlet', 'Lead Calculations', 'lead_head_inlet', 'lead_ans_inlet', 'lead_param_inlet', '', '_df_inlet', 'lead_divi_inlet'),
        # add_simple_formula_section('for_lead1_outlet', '', 'lead_head_outlet', 'lead_ans_outlet', 'lead_param_outlet', '', '_df_outlet', 'lead_divi_outlet'),
        if(data.get('lead_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('lead_head_outlet'),
                    None,
                    f"({data.get('for_lead1_outlet')} X {data.get('for_lead1_df_outlet')}) + ({data.get('for_lead2_outlet')} X {data.get('for_lead2_df_outlet')}) + ({data.get('for_lead3_outlet')} X {data.get('for_lead3_df_outlet')})",
                    f"{data['lead_ans_outlet']} {data.get('lead_param_outlet')}",
                    data.get('lead_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_manganese1_inlet', 'Manganese Calculations', 'manganese_head_inlet', 'manganese_ans_inlet', 'manganese_param_inlet', '', '_df_inlet', 'manganese_divi_inlet'),
        # add_simple_formula_section('for_manganese1_outlet', '', 'manganese_head_outlet', 'manganese_ans_outlet', 'manganese_param_outlet', '', '_df_outlet', 'manganese_divi_outlet'),
        if(data.get('manganese_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('manganese_head_outlet'),
                    None,
                    f"({data.get('for_manganese1_outlet')} X {data.get('for_manganese1_df_outlet')}) + ({data.get('for_manganese2_outlet')} X {data.get('for_manganese2_df_outlet')}) + ({data.get('for_manganese3_outlet')} X {data.get('for_manganese3_df_outlet')})",
                    f"{data['manganese_ans_outlet']} {data.get('manganese_param_outlet')}",
                    data.get('manganese_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_mercury1_inlet', 'Mercury Calculations', 'mercury_head_inlet', 'mercury_ans_inlet', 'mercury_param_inlet', '', '_df_inlet', 'mercury_divi_inlet'),
        # add_simple_formula_section('for_mercury1_outlet', '', 'mercury_head_outlet', 'mercury_ans_outlet', 'mercury_param_outlet', '', '_df_outlet', 'mercury_divi_outlet'),
        if(data.get('mercury_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('mercury_head_outlet'),
                    None,
                    f"({data.get('for_mercury1_outlet')} X {data.get('for_mercury1_df_outlet')}) + ({data.get('for_mercury2_outlet')} X {data.get('for_mercury2_df_outlet')}) + ({data.get('for_mercury3_outlet')} X {data.get('for_mercury3_df_outlet')})",
                    f"{data['mercury_ans_outlet']} {data.get('mercury_param_outlet')}",
                    data.get('mercury_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_nickel1_inlet', 'Nickel Calculations', 'nickel_head_inlet', 'nickel_ans_inlet', 'nickel_param_inlet', '', '_df_inlet', 'nickel_divi_inlet'),
        # add_simple_formula_section('for_nickel1_outlet', '', 'nickel_head_outlet', 'nickel_ans_outlet', 'nickel_param_outlet', '', '_df_outlet', 'nickel_divi_outlet'),
        if(data.get('nickel_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('nickel_head_outlet'),
                    None,
                    f"({data.get('for_nickel1_outlet')} X {data.get('for_nickel1_df_outlet')}) + ({data.get('for_nickel2_outlet')} X {data.get('for_nickel2_df_outlet')}) + ({data.get('for_nickel3_outlet')} X {data.get('for_nickel3_df_outlet')})",
                    f"{data['nickel_ans_outlet']} {data.get('nickel_param_outlet')}",
                    data.get('nickel_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_phenolic1_inlet', 'Phenolic Calculations', 'phenolic_head_inlet', 'phenolic_ans_inlet', 'phenolic_param_inlet', '', '_df_inlet', 'phenolic_divi_inlet'),
        # add_simple_formula_section('for_phenolic1_outlet', '', 'phenolic_head_outlet', 'phenolic_ans_outlet', 'phenolic_param_outlet', '', '_df_outlet', 'phenolic_divi_outlet'),
        if(data.get('phenolic_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('phenolic_head_outlet'),
                    None,
                    f"({data.get('for_phenolic1_outlet')} X {data.get('for_phenolic1_df_outlet')}) + ({data.get('for_phenolic2_outlet')} X {data.get('for_phenolic2_df_outlet')}) + ({data.get('for_phenolic3_outlet')} X {data.get('for_phenolic3_df_outlet')})",
                    f"{data['phenolic_ans_outlet']} {data.get('phenolic_param_outlet')}",
                    data.get('phenolic_divi_outlet')
                )
        for key in data.keys():
            match = re.match(r'(phenol_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
        add_simple_formula_section('for_selenium1_inlet', 'Selenium Calculations', 'selenium_head_inlet', 'selenium_ans_inlet', 'selenium_param_inlet', '', '_df_inlet', 'selenium_divi_inlet'),
        # add_simple_formula_section('for_selenium1_outlet', '', 'selenium_head_outlet', 'selenium_ans_outlet', 'selenium_param_outlet', '', '_df_outlet', 'selenium_divi_outlet'),
        if(data.get('selenium_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('selenium_head_outlet'),
                    None,
                    f"({data.get('for_selenium1_outlet')} X {data.get('for_selenium1_df_outlet')}) + ({data.get('for_selenium2_outlet')} X {data.get('for_selenium2_df_outlet')}) + ({data.get('for_selenium3_outlet')} X {data.get('for_selenium3_df_outlet')})",
                    f"{data['selenium_ans_outlet']} {data.get('selenium_param_outlet')}",
                    data.get('selenium_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_zinc1_inlet', 'Zinc Calculations', 'zinc_head_inlet', 'zinc_ans_inlet', 'zinc_param_inlet', '', '_df_inlet', 'zinc_divi_inlet'),
        # add_simple_formula_section('for_zinc1_outlet', '', 'zinc_head_outlet', 'zinc_ans_outlet', 'zinc_param_outlet', '', '_df_outlet', 'zinc_divi_outlet'),
        if(data.get('zinc_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('zinc_head_outlet'),
                    None,
                    f"({data.get('for_zinc1_outlet')} X {data.get('for_zinc1_df_outlet')}) + ({data.get('for_zinc2_outlet')} X {data.get('for_zinc2_df_outlet')}) + ({data.get('for_zinc3_outlet')} X {data.get('for_zinc3_df_outlet')})",
                    f"{data['zinc_ans_outlet']} {data.get('zinc_param_outlet')}",
                    data.get('zinc_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_beryllium1_1_inlet', 'Beryllium Calculations', 'beryllium_head_1_inlet', 'beryllium_ans_1_inlet', 'beryllium_param_1_inlet', '_1_inlet', '_1_df_inlet', 'beryllium_divi_inlet'),
        add_simple_formula_section('for_beryllium1_1_outlet', '', 'beryllium_head_1_outlet', 'beryllium_ans_1_outlet', 'beryllium_param_1_outlet', '_1_outlet', '_1_df_outlet', 'beryllium_divi_outlet'),
        add_simple_formula_section('for_ammonium1_1_inlet', 'Ammonium Calculations', 'ammonium_head_inlet', 'ammonium_ans_1_inlet', 'ammonium_param_1_inlet', '_1_inlet', '_1_df_inlet', 'ammonium_divi_inlet'),
        add_simple_formula_section('for_ammonium1_1_outlet', '', 'ammonium_head_outlet', 'ammonium_ans_1_outlet', 'ammonium_param_1_outlet', '_1_outlet', '_1_df_outlet', 'ammonium_divi_outlet'),
        add_simple_formula_section('for_formaldehyde1_inlet', 'Formaldehyde Calculations', 'formaldehyde_head_inlet', 'formaldehyde_ans_inlet', 'formaldehyde_param_inlet', '', '_df_inlet', 'formaldehyde_divi_inlet'),
        add_simple_formula_section('for_formaldehyde1_outlet', '', 'formaldehyde_head_outlet', 'formaldehyde_ans_outlet', 'formaldehyde_param_outlet', '', '_df_outlet', 'formaldehyde_divi_outlet'),
        add_simple_formula_section('for_iron1_inlet', 'Iron Calculations', 'iron_head_inlet', 'iron_ans_inlet', 'iron_param_inlet', '', '_df_inlet', 'iron_divi_inlet'),
        # add_simple_formula_section('for_iron1_outlet', '', 'iron_head_outlet', 'iron_ans_outlet', 'iron_param_outlet', '', '_df_outlet', 'iron_divi_outlet'),
        if(data.get('iron_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('iron_head_outlet'),
                    None,
                    f"({data.get('for_iron1_outlet')} X {data.get('for_iron1_df_outlet')}) + ({data.get('for_iron2_outlet')} X {data.get('for_iron2_df_outlet')}) + ({data.get('for_iron3_outlet')} X {data.get('for_iron3_df_outlet')})",
                    f"{data['iron_ans_outlet']} {data.get('iron_param_outlet')}",
                    data.get('iron_divi_outlet')
                )
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
            
        add_simple_formula_section('for_sodium1_inlet', 'Sodium Calculations', 'sodium_head_inlet', 'sodium_ans_inlet', 'sodium_param_inlet', '', '_df_inlet', 'sodium_divi_inlet'),
        # add_simple_formula_section('for_sodium1_outlet', '', 'sodium_head_outlet', 'sodium_ans_outlet', 'sodium_param_outlet', '', '_df_outlet', 'sodium_divi_outlet'),
        if(data.get('sodium_ans_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            add_formula_block(
                    data.get('sodium_head_outlet'),
                    None,
                    f"({data.get('for_sodium1_outlet')} X {data.get('for_sodium1_df_outlet')}) + ({data.get('for_sodium2_outlet')} X {data.get('for_sodium2_df_outlet')}) + ({data.get('for_sodium3_outlet')} X {data.get('for_sodium3_df_outlet')})",
                    f"{data['sodium_ans_outlet']} {data.get('sodium_param_outlet')}",
                    data.get('sodium_divi_outlet')
                )
        
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
        
        add_average_formula_section('for_color1_inlet', 'Color Calculation', 'color_hea_inletd', 'color_ans_inlet', 'color_param_inlet', 'color_divi_inlet')
        add_average_formula_section('for_color1_outlet', '', 'color_head_outlet', 'color_ans_outlet', 'color_param_outlet', 'color_divi_outlet')
        for key in data.keys():
            match = re.match(r'(color_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )

        # add_average_formula_section('for_cyanide1_inlet', 'Cyanide Inlet Calculation', 'cyanide_head_inlet', 'cyanide_ans_inlet', 'cyanide_param_inlet', 'cyanide_divi_inlet')
        # add_average_formula_section('for_cyanide1_outlet', 'Cyanide Outlet Calculation', 'cyanide_head_outlet', 'cyanide_ans_outlet', 'cyanide_param_outlet', 'cyanide_divi_outlet')
        
        
        if(data.get('cyanide_ans_inlet_simple')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Cyanide Calculations", ln=True)
            pdf.cell(0,6,data.get('cyanide_head_inlet_1'),ln=True)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_cyanide1_inlet')} + {data.get('for_cyanide2_inlet')} + {data.get('for_cyanide3_inlet')}",
                    f"{data['cyanide_ans_inlet_simple']} {data.get('cyanide_param_inlet_simple')}",
                    data.get('cyanide_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('cyanide_ans_inlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0,6,data.get('cyanide_head_inlet_2'),ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_cyanide1_1_inlet')} X {data.get('for_cyanide1_1_df_inlet')}) + ({data.get('for_cyanide1_2_inlet')} X {data.get('for_cyanide1_2_df_inlet')}) + ({data.get('for_cyanide1_3_inlet')} X {data.get('for_cyanide1_3_df_inlet')})",
                    f"{data['cyanide_ans_inlet_weighted']} {data.get('cyanide_param_inlet_weighted')}",
                    data.get('cyanide_divi1_inlet')
                )
        
        
        if(data.get('cyanide_ans_outlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0,6,data.get('cyanide_head_outlet_2'),ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_cyanide1_1_outlet')} X {data.get('for_cyanide1_1_df_outlet')}) + ({data.get('for_cyanide1_2_outlet')} X {data.get('for_cyanide1_2_df_outlet')}) + ({data.get('for_cyanide1_3_outlet')} X {data.get('for_cyanide1_3_df_outlet')})",
                    f"{data['cyanide_ans_outlet_weighted']} {data.get('cyanide_param_outlet_weighted')}",
                    data.get('cyanide_divi_outlet')
                )
        
        for key in data.keys():
            match = re.match(r'(cyanide_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
        
        
        # add_average_formula_section('for_fluoride1_inlet', 'Fluoride Inlet Calculation', 'fluoride_head_inlet', 'fluoride_ans_inlet', 'fluoride_param_inlet', 'fluoride_divi_inlet')
        # add_average_formula_section('for_fluoride1_outlet', 'Fluoride Outlet Calculation', 'fluoride_head_outlet', 'fluoride_ans_outlet', 'fluoride_param_outlet', 'fluoride_divi_outlet')
        
        if(data.get('fluoride_ans_inlet_simple')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Fluoride Calculations", ln=True)
            pdf.cell(0,6,data.get('fluoride_head_inlet_1'),ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_fluoride1_inlet')} + {data.get('for_fluoride2_inlet')} + {data.get('for_fluoride3_inlet')}",
                    f"{data['fluoride_ans_inlet_simple']} {data.get('fluoride_param_inlet_simple')}",
                    data.get('fluoride_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('fluoride_ans_inlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('fluoride_head_inlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_fluoride1_1_inlet')} X {data.get('for_fluoride1_1_df_inlet')}) + ({data.get('for_fluoride1_2_inlet')} X {data.get('for_fluoride1_2_df_inlet')}) + ({data.get('for_fluoride1_3_inlet')} X {data.get('for_fluoride1_3_df_inlet')})",
                    f"{data['fluoride_ans_inlet_weighted']} {data.get('fluoride_param_inlet_weighted')}",
                    data.get('fluoride_divi1_inlet')
                )
        
        if(data.get('fluoride_ans_outlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('fluoride_head_outlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_fluoride1_1_outlet')} X {data.get('for_fluoride1_1_df_outlet')}) + ({data.get('for_fluoride1_2_outlet')} X {data.get('for_fluoride1_2_df_outlet')}) + ({data.get('for_fluoride1_3_outlet')} X {data.get('for_fluoride1_3_df_outlet')})",
                    f"{data['fluoride_ans_outlet_weighted']} {data.get('fluoride_param_outlet_weighted')}",
                    data.get('fluoride_divi_outlet')
                )
        
        
        for key in data.keys():
            match = re.match(r'(fluoride_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
        
        
        # add_average_formula_section('for_nitrate1_inlet', 'Nitrate Inlet Calculation', 'nitrate_head_inlet', 'nitrate_ans_inlet', 'nitrate_param_inlet', 'nitrate_divi_inlet')
        # add_average_formula_section('for_nitrate1_outlet', 'Nitrate Outlet Calculation', 'nitrate_head_outlet', 'nitrate_ans_outlet', 'nitrate_param_outlet', 'nitrate_divi_outlet')
        
        
        if(data.get('nitrate_head_inlet_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Nitrate Calculations", ln=True)
            pdf.cell(0,6,data.get('nitrate_head_inlet_1'),ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_nitrate1_inlet')} + {data.get('for_nitrate2_inlet')} + {data.get('for_nitrate3_inlet')}",
                    f"{data['nitrate_ans_inlet_simple']} {data.get('nitrate_param_inlet_simple')}",
                    data.get('nitrate_divi1_inlet', "3")
                )
        
        if(data.get('nitrate_ans_inlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('nitrate_head_inlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_nitrate1_1_inlet')} X {data.get('for_nitrate1_1_df_inlet')}) + ({data.get('for_nitrate1_2_inlet')} X {data.get('for_nitrate1_2_df_inlet')}) + ({data.get('for_nitrate1_3_inlet')} X {data.get('for_nitrate1_3_df_inlet')})",
                    f"{data['nitrate_ans_inlet_weighted']} {data.get('nitrate_param_inlet_weighted')}",
                    data.get('nitrate_divi1_inlet')
                )
       
        if(data.get('nitrate_ans_outlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('nitrate_head_outlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_nitrate1_1_outlet')} X {data.get('for_nitrate1_1_df_outlet')}) + ({data.get('for_nitrate1_2_outlet')} X {data.get('for_nitrate1_2_df_outlet')}) + ({data.get('for_nitrate1_3_outlet')} X {data.get('for_nitrate1_3_df_outlet')})",
                    f"{data['nitrate_ans_outlet_weighted']} {data.get('nitrate_param_outlet_weighted')}",
                    data.get('nitrate_divi_outlet')
                )
        
        
        for key in data.keys():
            match = re.match(r'(nitrate_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
            
        add_average_formula_section('for_nitrite1_inlet', 'Nitrite Calculation', 'nitrite_head_inlet', 'nitrite_ans_inlet', 'nitrite_param_inlet', 'nitrite_divi_inlet')
        add_average_formula_section('for_nitrite1_outlet', '', 'nitrite_head_outlet', 'nitrite_ans_outlet', 'nitrite_param_outlet', 'nitrite_divi_outlet')
        for key in data.keys():
            match = re.match(r'(nitrite_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
            
        # add_average_formula_section('for_residual1_inlet', 'Chlorine Inlet Calculation', 'residual_head_inlet', 'residual_ans_inlet', 'residual_param_inlet', 'residual_divi_inlet')
        # add_average_formula_section('for_residual1_outlet', 'Chlorine Outlet Calculation', 'residual_head_outlet', 'residual_ans_outlet', 'residual_param_outlet', 'residual_divi_outlet')
        
        
        if(data.get('residual_ans_inlet_simple')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Chlorine Calculations", ln=True)
            pdf.cell(0,6,data.get('residual_head_inlet_1'),ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_residual1_inlet')} + {data.get('for_residual2_inlet')} + {data.get('for_residual3_inlet')}",
                    f"{data['residual_ans_inlet_simple']} {data.get('residual_param_inlet_simple')}",
                    data.get('residual_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('residual_ans_inlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('residual_head_inlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_residual1_1_inlet')} X {data.get('for_residual1_1_df_inlet')}) + ({data.get('for_residual1_2_inlet')} X {data.get('for_residual1_2_df_inlet')}) + ({data.get('for_residual1_3_inlet')} X {data.get('for_residual1_3_df_inlet')})",
                    f"{data['residual_ans_inlet_weighted']} {data.get('residual_param_inlet_weighted')}",
                    data.get('residual_divi1_inlet')
                )
        
        
        
        if(data.get('residual_ans_outlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('residual_head_outlet_2'), ln=True)
            pdf.set_font("Calibri", '', 10)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_residual1_1_outlet')} X {data.get('for_residual1_1_df_outlet')}) + ({data.get('for_residual1_2_outlet')} X {data.get('for_residual1_2_df_outlet')}) + ({data.get('for_residual1_3_outlet')} X {data.get('for_residual1_3_df_outlet')})",
                    f"{data['residual_ans_outlet_weighted']} {data.get('residual_param_outlet_weighted')}",
                    data.get('residual_divi_outlet')
                )
            
        for key in data.keys():
            match = re.match(r'(chlorine_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
        add_average_formula_section('for_turbidity1_inlet', 'Turbidity Calculation', 'turbidity_head_inlet', 'turbidity_ans_inlet', 'turbidity_param_inlet', 'turbidity_divi_inlet_weighted')
        add_average_formula_section('for_turbidity1_outlet', '', 'turbidity_head_outlet', 'turbidity_ans_outlet', 'turbidity_param_outlet', 'turbidity_divi_outlet_weighted')
        
        if(data.get('turbidity_ans_outlet_weighted')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('turbidity_head_outlet_2'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_turbidity1_1_outlet')} X {data.get('for_turbidity1_1_df_outlet')}) + ({data.get('for_turbidity1_2_outlet')} X {data.get('for_turbidity1_2_df_outlet')}) + ({data.get('for_turbidity1_3_outlet')} X {data.get('for_turbidity1_3_df_outlet')})",
                    f"{data['turbidity_ans_outlet_weighted']} {data.get('turbidity_param_outlet_weighted')}",
                    data.get('turbidity_divi_outlet')
                )
        
        pdf.ln(2)
        for key in data.keys():
            match = re.match(r'(turbidity_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
        # add_average_formula_section_2('for_ammonia1_inlet', 'Ammonia Inlet Calculation', 'ammonia_head_1_inlet', 'ammonia_ans_1_inlet', 'ammonia_param_1_inlet', 'ammonia_divi_inlet')  
        # add_average_formula_section_2('for_ammonia1_outlet', 'Ammonia Outlet Calculation', 'ammonia_head_1_outlet', 'ammonia_ans_1_outlet', 'ammonia_param_1_outlet', 'ammonia_divi_outlet')  
        
        
        if(data.get('ammonia_ans_inlet')):
            pdf.ln(5)
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Ammonia Calculations", ln=True)
            pdf.cell(0,6,data.get('ammonia_head_inlet'),ln=True)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_ammonia1_inlet')} + {data.get('for_ammonia2_inlet')} + {data.get('for_ammonia3_inlet')}",
                    f"{data['ammonia_ans_inlet']} {data.get('ammonia_param_inlet')}",
                    data.get('ammonia_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('ammonia_ans_1_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('ammonia_head_1_inlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_ammonia1_1_inlet')} X {data.get('for_ammonia1_1_df_inlet')}) + ({data.get('for_ammonia1_2_inlet')} X {data.get('for_ammonia1_2_df_inlet')}) + ({data.get('for_ammonia1_3_inlet')} X {data.get('for_ammonia1_3_df_inlet')})",
                    f"{data['ammonia_ans_1_inlet']} {data.get('ammonia_param_1_inlet')}",
                    data.get('ammonia_divi1_inlet')
                )
                    
        if(data.get('ammonia_ans_1_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('ammonia_head_1_outlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_ammonia1_1_outlet')} X {data.get('for_ammonia1_1_df_outlet')}) + ({data.get('for_ammonia1_2_outlet')} X {data.get('for_ammonia1_2_df_outlet')}) + ({data.get('for_ammonia1_3_outlet')} X {data.get('for_ammonia1_3_df_outlet')})",
                    f"{data['ammonia_ans_1_outlet']} {data.get('ammonia_param_1_outlet')}",
                    data.get('ammonia_divi_outlet')
                )
        for key in data.keys():
            match = re.match(r'(ammonia_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
        
        # add_average_formula_section_2('for_ionic_det1_inlet', 'An Ionic Detergent Calculation', 'ionic_det_head_1_inlet', 'ionic_det_ans_1_inlet', 'ionic_det_param_1_inlet', 'ionic_det_divi_inlet')   
        # add_average_formula_section_2('for_ionic_det1_outlet', 'An Ionic Detergent Outlet Calculation', 'ionic_det_head_1_outlet', 'ionic_det_ans_1_outlet', 'ionic_det_param_1_outlet', 'ionic_det_divi_outlet')   
        if(data.get('ionic_det_ans_inlet')):
            pdf.ln(5)
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Anionic Detergent Calculations", ln=True)
            pdf.cell(0,6,data.get('ionic_det_head_inlet'),ln=True)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_ionic_det1_inlet')} + {data.get('for_ionic_det2_inlet')} + {data.get('for_ionic_det3_inlet')}",
                    f"{data['ionic_det_ans_inlet']} {data.get('ammonia_param_inlet')}",
                    data.get('ammonia_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('ionic_det_ans_1_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('ionic_det_head_1_inlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_ionic_det1_1_inlet')} X {data.get('for_ionic_det1_1_df_inlet')}) + ({data.get('for_ionic_det1_2_inlet')} X {data.get('for_ionic_det1_2_df_inlet')}) + ({data.get('for_ionic_det1_3_inlet')} X {data.get('for_ionic_det1_3_df_inlet')})",
                    f"{data['ionic_det_ans_1_inlet']} {data.get('ionic_det_param_1_inlet')}",
                    data.get('ionic_det_divi_inlet')
                )
        
        if(data.get('ionic_det_ans_1_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('ionic_det_head_1_outlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_ionic_det1_1_outlet')} X {data.get('for_ionic_det1_1_df_outlet')}) + ({data.get('for_ionic_det1_2_outlet')} X {data.get('for_ionic_det1_2_df_outlet')}) + ({data.get('for_ionic_det1_3_outlet')} X {data.get('for_ionic_det1_3_df_outlet')})",
                    f"{data['ionic_det_ans_1_outlet']} {data.get('ionic_det_param_1_outlet')}",
                    data.get('ionic_det_divi_outlet')
                )
        for key in data.keys():
            match = re.match(r'(an_ionic_detergent_as_mbas_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
            
        
        add_average_formula_section_2('for_freechlorine1_inlet', 'Freechlorine Calculation', 'freechlorine_head_1_inlet', 'freechlorine_ans_1_inlet', 'freechlorine_param_1_inlet', 'freechlorine_divi_inlet')
        add_average_formula_section_2('for_freechlorine1_outlet', '', 'freechlorine_head_1_outlet', 'freechlorine_ans_1_outlet', 'freechlorine_param_1_outlet', 'freechlorine_divi_outlet')
        # add_average_formula_section_2('for_sulphate1_inlet', 'sulphate Inlet Calculation', 'sulphate_head_1_inlet', 'sulphate_ans_1_inlet', 'sulphate_param_1_inlet', 'sulphate_divi_inlet')
        # add_average_formula_section_2('for_sulphate1_outlet', 'sulphate Outlet Calculation', 'sulphate_head_1_outlet', 'sulphate_ans_1_outlet', 'sulphate_param_1_outlet', 'sulphate_divi_outlet')
        
        
        if(data.get('sulphate_ans_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Sulphate Calculations", ln=True)
            pdf.cell(0, 6, data.get('sulphate_head_inlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_sulphate1_inlet')} + {data.get('for_sulphate2_inlet')} + {data.get('for_sulphate3_inlet')}",
                    f"{data['sulphate_ans_inlet']} {data.get('sulphate_param_inlet')}",
                    data.get('sulphate_divi1_inlet',"3")
                )
            
        if(data.get('sulphate_ans_1_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('sulphate_head_1_inlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_sulphate1_1_inlet')} X {data.get('for_sulphate1_1_df_inlet')}) + ({data.get('for_sulphate1_2_inlet')} X {data.get('for_sulphate1_2_df_inlet')}) + ({data.get('for_sulphate1_3_inlet')} X {data.get('for_sulphate1_3_df_inlet')})",
                    f"{data['sulphate_ans_1_inlet']} {data.get('sulphate_param_1_inlet')}",
                    data.get('sulphate_divi1_inlet')
                )
        
        
        
        
        if(data.get('sulphate_ans_1_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('sulphate_head_1_outlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_sulphate1_1_outlet')} X {data.get('for_sulphate1_1_df_outlet')}) + ({data.get('for_sulphate1_2_outlet')} X {data.get('for_sulphate1_2_df_outlet')}) + ({data.get('for_sulphate1_3_outlet')} X {data.get('for_sulphate1_3_df_outlet')})",
                    f"{data['sulphate_ans_1_outlet']} {data.get('sulphate_param_1_outlet')}",
                    data.get('sulphate_divi_outlet')
                )
        
        
        
        
        
            
            
        
        for key in data.keys():
            match = re.match(r'(sulphate_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
        
        
        # add_average_formula_section_2('for_cod1_inlet', 'COD Inlet Calculation', 'cod_head_inlet', 'cod_ans_inlet', 'cod_param_inlet', 'cod_divi_inlet')
        # add_average_formula_section_2('for_cod1_outlet', 'COD Outlet Calculation', 'cod_head_outlet', 'cod_ans_outlet', 'cod_param_outlet', 'cod_divi_outlet')
        
        if(data.get('cod_ans_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "COD Calculations", ln=True)
            pdf.cell(0,6,data.get('cod_head_inlet'),ln=True)
            add_formula_block(
                    None,
                    None,
                    f"{data.get('for_cod1_inlet')} + {data.get('for_cod2_inlet')} + {data.get('for_cod3_inlet')}",
                    f"{data['cod_ans_inlet']} {data.get('cod_param_inlet')}",
                    data.get('cod_divi1_inlet', "3")
                )
            
       
        
        
        
        if(data.get('cod_ans_1_inlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('cod_head_1_inlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_cod1_1_inlet')} X {data.get('for_cod1_1_df_inlet')}) + ({data.get('for_cod1_2_inlet')} X {data.get('for_cod1_2_df_inlet')}) + ({data.get('for_cod1_3_inlet')} X {data.get('for_cod1_3_df_inlet')})",
                    f"{data['cod_ans_1_inlet']} {data.get('cod_param_1_inlet')}",
                    data.get('cod_divi1_inlet',"3")
                )
        
        
        if(data.get('cod_ans_1_outlet')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, data.get('cod_head_1_outlet'), ln=True)
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_cod1_1_outlet')} X {data.get('for_cod1_1_df_outlet')}) + ({data.get('for_cod1_2_outlet')} X {data.get('for_cod1_2_df_outlet')}) + ({data.get('for_cod1_3_outlet')} X {data.get('for_cod1_3_df_outlet')})",
                    f"{data['cod_ans_1_outlet']} {data.get('cod_param_1_outlet')}",
                    data.get('cod_divi_outlet')
                )
        
        
        
        pdf.ln(2)
        for key in data.keys():
            match = re.match(r'(chemical_oxygen_demandcod_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
                check_key=f"{base}_1",
                section_title="",
                head_key=f"{base}_head",
                ans_key=f"{base}_ans",
                param_key=f"{base}_param",
                div_key=f"{base}_divi"
            )
        
        pdf.ln(-4)
        
        
        # add_average_formula_section_2('for_ionic_det1_inlet', 'An Ionic Detergent Inlet Calculation', 'ionic_det_head_1_inlet', 'ionic_det_ans_1_inlet', 'ionic_det_param_1_inlet', 'ionic_det_divi_inlet')   
        # add_average_formula_section_2('for_ionic_det1_outlet', 'An Ionic Detergent Outlet Calculation', 'ionic_det_head_1_outlet', 'ionic_det_ans_1_outlet', 'ionic_det_param_1_outlet', 'ionic_det_divi_outlet')   
        
        
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
        
        
        if(data.get('silver_ans_inlet')):
            check_page_break(20)
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Silver Calculation:", 0, 1, 'L')
            pdf.cell(0, 6, data.get('silver_head_1_inlet'), 0, 1, 'L')
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_silver1_1_inlet')} X {data.get('for_silver1_1_df_inlet')}) + ({data.get('for_silver1_2_inlet')} X {data.get('for_silver1_2_df_inlet')}) + ({data.get('for_silver1_3_inlet')} X {data.get('for_silver1_3_df_inlet')})",
                    f"{data['silver_ans_inlet']} {data.get('silver_param_inlet')}",
                    data.get('silver_divi_inlet')
                )
            
        if(data.get('silver_ans_outlet')):
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('silver_head_1_outlet'), 0, 1, 'L')
            add_formula_block(
                    None,
                    None,
                    f"({data.get('for_silver1_1_outlet')} X {data.get('for_silver1_1_df_outlet')}) + ({data.get('for_silver1_2_outlet')} X {data.get('for_silver1_2_df_outlet')}) + ({data.get('for_silver1_3_outlet')} X {data.get('for_silver1_3_df_outlet')})",
                    f"{data['silver_ans_outlet']} {data.get('silver_param_outlet')}",
                    data.get('silver_divi_outlet')
                )
            
        
        for key in sorted(data.keys()):
            
            match = re.match(r'(crm_silver_crm_\d+_\d+)_1$', key)
            
            if not match:
                
                continue

            base = match.group(1)
            

            if not data.get(f"{base}_1"):
                continue

            
            # ---------- CRM HEADER ----------
            if data.get(f"{base}_crm_head"):
                check_page_break(20)
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

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
                
            
        
        if data.get('hardness_ans2_inlet'):
            # check_page_break(100)  # Reserve space for entire hardness section
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Hardness Calculation:", 0, 1, 'L')
            
            # Hardness Reading 1
            if data.get('hardness_reading_1_inlet'):
                add_formula_block(
                    data.get('hardness_head_inlet'),
                    data.get('hardness_reading_1_inlet'),
                    f"({data.get('hardness_2_1_inlet')} - {data.get('hardness_2_2_inlet')}) X 1000",
                    f"{data['hardness_ans2_inlet']} {data.get('hardness_param2_inlet')}",
                    data.get('hardness_2_3_inlet')
                )
            
            # Hardness Reading 2
            pdf.set_font("Calibri", 'B', 11)
            if data.get('hardness_reading_2_inlet'):
                add_formula_block(
                    None,  # No head for subsequent readings
                    data.get('hardness_reading_2_inlet'),
                    f"({data.get('hardness_3_1_inlet')} - {data.get('hardness_3_2_inlet')}) X 1000",
                    f"{data['hardness_ans3_inlet']} {data.get('hardness_param3_inlet')}",
                    data.get('hardness_3_3_inlet')
                )
            
            # Hardness Reading 3
            pdf.set_font("Calibri", 'B', 11)
            if data.get('hardness_reading_3_inlet'):
                add_formula_block(
                    None,  # No head for subsequent readings
                    data.get('hardness_reading_3_inlet'),
                    f"({data.get('hardness_4_1_inlet')} - {data.get('hardness_4_2_inlet')}) X 1000",
                    f"{data['hardness_ans4_inlet']} {data.get('hardness_param4_inlet')}",
                    data.get('hardness_4_3_inlet')
                )
                
            formula_parts = []

            if data.get('hardness_reading_1_inlet'):
                formula_parts.append(
                    f"({data.get('for_hardness1_inlet')} X {data.get('for_hardness1_df_inlet')})"
                )

            if data.get('hardness_reading_2_inlet'):
                formula_parts.append(
                    f"({data.get('for_hardness2_inlet')} X {data.get('for_hardness2_df_inlet')})"
                )

            if data.get('hardness_reading_3_inlet'):
                formula_parts.append(
                    f"({data.get('for_hardness3_inlet')} X {data.get('for_hardness3_df_inlet')})"
                )
            
            average_formula = " + ".join(formula_parts)
            # Hardness Average
            if formula_parts:
                add_formula_block(
                    data.get('hardness_avg_head_inlet'),
                    None,
                    average_formula,
                    f"{data['for_hardness_ans_inlet']} {data.get('for_hardness_param_inlet')}",
                    data.get('hardness_divi_inlet')
                )
                
                
        if data.get('hardness_2_1_outlet'):
            # check_page_break(100)  # Reserve space for entire hardness section
            
            
            # Hardness Reading 1
            if data.get('hardness_reading_1_outlet'):
                add_formula_block(
                    data.get('hardness_head_outlet'),
                    data.get('hardness_reading_1_outlet'),
                    f"({data.get('hardness_2_1_outlet')} - {data.get('hardness_2_2_outlet')}) X 1000",
                    f"{data['hardness_ans2_outlet']} {data.get('hardness_param2_outlet')}",
                    data.get('hardness_2_3_outlet')
                )
            
            # Hardness Reading 2
            pdf.set_font("Calibri", 'B', 11)
            if data.get('hardness_reading_2_outlet'):
                add_formula_block(
                    None,  # No head for subsequent readings
                    data.get('hardness_reading_2_outlet'),
                    f"({data.get('hardness_3_1_outlet')} - {data.get('hardness_3_2_outlet')}) X 1000",
                    f"{data['hardness_ans3_outlet']} {data.get('hardness_param3_outlet')}",
                    data.get('hardness_3_3_outlet')
                )
            
            # Hardness Reading 3
            pdf.set_font("Calibri", 'B', 11)
            if data.get('hardness_reading_3_outlet'):
                add_formula_block(
                    None,  # No head for subsequent readings
                    data.get('hardness_reading_3_outlet'),
                    f"({data.get('hardness_4_1_outlet')} - {data.get('hardness_4_2_outlet')}) X 1000",
                    f"{data['hardness_ans4_outlet']} {data.get('hardness_param4_outlet')}",
                    data.get('hardness_4_3_outlet')
                )
                
            formula_parts = []

            if data.get('hardness_reading_1_outlet'):
                formula_parts.append(
                    f"({data.get('for_hardness1_outlet')} X {data.get('for_hardness1_df_outlet')})"
                )

            if data.get('hardness_reading_2_outlet'):
                formula_parts.append(
                    f"({data.get('for_hardness2_outlet')} X {data.get('for_hardness2_df_outlet')})"
                )

            if data.get('hardness_reading_3_outlet'):
                formula_parts.append(
                    f"({data.get('for_hardness3_outlet')} X {data.get('for_hardness3_df_outlet')})"
                )
            
            average_formula = " + ".join(formula_parts)
            # Hardness Average
            if formula_parts:
                add_formula_block(
                    data.get('hardness_avg_head_outlet'),
                    None,
                    average_formula,
                    f"{data['for_hardness_ans_outlet']} {data.get('for_hardness_param_outlet')}",
                    data.get('hardness_divi_outlet')
                )

        # pdf.set_font("Calibri", 'B', size=10)
        # pdf.cell(0,5,"Total Hardness CRM Calculations",ln=True)
        # pdf.set_font("Calibri", '', size=10)
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(total_hardness_crm_\d+_\d+)_1$', key)
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
            add_formula_block(
                head,
                reading,
                f"({val_1} - {val_2}) X 1000",
                f"{ans} {param}",
                divisor
            )
        
        # ACIDITY CALCULATION
        if data.get('acidity_1_1_inlet'):
            check_page_break(120)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Acidity Calculation:", 0, 1, 'L')

            # Acidity Reading 1
            add_formula_block(
                data.get('acidity_head_1_inlet'),
                data.get('acidity_reading_1_inlet'),
                f"({data.get('acidity_1_1_inlet')} - {data.get('acidity_1_2_inlet')}) "
                f"X {data.get('acidity_1_3_inlet')} X 5000",
                f"{data.get('acidity_ans1_inlet')} {data.get('acidity_param1_inlet')}",
                data.get('acidity_1_4_inlet')
            )

            # Acidity Reading 2
            add_formula_block(
                None,
                data.get('acidity_reading_2_inlet'),
                f"({data.get('acidity_2_1_inlet')} - {data.get('acidity_2_2_inlet')}) "
                f"X {data.get('acidity_2_3_inlet')} X 5000",
                f"{data.get('acidity_ans2_inlet')} {data.get('acidity_param2_inlet')}",
                data.get('acidity_2_4_inlet')
            )

            # Acidity Reading 3
            add_formula_block(
                None,
                data.get('acidity_reading_3_inlet'),
                f"({data.get('acidity_3_1_inlet')} - {data.get('acidity_3_2_inlet')}) "
                f"X {data.get('acidity_3_3_inlet')} X 5000",
                f"{data.get('acidity_ans3_inlet')} {data.get('acidity_param3_inlet')}",
                data.get('acidity_3_4_inlet')
            )

            # Acidity Average (Weighted)
            if data.get('for_acidity1_inlet'):
                add_formula_block(
                    data.get('acidity_avg_head_inlet'),
                    None,
                    f"({data.get('for_acidity1_inlet')} X {data.get('for_acidity1_df_inlet')}) + "
                    f"({data.get('for_acidity2_inlet')} X {data.get('for_acidity2_df_inlet')}) + "
                    f"({data.get('for_acidity3_inlet')} X {data.get('for_acidity3_df_inlet')})",
                    f"{data.get('for_acidity_ans_inlet')} {data.get('for_acidity_param_inlet')}",
                    data.get('acidity_divi_inlet')
                )
                
                
        if data.get('acidity_1_1_outlet'):
            check_page_break(120)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Acidity Outlet Calculation:", 0, 1, 'L')

            # Acidity Reading 1
            add_formula_block(
                data.get('acidity_head_1_outlet'),
                data.get('acidity_reading_1_outlet'),
                f"({data.get('acidity_1_1_outlet')} - {data.get('acidity_1_2_outlet')}) "
                f"X {data.get('acidity_1_3_outlet')} X 5000",
                f"{data.get('acidity_ans1_outlet')} {data.get('acidity_param1_outlet')}",
                data.get('acidity_1_4_outlet')
            )

            # Acidity Reading 2
            add_formula_block(
                None,
                data.get('acidity_reading_2_outlet'),
                f"({data.get('acidity_2_1_outlet')} - {data.get('acidity_2_2_outlet')}) "
                f"X {data.get('acidity_2_3_outlet')} X 5000",
                f"{data.get('acidity_ans2_outlet')} {data.get('acidity_param2_outlet')}",
                data.get('acidity_2_4_outlet')
            )

            # Acidity Reading 3
            add_formula_block(
                None,
                data.get('acidity_reading_3_outlet'),
                f"({data.get('acidity_3_1_outlet')} - {data.get('acidity_3_2_outlet')}) "
                f"X {data.get('acidity_3_3_outlet')} X 5000",
                f"{data.get('acidity_ans3_outlet')} {data.get('acidity_param3_outlet')}",
                data.get('acidity_3_4_outlet')
            )

            # Acidity Average (Weighted)
            if data.get('for_acidity1_outlet'):
                add_formula_block(
                    data.get('acidity_avg_head_outlet'),
                    None,
                    f"({data.get('for_acidity1_outlet')} X {data.get('for_acidity1_df_outlet')}) + "
                    f"({data.get('for_acidity2_outlet')} X {data.get('for_acidity2_df_outlet')}) + "
                    f"({data.get('for_acidity3_outlet')} X {data.get('for_acidity3_df_outlet')})",
                    f"{data.get('for_acidity_ans_outlet')} {data.get('for_acidity_param_outlet')}",
                    data.get('acidity_divi_outlet')
                )


        # ALKALINITY CALCULATION
        if data.get('alkalinity_1_1_inlet'):
            check_page_break(120)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Alkalinity Calculation:", 0, 1, 'L')

            # Alkalinity Reading 1
            add_formula_block(
                data.get('alkalinity_head_1_inlet'),
                data.get('alkalinity_reading_1_inlet'),
                f"({data.get('alkalinity_1_1_inlet')} - {data.get('alkalinity_1_2_inlet')}) "
                f"X {data.get('alkalinity_1_3_inlet')} X 5000",
                f"{data.get('alkalinity_ans1_inlet')} {data.get('alkalinity_param1_inlet')}",
                data.get('alkalinity_1_4_inlet')
            )

            # Alkalinity Reading 2
            add_formula_block(
                None,
                data.get('alkalinity_reading_2_inlet'),
                f"({data.get('alkalinity_2_1_inlet')} - {data.get('alkalinity_2_2_inlet')}) "
                f"X {data.get('alkalinity_2_3_inlet')} X 5000",
                f"{data.get('alkalinity_ans2_inlet')} {data.get('alkalinity_param2_inlet')}",
                data.get('alkalinity_2_4_inlet')
            )

            # Alkalinity Reading 3
            add_formula_block(
                None,
                data.get('alkalinity_reading_3_inlet'),
                f"({data.get('alkalinity_3_1_inlet')} - {data.get('alkalinity_3_2_inlet')}) "
                f"X {data.get('alkalinity_3_3_inlet')} X 5000",
                f"{data.get('alkalinity_ans3_inlet')} {data.get('alkalinity_param3_inlet')}",
                data.get('alkalinity_3_4_inlet')
            )

            # Alkalinity Average (Weighted)
            if data.get('for_alkalinity1_inlet'):
                add_formula_block(
                    data.get('alkalinity_avg_head_inlet'),
                    None,
                    f"({data.get('for_alkalinity1_inlet')} X {data.get('for_alkalinity1_df_inlet')}) + "
                    f"({data.get('for_alkalinity2_inlet')} X {data.get('for_alkalinity2_df_inlet')}) + "
                    f"({data.get('for_alkalinity3_inlet')} X {data.get('for_alkalinity3_df_inlet')})",
                    f"{data.get('for_alkalinity_ans_inlet')} {data.get('for_alkalinity_param_inlet')}",
                    data.get('alkalinity_divi_inlet')
                )


            
            
            if data.get('alkalinity_1_1_outlet'):
                check_page_break(120)

                # Alkalinity Reading 1
                add_formula_block(
                    data.get('alkalinity_head_1_outlet'),
                    data.get('alkalinity_reading_1_outlet'),
                    f"({data.get('alkalinity_1_1_outlet')} - {data.get('alkalinity_1_2_outlet')}) "
                    f"X {data.get('alkalinity_1_3_outlet')} X 5000",
                    f"{data.get('alkalinity_ans1_outlet')} {data.get('alkalinity_param1_outlet')}",
                    data.get('alkalinity_1_4_outlet')
                )

                # Alkalinity Reading 2
                add_formula_block(
                    None,
                    data.get('alkalinity_reading_2_outlet'),
                    f"({data.get('alkalinity_2_1_outlet')} - {data.get('alkalinity_2_2_outlet')}) "
                    f"X {data.get('alkalinity_2_3_outlet')} X 5000",
                    f"{data.get('alkalinity_ans2_outlet')} {data.get('alkalinity_param2_outlet')}",
                    data.get('alkalinity_2_4_outlet')
                )

                # Alkalinity Reading 3
                add_formula_block(
                    None,
                    data.get('alkalinity_reading_3_outlet'),
                    f"({data.get('alkalinity_3_1_outlet')} - {data.get('alkalinity_3_2_outlet')}) "
                    f"X {data.get('alkalinity_3_3_outlet')} X 5000",
                    f"{data.get('alkalinity_ans3_outlet')} {data.get('alkalinity_param3_outlet')}",
                    data.get('alkalinity_3_4_outlet')
                )

                # Alkalinity Average (Weighted)
                if data.get('for_alkalinity1_outlet'):
                    add_formula_block(
                        data.get('alkalinity_avg_head_outlet'),
                        None,
                        f"({data.get('for_alkalinity1_outlet')} X {data.get('for_alkalinity1_df_outlet')}) + "
                        f"({data.get('for_alkalinity2_outlet')} X {data.get('for_alkalinity2_df_outlet')}) + "
                        f"({data.get('for_alkalinity3_outlet')} X {data.get('for_alkalinity3_df_outlet')})",
                        f"{data.get('for_alkalinity_ans_outlet')} {data.get('for_alkalinity_param_outlet')}",
                        data.get('alkalinity_divi_outlet')
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

        # CHLORIDE CALCULATION (INLET)
        if data.get('chloride_ans1_inlet'):

            check_page_break(120)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Chloride Calculation:", 0, 1, 'L')

            # Chloride Reading 1
            add_formula_block(
                data.get('chloride_head_1_inlet'),
                None,
                f"({data.get('chloride_1_1_inlet')} - {data.get('chloride_1_2_inlet')}) - "
                f"({data.get('chloride_1_3_inlet')} - {data.get('chloride_1_4_inlet')}) "
                f"X {data.get('chloride_1_5_inlet')} X 35450",
                f"{data.get('chloride_ans1_inlet')} {data.get('chloride_param1_inlet')}",
                data.get('chloride_1_6_inlet')
            )

        # Chloride Reading 2
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_1_inlet'):
                add_formula_block(
                    data.get('chloride_head_2_inlet'),
                    data.get('chloride_reading_1_inlet'),
                    f"({data.get('chloride_2_1_inlet')} - {data.get('chloride_2_2_inlet')}) - "
                    f"({data.get('chloride_2_3_inlet')} - {data.get('chloride_2_4_inlet')}) "
                    f"X {data.get('chloride_2_5_inlet')} X 35450",
                    f"{data.get('chloride_ans2_inlet', data.get('chloride_ans1_inlet', ''))} "
                    f"{data.get('chloride_param2_inlet', data.get('chloride_param1_inlet', ''))}",
                    data.get('chloride_2_6_inlet')
                )

            # Chloride Reading 3
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_2_inlet'):
                add_formula_block(
                    data.get('chloride_head_3_inlet'),
                    data.get('chloride_reading_2_inlet'),
                    f"({data.get('chloride_3_1_inlet')} - {data.get('chloride_3_2_inlet')}) - "
                    f"({data.get('chloride_3_3_inlet')} - {data.get('chloride_3_4_inlet')}) "
                    f"X {data.get('chloride_3_5_inlet')} X 35450",
                    f"{data.get('chloride_ans3_inlet', data.get('chloride_ans1_inlet', ''))} "
                    f"{data.get('chloride_param3_inlet', data.get('chloride_param1_inlet', ''))}",
                    data.get('chloride_3_6_inlet')
                )

            # Chloride Reading 4
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_3_inlet'):
                add_formula_block(
                    data.get('chloride_head_4_inlet'),
                    data.get('chloride_reading_3_inlet'),
                    f"({data.get('chloride_4_1_inlet')} - {data.get('chloride_4_2_inlet')}) - "
                    f"({data.get('chloride_4_3_inlet')} - {data.get('chloride_4_4_inlet')}) "
                    f"X {data.get('chloride_4_5_inlet')} X 35450",
                    f"{data.get('chloride_ans4_inlet', data.get('chloride_ans1_inlet', ''))} "
                    f"{data.get('chloride_param4_inlet', data.get('chloride_param1_inlet', ''))}",
                    data.get('chloride_4_6_inlet')
                )

            # Weighted Average
            chloride_formula_parts = []

            if data.get('chloride_reading_1_inlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride1_inlet')} X {data.get('for_chloride1_df_inlet')})"
                )

            if data.get('chloride_reading_2_inlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride2_inlet')} X {data.get('for_chloride2_df_inlet')})"
                )

            if data.get('chloride_reading_3_inlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride3_inlet')} X {data.get('for_chloride3_df_inlet')})"
                )

            chloride_avg_formula = " + ".join(chloride_formula_parts)

            if data.get('for_chloride1_inlet'):
                add_formula_block(
                    data.get('chloride_avg_head_inlet', "Chloride Average"),
                    None,
                    chloride_avg_formula,
                    f"{data.get('for_chloride_ans_inlet', '')} {data.get('for_chloride_param_inlet', '')}",
                    data.get('chloride_divi_inlet')
                )



        # CHLORIDE CALCULATION (outlet)
        if data.get('chloride_ans2_outlet'):

            check_page_break(20)

            # Chloride Reading 1
            # add_formula_block(
            #     data.get('chloride_head_2_outlet'),
            #     None,
            #     f"({data.get('chloride_1_1_outlet')} - {data.get('chloride_1_2_outlet')}) - "
            #     f"({data.get('chloride_1_3_outlet')} - {data.get('chloride_1_4_outlet')}) "
            #     f"X {data.get('chloride_1_5_outlet')} X 35450",
            #     f"{data.get('chloride_ans1_outlet')} {data.get('chloride_param1_outlet')}",
            #     data.get('chloride_1_6_outlet')
            # )

            # Chloride Reading 2
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_1_outlet'):
                add_formula_block(
                    data.get('chloride_head_2_outlet'),
                    data.get('chloride_reading_1_outlet'),
                    f"({data.get('chloride_2_1_outlet')} - {data.get('chloride_2_2_outlet')}) - "
                    f"({data.get('chloride_2_3_outlet')} - {data.get('chloride_2_4_outlet')}) "
                    f"X {data.get('chloride_2_5_outlet')} X 35450",
                    f"{data.get('chloride_ans2_outlet', data.get('chloride_ans1_outlet', ''))} "
                    f"{data.get('chloride_param2_outlet', data.get('chloride_param1_outlet', ''))}",
                    data.get('chloride_2_6_outlet')
                )

            # Chloride Reading 3
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_2_outlet'):
                add_formula_block(
                    data.get('chloride_head_3_outlet'),
                    data.get('chloride_reading_2_outlet'),
                    f"({data.get('chloride_3_1_outlet')} - {data.get('chloride_3_2_outlet')}) - "
                    f"({data.get('chloride_3_3_outlet')} - {data.get('chloride_3_4_outlet')}) "
                    f"X {data.get('chloride_3_5_outlet')} X 35450",
                    f"{data.get('chloride_ans3_outlet', data.get('chloride_ans1_outlet', ''))} "
                    f"{data.get('chloride_param3_outlet', data.get('chloride_param1_outlet', ''))}",
                    data.get('chloride_3_6_outlet')
                )

            # Chloride Reading 4
            pdf.set_font("Calibri", 'B', 11)
            if data.get('chloride_reading_3_outlet'):
                add_formula_block(
                    data.get('chloride_head_4_outlet'),
                    data.get('chloride_reading_3_outlet'),
                    f"({data.get('chloride_4_1_outlet')} - {data.get('chloride_4_2_outlet')}) - "
                    f"({data.get('chloride_4_3_outlet')} - {data.get('chloride_4_4_outlet')}) "
                    f"X {data.get('chloride_4_5_outlet')} X 35450",
                    f"{data.get('chloride_ans4_outlet', data.get('chloride_ans1_outlet', ''))} "
                    f"{data.get('chloride_param4_outlet', data.get('chloride_param1_outlet', ''))}",
                    data.get('chloride_4_6_outlet')
                )

            # Weighted Average
            chloride_formula_parts = []

            if data.get('chloride_reading_1_outlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride1_outlet')} X {data.get('for_chloride1_df_outlet')})"
                )

            if data.get('chloride_reading_2_outlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride2_outlet')} X {data.get('for_chloride2_df_outlet')})"
                )

            if data.get('chloride_reading_3_outlet'):
                chloride_formula_parts.append(
                    f"({data.get('for_chloride3_outlet')} X {data.get('for_chloride3_df_outlet')})"
                )

            chloride_avg_formula = " + ".join(chloride_formula_parts)

            if data.get('for_chloride1_outlet'):
                add_formula_block(
                    data.get('chloride_avg_head_outlet', "Chloride Average"),
                    None,
                    chloride_avg_formula,
                    f"{data.get('for_chloride_ans_outlet', '')} {data.get('for_chloride_param_outlet', '')}",
                    data.get('chloride_divi_outlet')
                )



        # pdf.set_font("Calibri", 'B', size=10)
        # pdf.cell(0,5,"Chloride CRM Calculations",ln=True)
        pdf.set_font("Calibri", '', size=10)
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(chloride_crm_\d+_\d+)_1$', key)
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
            #     pdf.set_font("Calibri", 'B', 11)
            #     pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # # ---------- CRM STANDARDS ----------
            # pdf.set_font("Calibri", '', 10)

            # for i in range(1, 4):
            #     std = data.get(f"{base}_crm_standard_{i}")
            #     srm = data.get(f"{base}_crm_srm{i}")

            #     if std or srm:
            #         pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            # pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
                add_average_formula_section(
                    check_key=f"{base}_1",
                    section_title="",
                    head_key=f"{base}_head",
                    ans_key=f"{base}_ans",
                    param_key=f"{base}_param",
                    div_key=f"{base}_divi"
                )
                pdf.ln(-4)
                
        # Calcium Calculation Section
        if data.get('calcium_head_inlet') or data.get('calcium_head_1_inlet') or data.get('calcium_head_2_inlet'):
            check_page_break(100)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Calcium Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            # Method 1: Direct Calcium Calculation (APHA 3111-B)
            if data.get('calcium_ans_1_inlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_inlet', 'Calcium: (APHA 3111-B) (Inlet)'), border=False, align="L", ln=True)

                pdf.set_x(10)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(30, 6, "Formula = ", border=False, align="L")

                formula_parts = []
                for i in range(1, 4):
                    val = data.get(f'for_calcium1_{i}_inlet', '')
                    df = data.get(f'for_calcium1_{i}_df_inlet', '')
                    if val and df:
                        formula_parts.append(f"({val} X {df})")

                if formula_parts:
                    formula_content = " + ".join(formula_parts)
                    result_text = f"{data.get('calcium_ans_1_inlet', '')} {data.get('calcium_param_1_inlet', 'mg/L')}"
                    divisor = data.get('calcium_divi_inlet', '3')
                    add_formula_with_line(formula_content, result_text, divisor, 25)
                
            # Method 2: ASTM D 1126
            if data.get('cal_r1_final_inlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_1_inlet', 'Calcium: (ASTM D 1126) (Inlet)'), border=False, align="L", ln=True)

                calcium_sections_1 = [
                    ('cal_r1_inlet', 'cal_r1_final_inlet', 'cal_r1_initial_inlet', 'cal_r1_multiply_inlet',
                    'cal_r1_divi_inlet', 'cal_r1_ans_inlet', 'cal_r1_param_inlet',
                    'cal_r1_cah_inlet', 'cal_r1_df_inlet', 'cal_r1_cah1_inlet', 'cal_r1_cah_param_inlet'),

                    ('cal_r2_inlet', 'cal_r2_final_inlet', 'cal_r2_initial_inlet', 'cal_r2_multiply_inlet',
                    'cal_r2_divi_inlet', 'cal_r2_ans_inlet', 'cal_r2_param_inlet',
                    'cal_r2_cah_inlet', 'cal_r2_df_inlet', 'cal_r2_cah1_inlet', 'cal_r2_cah_param_inlet'),

                    ('cal_r3_inlet', 'cal_r3_final_inlet', 'cal_r3_initial_inlet', 'cal_r3_multiply_inlet',
                    'cal_r3_divi_inlet', 'cal_r3_ans_inlet', 'cal_r3_param_inlet',
                    'cal_r3_cah_inlet', 'cal_r3_df_inlet', 'cal_r3_cah1_inlet', 'cal_r3_cah_param_inlet')
                ]

                for section in calcium_sections_1:
                    (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                    cah_key, df_key, cah1_key, cah_param_key) = section
                    
                    if data.get(final_key):
                        check_page_break(40)

                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'),
                                border=False, align="L", ln=True)

                        pdf.set_x(10)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(20, 6, "Formula:", border=False, align="L")

                        formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                        result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                        divisor = data.get(divi_key, '50')

                        add_formula_with_line(formula_text, result_text, divisor, 25)

                        if data.get(cah_key) and data.get(df_key):
                            pdf.set_x(25)
                            pdf.cell(
                                0, 6,
                                f"{data.get(cah_key, '')} X {data.get(df_key, '')} = "
                                f"{data.get(cah1_key, '')} {data.get(cah_param_key, 'mg/L')}",
                                align="L", ln=True
                            )

                        pdf.ln(4)

                if data.get('cal_avg_ans1_inlet'):
                    check_page_break(20)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get('cal_avg_head_inlet', 'Average of Calcium (ASTM D 1126) (Inlet):'), border=False, align="L", ln=True)

                    formula_text = f"{data.get('cal_avg_ans1_inlet', '')} + {data.get('cal_avg_ans2_inlet', '')} + {data.get('cal_avg_ans3_inlet', '')}"
                    result_text = f"{data.get('cal_avg_final_ans_inlet', '')} {data.get('cal_avg_param_inlet', 'mg/L')}"
                    divisor = data.get('cal_avg_divi_inlet', '3')

                    add_formula_with_line(formula_text, result_text, divisor, 40)

            # Method 3: APHA 3500 Ca-B (if data exists)
            if data.get('ch_r1_final_inlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_2_inlet', 'Calcium: (APHA 3500 Ca-B) Calculation Method'),
                        border=False, align="L", ln=True)

                calcium_sections_2 = [
                    ('ch_r1_inlet', 'ch_r1_final_inlet', 'ch_r1_initial_inlet', 'ch_r1_multiply_inlet',
                    'ch_r1_divi_inlet', 'ch_r1_ans_inlet', 'ch_r1_param_inlet',
                    'ch_r1_cah_inlet', 'ch_r1_df_inlet', 'ch_r1_cah1_inlet', 'ch_r1_cah_param_inlet',
                    'ch_c1_ans1_inlet', 'ch_c1_divi_inlet', 'ch_c1_multiply_inlet',
                    'ch_c1_ans_inlet', 'ch_c1_param_inlet'),

                    ('ch_r2_inlet', 'ch_r2_final_inlet', 'ch_r2_initial_inlet', 'ch_r2_multiply_inlet',
                    'ch_r2_divi_inlet', 'ch_r2_ans_inlet', 'ch_r2_param_inlet',
                    'ch_r2_cah_inlet', 'ch_r2_df_inlet', 'ch_r2_cah1_inlet', 'ch_r2_cah_param_inlet',
                    'ch_c2_ans1_inlet', 'ch_c2_divi_inlet', 'ch_c2_multiply_inlet',
                    'ch_c2_ans_inlet', 'ch_c2_param_inlet'),

                    ('ch_r3_inlet', 'ch_r3_final_inlet', 'ch_r3_initial_inlet', 'ch_r3_multiply_inlet',
                    'ch_r3_divi_inlet', 'ch_r3_ans_inlet', 'ch_r3_param_inlet',
                    'ch_r3_cah_inlet', 'ch_r3_df_inlet', 'ch_r3_cah1_inlet', 'ch_r3_cah_param_inlet',
                    'ch_c3_ans1_inlet', 'ch_c3_divi_inlet', 'ch_c3_multiply_inlet',
                    'ch_c3_ans_inlet', 'ch_c3_param_inlet')
                ]

                for section in calcium_sections_2:
                    (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                    cah_key, df_key, cah1_key, cah_param_key,
                    cal_ans1_key, cal_divi_key, cal_multiply_key, cal_ans_key, cal_param_key) = section

                    if data.get(final_key):
                        check_page_break(40)

                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'),
                                border=False, align="L", ln=True)

                        formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                        result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                        divisor = data.get(divi_key, '50')

                        add_formula_with_line(formula_text, result_text, divisor, 45)

                if data.get('ch_avg_ans1_inlet'):
                    check_page_break(20)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get('ch_avg_head_inlet', 'Average of Calcium:'), border=False, align="L", ln=True)
                    pdf.set_font("Calibri", '', 10)

                    formula_text = f"{data.get('ch_avg_ans1_inlet', '')} + {data.get('ch_avg_ans2_inlet', '')} + {data.get('ch_avg_ans3_inlet', '')}"
                    result_text = f"{data.get('ch_avg_final_ans_inlet', '')} {data.get('ch_avg_param_inlet', 'mg/L')}"
                    divisor = data.get('ch_avg_divi_inlet', '3')

                    add_formula_with_line(formula_text, result_text, divisor, 40)

        if data.get('calcium_head_outlet') or data.get('calcium_head_1_outlet') or data.get('calcium_head_2_outlet'):
            check_page_break(30)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Calcium Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            # Method 1: Direct Calcium Calculation (APHA 3111-B)
            if data.get('calcium_ans_1_outlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_outlet', 'Calcium: (APHA 3111-B) (Outlet)'), border=False, align="L", ln=True)

                pdf.set_x(10)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(30, 6, "Formula = ", border=False, align="L")

                formula_parts = []
                for i in range(1, 4):
                    val = data.get(f'for_calcium1_{i}_outlet', '')
                    df = data.get(f'for_calcium1_{i}_df_outlet', '')
                    if val and df:
                        formula_parts.append(f"({val} X {df})")

                if formula_parts:
                    formula_content = " + ".join(formula_parts)
                    result_text = f"{data.get('calcium_ans_1_outlet', '')} {data.get('calcium_param_1_outlet', 'mg/L')}"
                    divisor = data.get('calcium_divi_outlet', '3')
                    add_formula_with_line(formula_content, result_text, divisor, 25)
                
            # Method 2: ASTM D 1126
            if data.get('cal_r1_final_outlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_1_outlet', 'Calcium: (ASTM D 1126) (Outlet)'), border=False, align="L", ln=True)

                calcium_sections_1 = [
                    ('cal_r1_outlet', 'cal_r1_final_outlet', 'cal_r1_initial_outlet', 'cal_r1_multiply_outlet',
                    'cal_r1_divi_outlet', 'cal_r1_ans_outlet', 'cal_r1_param_outlet',
                    'cal_r1_cah_outlet', 'cal_r1_df_outlet', 'cal_r1_cah1_outlet', 'cal_r1_cah_param_outlet'),

                    ('cal_r2_outlet', 'cal_r2_final_outlet', 'cal_r2_initial_outlet', 'cal_r2_multiply_outlet',
                    'cal_r2_divi_outlet', 'cal_r2_ans_outlet', 'cal_r2_param_outlet',
                    'cal_r2_cah_outlet', 'cal_r2_df_outlet', 'cal_r2_cah1_outlet', 'cal_r2_cah_param_outlet'),

                    ('cal_r3_outlet', 'cal_r3_final_outlet', 'cal_r3_initial_outlet', 'cal_r3_multiply_outlet',
                    'cal_r3_divi_outlet', 'cal_r3_ans_outlet', 'cal_r3_param_outlet',
                    'cal_r3_cah_outlet', 'cal_r3_df_outlet', 'cal_r3_cah1_outlet', 'cal_r3_cah_param_outlet')
                ]

                for section in calcium_sections_1:
                    (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                    cah_key, df_key, cah1_key, cah_param_key) = section

                    if data.get(final_key):
                        check_page_break(40)

                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'),
                                border=False, align="L", ln=True)

                        pdf.set_x(10)
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(20, 6, "Formula:", border=False, align="L")

                        formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                        result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                        divisor = data.get(divi_key, '50')

                        add_formula_with_line(formula_text, result_text, divisor, 25)

                        if data.get(cah_key) and data.get(df_key):
                            pdf.set_x(25)
                            pdf.cell(
                                0, 6,
                                f"{data.get(cah_key, '')} X {data.get(df_key, '')} = "
                                f"{data.get(cah1_key, '')} {data.get(cah_param_key, 'mg/L')}",
                                align="L", ln=True
                            )

                        pdf.ln(4)

                if data.get('cal_avg_ans1_outlet'):
                    check_page_break(20)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get('cal_avg_head_outlet', 'Average of Calcium (ASTM D 1126) (Outlet):'), border=False, align="L", ln=True)

                    formula_text = f"{data.get('cal_avg_ans1_outlet', '')} + {data.get('cal_avg_ans2_outlet', '')} + {data.get('cal_avg_ans3_outlet', '')}"
                    result_text = f"{data.get('cal_avg_final_ans_outlet', '')} {data.get('cal_avg_param_outlet', 'mg/L')}"
                    divisor = data.get('cal_avg_divi_outlet', '3')

                    add_formula_with_line(formula_text, result_text, divisor, 40)

            # Method 3: APHA 3500 Ca-B
            if data.get('ch_r1_final_outlet'):
                check_page_break(25)

                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('calcium_head_2_outlet', 'Calcium: (APHA 3500 Ca-B) Calculation Method'),
                        border=False, align="L", ln=True)

                calcium_sections_2 = [
                    ('ch_r1_outlet', 'ch_r1_final_outlet', 'ch_r1_initial_outlet', 'ch_r1_multiply_outlet', 'ch_r1_divi_outlet', 'ch_r1_ans_outlet', 'ch_r1_param_outlet',
                    'ch_r1_cah_outlet', 'ch_r1_df_outlet', 'ch_r1_cah1_outlet', 'ch_r1_cah_param_outlet',
                    'ch_c1_ans1_outlet', 'ch_c1_divi_outlet', 'ch_c1_multiply_outlet', 'ch_c1_ans_outlet', 'ch_c1_param_outlet'),

                    ('ch_r2_outlet', 'ch_r2_final_outlet', 'ch_r2_initial_outlet', 'ch_r2_multiply_outlet', 'ch_r2_divi_outlet', 'ch_r2_ans_outlet', 'ch_r2_param_outlet',
                    'ch_r2_cah_outlet', 'ch_r2_df_outlet', 'ch_r2_cah1_outlet', 'ch_r2_cah_param_outlet',
                    'ch_c2_ans1_outlet', 'ch_c2_divi_outlet', 'ch_c2_multiply_outlet', 'ch_c2_ans_outlet', 'ch_c2_param_outlet'),

                    ('ch_r3_outlet', 'ch_r3_final_outlet', 'ch_r3_initial_outlet', 'ch_r3_multiply_outlet', 'ch_r3_divi_outlet', 'ch_r3_ans_outlet', 'ch_r3_param_outlet',
                    'ch_r3_cah_outlet', 'ch_r3_df_outlet', 'ch_r3_cah1_outlet', 'ch_r3_cah_param_outlet',
                    'ch_c3_ans1_outlet', 'ch_c3_divi_outlet', 'ch_c3_multiply_outlet', 'ch_c3_ans_outlet', 'ch_c3_param_outlet')
                ]

                for section in calcium_sections_2:
                    (reading_key, final_key, initial_key, multiply_key, divi_key, ans_key, param_key,
                    cah_key, df_key, cah1_key, cah_param_key,
                    cal_ans1_key, cal_divi_key, cal_multiply_key, cal_ans_key, cal_param_key) = section

                    if data.get(final_key):
                        check_page_break(40)

                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data.get(reading_key, f'Reading {reading_key[-1]}'),
                                border=False, align="L", ln=True)

                        formula_text = f"({data.get(final_key, '')} - {data.get(initial_key, '')}) X {data.get(multiply_key, '1000')}"
                        result_text = f"{data.get(ans_key, '')} {data.get(param_key, 'mg/L')}"
                        divisor = data.get(divi_key, '50')

                        add_formula_with_line(formula_text, result_text, divisor, 45)

                if data.get('ch_avg_ans1_outlet'):
                    check_page_break(20)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data.get('ch_avg_head_outlet', 'Average of Calcium:'), border=False, align="L", ln=True)
                    pdf.set_font("Calibri", '', 10)

                    formula_text = f"{data.get('ch_avg_ans1_outlet', '')} + {data.get('ch_avg_ans2_outlet', '')} + {data.get('ch_avg_ans3_outlet', '')}"
                    result_text = f"{data.get('ch_avg_final_ans_outlet', '')} {data.get('ch_avg_param_outlet', 'mg/L')}"
                    divisor = data.get('ch_avg_divi_outlet', '3')

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
            
            
        
        if data.get('sulphide_1_final_ans_inlet'):
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0, 6, data.get('sulphide_head_inlet'), border=False, align="L", ln=True)
            if data.get('sulphide_read_1_inlet'):
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"{data.get('sulphide_read_1_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_1_a_inlet')}",ln=2)
                pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_1_b_inlet')}",ln=2)
                pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_1_c_inlet')}",ln=2)
                pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_1_d_inlet')}",ln=2)
                pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_1_vs_inlet')}",ln=2)
                add_formula_block(
                    None,
                    None,
                    f"({data.get('sulphide_1_final_a_inlet')} X {data.get('sulphide_1_final_b_inlet')}) - ({data.get('sulphide_1_final_c_inlet')} X {data.get('sulphide_1_final_d_inlet')}) X 16000",
                    
                    f"{data['sulphide_1_final_ans_inlet']} {data.get('sulphide_1_param_inlet')}",
                    data.get('sulphide_1_divi_inlet')
                )
            
            
            if data.get('sulphide_read_2_inlet'):
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"{data.get('sulphide_read_2_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_2_a_inlet')}",ln=2)
                pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_2_b_inlet')}",ln=2)
                pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_2_c_inlet')}",ln=2)
                pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_2_d_inlet')}",ln=2)
                pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_2_vs_inlet')}",ln=2)
                add_formula_block(
                    None,
                    None,
                    f"({data.get('sulphide_2_final_a_inlet')} X {data.get('sulphide_2_final_b_inlet')}) - ({data.get('sulphide_2_final_c_inlet')} X {data.get('sulphide_2_final_d_inlet')}) X 16000",
                    
                    f"{data['sulphide_2_final_ans_inlet']} {data.get('sulphide_2_param_inlet')}",
                    data.get('sulphide_2_divi_inlet')
                )
            
            
            if data.get('sulphide_read_3_inlet'):
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"{data.get('sulphide_read_3_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_3_a_inlet')}",ln=2)
                pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_3_b_inlet')}",ln=2)
                pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_3_c_inlet')}",ln=2)
                pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_3_d_inlet')}",ln=2)
                pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_3_vs_inlet')}",ln=2)
                add_formula_block(
                    None,
                    None,
                    f"({data.get('sulphide_3_final_a_inlet')} X {data.get('sulphide_3_final_b_inlet')}) - ({data.get('sulphide_3_final_c_inlet')} X {data.get('sulphide_3_final_d_inlet')}) X 16000",
                    
                    f"{data['sulphide_3_final_ans_inlet']} {data.get('sulphide_3_param_inlet')}",
                    data.get('sulphide_3_divi_inlet')
                )
                
                # ------------------ Sulphide Average (Inlet) ------------------
            check_page_break(20)
            formula_parts = []

            if data.get('answer1_inlet'):
                formula_parts.append(
                    f"({data.get('answer1_inlet')} X {data.get('answer1_df_inlet')})"
                )

            if data.get('answer2_inlet'):
                formula_parts.append(
                    f"({data.get('answer2_inlet')} X {data.get('answer2_df_inlet')})"
                )

            if data.get('answer3_inlet'):
                formula_parts.append(
                    f"({data.get('answer3_inlet')} X {data.get('answer3_df_inlet')})"
                )

            average_formula = " + ".join(formula_parts)
            if formula_parts:
                check_page_break(20)
                add_formula_block(
                    data.get('sulphide_avg_head_inlet'),
                    None,
                    average_formula,
                    f"{data.get('for_sulphide_avg_ans_inlet')} {data.get('for_sulphide_avg_param_inlet')}",
                    data.get('sulphide_avg_divi_inlet')
                )
            
            check_page_break(20)
            if data.get('sulphide_1_final_ans_outlet'):
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 6, data.get('sulphide_head_outlet'), border=False, align="L", ln=True)
                if data.get('sulphide_read_1_outlet'):
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0,4,f"{data.get('sulphide_read_1_outlet')}",ln=True)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_1_a_outlet')}",ln=2)
                    pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_1_b_outlet')}",ln=2)
                    pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_1_c_outlet')}",ln=2)
                    pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_1_d_outlet')}",ln=2)
                    pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_1_vs_outlet')}",ln=2)
                    add_formula_block(
                        None,
                        None,
                        f"({data.get('sulphide_1_final_a_outlet')} X {data.get('sulphide_1_final_b_outlet')}) - ({data.get('sulphide_1_final_c_outlet')} X {data.get('sulphide_1_final_d_outlet')}) X 16000",
                        
                        f"{data['sulphide_1_final_ans_outlet']} {data.get('sulphide_1_param_outlet')}",
                        data.get('sulphide_1_divi_outlet')
                    )
                
                
                if data.get('sulphide_read_2_outlet'):
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0,4,f"{data.get('sulphide_read_2_outlet')}",ln=True)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_2_a_outlet')}",ln=2)
                    pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_2_b_outlet')}",ln=2)
                    pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_2_c_outlet')}",ln=2)
                    pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_2_d_outlet')}",ln=2)
                    pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_2_vs_outlet')}",ln=2)
                    add_formula_block(
                        None,
                        None,
                        f"({data.get('sulphide_2_final_a_outlet')} X {data.get('sulphide_2_final_b_outlet')}) - ({data.get('sulphide_2_final_c_outlet')} X {data.get('sulphide_2_final_d_outlet')}) X 16000",
                        
                        f"{data['sulphide_2_final_ans_outlet']} {data.get('sulphide_2_param_outlet')}",
                        data.get('sulphide_2_divi_outlet')
                    )
                
                
                if data.get('sulphide_read_3_outlet'):
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0,4,f"{data.get('sulphide_read_3_outlet')}",ln=True)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide_3_a_outlet')}",ln=2)
                    pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide_3_b_outlet')}",ln=2)
                    pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide_3_c_outlet')}",ln=2)
                    pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide_3_d_outlet')}",ln=2)
                    pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide_3_vs_outlet')}",ln=2)
                    add_formula_block(
                        None,
                        None,
                        f"({data.get('sulphide_3_final_a_outlet')} X {data.get('sulphide_3_final_b_outlet')}) - ({data.get('sulphide_3_final_c_outlet')} X {data.get('sulphide_3_final_d_outlet')}) X 16000",
                        
                        f"{data['sulphide_3_final_ans_outlet']} {data.get('sulphide_3_param_outlet')}",
                        data.get('sulphide_3_divi_outlet')
                    )
                    
                    # ------------------ Sulphide Average (outlet) ------------------

                formula_parts = []

                if data.get('answer1_outlet'):
                    formula_parts.append(
                        f"({data.get('answer1_outlet')} X {data.get('answer1_df_outlet')})"
                    )

                if data.get('answer2_outlet'):
                    formula_parts.append(
                        f"({data.get('answer2_outlet')} X {data.get('answer2_df_outlet')})"
                    )

                if data.get('answer3_outlet'):
                    formula_parts.append(
                        f"({data.get('answer3_outlet')} X {data.get('answer3_df_outlet')})"
                    )

                average_formula = " + ".join(formula_parts)

                if formula_parts:
                    add_formula_block(
                        data.get('sulphide_avg_head_outlet'),
                        None,
                        average_formula,
                        f"{data.get('for_sulphide_avg_ans_outlet')} {data.get('for_sulphide_avg_param_outlet')}",
                        data.get('sulphide_avg_divi_outlet')
                    )
                pdf.ln(3)
                
                    

            for key in sorted(data.keys()):
                # Match keys like: sulphide-3.1-crm_head
                match = re.match(r'(sulphide-\d+\.\d+)-crm_head$', key)

                if not match:
                    continue

                base = match.group(1)  # sulphide-3.1

                # Skip if CRM head empty
                if not data.get(f"{base}-crm_head"):
                    continue

                # ---------- HEADER ----------
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 4, f"{data.get(f'{base}-crm_head')}", ln=True)

                pdf.set_font("Calibri", '', 10)

                # ---------- VALUES ----------
                pdf.cell(0, 4, f"A mL iodine solutions = {data.get(f'{base}-a')}", ln=2)
                pdf.cell(0, 4, f"B normality iodine solution = {data.get(f'{base}-b')}", ln=2)
                pdf.cell(0, 4, f"C mL Na2S2O3 solution = {data.get(f'{base}-c')}", ln=2)
                pdf.cell(0, 4, f"D normality of Na2S2O3 solution = {data.get(f'{base}-d')}", ln=2)
                pdf.cell(0, 4, f"Volume of Sample = {data.get(f'{base}-vs')}", ln=2)

                # ---------- FORMULA ----------
                formula_text = (
                    f"({data.get(f'{base}-final-a')} X {data.get(f'{base}-final-b')}) - "
                    f"({data.get(f'{base}-final-c')} X {data.get(f'{base}-final-d')}) X 16000"
                )

                result_text = (
                    f"{data.get(f'{base}_final_ans')} {data.get(f'{base}_param')}"
                )

                add_formula_block(
                    None,
                    None,
                    formula_text,
                    result_text,
                    data.get(f"{base}-divi")
                )

                    
            
            if data.get('bod_1_ans_inlet'):
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,8,f"BOD Calculations",ln=True)
                pdf.cell(0,6,f"{data.get('bod_head_1_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.ln(3)
                pdf.cell(0,4,f"{data.get('bod_1_inlet')} X {data.get('bod_1_df_inlet')} = {data.get('bod_1_ans_inlet')} {data.get('bod_1_param_inlet')}",ln=True)
            if data.get('bod_ans_inlet'):
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"{data.get('bod_head_2_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                add_formula_block(
                    None,
                    None,
                    data.get('bod_sv_inlet'),
                    data.get('bod_1_p_inlet'),
                    data.get('bod_tv_inlet'),
                    
                    
                )
                
                add_formula_block(
                    None,
                    None,
                    f"({data.get('bod_initial_inlet')} - {data.get('bod_final_inlet')}) - "
                    f"{{({data.get('bod_seed_1_inlet')} - {data.get('bod_seed_2_inlet')}) X {data.get('bod_seed_vol_inlet')}}}",
                    f"{data.get('bod_ans_inlet')} {data.get('bod_param_inlet')}",
                    data.get('bod_divi_inlet')
                )
                
                
            if data.get('bod_1_ans_outlet'):
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"BOD Calculations (Outlet)",ln=True)
                pdf.cell(0,4,f"{data.get('bod_head_1_outlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.ln(3)
                pdf.cell(0,4,f"{data.get('bod_1_outlet')} X {data.get('bod_1_df_outlet')} = {data.get('bod_1_ans_outlet')} {data.get('bod_1_param_outlet')}",ln=True)
            if data.get('bod_ans_outlet'):
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0,4,f"{data.get('bod_head_2_inlet')}",ln=True)
                pdf.set_font("Calibri", '', 10)
                add_formula_block(
                    None,
                    None,
                    data.get('bod_sv_outlet'),
                    data.get('bod_1_p_outlet'),
                    data.get('bod_tv_outlet'),
                    
                    
                )
                
                add_formula_block(
                    None,
                    None,
                    f"({data.get('bod_initial_outlet')} - {data.get('bod_final_outlet')}) - "
                    f"{{({data.get('bod_seed_1_outlet')} - {data.get('bod_seed_2_outlet')}) X {data.get('bod_seed_vol_outlet')}}}",
                    f"{data.get('bod_ans_outlet')} {data.get('bod_param_outlet')}",
                    data.get('bod_divi_outlet')
                )

            
            for key in sorted(data.keys()):
                # match keys like: biological_oxygen_demandbod5_crm_4_1_final_ans
                match = re.match(r'(biological_oxygen_demandbod5_crm_\d+_\d+)_final_ans$', key)
                if not match:
                    continue

                base = match.group(1)

                if not data.get(f"{base}_final_ans"):
                    continue

                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 10)
                pdf.cell(0, 4, data.get(f"{base}_head"), ln=True)

                # ---------------- HACH PART ----------------
                if data.get(f'{base}_hach_ans'):
                    pdf.ln(5)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 4, f"{data.get(f'{base}_hach_label')}", ln=True)
                    pdf.set_font("Calibri", '', 10)
                    pdf.ln(3)
                    
                    pdf.cell(
                        0, 4,
                        f"{data.get(f'{base}_hach_r')} X {data.get(f'{base}_hach_df')} = "
                        f"{data.get(f'{base}_hach_ans')} {data.get(f'{base}_hach_unit')}",
                        ln=True
                    )

                # ---------------- BOD5 PART ----------------
                if data.get(f"{base}_final_ans"):
                    pdf.ln(5)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 4, f"{data.get(f'{base}_bod5_label')}", ln=True)
                    pdf.set_font("Calibri", '', 10)

                    add_formula_block(
                        None,
                        None,
                        data.get(f"{base}_sv"),
                        data.get(f"{base}_p"),
                        data.get(f"{base}_tv"),
                    )

                    add_formula_block(
                        None,
                        None,
                        f"({data.get(f'{base}_ido')} - {data.get(f'{base}_fdo')}) - "
                        f"{{({data.get(f'{base}_sido')} - {data.get(f'{base}_sfdo')}) X "
                        f"{data.get(f'{base}_seed_vol')}}}",
                        f"{data.get(f'{base}_final_ans')} {data.get(f'{base}_final_unit')}",
                        data.get(f"{base}_divi")
                    )

                
            if data.get('toxic_ans_inlet'):
                check_page_break(20)
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0,4,"Toxic Metals Inlet Calculations",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.ln(3)
                pdf.cell(0,4,f"{data.get('toxic_1_inlet')} = {data.get('toxic_1_1_inlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_2_inlet')} = {data.get('toxic_2_1_inlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_3_inlet')} = {data.get('toxic_3_1_inlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_4_inlet')} = {data.get('toxic_4_1_inlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_5_inlet')} = {data.get('toxic_5_1_inlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_6_inlet')} = {data.get('toxic_6_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_7_inlet')} = {data.get('toxic_7_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_8_inlet')} = {data.get('toxic_8_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_9_inlet')} = {data.get('toxic_9_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_10_inlet')} = {data.get('toxic_10_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_11_inlet')} = {data.get('toxic_11_1_inlet')}",ln=2)
                check_page_break(20)
                pdf.ln(3)
                add_formula_block(
                        None,
                        None,
                        f"{data.get('toxic_r1_inlet')} + {data.get('toxic_r2_inlet')} + {data.get('toxic_r3_inlet')} + {data.get('toxic_r4_inlet')} + {data.get('toxic_r5_inlet')} + {data.get('toxic_r6_inlet')} + {data.get('toxic_r7_inlet')} + {data.get('toxic_r8_inlet')} + {data.get('toxic_r9_inlet')} + {data.get('toxic_r10_inlet')} + {data.get('toxic_r11_inlet')}",
                        f"{data.get('toxic_ans_inlet')} {data.get('toxic_param_inlet')}",
                        data.get('toxic_divi_inlet')
                    )
            
            
            if data.get('toxic_ans_outlet'):
                check_page_break(20)
                pdf.ln(5)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0,4,"Toxic Metals Outlet Calculations",ln=True)
                pdf.set_font("Calibri", '', 10)
                pdf.ln(3)
                pdf.cell(0,4,f"{data.get('toxic_1_outlet')} = {data.get('toxic_1_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_2_outlet')} = {data.get('toxic_2_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_3_outlet')} = {data.get('toxic_3_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_4_outlet')} = {data.get('toxic_4_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_5_outlet')} = {data.get('toxic_5_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_6_outlet')} = {data.get('toxic_6_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_7_outlet')} = {data.get('toxic_7_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_8_outlet')} = {data.get('toxic_8_1_outlet')}",ln=2)
                check_page_break(20)
                pdf.cell(0,4,f"{data.get('toxic_9_outlet')} = {data.get('toxic_9_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_10_outlet')} = {data.get('toxic_10_1_outlet')}",ln=2)
                pdf.cell(0,4,f"{data.get('toxic_11_outlet')} = {data.get('toxic_11_1_outlet')}",ln=2)
                pdf.ln(3)
                add_formula_block(
                        None,
                        None,
                        f"{data.get('toxic_r1_outlet')} + {data.get('toxic_r2_outlet')} + {data.get('toxic_r3_outlet')} + {data.get('toxic_r4_outlet')} + {data.get('toxic_r5_outlet')} + {data.get('toxic_r6_outlet')} + {data.get('toxic_r7_outlet')} + {data.get('toxic_r8_outlet')} + {data.get('toxic_r9_outlet')} + {data.get('toxic_r10_outlet')} + {data.get('toxic_r11_outlet')}",
                        f"{data.get('toxic_ans_outlet')} {data.get('toxic_param_outlet')}",
                        data.get('toxic_divi_outlet')
                    )
                
        
        
    else:
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
            match = re.match(r'(total_dissolved_solids_crm_\d+_\d+)_bw$', key)
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
        
        
        if data.get('tss_final_ans'):
            check_page_break(100)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Total Suspended Solids (TSS) Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            tss_sections = [
                ('tss_head_1', 'iw1', 'FW05', 'tss_vs1', 'tss_ans1', 'tss_ans_param', ''),
                ('tss_head_2', 'iw2', 'FW10', 'tss_vs2', 'tss_ans2', 'tss_ans_param_2', 'tss_read_1'),
                ('tss_head_3', 'iw3', 'FW15', 'tss_vs3', 'tss_ans3', 'tss_ans_param_3', 'tss_read_2'),
                ('tss_head_4', 'iw4', 'FW20', 'tss_vs4', 'tss_ans4', 'tss_ans_param_4', 'tss_read_3'),
            ]

            for head, iw, fw, vs, ans, param, read in tss_sections:
                if data.get(head):
                    check_page_break(25)

                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(0, 6, data[head], ln=True)

                    if read and data.get(read):
                        pdf.cell(0, 6, data[read], ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", '', 10)
                    pdf.cell(35, 6, "Initial Weight  = ")
                    pdf.cell(0, 6, data.get(iw, ''), ln=True)

                    fw_num = int(fw[2:4])
                    fw_values = [
                        data.get(f'FW{i:02d}', '')
                        for i in range(fw_num - 4, fw_num + 1)
                        if data.get(f'FW{i:02d}')
                    ]

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Final Weight   = ")
                    pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Value of Sample = ")
                    pdf.cell(0, 6, data.get(vs, ''), ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(35, 6, "Formula :", ln=True)

                    pdf.set_font("Calibri", '', 10)
                    formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                    result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                    add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)

            # ---------- FINAL AVERAGE ----------
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, "Average of Total Suspended Solids:", ln=True)
            pdf.set_font("Calibri", '', 10)

            final_text = (
                f"{data.get('tss_final_ans1','')} + "
                f"{data.get('tss_final_ans2','')} + "
                f"{data.get('tss_final_ans3','')}"
            )
            result_text = f"{data.get('tss_final_ans')} {data.get('tss_final_param','')}"

            add_formula_with_line(
                final_text,
                result_text,
                data.get('tss_final_divi', '3'),
                40
            )

            pdf.ln(-4)


        
        for key in sorted(data.keys()):

            # Match keys like: tds_crm_36_1_bw
            match = re.match(r'(total_suspended_solids_tss_crm_\d+_\d+)_bw$', key)
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

            # ---------- FORMULA (USE ONLY LAST AW) ----------
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

        
        
        
        if data.get('oil_final_ans'):
            check_page_break(100)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 4, "Oil & Grease Calculation:", 0, 1, 'L')
            pdf.set_font("Calibri", size=10)
            pdf.ln(3)

            oil_sections = [
                ('oil_head_1', 'oil_iw1', 'oil_FW05', 'oil_vs1', 'oil_ans1', 'oil_ans_param', 'oil_read_1'),
                ('',          'oil_iw2', 'oil_FW10', 'oil_vs2', 'oil_ans2', 'oil_ans_param_2', 'oil_read_2'),
                ('',          'oil_iw3', 'oil_FW15', 'oil_vs3', 'oil_ans3', 'oil_ans_param_3', 'oil_read_3'),
            ]

            for head, iw, fw, vs, ans, param, read in oil_sections:
                if data.get(iw):
                    check_page_break(25)

                    if head and data.get(head):
                        pdf.set_font("Calibri", 'B', 10)
                        pdf.cell(0, 6, data[head], ln=True)

                    if read and data.get(read):
                        pdf.set_font("Calibri", '', 10)
                        pdf.cell(0, 6, data[read], ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Initial Weight  = ")
                    pdf.cell(0, 6, data.get(iw, ''), ln=True)

                    fw_num = int(fw[6:8])
                    fw_values = [
                        data.get(f'oil_FW{i:02d}', '')
                        for i in range(fw_num - 4, fw_num + 1)
                        if data.get(f'oil_FW{i:02d}')
                    ]

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Final Weight   = ")
                    pdf.cell(0, 6, ", ".join(fw_values), ln=True)

                    pdf.set_x(30)
                    pdf.cell(35, 6, "Value of Sample = ")
                    pdf.cell(0, 6, data.get(vs, ''), ln=True)

                    pdf.set_x(30)
                    pdf.set_font("Calibri", 'B', 10)
                    pdf.cell(35, 6, "Formula :", ln=True)

                    pdf.set_font("Calibri", '', 10)
                    formula_text = f"({data.get(fw)} - {data.get(iw)}) X 1000000"
                    result_text = f"{data.get(ans, '')} {data.get(param, '')}"

                    add_formula_with_line(formula_text, result_text, data.get(vs, ''), 40)

            # ---------- FINAL AVERAGE ----------
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, "Average of Oil & Grease:", ln=True)
            pdf.set_font("Calibri", '', 10)

            final_text = (
                f"{data.get('oil_final_ans1','')} + "
                f"{data.get('oil_final_ans2','')} + "
                f"{data.get('oil_final_ans3','')}"
            )
            result_text = f"{data.get('oil_final_ans')} {data.get('oil_final_param','')}"

            add_formula_with_line(
                final_text,
                result_text,
                data.get('oil_final_divi', '3'),
                40
            )

        
        for key in sorted(data.keys()):

            # Match keys like: tds_crm_36_1_bw
            match = re.match(r'(oil_grease_crm_\d+_\d+)_bw$', key)
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

            # ---------- FORMULA (USE ONLY LAST AW) ----------
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
        
        add_average_formula_section('for_color1', 'Color Calculation', 'color_head', 'color_ans', 'color_param', 'color_divi')
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
        if data.get('cyanide_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Cyanide Calculations", ln=True)
            pdf.cell(0, 6, data.get('cyanide_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_cyanide{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('cyanide_ans')} {data.get('cyanide_param')}",
                data.get('cyanide_divi1', "3")
            )
            
       
        
        
        
        if(data.get('cyanide_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('cyanide_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_cyanide1_1') and data.get('for_cyanide1_1_df'):
                formula_parts.append(
                    f"({data.get('for_cyanide1_1')} X {data.get('for_cyanide1_1_df')})"
                )

            # Pair 2
            if data.get('for_cyanide1_2') and data.get('for_cyanide1_2_df'):
                formula_parts.append(
                    f"({data.get('for_cyanide1_2')} X {data.get('for_cyanide1_2_df')})"
                )

            # Pair 3
            if data.get('for_cyanide1_3') and data.get('for_cyanide1_3_df'):
                formula_parts.append(
                    f"({data.get('for_cyanide1_3')} X {data.get('for_cyanide1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
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
        
        if data.get('fluoride_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Fluoride Calculations", ln=True)
            pdf.cell(0, 6, data.get('fluoride_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_fluoride{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('fluoride_ans')} {data.get('fluoride_param')}",
                data.get('fluoride_divi1', "3")
            )
            
       
        
        
        
        if(data.get('fluoride_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('fluoride_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_fluoride1_1') and data.get('for_fluoride1_1_df'):
                formula_parts.append(
                    f"({data.get('for_fluoride1_1')} X {data.get('for_fluoride1_1_df')})"
                )

            # Pair 2
            if data.get('for_fluoride1_2') and data.get('for_fluoride1_2_df'):
                formula_parts.append(
                    f"({data.get('for_fluoride1_2')} X {data.get('for_fluoride1_2_df')})"
                )

            # Pair 3
            if data.get('for_fluoride1_3') and data.get('for_fluoride1_3_df'):
                formula_parts.append(
                    f"({data.get('for_fluoride1_3')} X {data.get('for_fluoride1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
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
        if data.get('nitrate_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Nitrate Calculations", ln=True)
            pdf.cell(0, 6, data.get('nitrate_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_nitrate{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('nitrate_ans')} {data.get('nitrate_param')}",
                data.get('nitrate_divi1', "3")
            )
            
       
        
        
        
        if(data.get('nitrate_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('nitrate_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_nitrate1_1') and data.get('for_nitrate1_1_df'):
                formula_parts.append(
                    f"({data.get('for_nitrate1_1')} X {data.get('for_nitrate1_1_df')})"
                )

            # Pair 2
            if data.get('for_nitrate1_2') and data.get('for_nitrate1_2_df'):
                formula_parts.append(
                    f"({data.get('for_nitrate1_2')} X {data.get('for_nitrate1_2_df')})"
                )

            # Pair 3
            if data.get('for_nitrate1_3') and data.get('for_nitrate1_3_df'):
                formula_parts.append(
                    f"({data.get('for_nitrate1_3')} X {data.get('for_nitrate1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
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
            
            
        add_average_formula_section('for_nitrite1', 'Nitrite Calculation', 'nitrite_head', 'nitrite_ans', 'nitrite_param', 'nitrite_divi')
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
            
            
        # add_average_formula_section('for_residual1', 'Chlorine Calculation', 'residual_head', 'residual_ans', 'residual_param', 'residual_divi')
        
        if data.get('residual_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Chlorine Calculations", ln=True)
            pdf.cell(0, 6, data.get('residual_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_residual{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('residual_ans')} {data.get('residual_param')}",
                data.get('residual_divi1', "3")
            )
            
       
        
        
        
        if(data.get('residual_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('residual_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_residual1_1') and data.get('for_residual1_1_df'):
                formula_parts.append(
                    f"({data.get('for_residual1_1')} X {data.get('for_residual1_1_df')})"
                )

            # Pair 2
            if data.get('for_residual1_2') and data.get('for_residual1_2_df'):
                formula_parts.append(
                    f"({data.get('for_residual1_2')} X {data.get('for_residual1_2_df')})"
                )

            # Pair 3
            if data.get('for_residual1_3') and data.get('for_residual1_3_df'):
                formula_parts.append(
                    f"({data.get('for_residual1_3')} X {data.get('for_residual1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
                    f"{data['residual_ans_1']} {data.get('residual_param_1')}",
                    data.get('residual_divi')
                )
        
        for key in data.keys():
            match = re.match(r'(chlorine_crm_\d+_\d+)_1$', key)
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
        if data.get('trubidity_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Turbidity Calculations", ln=True)
            pdf.cell(0, 6, data.get('trubidity_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_trubidity{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('trubidity_ans')} {data.get('trubidity_param')}",
                data.get('trubidity_divi1', "3")
            )
            
       
        
        
        
        if(data.get('trubidity_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('trubidity_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_trubidity1_1') and data.get('for_trubidity1_1_df'):
                formula_parts.append(
                    f"({data.get('for_trubidity1_1')} X {data.get('for_trubidity1_1_df')})"
                )

            # Pair 2
            if data.get('for_trubidity1_2') and data.get('for_trubidity1_2_df'):
                formula_parts.append(
                    f"({data.get('for_trubidity1_2')} X {data.get('for_trubidity1_2_df')})"
                )

            # Pair 3
            if data.get('for_trubidity1_3') and data.get('for_trubidity1_3_df'):
                formula_parts.append(
                    f"({data.get('for_trubidity1_3')} X {data.get('for_trubidity1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
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
        for key in data.keys():
            match = re.match(r'(ammonia_crm_\d+_\d+)_1$', key)
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
        
        
        add_average_formula_section('for_ionic_det1', 'Ionic Detergent Calculation', 'ionic_det_head', 'ionic_det_ans', 'ionic_det_param', 'ionic_det_divi')   
        for key in data.keys():
            match = re.match(r'(an_ionic_detergent_as_mbas_crm_\d+_\d+)_1$', key)
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
        
        
        add_average_formula_section('for_freechlorine1', 'Freechlorine Calculation', 'freechlorine_head', 'freechlorine_ans', 'freechlorine_param', 'freechlorine_divi')
        # add_average_formula_section('for_sulphate1', 'sulphate Calculation', 'sulphate_head', 'sulphate_ans', 'sulphate_param', 'sulphate_divi')
        
        if data.get('sulphate_ans'):

            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "sulphate Calculations", ln=True)
            pdf.cell(0, 6, data.get('sulphate_head'), ln=True)
            pdf.set_font("Calibri", '', 10)

            # Build formula dynamically
            formula_parts = []

            for i in range(1, 4):
                value = data.get(f'for_sulphate{i}')
                if value not in [None, ""]:
                    formula_parts.append(str(value))

            final_formula = " + ".join(formula_parts)

            add_formula_block(
                None,
                None,
                final_formula,
                f"{data.get('sulphate_ans')} {data.get('sulphate_param')}",
                data.get('sulphate_divi1', "3")
            )
            
       
        
        
        
        if(data.get('sulphate_ans_1')):
            check_page_break(20)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 6, data.get('sulphate_head_1'), ln=True)
            pdf.set_font("Calibri", '', 10)
            formula_parts = []

            # Pair 1
            if data.get('for_sulphate1_1') and data.get('for_sulphate1_1_df'):
                formula_parts.append(
                    f"({data.get('for_sulphate1_1')} X {data.get('for_sulphate1_1_df')})"
                )

            # Pair 2
            if data.get('for_sulphate1_2') and data.get('for_sulphate1_2_df'):
                formula_parts.append(
                    f"({data.get('for_sulphate1_2')} X {data.get('for_sulphate1_2_df')})"
                )

            # Pair 3
            if data.get('for_sulphate1_3') and data.get('for_sulphate1_3_df'):
                formula_parts.append(
                    f"({data.get('for_sulphate1_3')} X {data.get('for_sulphate1_3_df')})"
                )

            # Join only available parts
            final_formula = " + ".join(formula_parts)
            add_formula_block(
                    None,
                    None,
                    final_formula,
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
        
        
        
        add_average_formula_section('for_cod1', 'COD Calculation', 'cod_head', 'cod_ans', 'cod_param', 'cod_divi')
        
        for key in data.keys():
            match = re.match(r'(chemical_oxygen_demandcod_crm_\d+_\d+)_1$', key)
            if not match:
                continue

            base = match.group(1)

            # render only if checkbox/value is true
            if not data.get(f"{base}_1"):
                continue

            add_average_formula_section_crm(
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
        # def add_formula_block(head_text, reading_text, formula_content, result_text, divisor_text=None, start_x=30):
        #     """Add a formula block with automatic page break check"""
        #     # Check page break before each formula (estimate 25px needed)
        #     check_page_break(25)
            
        #     if head_text:
        #         pdf.set_font("Calibri", 'B', size=10)
        #         pdf.cell(0, 6, head_text, ln=True)
            
        #     if reading_text:
        #         pdf.cell(0, 6, reading_text, ln=True)
            
        #     pdf.cell(0, 6, "Formula:", ln=True)
        #     pdf.set_font("Calibri", '', 10)
            
        #     # Save current Y position
        #     old_y = pdf.get_y()
            
        #     # Get the width of the formula content
        #     text_width = pdf.get_string_width(formula_content)
            
        #     # Calculate line position to match text width
        #     line_start_x = start_x
        #     line_end_x = start_x + text_width
            
        #     # Draw the formula text
        #     pdf.set_x(start_x)
        #     pdf.cell(text_width, 6, f"{formula_content} = {result_text}", align='L', ln=True)
            
        #     # Draw the line below the formula
        #     pdf.line(line_start_x, old_y+5.5, line_end_x, old_y+5.5)
            
        #     if divisor_text:
        #         # Center the divisor below the line
        #         divisor_width = pdf.get_string_width(divisor_text)
        #         center_divisor_x = line_start_x + (text_width / 2) - (divisor_width / 2)
        #         pdf.set_x(center_divisor_x)
        #         pdf.cell(divisor_width, 3, divisor_text, align="C", ln=True)
                
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

        
        
        
        if data.get('silver_ans_1'):
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0, 8, "Silver Calculation:", 0, 1, 'L')
            add_formula_block(
                None,
                None,
                f"({data.get('for_silver1_1')} X {data.get('for_silver1_1_df')}) + "
                f"({data.get('for_silver1_2')} X {data.get('for_silver1_2_df')}) + "
                f"({data.get('for_silver1_3')} X {data.get('for_silver1_3_df')})",
                f"{data.get('silver_ans_1')} {data.get('silver_param_1')}",
                data.get('silver_divi')
            )

        
        for key in sorted(data.keys()):
            
            match = re.match(r'(crm_silver_crm_\d+_\d+)_1$', key)
            
            if not match:
                
                continue

            base = match.group(1)
            

            if not data.get(f"{base}_1"):
                continue

            
            # ---------- CRM HEADER ----------
            if data.get(f"{base}_crm_head"):
                check_page_break(20)
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

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

        # pdf.set_font("Calibri", 'B', size=10)
        # pdf.cell(0,5,"Total Hardness CRM Calculations",ln=True)
        # pdf.set_font("Calibri", '', size=10)
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(total_hardness_crm_\d+_\d+)_1$', key)
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
        if data.get('chloride_ans2'):
            add_formula_block(
                data.get('chloride_head_2'),
                data.get('chloride_reading_1'),
                f"({data.get('chloride_2_1')} - {data.get('chloride_2_2')}) - ({data.get('chloride_2_3')} - {data.get('chloride_2_4')}) X {data.get('chloride_2_5')} X 35450",
                f"{data.get('chloride_ans2', data.get('chloride_ans1', ''))} {data.get('chloride_param2', data.get('chloride_param1', ''))}",
                data.get('chloride_2_6')
            )
        
        # Chloride Reading 3
        pdf.set_font("Calibri", 'B', 11)
        if data.get('chloride_ans3'):
            add_formula_block(
                data.get('chloride_head_3'),
                data.get('chloride_reading_2'),
                f"({data.get('chloride_3_1')} - {data.get('chloride_3_2')}) - ({data.get('chloride_3_3')} - {data.get('chloride_3_4')}) X {data.get('chloride_3_5')} X 35450",
                f"{data.get('chloride_ans3', data.get('chloride_ans1', ''))} {data.get('chloride_param3', data.get('chloride_param1', ''))}",
                data.get('chloride_3_6')
            )
        
        # Chloride Reading 4
        pdf.set_font("Calibri", 'B', 11)
        if data.get('chloride_ans4'):
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
        if data.get('for_chloride_ans'):
            add_formula_block(
                data.get('chloride_avg_head', "Chloride Average"),
                None,
                chloride_avg_formula,
                f"{data.get('for_chloride_ans', '')} {data.get('for_chloride_param', '')}",
                data.get('chloride_divi')
            )
        # pdf.set_font("Calibri", 'B', size=10)
        # pdf.cell(0,5,"Chloride CRM Calculations",ln=True)
        # pdf.set_font("Calibri", '', size=10)
        for key in sorted(data.keys()):
            # Match keys like 'alkalinity_crm_36_1_1'
            match = re.match(r'(chloride_crm_\d+_\d+)_1$', key)
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
                pdf.set_font("Calibri", 'B', 11)
                pdf.cell(0, 8, data.get(f"{base}_crm_head"), ln=True)

            # ---------- CRM STANDARDS ----------
            pdf.set_font("Calibri", '', 10)

            for i in range(1, 4):
                std = data.get(f"{base}_crm_standard_{i}")
                srm = data.get(f"{base}_crm_srm{i}")

                if std or srm:
                    pdf.cell(0, 6, f"{std} : {srm}", ln=True)

            pdf.ln(3)

            # ---------- AVERAGE FORMULA ----------
            add_average_formula_section(
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
        
        

        if data.get('sulphide-1_final_ans'):
            pdf.ln(5)
            pdf.cell(0, 6, data.get('sulphide-head'), border=False, align="L", ln=True)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,4,f"{data.get('sulphide-read_1')}",ln=True)
            pdf.set_font("Calibri", '', 10)
            pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide-1-a')}",ln=2)
            pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide-1-b')}",ln=2)
            pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide-1-c')}",ln=2)
            pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide-1-d')}",ln=2)
            pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide-1-vs')}",ln=2)
            add_formula_block(
                None,
                None,
                f"({data.get('sulphide-1-final-a')} X {data.get('sulphide-1-final-b')}) - "
                f"({data.get('sulphide-1-final-c')} X {data.get('sulphide-1-final-d')}) X 16000",
                f"{data.get('sulphide-1_final_ans')} {data.get('sulphide-1_param')}",
                data.get('sulphide-1-divi')
            )

        if data.get('sulphide-2_final_ans'):
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,4,f"{data.get('sulphide-read_2')}",ln=True)
            pdf.set_font("Calibri", '', 10)
            pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide-2-a')}",ln=2)
            pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide-2-b')}",ln=2)
            pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide-2-c')}",ln=2)
            pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide-2-d')}",ln=2)
            pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide-2-vs')}",ln=2)
            add_formula_block(
                None,
                None,
                f"({data.get('sulphide-2-final-a')} X {data.get('sulphide-2-final-b')}) - "
                f"({data.get('sulphide-2-final-c')} X {data.get('sulphide-2-final-d')}) X 16000",
                f"{data.get('sulphide-2_final_ans')} {data.get('sulphide-2_param')}",
                data.get('sulphide-2-divi')
            )

        if data.get('sulphide-3_final_ans'):
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,4,f"{data.get('sulphide-read_3')}",ln=True)
            pdf.set_font("Calibri", '', 10)
            pdf.cell(0,4,f"A mL iodine solutions = {data.get('sulphide-3-a')}",ln=2)
            pdf.cell(0,4,f"B normality iodine solution = {data.get('sulphide-3-b')}",ln=2)
            pdf.cell(0,4,f"C mL Na2S2O3 solution = {data.get('sulphide-3-c')}",ln=2)
            pdf.cell(0,4,f"D normality of Na2S2O3 solution = {data.get('sulphide-3-d')}",ln=2)
            pdf.cell(0,4,f"Volume of Sample = {data.get('sulphide-3-vs')}",ln=2)
            add_formula_block(
                None,
                None,
                f"({data.get('sulphide-3-final-a')} X {data.get('sulphide-3-final-b')}) - "
                f"({data.get('sulphide-3-final-c')} X {data.get('sulphide-3-final-d')}) X 16000",
                f"{data.get('sulphide-3_final_ans')} {data.get('sulphide-3_param')}",
                data.get('sulphide-3-divi')
            )

            # ------------------ Sulphide Average ------------------

            formula_parts = []

            if data.get('answer1'):
                formula_parts.append(f"({data.get('answer1')} X {data.get('answer1_df')})")

            if data.get('answer2'):
                formula_parts.append(f"({data.get('answer2')} X {data.get('answer2_df')})")

            if data.get('answer3'):
                formula_parts.append(f"({data.get('answer3')} X {data.get('answer3_df')})")

            average_formula = " + ".join(formula_parts)

            if formula_parts:
                add_formula_block(
                    data.get('sulphide_avg_head'),
                    None,
                    average_formula,
                    f"{data.get('for_sulphide_avg_ans')} {data.get('for_sulphide_avg_param')}",
                    data.get('sulphide_avg_divi')
                )

        
        
        if data.get('bod_1_ans'):
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,4,f"BOD Calculations",ln=True)
            pdf.cell(0,4,f"{data.get('bod_head_1')}",ln=True)
            pdf.set_font("Calibri", '', 10)
            pdf.ln(3)
            pdf.cell(
                0,4,
                f"{data.get('bod_1')} X {data.get('bod_1_df')} = "
                f"{data.get('bod_1_ans')} {data.get('bod_1_param')}",
                ln=True
            )

        if data.get('bod_ans'):
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 10)
            pdf.cell(0,4,f"{data.get('bod_head_2')}",ln=True)
            pdf.set_font("Calibri", '', 10)

            add_formula_block(
                None,
                None,
                data.get('bod_sv'),
                data.get('bod_1_p'),
                data.get('bod_tv'),
            )

            add_formula_block(
                None,
                None,
                f"({data.get('bod_initial')} - {data.get('bod_final')}) - "
                f"{{({data.get('bod_seed_1')} - {data.get('bod_seed_2')}) X {data.get('bod_seed_vol')}}}",
                f"{data.get('bod_ans')} {data.get('bod_param')}",
                data.get('bod_divi')
            )

        if data.get('toxic_ans'):
            check_page_break(20)
            pdf.ln(5)
            pdf.set_font("Calibri", 'B', 11)
            pdf.cell(0,4,"Toxic Metals Calculations",ln=True)
            pdf.set_font("Calibri", '', 10)
            pdf.ln(3)
            pdf.cell(0,4,f"{data.get('toxic_1')} = {data.get('toxic_1_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_2')} = {data.get('toxic_2_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_3')} = {data.get('toxic_3_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_4')} = {data.get('toxic_4_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_5')} = {data.get('toxic_5_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_6')} = {data.get('toxic_6_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_7')} = {data.get('toxic_7_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_8')} = {data.get('toxic_8_1')}",ln=2)
            check_page_break(20)
            pdf.cell(0,4,f"{data.get('toxic_9')} = {data.get('toxic_9_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_10')} = {data.get('toxic_10_1')}",ln=2)
            pdf.cell(0,4,f"{data.get('toxic_11')} = {data.get('toxic_11_1')}",ln=2)
            pdf.ln(3)
            add_formula_block(
                None,
                None,
                f"{data.get('toxic_r1')} + {data.get('toxic_r2')} + {data.get('toxic_r3')} + {data.get('toxic_r4')} + "
                f"{data.get('toxic_r5')} + {data.get('toxic_r6')} + {data.get('toxic_r7')} + {data.get('toxic_r8')} + "
                f"{data.get('toxic_r9')} + {data.get('toxic_r10')} + {data.get('toxic_r11')}",
                f"{data.get('toxic_ans')} {data.get('toxic_param')}",
                data.get('toxic_divi')
            )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={sample_id}.pdf'

    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())

    return response




def ww_rds_list(request):
    dw_list = Ww_rds.objects.all().order_by('-created_at')
    return render(request,'ww_rds_list.html',context={'list':dw_list})


@csrf_exempt
def create_ww_qc_manual(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            
           
            for k in body.keys():
                pass

            sample_id = body.get('sample_id')
            data = body.copy()
            if 'sample_id' in data:
                del data['sample_id']

            report = Ww_rds.objects.create(
                sample_id=sample_id,
                rds=data
            )
            return redirect(f"/qc/generate_ww_qc_pdf_response/{report.id}/")
            # return generate_dw_qc_pdf_response(report, data, sample_id)
            # return JsonResponse({
            #     "status": "success",
            #     "id": report.id,
            #     "sample_id": report.sample_id
            # })
            
            
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    sample_ids = Sample_registration.objects.all()
    ww_ids = WasteWaterForm2.objects.all()
    sample = serializers.serialize('json',sample_ids,fields=('sample_id',))
    ww = serializers.serialize('json',ww_ids,fields=('sample_id',))
    signs_list = []
    for sign in signs:
        signs_list.append({
            'id': sign.id,
            'name': sign.user.get_full_name() or sign.user.username,
            'user_id': sign.user.id,
            
        })

    user_signs = json.dumps(signs_list)
    context={'sample':sample,'ww':ww,'signs':user_signs}
    return render(request,"rds_ww_manual.html",context)

def ww_testing_results_sample(request):
    if request.method == 'POST':
        sample_id = request.POST.get('sample_id')
        
        if not sample_id:
            return JsonResponse({'error': 'sample_id is required'}, status=400)
        
        try:
            ww_data = Ww_rds.objects.get(sample_id=sample_id)
            
            # Get report_type from the rds JSON field
            report_type = ww_data.rds.get('report_type', 'standard') if ww_data.rds else 'standard'
            
            # Convert model to dictionary
            ww_data_dict = {
                'sample_id': ww_data.sample_id,
                'report_type': report_type,
                'created_at': ww_data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'rds': ww_data.rds  # This is already a dict if JSONField
            }
            
            return JsonResponse({
                'success': True,
                'ww_data': ww_data_dict,
                'sample_id': sample_id,
                'report_type': report_type
            })
            
        except Ww_rds.DoesNotExist:
            return JsonResponse({'error': f'Sample ID {sample_id} not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # For GET requests
    all_sample_ids = Ww_rds.objects.values_list('sample_id', flat=True)
    return render(request, 'rds_testing_results_ww.html', {'all_sample_ids': all_sample_ids})


@csrf_exempt
def ww_testing_results_sample_save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        report_type = data.get('report_type', 'standard')
        results = {
            'report_type': report_type,
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
                try:
                    idx = int(key.split('_')[1])
                    row_indices.append(idx)
                except (ValueError, IndexError):
                    continue
        
        row_indices.sort()
        
        def get_value(name, default="-"):
            v = data.get(name)
            return v if v not in [None, "", "null"] else default
        
        for idx in row_indices:
            # Get CRM result
            crm_value = data.get(f'crm_result_{idx}', '-')
            
            if isinstance(crm_value, list):
                crm_text = ', '.join([str(c) for c in crm_value if c and c != '-'])
            else:
                crm_text = str(crm_value) if crm_value and crm_value != '-' else '-'
            
            # Build row data based on report_type
            row_data = {
                "date": get_value(f'date_{idx}'),
                "parameter": get_value(f'parameter_{idx}'),
                "equipment": get_value(f'equipment_{idx}'),
                "method": get_value(f'method_{idx}'),
                "certified": get_value(f'certified_{idx}'),
                "acceptance": get_value(f'acceptance_{idx}'),
                "crm_results": crm_text,
                "performed_by": get_value(f'performed_by_{idx}'),
                "reviewed_by": get_value(f'reviewed_by_{idx}'),
                "status": get_value(f'status_{idx}')
            }
            
            # Add report_type specific fields
            if report_type == 'in-out':
                row_data["inlet"] = get_value(f'inlet_{idx}')
                row_data["outlet"] = get_value(f'outlet_{idx}')
            else:
                row_data["sample_result"] = get_value(f'sample_result_{idx}')
            
            results[f'row_{idx}'] = row_data

        # Get title and sample_id
        sample_id = data.get('sample_id', 'N/A')
        title = data.get('title', 'QC Report')
        
        obj = TestingResultsOfWWSamples.objects.create(
            sample_id=sample_id,
            title=title,
            results=results,
            location=data.get('location', 'N/A')
        )

        return generate_pdf_for_ww_testing_results(obj)




def generate_pdf_for_ww_testing_results(obj):
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
                    # Calculate image position to center it
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

        def draw_text_centered(self, x, y, w, h, text):
            """Draw text centered both horizontally and vertically with wrapping"""
            self.set_font("Calibri", "", 8)
            
            # Calculate how many lines are needed
            lines = self.multi_cell(w - 4, 5, str(text), split_only=True)
            num_lines = len(lines) if lines else 1
            text_height = num_lines * 5
            
            # Calculate Y position to center vertically
            y_pos = y + (h - text_height) / 2
            
            # Draw the text centered
            self.set_xy(x + 2, y_pos)
            self.multi_cell(w - 4, 5, str(text), border=0, align='C')
            
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
        
        def draw_table_header(self, report_type):
            """Draw the table header based on report_type using stored header values"""
            # Get custom headers from results
            headers_dict = obj.results.get('headers', {})
            crm_head_1 = headers_dict.get('crm_head_1', 'RM/CRM Certified Value')
            crm_head_2 = headers_dict.get('crm_head_2', 'RM/CRM Acceptance Limit')
            crm_head_3 = headers_dict.get('crm_head_3', 'RM/CRM Test Results')
            
            if report_type == 'in-out':
                col_widths = [10, 25, 35, 25, 25, 25, 25, 20, 15, 15, 19, 19, 20]
                headers = [
                    "S.no", "Date", "Parameter", "Equipment ID", "Test Method",
                    crm_head_1, crm_head_2, crm_head_3,
                    "Inlet", "Outlet", "Performed By Initials", "Reviewed By Initials", "Conformance Status (By Reviewer)"
                ]
            else:
                col_widths = [10, 25, 35, 25, 25, 25, 25, 25, 25, 19, 19, 20]
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
                # Calculate how many lines each header needs
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
                
                # Calculate vertical center position for this specific header
                num_lines = header_line_counts[i]
                text_height = num_lines * 4
                y_pos = start_y + (header_height - text_height) / 2
                
                # Draw header text centered
                self.set_xy(current_x + 1, y_pos)
                self.multi_cell(width - 2, 4, header, border=0, align='C')
                
                current_x += width
            
            # Move cursor below the header row
            self.set_y(start_y + header_height)
            self.set_x(start_x)
        
        def check_page_break(self, row_height):
            if self.get_y() + row_height > self.h - 20:
                self.add_page()
                self.set_y(36)
                self.draw_table_header(getattr(self, 'current_report_type', 'standard'))
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
            else:
                self.text(18,self.h-13,txt="+92 310 2288801")
                self.text(60,self.h-15,txt="Head Office:345,First Floor, Street-15,Block-3")
                self.text(60,self.h-11,txt="Bahadurabad, Karachi, 75900, Pakistan")

            self.image('static/assets/polyPNG-removebg-preview.png',202,184,90,22)

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
            from datetime import datetime
            return datetime.strptime(date_str, "%d-%B-%Y")
        except:
            try:
                return datetime.strptime(date_str, "%d-%b-%Y")
            except:
                return None

    # Get report_type from the results
    report_type = obj.results.get('report_type', 'standard') if isinstance(obj.results, dict) else 'standard'
    
    pdf = CustomPDF(orientation='L', unit='mm', format='A4')
    pdf.current_report_type = report_type
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("Calibri", "B", 10)
    pdf.ln(4)
    pdf.cell(160, 6, f"Sample ID : {obj.sample_id}")
    pdf.cell(100, 6, f"Title : {obj.title}", ln=True, align="R")
    pdf.draw_table_header(report_type)

    pdf.set_font("Calibri", "", 8)
    serial = 1

    # Get all rows
    rows = [(k, v) for k, v in obj.results.items() if k.startswith('row_')]
    
    # Sort by date (parse date string to datetime for comparison)
    rows_with_dates = []
    for row_key, row in rows:
        date_str = row.get("date", "")
        date_obj = parse_date(date_str)
        rows_with_dates.append((row_key, row, date_obj, date_str))
    
    # Sort by date (None values go to the end)
    rows_with_dates.sort(key=lambda x: (x[2] is None, x[2]))
    
    for row_key, row, date_obj, date_str in rows_with_dates:
        # Get CRM result
        crm_text = str(row.get("crm_results", "-"))
        if crm_text == "-" or not crm_text:
            crm_text = "-"
        
        # Get signature IDs
        performed_id = row.get("performed_by", "-")
        reviewed_id = row.get("reviewed_by", "-")
        
        # Build row data based on report_type
        if report_type == 'in-out':
            row_data = [
                str(serial),
                date_str,  # Use the original date string
                row.get("parameter", "-"),
                row.get("equipment", "-"),
                row.get("method", "-"),
                row.get("certified", "-"),
                row.get("acceptance", "-"),
                crm_text,
                row.get("inlet", "-"),
                row.get("outlet", "-"),
                performed_id,
                reviewed_id,
                row.get("status", "-")
            ]
            signature_col_indices = [10, 11]
        else:
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
            signature_col_indices = [9, 10]
        
        # Calculate row height
        line_counts = []
        for i, text in enumerate(row_data):
            if i in signature_col_indices and text != '-' and text != '':
                line_counts.append(3)  # Signature needs 3 lines height
            else:
                pdf.set_font("Calibri", "", 8)
                lines = pdf.multi_cell(pdf.col_widths[i] - 4, 5, str(text), split_only=True)
                line_counts.append(len(lines) if lines else 1)
        
        max_lines = max(line_counts) if line_counts else 1
        row_height = max(max_lines * 5, 15)
        
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
                # Draw text centered both horizontally and vertically with wrapping
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

    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())

    return response


def ww_testing_results_sample_pdf_from_list(request, pk=None):
    if pk:  # PDF generation for specific ID
        obj = get_object_or_404(TestingResultsOfWWSamples, id=pk)
        return generate_pdf_for_ww_testing_results(obj)
    else:  # List view
        data = TestingResultsOfWWSamples.objects.all().order_by('-created_at')
        return render(request, 'ww_testing_results_sample_list.html', {'list': data})
    
    
def ww_testing_results_sample_list(request):
    data = TestingResultsOfWWSamples.objects.all().order_by('-created_at')
    return render(request, 'ww_testing_results_sample_list.html', {'list': data})
__all__ = [
    'create_ww_qc',
    'get_ww',
    'generate_ww_qc_pdf_response',
    'ww_rds_list',
    'create_ww_qc_manual',
    'ww_testing_results_sample',
    'ww_testing_results_sample_save',
    'generate_pdf_for_ww_testing_results',
    'ww_testing_results_sample_pdf_from_list',
    'ww_testing_results_sample_list',
]
