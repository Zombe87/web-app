from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Tickets

class TicketAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'ticket', 'email', 'nrc', 'ref_code', 'number', 'ticket_code', 'ticket_number', 'is_approved', 'approve_button')
    search_fields = ['first_name', 'surname', 'email', 'nrc', 'ref_code', 'ticket_code']

    def approve_button(self, obj):
        admin_dashboard_url = reverse('admin_dashboard')  # Update 'admin_dashboard' with the correct URL name
        return mark_safe(f'<a href="{admin_dashboard_url}">approval list</a>')

    approve_button.short_description = 'Approval List'

admin.site.register(Tickets, TicketAdmin)

