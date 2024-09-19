from django.urls import path
from .views import download_hcpcs_codes
from .views import generate_pdf

urlpatterns = [
    path('generate-csv/', download_hcpcs_codes, name='generate_csv'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
]
