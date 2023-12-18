from django.db import models
import secrets
from django.template.loader import render_to_string
from django.core.mail import send_mail


class Tickets(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    ticket = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    number = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    nrc = models.CharField(max_length=100)
    ref_code = models.CharField(max_length=100)
    ticket_code = models.CharField(max_length=20, default="", blank=True)
    ticket_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate ticket code if it's not set
        if not self.ticket_code:
            self.ticket_code = f'KWA-{secrets.token_hex(4)}'

            

        # Generate ticket number if it's not set
        if not self.ticket_number:
            # Logic to generate ticket number, you can use secrets or any other method
            self.ticket_number = f'TN-{secrets.token_hex(4)}'

        # Calculate total cost before saving
        self.total_cost = self.ticket * 500

        super().save(*args, **kwargs)

        # Send email only when the object is created (not when it's updated)
        

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.email}"
