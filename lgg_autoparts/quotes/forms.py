from django import forms
from .models import QuoteRequest

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['origin', 'destination', 'full_name', 'email', 'loading_date', 'message']
        widgets = {
            'origin': forms.TextInput(attrs={
                'placeholder': 'City or Pincode',
                'class': 'w-full border border-gray-300 rounded-lg px-4 inputbx focus:outline-none focus:border-[#16428c]'
            }),
            'destination': forms.TextInput(attrs={
                'placeholder': 'City or Pincode',
                'class': 'w-full border border-gray-300 rounded-lg px-4 inputbx focus:outline-none focus:border-[#16428c]'
            }),
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter Name',
                'class': 'w-full border border-gray-300 rounded-lg px-4 inputbx focus:outline-none focus:border-[#16428c]'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email',
                'class': 'w-full border border-gray-300 rounded-lg px-4 inputbx focus:outline-none focus:border-[#16428c]'
            }),
            'loading_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded-lg px-4 inputbx focus:outline-none focus:border-[#16428c]'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Additional message or special requirements (optional)',
                'rows': 3,
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-[#16428c]'
            }),
        }