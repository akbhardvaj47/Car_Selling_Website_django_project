from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from account.models import Contact
from listings.models import Car, CarInquiry, Category

# ------------------ LOGIN VIEW ------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'pages/login.html')


# ------------------ REGISTER VIEW ------------------
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'pages/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'pages/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'pages/signup.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        send_mail(
            subject='Welcome to Our Car Selling Store!',
            message=f"""
Hi {first_name},

Welcome to Ak Car Store! 🚗

We're excited to have you on board. Whether you're looking to buy your dream car or sell your current one, you've just joined a community of car enthusiasts who value great deals and trusted service.

Here’s what you can do next:
- 🚘 Browse thousands of verified car listings
- 📤 Post your own car for sale with ease
- 🤝 Connect directly with buyers and sellers

We're here to help you every mile of the way.

Thanks again for joining us — your journey starts now!

Best regards,  
The Ak Car Store Team  
www.akcarstore.com
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'pages/signup.html')


# ------------------ LOGOUT VIEW ------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------ DASHBOARD ------------------
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/admin/')
    user = request.user
    cars = CarInquiry.objects.filter(user=user)
    return render(request, 'pages/dashboard.html', {
        'cars': cars,
    })


# ------------------ CONTACT ------------------
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save to DB
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            phone=phone,
            message=message
        )

        send_mail(
            subject="Thank You for Contacting Ak Car Store!",
            message=f"""
Hi {name},

Thank you for reaching out to Ak Car Store!

We’ve received your message and one of our team members will get back to you shortly.

Here’s a summary of your inquiry:
-------------------------------------------------
Subject: {subject}
Message: {message}
-------------------------------------------------

If you have any urgent questions, feel free to call us at +91 83031 66787 or reply to this email (anshh9335@gmail.com).

Thank you again for your interest in Ak Car Store — your trusted place to buy and sell cars!

Best regards,  
Ak Car Store Team  
www.akcarstore.com
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True
        )

        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')

    return render(request, 'pages/contact.html')

