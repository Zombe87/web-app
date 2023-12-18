from django import views
from django.urls import path
from .views import *
from .views import admin_dashboard, approve_appointment
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', home, name='home'),
    path('appointment/', create_appointment, name='create_appointment'),
    path('process_form/', process_form, name='process_form'),
    path('approve_appointment/<int:appointment_id>/', approve_appointment, name='approve_appointment'),  
] 