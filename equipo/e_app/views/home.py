from django.shortcuts import render
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def home(request):
    doctors = User.objects.filter(profile__role='doctor')
    return render(request, 'home.html', {'doctors': doctors})
