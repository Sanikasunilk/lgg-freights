from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import QuoteRequestForm


def quote_form(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()

            # Default success message
            messages.success(request, "Quote request submitted successfully! We'll contact you soon.")

            try:
                # === Email to Admin ===
                admin_subject = f"New Quote Request from {quote.full_name}"
                admin_message = f"""
New Freight Quote Request Received!

Name: {quote.full_name}
Email: {quote.email}
Origin: {quote.origin}
Destination: {quote.destination}
Loading Date: {quote.loading_date}
Message: {quote.message or 'No message provided'}
Submitted at: {quote.created_at}
                """.strip()

                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                # === Thank You Email to Customer ===
                customer_subject = "Thank You for Your Quote Request - LGG Freights"
                customer_message = f"""
Dear {quote.full_name},

Thank you for requesting a freight quote with LGG Freights.

We have received your request and will get back to you shortly with the best rates.

Best regards,
LGG Freights Team
                """.strip()

                send_mail(
                    subject=customer_subject,
                    message=customer_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[quote.email],
                    fail_silently=False,
                )

            except Exception as e:
                print("Email Error:", str(e))  # Visible in Render Logs
                messages.warning(request, "Quote saved successfully. Email notification failed.")

            return redirect('home')

    else:
        form = QuoteRequestForm()

    return render(request, 'quote_form.html', {'form': form})