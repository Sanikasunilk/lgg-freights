from django.db import models
from tracking.models import Shipment

class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Quoted', 'Quoted'),
        ('Closed', 'Closed'),
    ]

    origin = models.CharField(max_length=200, verbose_name="Origin")
    destination = models.CharField(max_length=200, verbose_name="Destination")
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    loading_date = models.DateField(verbose_name="Requested Loading Date")
    message = models.TextField(blank=True, null=True, verbose_name="Additional Message")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)
    shipment = models.OneToOneField(
        Shipment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='quote'
    )

    def __str__(self):
        return f"{self.full_name} - {self.origin} → {self.destination}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"