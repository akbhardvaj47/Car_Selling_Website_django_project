from django import forms
from .models import CarInquiry, Car

class CarInquiryForm(forms.ModelForm):
    class Meta:
        model = CarInquiry
        fields = '__all__'



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'title',
            'location',
            'fuel_type',
            'kilometers',
            'transmission',
            'category',
            'color',
            'year',
            'original_price',
            'discounted_price',
            'rent_price',
            'body_style',
            'engine',
            'drivetrain',
            'exterior_color',
            'interior_color',
            'doors',
            'passengers',
            'vin',
            'fuel_mileage_city',
            'fuel_mileage_highway',
            'condition',
            'owners',
            'warranty',
            'short_description',
            'long_description',
            'main_image',
            'gallery_image_1',
            'gallery_image_2',
            'gallery_image_3',
            'gallery_image_4',
        ]