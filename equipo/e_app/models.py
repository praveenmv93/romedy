from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True, help_text="For doctors only")
    
    # Hybrid SQL+NoSQL schema flexibility
    no_sql_data = models.JSONField(default=dict, blank=True, help_text="Flexible dynamic metadata (NoSQL-like)")

    def __str__(self):
        return f"{self.user.username} - {self.role.capitalize()}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('checked-in', 'Checked In'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    TIME_SLOTS = [
        ('09:00 - 10:00 AM', '09:00 - 10:00 AM'),
        ('10:00 - 11:00 AM', '10:00 - 11:00 AM'),
        ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
        ('02:00 - 03:00 PM', '02:00 - 03:00 PM'),
        ('03:00 - 04:00 PM', '03:00 - 04:00 PM'),
        ('04:00 - 05:00 PM', '04:00 - 05:00 PM'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_doctor')
    date = models.DateField()
    time_slot = models.CharField(max_length=50, choices=TIME_SLOTS)
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Hybrid SQL+NoSQL data for clinical vitals or dynamically added checklist inputs
    no_sql_data = models.JSONField(default=dict, blank=True, help_text="Vitals, dynamic health data, checklist parameters")

    def __str__(self):
        doctor_name = self.doctor.get_full_name() if self.doctor else "Unassigned"
        return f"Appt: {self.patient.username} with Dr. {doctor_name} on {self.date}"
