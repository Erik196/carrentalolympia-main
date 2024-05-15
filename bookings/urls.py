from django.urls import path
from .views import booking_form
from . import views

urlpatterns = [
    path('', booking_form, name='booking_form'),
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('unavailable-dates/<int:car_id>/', views.get_unavailable_dates, name='unavailable_dates'),
]
