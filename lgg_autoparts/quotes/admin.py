from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import QuoteRequest
from tracking.models import Shipment


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'origin', 'destination', 'email', 'status', 'is_approved', 'created_at')
    list_filter = ('status', 'is_approved', 'created_at')
    search_fields = ('full_name', 'email', 'origin', 'destination')
    readonly_fields = ('created_at',)

    actions = ['approve_and_create_shipment']

    def approve_and_create_shipment(self, request, queryset):
        for quote in queryset:
            if not quote.is_approved:
                # Create Shipment
                shipment = Shipment.objects.create(
                    full_name=quote.full_name,
                    email=quote.email,
                    origin=quote.origin,
                    destination=quote.destination,
                    loading_date=quote.loading_date,
                    status='Pending',
                    notes=f"Generated from Quote Request #{quote.id}"
                )
                
                # Link shipment to quote
                quote.shipment = shipment
                quote.is_approved = True
                quote.status = 'Quoted'
                quote.save()

                # Send Tracking ID to Customer
                self.send_tracking_email(quote, shipment)

        self.message_user(request, "Selected quotes approved, shipments created, and tracking IDs sent.")

    approve_and_create_shipment.short_description = "Approve & Create Shipment + Send Tracking ID"

    def send_tracking_email(self, quote, shipment):
        subject = f"Your Freight Tracking ID - LGG Auto Parts"
        message = f"""
Dear {quote.full_name},

Your freight quote has been approved!

Here is your **Tracking ID**:

**{shipment.tracking_id}**

You can track your shipment 24/7 here:
https://yourwebsite.com/track/

Best regards,
LGG Auto Parts Team
"""

        try:
            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quote.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email failed: {e}")
