from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from e_app.models import Appointment
from django.contrib.auth.models import User

# Decorator to restrict access to doctors
def doctor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'doctor':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Only doctors can view this page.")
        return redirect('home page')
    return _wrapped_view

@doctor_required
def doctor_dashboard(request):
    # Fetch scheduled and checked-in appointments for this doctor
    appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time_slot')
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

@doctor_required
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    appointment.status = 'completed'
    appointment.save()
    messages.success(request, f"Appointment for {appointment.patient.username} completed.")
    return redirect('doctor_dashboard')
