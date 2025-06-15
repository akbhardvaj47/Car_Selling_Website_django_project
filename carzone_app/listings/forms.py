from django import forms
from .models import CarInquiry

class CarInquiryForm(forms.ModelForm):
    class Meta:
        model = CarInquiry
        fields = '__all__'
