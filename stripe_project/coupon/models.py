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
        validators=[RegexValidator(r"\A[a-zA-Z0-9_\-]+$")]
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            stripe.Coupon.create(id=self.code,
                                 percent_off=self.discount)
        return super(Coupon, self).save(*args, **kwargs)
