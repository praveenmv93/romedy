import logging
import os
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from e_app.forms import ConsultationForm
from weasyprint import HTML

logger = logging.getLogger(__name__)


def clear_folder(folder_path):
    """Removing all files and subdirectories inside the specified folder."""
    if not os.path.exists(folder_path):
        logger.warning(f"Folder '{folder_path}' does not exist.")
        return

    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                logger.info(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logger.info(f"Removed directory: {item_path}")
    except Exception as e:
        logger.error(f"Error while clearing folder '{folder_path}': {e}", exc_info=True)


def handle_uploaded_image(image_file):
    """Handle saving the uploaded image and return its absolute path."""
    try:
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))
        filename = fs.save(image_file.name, image_file)
        absolute_image_path = fs.path(filename)
        logger.info(f"Image uploaded successfully: {absolute_image_path}")
        return absolute_image_path
    except Exception as e:
        logger.error(f"Error saving uploaded image '{image_file.name}': {e}", exc_info=True)
        raise


def prepare_context(data, image_path, request):
    """Prepare the context dictionary for rendering the PDF."""
    return {
        'clinic_name': data['clinic_name'],
        'physician_name': data['physician_name'],
        'clinic_logo': f'file://{image_path}',
        'physician_contact': data['physician_contact'],
        'patient_first_name': data['patient_first_name'],
        'patient_last_name': data['patient_last_name'],
        'patient_dob': data['patient_dob'],
        'patient_contact': data['patient_contact'],
        'chief_complaint': data['chief_complaint'] or 'NA',
        'consultation_note': data['consultation_note'] or 'NA',
        'timestamp': timezone.now(),
        'ip_address': get_client_ip(request)
    }


def generate_pdf_response(html_string, filename):
    """Generate the PDF file and return it as a response."""
    try:
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        logger.info(f"PDF generated: {filename}")
        return response
    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return HttpResponse("An error occurred while generating the PDF", status=500)


def generate_pdf(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            image_file = request.FILES.get('clinic_logo')

            try:
                # Handle image upload
                absolute_image_path = handle_uploaded_image(image_file)

                # Prepare context for the PDF
                context = prepare_context(data, absolute_image_path, request)

                # Render the HTML and generate the PDF response
                html_string = render_to_string('consultation_report_template.html', context)
                filename = f"CR_{data['patient_last_name']}_{data['patient_first_name']}_{data['patient_dob']}.pdf"
                response = generate_pdf_response(html_string, filename)

                # Clear temporary stored images
                clear_folder(os.path.join(settings.MEDIA_ROOT, 'images'))

                return response

            except Exception as e:
                logger.error(f"An error occurred during PDF generation: {e}", exc_info=True)
                return HttpResponse("An error occurred", status=500)
        else:
            logger.warning("Invalid form data submitted.")
            errors = form.errors.as_json()
            logger.warning(f"Form validation errors: {errors}")
            return HttpResponse(f"Invalid form data: {errors}", status=400)

    else:
        form = ConsultationForm()

    return render(request, 'generate_report.html', {'form': form})


def get_client_ip(request):
    """Retrieve the client's IP address."""
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    return ip.split(',')[0] if ip else request.META.get('REMOTE_ADDR')
