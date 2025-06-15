from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Teams
from listings.models import Car, Category
# Create your views here.

def home(request):
    teams = Teams.objects.all()
    cars = Car.objects.all()
    featured_car=Car.objects.filter(is_featured=True)
    latest_cars = Car.objects.all().order_by('-id')[:6] 
    brands = Category.objects.all()
    models = Car.objects.values_list('title', flat=True).distinct()
    car_types = Car.objects.values_list('condition', flat=True).distinct()

    return render(request, 'pages/index.html',{
        'teams':teams,
        'cars':cars,
        'brands':brands,
        'models':models,
        'car_types':car_types,
        'featured_car':featured_car,
        'latest_cars':latest_cars,
        })


def about(request):
    return render(request, 'pages/about.html')
def services(request):
    return render(request, 'pages/services.html')
