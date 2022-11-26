from django import forms
from .models import Order
from django.core.exceptions import ValidationError
from coupon.models import Coupon
from django.utils import timezone


class OrderCreationForm(forms.ModelForm):
    def clean_coupon_code(self):
        data = self.cleaned_data['coupon_code']
        if data is None:
            return data
        try:
            coupon = Coupon.objects.get(code=data)
        except Coupon.DoesNotExist:
            raise ValidationError('Такого кода нет.', 'invalid')
        is_date_valid = coupon.valid_to > timezone.now() > coupon.valid_from
        if coupon.active and is_date_valid:
            return data
        raise ValidationError('Данный код не активен.', 'expired')

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'coupon_code'
        ]
