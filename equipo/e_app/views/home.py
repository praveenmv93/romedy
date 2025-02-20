import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)

def home(request):


    return render(request, 'home.html')
