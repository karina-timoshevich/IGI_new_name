from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from .models import Order, PickupLocation


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_location']
        widgets = {
            'pickup_location': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pickup_location'].queryset = PickupLocation.objects.all()