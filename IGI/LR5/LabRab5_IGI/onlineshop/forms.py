from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

from .models import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
