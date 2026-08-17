from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from e_app.models import Appointment, UserProfile
from django.contrib.auth.models import User

@login_required
def book_appointment(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        symptoms = request.POST.get('symptoms')
        doctor_id = request.POST.get('doctor')
        
        # Get doctor user if selected
        doctor = None
        if doctor_id:
            try:
                doctor = User.objects.get(id=doctor_id)
            except User.DoesNotExist:
                pass
        
        # NoSQL-like dynamic metadata if needed (e.g. tracking patient device, insurance name, preferences)
        insurance_provider = request.POST.get('insurance_provider', '')
        dynamic_data = {}
        if insurance_provider:
            dynamic_data['insurance_provider'] = insurance_provider
            
        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date,
            time_slot=time_slot,
            symptoms=symptoms,
            status='scheduled',
            no_sql_data=dynamic_data
        )
        messages.success(request, "Your appointment has been successfully booked!")
        return redirect('home page')
        
    doctors = User.objects.filter(profile__role='doctor')
    time_slots = Appointment.TIME_SLOTS
    return render(request, 'book_appointment.html', {'doctors': doctors, 'time_slots': time_slots})
