from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from listings.models import Car, Category, CarInquiry
from django.core.paginator import Paginator
from django.utils.text import slugify

# ------------------- Car Listings Page -------------------

def cars(request):
    cars = Car.objects.all().order_by('-id')
    paginator = Paginator(cars, 6) 
    page = request.GET.get('page')
    cars = paginator.get_page(page)

    return render(request, 'pages/cars.html', {
        'cars': cars,
    })


# ------------------- Car Details + Inquiry Form -------------------
def car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)

    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        customer_need = request.POST.get('customer_need')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # 🛑 Prevent duplicate inquiries for logged-in users
        if user and CarInquiry.objects.filter(user=user, car=car).exists():
            messages.warning(request, 'You have already submitted an inquiry for this car.')
            return redirect('car_details', slug=car.slug)

        # ✅ Create new inquiry
        CarInquiry.objects.create(
            user=user,
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

        # ✅ Send confirmation email
        email_subject = f"Inquiry Received for {car.title}"
        email_message = f"""
Dear {first_name} {last_name},

Thank you for your interest in the {car.title}!

Our team has received your inquiry and will get back to you shortly.

Here’s a quick summary:
Car: {car.title}
Location: {car.location}
Message: {message or "No message provided"}

Best regards,  
CarZone Auto Sales Team
www.carzone.com
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


# ------------------- Search -------------------
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

    # Apply filters if provided
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
        try:
            cars = cars.filter(discounted_price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            cars = cars.filter(discounted_price__lte=float(max_price))
        except ValueError:
            pass

    return render(request, 'pages/search.html', {'cars': cars})

# -------------------- Add car ---------------------
from .forms import CarForm
@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('home')
    else:
        form = CarForm()

    return render(request, 'pages/add_car.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, user=request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm(instance=car)

    return render(request, 'pages/add_car.html', {'form': form})