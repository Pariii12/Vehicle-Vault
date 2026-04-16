from django import forms
from .models import (
    Vehicle,
    VehicleImage,
    TestDrive,
    VehicleInspection,
    Message,
    Offer,
    Transaction
)
from django.forms.widgets import ClearableFileInput



class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

class VehicleForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={ 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Vehicle
        exclude = ['seller', 'status', 'listed_at', 'updated_at', 'featured']

        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'variant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Variant'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'km_driven': forms.NumberInput(attrs={'class': 'form-control'}),
            'owner_type': forms.TextInput(attrs={'class': 'form-control'}),
            'body_type': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_cc': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_power': forms.TextInput(attrs={'class': 'form-control'}),
            'torque': forms.TextInput(attrs={'class': 'form-control'}),
            'seating_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }



class VehicleImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=MultiFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = VehicleImage
        fields = ['image']



class VehicleFilterForm(forms.Form):

    brand = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brand'
        })
    )

    model = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Model'
        })
    )

    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )

    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )

    min_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Year'
        })
    )

    max_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Year'
        })
    )

    fuel_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Fuel Type')] + Vehicle.FUEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    transmission = forms.ChoiceField(
        required=False,
        choices=[('', 'Transmission')] + Vehicle.TRANSMISSION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    body_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Body Type')] + Vehicle.BODY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )

    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State'
        })
    )

    radius = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Any Distance'),
            ('10', 'Within 10 km'),
            ('25', 'Within 25 km'),
            ('50', 'Within 50 km'),
            ('100', 'Within 100 km'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    user_lat = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )

    user_lon = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['scheduled_date']
        widgets = {
            'scheduled_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }


class VehicleInspectionForm(forms.ModelForm):
    class Meta:
        model = VehicleInspection
        fields = ['report_details', 'inspection_date', 'inspection_status']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'report_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'inspection_status': forms.Select(attrs={'class': 'form-select'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_text']
        widgets = {
            'message_text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message...'}
            ),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offered_price']
        widgets = {
            'offered_price': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your offer price'}
            ),
        }



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['final_price']