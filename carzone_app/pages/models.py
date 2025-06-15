from django.db import models

# Create your models here.
class Teams(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    designation=models.CharField(max_length=200)
    image=models.ImageField(upload_to='photos/%Y/%m/%d/')
    facebook_link=models.URLField(max_length=100)
    twitter_link=models.URLField(max_length=100)
    google_plus_link=models.URLField(max_length=100)
    create_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name +' '+ self.last_name

    class Meta:
        verbose_name_plural='Teams'

