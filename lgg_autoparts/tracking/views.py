from django.shortcuts import render
from .models import Shipment

def track_shipment(request):
    shipment = None
    error = None

    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id', '').strip().upper()
        if tracking_id:
            try:
                shipment = Shipment.objects.get(tracking_id=tracking_id)
            except Shipment.DoesNotExist:
                error = "Invalid Tracking ID. Please check your tracking number and try again."
        else:
            error = "Please enter a tracking ID."

    return render(request, 'tracking.html', {
        'shipment': shipment,
        'error': error
    })