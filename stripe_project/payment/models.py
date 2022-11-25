from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'item_id': self.pk})
