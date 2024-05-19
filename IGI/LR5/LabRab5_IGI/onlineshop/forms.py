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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.validators import RegexValidator


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        help_text="Required. Format: DD.MM.YYYY",
        input_formats=['%d.%m.%Y']
    )
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
                message="Phone number must be entered in the format: '+375 (29) XXX-XX-XX'. Up to 15 digits allowed."
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2", "date_of_birth", "phone_number"]

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 18 years old to register.')
        return dob

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_location']
        widgets = {
            'pickup_location': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['pickup_location'].empty_label = None

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ['rating', 'text']