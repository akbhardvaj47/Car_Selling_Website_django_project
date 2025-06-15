from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from listings.models import Car
from .models import CarInquiry
from django.db.models import Q

def cars(request):
    return render(request, 'pages/cars.html')

def car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        customer_need = request.POST.get('customer_need')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        CarInquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            car=car,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            city=city,
            state=state,
            email=email,
            phone=phone,
            message=message
        )

        email_subject = f"Your Car Inquiry for {car.title} Has Been Received"
        email_message = f"""
        Dear {first_name} {last_name},

        Thank you for your interest in the {car.title}!

        We have received your inquiry...

        Best regards,
        CarZone Auto Sales Team
        """

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Your inquiry has been submitted successfully.")
        return redirect('car_details', slug=slug)

    return render(request, 'pages/car-details.html', {
        'car': car
    })



def search(request):
    cars = Car.objects.all()

    keyword = request.GET.get('keyword')
    brand = request.GET.get('select-brand')
    model = request.GET.get('select-model')
    location = request.GET.get('select-location')
    year = request.GET.get('select-year')
    car_type = request.GET.get('select-type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if keyword:
        cars = cars.filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(long_description__icontains=keyword) |
            Q(location__icontains=keyword)
        )

    if brand:
        cars = cars.filter(category__name__iexact=brand)

    if model:
        cars = cars.filter(title__icontains=model)

    if location:
        cars = cars.filter(location__icontains=location)

    if year:
        cars = cars.filter(year__iexact=year)

    if car_type:
        cars = cars.filter(body_style__iexact=car_type)

    if min_price:
        cars = cars.filter(discounted_price__gte=min_price)

    if max_price:
        cars = cars.filter(discounted_price__lte=max_price)

    context = {
        'cars': cars,
    }
    return render(request, 'pages/search.html', context)