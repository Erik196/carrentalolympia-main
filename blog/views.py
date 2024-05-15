from django.shortcuts import render
from .models import Car

def car_list(request):
    cars = Car.objects.prefetch_related('additional_photos').all()
    return render(request, 'blog/car_list.html', {'cars': cars})
