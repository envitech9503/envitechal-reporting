from datetime import datetime, timedelta
import json
from django.shortcuts import render
from EnviTechAlApp.models import *
from detox.models import *
from django.db.models import Count, DateField, DurationField
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.http import JsonResponse
from itertools import chain
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, fields
from django.db.models.functions import Cast
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# Create your views here.
def dashboard(request):
    if request.user.is_superuser:
        print('hello')
        return render(request,'dashboard.html')
    else:
        return HttpResponseForbidden("Sorry, You don't have access!!")


def month_range(year, month):
    first_day = datetime(year, month, 1)
    # add one month, subtract one second → last moment of that month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(seconds=1)
    return make_aware(first_day), make_aware(last_day)

all_models = [
        DrinkingWaterForm, GaseousEmissionForm, AmbientAirForm, 
        WasteWaterSludge, VehiculEmissionForm, LuxAnalysisForm,
        PackingPolyBagForm, MachineOilForm, MicrobialAnalysis,
        ViscousLiquid, AmbientAir2, WasteWaterForm2, NoiseAnalysis,
    ]



def get_simple_late_reports(date_filter):
    """Simple function to get all late reports with date filtering"""
    all_late_reports = []
    
    for model in all_models:
        # Apply the date filter to only get reports from the current time period
        for report in model.objects.filter(date_filter):
            try:
                if not report.sample_id:
                    continue
                
                sample_reg = Sample_registration.objects.filter(sample_id=report.sample_id).first()
                if not sample_reg or not sample_reg.inp9 or not report.reporting_date:
                    continue
                
                # Convert dates from string to actual dates
                estimated_date = datetime.strptime(sample_reg.inp9, '%d-%m-%Y').date()
                
                # reporting_date format: "20-August-2025" (day-month-year)
                # Replace hyphens with spaces: "20 August 2025"
                report_date_str = report.reporting_date.replace('-', ' ')
                reporting_date = datetime.strptime(report_date_str, '%d %B %Y').date()
                
                # Check if report is late
                if reporting_date > estimated_date:
                    days_late = (reporting_date - estimated_date).days
                    
                    all_late_reports.append({
                        'type': model.__name__,
                        'sample_id': report.sample_id,
                        'client': report.report_to,
                        'lab_no': report.lab_report_no,
                        'estimated': estimated_date.strftime('%Y-%m-%d'),
                        'actual': reporting_date.strftime('%Y-%m-%d'),
                        'days_late': days_late
                    })
                    
            except Exception as e:
                # If any error occurs, skip this report
                print(f"Error processing late report {model.__name__}: {e}")
                continue
    
    return all_late_reports


