from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings  # Add this import statement

from mysite.views import admin_dashboard, home, create_appointment, process_form, approve_appointment

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home, name='home'),
    path('appointment/', create_appointment, name='create_appointment'),
    path('process_form/', process_form, name='process_form'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve_appointment/<int:appointment_id>/', approve_appointment, name='approve_appointment'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)