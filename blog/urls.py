from django.contrib import admin
from django.urls import path, include  # Import include
from django.conf import settings
from django.conf.urls.static import static
from .views import car_list

urlpatterns = [
    path('', car_list, name='car_list'),
    path('bookings/', include('bookings.urls')),  # Include URLs from the bookings app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
