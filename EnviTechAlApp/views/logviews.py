# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403


def logoutUser(request):
     logout(request)
     if request.user.is_authenticated:
          return redirect('nav') 
     else:
          return redirect("login")


def loggingSheet(request):
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        selected_location = request.POST.get('selected_location')
        if selected_month:
            try:
                # Parse the date input with a custom format
                selected_date = datetime.strptime(selected_month, '%Y-%m')
            except ValueError:
                # Handle the case where the input is not a valid date
                # You might want to add proper error handling or redirect to an error page
                return render(request, 'error_page.html')

            # Filter the queryset based on the year and month components
            log = LoggingSheet.objects.filter(month__year=selected_date.year, month__month=selected_date.month,city_location=selected_location).order_by('-id')
            logging = LoggingSheet.objects.first()
            context = {'data': log,"dt":selected_date.month,"yr":selected_date.year,'logging':logging,'selected_location':selected_location}
            
            return render(request, 'loggingSheet.html', context)
        else:
            log = LoggingSheet.objects.all().order_by('-id')
    else:
        log = LoggingSheet.objects.all().order_by('-id')

    
    return render(request, 'loggingSheet.html',)


def loggingList(request):
     log, _srch = _sampling_filter(request, LoggingSheet)
     context = {'searched':_srch, 'data':log}
     return render(request,"loggingList.html",context)

def loggingEdit(request,pk):
     log = LoggingSheet.objects.get(id=pk)
     context = {'data':log}
     return render(request,"loggingEdit.html",context)

def loggingUpdate(request,pk):
     log = LoggingSheet.objects.get(id=pk)    
     if request.method=='POST':
          log.city_location = request.POST['city_location']
          log.sample_id = request.POST['sample_id']
          log.client_name = request.POST['client_name']
          log.address = request.POST['address']
          log.att_person = request.POST['att_person']
          log.email = request.POST['email']
          log.sample_nature = request.POST['sample_nature']
          log.rec_date = request.POST['rec_date']
          log.exp_date = request.POST['exp_date']
          log.rep_date = request.POST['rep_date']

          # log.month = datetime.strptime(request.POST['month'], '%Y-%m-%d').date() if request.POST['month'] else None
          log.month = request.POST.get('month')
          log.rec_by = request.POST['rec_by']
          log.remarks = request.POST['remarks']
          log.lab = request.POST['lab']
          log.issue_no = request.POST['issue_no']
          log.issue_date = request.POST['issue_date']
          log.issue = request.POST['issue']


          log.save()
          user = request.user
          action = f'Logging Sheet Edited by {user.username}'
          # AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Sample successfully added!')
          if "submit_and_view" in request.POST:
               return redirect(to='loggingSheet')
          if "submit_and_new" in request.POST:
               
               return render(request, "loggingList.html")  
     return render(request,"addLogging.html") 


def loggingClone(request,pk):
     log = LoggingSheet.objects.get(id=pk)
     context = {'data':log}
     return render(request,"loggingClone.html",context)

def loggingCloneUpdate(request,pk):
     log = LoggingSheet.objects.get(id=pk)    
     if request.method=='POST':
          log.city_location = request.POST['city_location']
          log.sample_id = request.POST['sample_id']
          log.client_name = request.POST['client_name']
          log.address = request.POST['address']
          log.att_person = request.POST['att_person']
          log.email = request.POST['email']
          log.sample_nature = request.POST['sample_nature']
          log.rec_date = request.POST['rec_date']
          log.exp_date = request.POST['exp_date']
          log.rep_date = request.POST['rep_date']


          # log.month = datetime.strptime(request.POST['month'], '%Y-%m-%d').date() if request.POST['month'] else None
          log.month = request.POST.get('month')
          log.rec_by = request.POST['rec_by']
          log.remarks = request.POST['remarks']
          log.lab = request.POST['lab']
          log.issue_no = request.POST['issue_no']
          log.issue_date = request.POST['issue_date']
          log.issue = request.POST['issue']

          log.pk = None
          log.id = None
          log.save()
          id = log.id
          user = request.user
          action = f'Logging Sheet Edited by {user.username}'
          AuditLog.objects.create(user=user, action=action, timestamp=local_date)
          messages.success(request, 'Sample successfully added!')
          
          if "submit_and_view" in request.POST:
               url = f"/loggingView/{str(id)}/"
               return redirect(to=url)
          if "submit_and_new" in request.POST: 
               return render(request, "loggingList.html")  
     return render(request,"addLogging.html") 

def loggingView(request,pk):
     log = LoggingSheet.objects.get(id=pk)
     month = log.month
     month = str(month)
     context = {'data':log,'month':month}
     return render(request,'loggingView.html',context)

def loggingDelete(request,pk):
     log = LoggingSheet.objects.get(id=pk)
     user = request.user
     action = f'Logging Sheet {log.sample_id} Deleted by {user.username}'
     AuditLog.objects.create(user=user, action=action, timestamp=local_date)
     messages.success(request, 'Sample successfully Deleted!')
     log.delete()
     return redirect("loggingList")


def logPdf(request):
    mn = request.GET.get('dt')
    yr =  request.GET.get('yr')
    loc = request.GET.get('loc')
    
    data = LoggingSheet.objects.filter(month__year=yr, month__month=mn,city_location=loc)
    logging = LoggingSheet.objects.first()
    from fpdf import FPDF
    from EnviTechAlApp.pdf_common import PDF_logPdf as PDFWithPageNumbers
    pdf = PDFWithPageNumbers()
    pdf._rq_data, pdf._rq_logging = data, logging
    pdf.add_page()
    font_path = "static/fonts/calibri.ttf"
    font_path_bold = "static/fonts/calibrib.ttf"
    pdf.add_font("Calibri","",font_path,uni=True)
    pdf.add_font("Calibri","B",font_path_bold,uni=True)
    pdf.set_font("Calibri","", 5)
    

    # Add table headers
    headers = [
        ["s.No", "Sample/ Test ID", "Client Name", "Address", "Name of Attention Person", "Contact Detail/Email Address",
        "Nature of Sample/Test", "Receiving Date", "Expected Reported Date", "Reporting Date", "Received By", "Remarks"
    ],]
    sr =1
    # Add table rows
    for log in data:
        if log.sample_id:
            a = [
                str(sr),log.sample_id, log.client_name, log.address, log.att_person, log.email, log.sample_nature,
                log.rec_date, log.exp_date, log.rep_date, log.rec_by, log.remarks
            ]
            sr+=1
            
            headers.append(a)

    with pdf.table(col_widths=(8, 15, 17, 30, 15, 40, 20, 20, 20, 20, 18, 14),
                  line_height=3, text_align=("CENTER", "CENTER", "CENTER", "CENTER", 'CENTER', 'CENTER', "CENTER",
                                             "CENTER", "CENTER", "CENTER", 'CENTER', 'CENTER')) as table:
        for data_row in headers:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={logging.lab}.pdf'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    # Output the PDF to the response
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S'))
    response.write(pdf_output.getvalue())

    return response

__all__ = [
    'logoutUser',
    'loggingSheet',
    'loggingList',
    'loggingEdit',
    'loggingUpdate',
    'loggingClone',
    'loggingCloneUpdate',
    'loggingView',
    'loggingDelete',
    'logPdf',
]
