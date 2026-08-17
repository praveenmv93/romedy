from django.urls import path
from e_app.views.csv_generate import download_hcpcs_codes
from e_app.views.pdf_generate import generate_pdf
from e_app.views.home import home
from e_app.views.auth import login_view, signup_view, logout_view
from e_app.views.appointments import book_appointment
from e_app.views.doctor import doctor_dashboard, complete_appointment
from e_app.views.staff import staff_dashboard
from e_app.views.knowledge import knowledge_hub
from e_app.views.dating import dating_request

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    
    # App URLs
    path('', home, name='home page'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/complete/<int:appointment_id>/', complete_appointment, name='complete_appointment'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('generate-csv/', download_hcpcs_codes, name='generate_csv'),
    path('knowledge/', knowledge_hub, name='knowledge_hub'),
    path('coffee-date/', dating_request, name='dating_request'),
]
