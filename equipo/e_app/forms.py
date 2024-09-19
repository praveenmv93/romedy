from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError


class ConsultationForm(forms.Form):
    clinic_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Clinic Name'}))
    physician_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Physician Name'}))
    clinic_logo = forms.FileField(required=False)
    physician_contact = forms.CharField(max_length=255,
                                        widget=forms.TextInput(attrs={'placeholder': 'Physician Contact'}))
    patient_first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    patient_last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    patient_dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    patient_contact = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Patient Contact'}))
    chief_complaint = forms.CharField(widget=CKEditorWidget(), max_length=5000, required=False)
    consultation_note = forms.CharField(widget=CKEditorWidget(), max_length=5000, required=False)

    def clean_clinic_logo(self):
        """Validate clinic_logo to ensure it is a .png or .jpeg file."""
        logo = self.cleaned_data.get('clinic_logo')

        if logo:
            file_extension = logo.name.split('.')[-1].lower()
            allowed_extensions = ['png', 'jpeg', 'jpg']

            if file_extension not in allowed_extensions:
                raise ValidationError("Only .png, .jpeg, or .jpg files are allowed.")

        return logo
