
from django.contrib.auth.models import AbstractUser
from django.db import models
import  datetime
# Create your models here.

class User(AbstractUser):
    image_user = models.ImageField(upload_to='user_profile_photo',default=None)
    number_order = models.IntegerField(default=0)
class WhyChooseUs(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='products_images')

class Feedback(models.Model):
    email = models.CharField(max_length=100)
    user_request = models.TextField(null=True)

    def __str__(self):
        return f"Пользователь {self.email} | Новое обращение"

class ReviewUser(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    description = models.TextField()

class Catalog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="products_photos", default=None)
class BasketUser(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    product = models.ForeignKey(to=Catalog,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

class OrderStatus(models.Model):
    name_status = models.CharField(max_length=40)

class OrderUser(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,default=None)
    number_order = models.IntegerField(default=0)
    summa_order = models.IntegerField(default=0)
    status_order = models.ForeignKey(to= OrderStatus, on_delete= models.CASCADE, default=4)
    date =   models.DateField(default= datetime.datetime.now())

