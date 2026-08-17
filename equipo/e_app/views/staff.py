from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from e_app.models import Appointment
from django.contrib.auth.models import User

# Decorator to restrict access to staff
def staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'staff':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Only hospital staff can view this page.")
        return redirect('home page')
    return _wrapped_view

@staff_required
def staff_dashboard(request):
    appointments = Appointment.objects.all().order_by('-date', 'time_slot')
    doctors = User.objects.filter(profile__role='doctor')
    
    if request.method == 'POST':
        appt_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        appointment = get_object_or_404(Appointment, id=appt_id)
        
        if action == 'check-in':
            appointment.status = 'checked-in'
            appointment.save()
            messages.success(request, f"Patient {appointment.patient.username} successfully checked in!")
        elif action == 'assign-doctor':
            doc_id = request.POST.get('doctor_id')
            if doc_id:
                try:
                    doctor_user = User.objects.get(id=doc_id)
                    appointment.doctor = doctor_user
                    appointment.save()
                    messages.success(request, f"Assigned Dr. {doctor_user.get_full_name()} to {appointment.patient.username}'s appointment.")
                except User.DoesNotExist:
                    messages.error(request, "Selected doctor does not exist.")
            else:
                messages.error(request, "Please select a doctor to assign.")
                
        return redirect('staff_dashboard')
        
    return render(request, 'staff_dashboard.html', {'appointments': appointments, 'doctors': doctors})
