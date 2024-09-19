from ckeditor.widgets import CKEditorWidget
from django import forms


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
    chief_complaint = forms.CharField(widget=CKEditorWidget(), max_length=5000)
    consultation_note = forms.CharField(widget=CKEditorWidget(), max_length=5000)
