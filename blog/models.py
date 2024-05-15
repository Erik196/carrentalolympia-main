from django.db import models
from django.utils import timezone

class Car(models.Model):
    name = models.CharField(max_length=100)
    main_photo = models.ImageField(upload_to='cars/')
    car_type = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='additional_photos')
    photo = models.ImageField(upload_to='cars/others/')

    def __str__(self):
        return f'Photo for {self.car.name}'