# admin.py

from django.contrib import admin
from .models import BusyDate, Booking

admin.site.register(BusyDate)
admin.site.register(Booking)