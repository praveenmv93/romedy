from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.utils import timezone
import os
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from e_app.forms import ConsultationForm

def clear_folder(folder_path):
    """
    Remove all files and subdirectories inside the specified folder.

    :param folder_path: Path to the folder from which to remove files and subdirectories.
    """
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Iterate over all items in the folder
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    # Remove file
                    print(f"Removing file: {item_path}")
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    # Remove directory and its contents
                    print(f"Removing directory: {item_path}")
                    shutil.rmtree(item_path)
        else:
            print(f"The folder {folder_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while clearing the folder: {e}")


def generate_pdf(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            # Collect form data
            data = form.cleaned_data

            image_file = request.FILES['clinic_logo']

            # Create a FileSystemStorage object to save the file
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))

            # Save the file
            filename = fs.save(image_file.name, image_file)

            absolute_image_path = fs.path(filename)


            clinic_logo_url = f'file://{absolute_image_path}'

            # Prepare the context for rendering the PDF
            context = {
                'clinic_name': data['clinic_name'],
                'physician_name': data['physician_name'],
                'clinic_logo': clinic_logo_url,
                'physician_contact': data['physician_contact'],
                'patient_first_name': data['patient_first_name'],
                'patient_last_name': data['patient_last_name'],
                'patient_dob': data['patient_dob'],
                'patient_contact': data['patient_contact'],
                'chief_complaint': data['chief_complaint'],
                'consultation_note': data['consultation_note'],
                'timestamp': timezone.now(),
                'ip_address': get_client_ip(request)
            }

            # Render the HTML
            html_string = render_to_string('consultation_report_template.html', context)

            # Generate the PDF
            pdf_file = HTML(string=html_string).write_pdf()

            # Create a response object to return the PDF as a downloadable file
            response = HttpResponse(pdf_file, content_type='application/pdf')
            filename = f"CR_{data['patient_last_name']}_{data['patient_first_name']}_{data['patient_dob']}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # cleanint the temp stored images.
            folder_path = os.path.join(settings.MEDIA_ROOT, 'images')

            if os.path.exists(folder_path):
                clear_folder(folder_path)

            return response
    else:
        form = ConsultationForm()

    return render(request, 'generate_report.html', {'form': form})

def get_client_ip(request):
    """Retrieve the client's IP address"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
