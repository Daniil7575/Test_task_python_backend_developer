from django.db import models
from payment.models import Item


class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    # Была идея отправки письма после оформления/оплаты заказа,
    # но и так получилось очень перегруженно (по сравнению с тз)...
    email = models.EmailField(verbose_name='E-mail', default='test@test.ru')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('paid', '-created')

    def __str__(self) -> str:
        return f'Заказ номер {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена в рублях'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price
