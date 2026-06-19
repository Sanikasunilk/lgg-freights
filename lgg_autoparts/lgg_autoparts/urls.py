from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import about, contact, faq, services

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Quote App
    path('quote/', include('quotes.urls')),
    
    # Tracking App
    path('track/', include('tracking.urls', namespace='tracking')),       # ← Best way
    
    # Main Pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('services/', services, name='services'),
]