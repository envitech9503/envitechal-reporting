# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from EnviTechAlApp.listfilter import _list_filter, _sampling_filter, _cert_filter, _work_filter, _by_date_desc, _parse_date
from EnviTechAlApp.view_helpers import _etal_mo_exceeds, _etal_red_style
import tempfile
from urllib import response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect,FileResponse,JsonResponse,HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import fpdf
from fpdf.enums import AccessPermission, EncryptionMethod
from ..models import *
import io
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
import pdfkit
import qrcode
from xhtml2pdf import pisa
import json
from distutils.util import strtobool
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
from django.core import serializers
from EnviTechAlApp import settings
import base64
from PIL import Image
from django.views.decorators.csrf import csrf_exempt

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.paginator import Paginator
import logging
from django.db.models import Q
from fpdf import FPDF

# print('hello')
# karachi_analyst = Signatures.objects.get(user__username='Muneeza')

# karachi_lab_manager = Signatures.objects.get(user__username='Hina')

# karachi_assistant = Signatures.objects.get(user__username='Samia')

# karachi_field= Signatures.objects.get(user__username='Adnan')

# lahore_analyst = Signatures.objects.get(user__username='saba')

# lahore_lab_manager = Signatures.objects.get(user__username='saqib')

# lahore_assistant = Signatures.objects.get(user__username='Sana')

# lahore_field= Signatures.objects.get(user__username='saqib')

# karachi_names = ['karachi', 'karachi.', 'Karachi', 'Karachi.']
# lahore_names = ['lahore', 'lahore.', 'Lahore', 'Lahore.']

# updated_count = 0

# for report in Verification.objects.all():
# #     print("REPORT",report) 
#     city = report.city_location.strip() if report.city_location else ''

#     if city in karachi_names:
#         report.verif_by_signature = karachi_field
        
#         report.check1_signature = karachi_lab_manager
#      #    report.lab_manager_signature = karachi_lab_manager
#         report.save()
#         updated_count += 1

#     elif city in lahore_names:
#         report.verif_by_signature = lahore_field
        
#         report.check1_signature = lahore_lab_manager
#      #    report.lab_manager_signature = lahore_lab_manager
#         report.save()
#         updated_count += 1
#     else:
#      #     print("LOcation Doest not exists")
#          pass

# print(f"✅ Updated {updated_count} reports with proper signatures.")


envitech_logo = '/home/django/EnviTechAlApp/static/assets/approvedby-removebg-preview.png'
logo = '/static/assets/approvedby-removebg-preview.png'






active_users = User.objects.filter(is_active=True)
signs = Signatures.objects.filter(user__in=active_users)
# karachi_office_signs = signs.filter(office='Karachi')
# lahore_office_signs = signs.filter(office='Lahore')


# karachi_analyst = karachi_office_signs.filter(role__role='Analyst').first()
# karachi_lab_manager = karachi_office_signs.filter(role__role='Lab Manager').first()
# karachi_assistant_manager = karachi_office_signs.filter(role__role='Assistant Manager QC').first()
# karachi_field_officer = karachi_office_signs.filter(role__role='Field officer').first()


# lahore_analyst = lahore_office_signs.filter(role__role='Analyst').first()
# lahore_lab_manager = lahore_office_signs.filter(role__role='Lab Manager').first()
# lahore_assistant_manager = lahore_office_signs.filter(role__role='Assistant Manager QC').first()
# lahore_field_officer = lahore_office_signs.filter(role__role='Field officer').first()


# print(karachi_analyst)
# print(karachi_lab_manager)
# print(karachi_assistant_manager)
# print(karachi_field_officer)

# print('lahore',lahore_analyst)
# print('lahore',lahore_lab_manager)
# print('lahore',lahore_assistant_manager)
# print('lahore',lahore_field_officer)


industries = Industry_sector.objects.all()





current_datetime_utc = timezone.now()

# Set the target timezone to 'Asia/Karachi'
target_timezone = pytz.timezone('Asia/Karachi')

# Convert UTC time to the local time of Pakistan
current_datetime_pakistan = current_datetime_utc.astimezone(target_timezone)

# Extract the local date
local_date_pakistan = current_datetime_pakistan.date()

# Extract the local time as a string in the "HH:MM:SS" format
local_time_str_pakistan = current_datetime_pakistan.strftime("%H:%M:%S")

# Create a formatted string
local_date = f"Date: {local_date_pakistan}, Time: {local_time_str_pakistan}"


logger = logging.getLogger(__name__)




from datetime import datetime, time
import math

from django.views.decorators.http import require_http_methods





# Export everything (incl. underscore helpers) to family modules.
__all__ = [_k for _k in list(globals()) if not _k.startswith("__")]
