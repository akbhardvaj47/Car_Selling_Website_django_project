from django.urls import path
from . import views
urlpatterns = [
   path('', views.cars, name='cars'),
   path('car-details/<slug:slug>/', views.car_details, name='car_details'),
   path('search/', views.search, name='search'),
   path('add-car/', views.add_car, name='add_car'),
]