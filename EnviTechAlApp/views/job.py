# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
from .shared import *  # noqa: F401,F403



def job_completion_form(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Get form data
            company_name = data.get('company_name')
            address = data.get('address')
            contact_person = data.get('contact_person')
            contact_number = data.get('contact_number')
            email = data.get('email')
            invoice_ref = data.get('invoice_ref')
            po_reference = data.get('po_reference')
            representative_sign = data.get('sign')
            representative_name = data.get('representative_name')
            receiver_name = data.get('receiver_name')
            location = data.get('location')
            custom_po_fields = data.get('custom_po_fields', [])  # Get custom PO fields
            
            # Get or create company
            company, created = ClientDetails.objects.update_or_create(
                company_name=company_name,
                defaults={
                    'address': address,
                    'contact_person': contact_person,
                    'contact_number': contact_number,
                    'email': email,
                    'po_reference': po_reference,  # Save to company
                    'custom_po_fields': custom_po_fields,  # Save to company
                }
            )
            
            # Collect service details from the data
            service_details = []
            services = data.get('services', [])
            
            for idx, service in enumerate(services, 1):
                if service.get('service'):  # Only add if service has value
                    service_details.append({
                        'sr_no': idx,
                        'service': service.get('service', ''),
                        'site_location': service.get('site_location', ''),
                        'qty': int(service.get('qty', 0)),
                        'date': service.get('date', '')
                    })
            
            # Create job completion record with custom_po_fields
            job = JobCompletionForm.objects.create(
                company=company,
                invoice_ref=invoice_ref,
                po_reference=po_reference,
                service_details=service_details,
                custom_po_fields=custom_po_fields,  # Save custom PO fields
                representative_name=representative_name,
                service_receiver=receiver_name,
                representative_sign=representative_sign,
                location=location,
            )
            
            # Generate PDF as blob
          #   return job_completion_pdf(request,job.id)
            return JsonResponse({
                'success': True,
                'job_id': job.id,
                'job_number': job.job_number,
                'message': 'Job created successfully'
            })
            
        except Exception as e:
            import traceback
            
            return JsonResponse({
                'success': False,
                'error': 'An internal error occurred. Please try again or contact the administrator.'
            }, status=400)
    
    
    success_message = request.session.pop('success_message', None)
    
    return render(request, 'job_completion_form.html', {
        'success_message': success_message,
        'signs': signs
    })


def job_completion_list(request):
     data, _srch = _work_filter(request, JobCompletionForm)
     return render(request,'job_completion_list.html',{'data':data,'searched':_srch})

def job_completion_edit(request, pk):
    job = get_object_or_404(JobCompletionForm, id=pk)
    
    # Parse service details
    service_details = job.service_details if isinstance(job.service_details, list) else json.loads(job.service_details)
    
    return render(request, 'job_completion_edit_form.html', {
        'job': job,
        'signs': signs,
        'service_details': json.dumps(service_details)
    })
        

def job_completion_clone(request, pk):
    """Clone job completion - GET request"""
    original_job = get_object_or_404(JobCompletionForm, id=pk)
    signs = Signatures.objects.all()
    
    # Parse service details
    service_details = original_job.service_details if isinstance(original_job.service_details, list) else json.loads(original_job.service_details)
    
    return render(request, 'job_completion_clone_form.html', {
        'original_job': original_job,
        'signs': signs,
        'service_details': json.dumps(service_details)
    })
        
def job_completion_pdf(request, pk):
    job = get_object_or_404(JobCompletionForm, id=pk)
    return generate_job_completion_pdf(job)

def job_main(request):
     return render(request,'job_completion_main.html')
@require_http_methods(["DELETE", "POST"])
def job_completion_delete(request, pk):
    """Delete job completion record"""
    try:
        job = get_object_or_404(JobCompletionForm, id=pk)
        job_number = job.job_number
        job.delete()
        
        return JsonResponse({
            'success': True,
            'job_id': pk,
            'job_number': job_number,
            'message': f'{job_number} Deleted Successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An internal error occurred. Please try again or contact the administrator.'
        }, status=400)

__all__ = [
    'job_completion_form',
    'job_completion_list',
    'job_completion_edit',
    'job_completion_clone',
    'job_completion_pdf',
    'job_main',
    'job_completion_delete',
]
