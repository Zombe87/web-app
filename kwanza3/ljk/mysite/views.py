from django.shortcuts import get_object_or_404, render
from django.shortcuts import render

# Create your views here.
from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import HttpResponse

from mysite.admin import TicketAdmin
from .models import *
from django.contrib.auth.models import User,GroupManager
from .models import Tickets
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.db.models import Q
import secrets


def home(request):
    return render(request,'index.html')



def process_form(request):
    try:
        # Your form processing logic here...

        # Assuming you have variables like subject, message, and recipient_email
        subject = 'New Form Submission'
        message = f'Name: {request.POST["name"]}\nEmail: {request.POST["email"]}\nMessage: {request.POST["message"]}'
        recipient_email = 'recipient@gmail.com'

        # Send email
        send_mail(subject, message, 'kwanzaa.zambia@gmail.com', [recipient_email])

        # Optionally, you can add a success message to display to the user
        success_message = "Your form has been submitted successfully."

    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")

        # Optionally, you can raise the exception again if you want to see the full traceback in the console
        raise

    # Redirect to home with a success message
    return render(request, 'index.html', {'success_message': success_message}) 

def approve_appointment(request, appointment_id):
    try:
        # Retrieve the appointment
        appointment = get_object_or_404(Tickets, id=appointment_id)

        # Generate ticket code if not set
        if not appointment.ticket_code:
            appointment.ticket_code = secrets.token_hex(4)
            appointment.save()

        # Define subject_approved here
        subject_approved = 'Ticket Purchase Approved'

        # Send email to the user (approved)
        message_approved = render_to_string('email/ticket_approval.html', {'ticket': appointment})
        user_email_approved = appointment.email

        # Call send_mail with defined subject_approved
        send_mail(subject_approved, message_approved, 'noreply@example.com', [user_email_approved], html_message=message_approved)

        # Approve the appointment
        appointment.is_approved = True
        appointment.save()

        return redirect('admin_dashboard')

    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")

        # Optionally, you can raise the exception again if you want to see the full traceback in the console
        raise



def admin_dashboard(request):
    print("Admin dashboard view called!")
    search_query = request.GET.get('q', '')

    if search_query:
        # Perform a case-insensitive search on multiple fields
        pending_appointments = Tickets.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(surname__icontains=search_query) |
            Q(ticket_code__icontains=search_query),
            is_approved=False
        )
    else:
        # No search query, retrieve all pending appointments
        pending_appointments = Tickets.objects.filter(is_approved=False)

    return render(request, 'admin.html', {'pending_appointments': pending_appointments, 'search_query': search_query})



def create_appointment(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        number = request.POST.get('number')
        nrc = request.POST.get('nrc')  # Corrected from 'id'
        tickets = int(request.POST.get('tickets', 0))
        total_cost = tickets * 500
        ref_code = request.POST.get('ref_code')

        new_appointment = Tickets(
            first_name=first_name,
            surname=surname,
            email=email,
            number=number,
            nrc=nrc,  # Corrected from 'ticket'
            ref_code=ref_code,
            ticket=tickets,
            total_cost=total_cost
        )

        new_appointment.save()

        # Send email to the user
        subject = 'Pending Approval for Ticket Purchase'
        message = f'Thank you for your submission. Your ticket purchase is pending approval. You will receive another email once it is approved.'
        user_email = new_appointment.email
        send_mail(subject, message, 'noreply@example.com', [user_email])

        success_message = "Your submission is pending approval."

        # Render the same page with the success message
        return render(request, 'index.html', {'success_message': success_message})

    return render(request, 'index.html')


# Create your views here.