@login_required
@csrf_exempt
def get_reports_data(request):
    if request.user.is_superuser:
        print('hello2')
        if request.method == "POST":
            body = json.loads(request.body.decode("utf-8"))
        else:  
            body = request.GET.dict()  # converts query params to dict)
        filter_type = body.get("filter",'month')

        today = datetime.today()

        if filter_type == "monthly":
            first_day, last_day = month_range(today.year, today.month)
            date_filter = Q(created_at__range=[first_day, last_day])
            print('date',date_filter)
        elif filter_type == "yearly":
            first_day = make_aware(datetime(today.year, 1, 1))
            last_day = make_aware(datetime(today.year, 12, 31, 23, 59, 59))
            date_filter = Q(created_at__range=[first_day, last_day])
            

        elif filter_type == "quarterly":
            try:
                quarter = int(body.get("quarter", 1))
                year = today.year
                quarter_months = {1: (1, 3), 2: (4, 6), 3: (7, 9), 4: (10, 12)}

                if quarter not in quarter_months:
                    return JsonResponse({"error": "Invalid quarter"}, status=400)

                start_month, end_month = quarter_months[quarter]
                first_day = make_aware(datetime(year, start_month, 1))

                if end_month == 12:
                    last_day = make_aware(datetime(year, 12, 31, 23, 59, 59))
                else:
                    last_day = make_aware(datetime(year, end_month + 1, 1)) - timedelta(seconds=1)

                date_filter = Q(created_at__range=[first_day, last_day])
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        elif filter_type == "custom":
            from_date = parse_date(body.get("from"))
            to_date = parse_date(body.get("to"))
            if not (from_date and to_date):
                return JsonResponse({"error": "Invalid date range"}, status=400)
            first_day = make_aware(datetime.combine(from_date, datetime.min.time()))
            last_day = make_aware(datetime.combine(to_date, datetime.max.time()))
            
            date_filter = Q(created_at__range=[first_day, last_day])
        else:
            return JsonResponse({"error": "Invalid filter"}, status=400)
        
        
        
        # report_count = get_report_counts(date_filter)
        
        
        
        reports_data = {}
        for model_name, model in {
            'drinking_water': DrinkingWaterForm,
            'gaseous_emission': GaseousEmissionForm,
            'ambient_air': AmbientAirForm,
            'waste_water_sludge': WasteWaterSludge,
            'vehicular_emission': VehiculEmissionForm,
            'lux_analysis': LuxAnalysisForm,
            'packing_polybag': PackingPolyBagForm,
            'machine_oil': MachineOilForm,
            'microbial_analysis': MicrobialAnalysis,
            'viscous_liquid': ViscousLiquid,
            'ambient_air2': AmbientAir2,
            'waste_water2': WasteWaterForm2,
            'noise_analysis': NoiseAnalysis,
            'detox': Detox,
        }.items():
            try:
                reports_data[model_name] = model.objects.filter(date_filter).count()
            except Exception as e:
                print(f"Error counting {model_name}: {e}")
                reports_data[model_name] = 0
        

        certs_data = {
            'calibration': Calibration.objects.filter(date_filter).count(),
            'inspection': Inspection.objects.filter(date_filter).count(),
            'verification': Verification.objects.filter(date_filter).count(),
        }
        print('cert',certs_data)
        
        #late reports - PASS THE DATE FILTER
        late_reports_list = get_simple_late_reports(date_filter)
        print('late-------->>>',late_reports_list)
        
        monthly_reports = [0] * 12
        monthly_certs = [0] * 12
        
        
        
        all_cert_models = [Calibration, Inspection, Verification]
        
        for month in range(1, 13):
            month_start = make_aware(datetime(today.year, month, 1))
            if month == 12:
                month_end = make_aware(datetime(today.year, 12, 31, 23, 59, 59))
            else:
                month_end = make_aware(datetime(today.year, month + 1, 1)) - timedelta(seconds=1)
            
            month_filter = Q(created_at__range=[month_start, month_end])
            
            # Count reports for this month
            for model in all_models:
                monthly_reports[month-1] += model.objects.filter(month_filter).count()
            
            # Count certificates for this month
            for model in all_cert_models:
                monthly_certs[month-1] += model.objects.filter(month_filter).count()
        
        #user created reports
        user_reports_data = defaultdict(int)
        

        for model in all_models:  
            qs = (
                model.objects
                .filter(date_filter)
                .values("created_by__username")
                .annotate(total=Count("id"))
            )
            for row in qs:
                username = row["created_by__username"] or "Unknown"
                user_reports_data[username] += row["total"]
        
        # pending = get_pending_reports()
        # for sample in pending:
        #     print(f"Sample ID: {sample.sample_id}, Estimated Date: {sample.inp9}")
        if reports_data:
            most_active_report = max(reports_data, key=reports_data.get)
            least_active_report = min(reports_data, key=reports_data.get)
        else:
            most_active_report, least_active_report = None, None
            
            
        # industry distribution
        
        industry_data = defaultdict(int)
        try:
            for model in all_models:  
                qs = (
                    model.objects
                    .filter(date_filter)
                    .values("industry__name")
                    .annotate(total=Count("id"))
                )
                for row in qs:
                    industry_name = row["industry__name"] or "Unknown"
                    industry_data[industry_name] += row["total"]
        except Exception as e:
                print(f"Error counting {e}")
        
        return JsonResponse({
            "filter": filter_type,
            "reports": reports_data,
            "certificates": certs_data,
            "monthly_reports": monthly_reports,  
            "monthly_certs": monthly_certs,      
            'total_reports': sum(reports_data.values()),
            'total_certs': sum(certs_data.values()),
            'total_late_count': len(late_reports_list), 
            'total_late': late_reports_list,
            'user_report_data':user_reports_data,
            "most_active_report": {
                "type": most_active_report,
                "count": reports_data.get(most_active_report, 0)
            },
            "least_active_report": {
                "type": least_active_report,
                "count": reports_data.get(least_active_report, 0)
            },
             "industry_data": {
                "labels": list(industry_data.keys()),
                "counts": list(industry_data.values())
            }
        })
    else:
        return HttpResponseForbidden("Sorry, you don't have access!!!")