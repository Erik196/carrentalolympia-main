from django import forms
from django.forms.widgets import DateTimeInput
from .models import Booking
from blog.models import Car
from django.utils.safestring import mark_safe

class CarModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return mark_safe(f'<b>{obj.name}</b>')  # Customize label as needed

class BookingForm(forms.ModelForm):
    car = CarModelChoiceField(
        queryset=Car.objects.all(),
        empty_label=None
    )

    class Meta:
        model = Booking
        fields = ['name', 'surname', 'nationality', 'city', 'address', 'phone_number', 'patent_number', 'insurance', 'period_start', 'period_end']
        widgets = {
            'period_start': DateTimeInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
            'period_end': DateTimeInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
