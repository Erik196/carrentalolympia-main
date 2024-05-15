from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import timedelta
from .forms import BookingForm
from .models import Booking
from blog.models import Car
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
import requests
from .models import BusyDate
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            car = form.cleaned_data['car'].id
            start_time = form.cleaned_data['period_start']
            end_time = form.cleaned_data['period_end']

            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            nationality = form.cleaned_data['nationality']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            patent_number = form.cleaned_data['patent_number']
            insurance = form.cleaned_data['insurance']

            booking = form.save(commit=False)
            booking.save()

            # Store the unavailable date range
            BusyDate.objects.create(
                car_id=car,
                start_date=start_time,
                end_date=end_time
            )

            form_data_string = f"Car ID: {car}\nStart Time: {start_time}\nEnd Time: {end_time}\n\nName: {name}\nSurname: {surname}\nNationality: {nationality}\nCity: {city}\n Address: {address}\nPhone Number: {phone_number}\nPatent Number: {patent_number}\nInsurance: {insurance}"

            send_mail(
                'Booking Form',
                form_data_string,
                settings.EMAIL_HOST_USER,
                ['carrentalolympia@gmail.com'],
                fail_silently=False
            )

            messages.success(request, "Your booking has been successfully submitted.")
            return redirect(reverse('booking_confirmation'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        # Set default values for period_start and period_end
        start_time = timezone.now().strftime('%Y-%m-%d')
        end_time = (timezone.now().date()  + timedelta(days=1)).strftime('%Y-%m-%d')
        initial_data = {'period_start': start_time, 'period_end': end_time}
        form = BookingForm(initial=initial_data)
        
        # Retrieve unavailable dates for selected car
        car_id = request.GET.get('car_id')  # Assuming the car_id is passed in the request
        if car_id:
            try:
                car = Car.objects.get(id=car_id)
                start_date = timezone.now().strftime('%Y-%m-%d')
                end_date = (timezone.now().date()  + timedelta(days=1)).strftime('%Y-%m-%d')
                response = requests.get(
                    reverse('get_unavailable_dates', args=[car_id]),
                    params={'start_date': start_date, 'end_date': end_date}
                )
                if response.status_code == 200:
                    unavailable_dates_str = response.text.split('\n')
                    unavailable_dates = [parse_date(date_str) for date_str in unavailable_dates_str]
                    form.fields['period_start'].unavailable_dates = unavailable_dates
                    form.fields['period_end'].unavailable_dates = unavailable_dates
                else:
                    messages.error(request, "Failed to retrieve unavailable dates.")
            except Car.DoesNotExist:
                messages.error(request, "Car not found.")
    return render(request, 'bookings/booking_form.html', {'form': form})

def booking_confirmation(request):
    try:
        latest_booking = Booking.objects.latest('id')
    except Booking.DoesNotExist:
        latest_booking = None
        messages.error(request, "No bookings found.")
        return redirect('booking_form')  # Redirect back to booking form if no bookings found
    return render(request, 'bookings/booking_confirmation.html', {'booking': latest_booking})

def get_unavailable_dates(request, car_id):
    try:
        busy_dates = BusyDate.objects.filter(car_id=car_id)
        busy_dates_json = [{'title': 'Busy', 'start': str(busy.start_date), 'end': str(busy.end_date)} for busy in busy_dates]
        return JsonResponse(busy_dates_json, safe=False)
    except BusyDate.DoesNotExist:
        return JsonResponse([], safe=False)

def render_calendar(request):
    busy_dates = BusyDate.objects.all()
    busy_dates_json = [{'title': 'Unavailable', 'start': str(busy.start_date), 'end': str(busy.end_date)} for busy in busy_dates]
    return JsonResponse(busy_dates_json, safe=False)
