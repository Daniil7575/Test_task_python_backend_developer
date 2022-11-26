from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator
)
import stripe


class Coupon(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r"\A[a-zA-Z0-9_\-]+$")],
        verbose_name='Активационный код'
    )
    valid_from = models.DateTimeField(verbose_name='Активен с')
    valid_to = models.DateTimeField(verbose_name='Активен до')
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Скидка в процентах'
    )
    active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            stripe.Coupon.create(id=self.code,
                                 percent_off=self.discount)
        return super(Coupon, self).save(*args, **kwargs)
