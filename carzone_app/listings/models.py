from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name   



class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    CONDITION_CHOICES = [
        ('Brand New', 'Brand New'),
        ('Used', 'Used'),
        ('Semi New', 'Semi new'),
        ('Damaged', 'Damaged'),
        ('Any','Any'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=255)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
    kilometers = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cars')
    color = models.CharField(max_length=50, default='White')
    year = models.PositiveIntegerField()
    
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,  help_text="Price per day/week/month for rent")
    is_featured = models.BooleanField(default=False)

    # Detailed specs
    body_style = models.CharField(max_length=50, default='Convertible')
    engine = models.CharField(max_length=100, default='3.4L Mid-Engine V6')
    drivetrain = models.CharField(max_length=50, default='Rear Wheel Drive')
    exterior_color = models.CharField(max_length=50, default='Lime Gold Metallic')
    interior_color = models.CharField(max_length=50, default='Agate Grey')
    doors = models.PositiveIntegerField(default=2)
    passengers = models.PositiveIntegerField(default=2)
    vin = models.CharField(max_length=100, unique=True, blank=True)
    fuel_mileage_city = models.PositiveIntegerField(default=20)
    fuel_mileage_highway = models.PositiveIntegerField(default=28)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default='Brand New')
    owners = models.CharField(max_length=50, blank=True, null=True)
    warranty = models.CharField(max_length=100, default='3 Years Limited')

    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)

    # Images
    main_image = models.ImageField(upload_to='cars/')
    gallery_image_1 = models.ImageField(upload_to='cars/', null=True, blank=True)
    gallery_image_2 = models.ImageField(upload_to='cars/', null=True, blank=True)
    gallery_image_3 = models.ImageField(upload_to='cars/', null=True, blank=True)
    gallery_image_4 = models.ImageField(upload_to='cars/', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class CarInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # ✅ Replace `car_title`
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    customer_need = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.car.title}"
