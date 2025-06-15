from django.contrib import admin
from .models import Car
from .models import Car, Category, CarInquiry

# Register your models here.


admin.site.register(Car)
admin.site.register(Category)
admin.site.register(CarInquiry)



