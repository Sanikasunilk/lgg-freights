# tracking/models.py
from django.db import models
import uuid
from django.utils.timezone import now

class Shipment(models.Model):
    tracking_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Addresses
    origin = models.CharField(max_length=300)
    destination = models.CharField(max_length=300)
    shipping_address = models.TextField(blank=True, null=True, verbose_name="Delivery Address")
    
    loading_date = models.DateField()
    
    current_location = models.CharField(max_length=300, blank=True, null=True)  # ← Fixed
    status = models.CharField(max_length=50, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Ordered', 'Ordered'),
        ('Dispatched', 'Dispatched'),
        ('Shipped', 'Shipped'),
        ('In Transit', 'In Transit'),
        ('Arrived', 'Arrived at Hub'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ])

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = "LGG" + str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} - {self.full_name}"


class ShipmentHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.shipment.tracking_id} - {self.status}"