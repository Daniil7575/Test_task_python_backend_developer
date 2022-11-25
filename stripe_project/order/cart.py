from django.http.request import HttpRequest
from django.conf import settings
from payment.models import Item
from decimal import Decimal


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)

        cart = self.cart.copy()

        for item in items:
            cart[str(item.id)]['item'] = item

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['quantity'] * item['price']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, item: Item, quantity: int = 1) -> None:
        item_id = str(item.id)

        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(item.price)
            }

        self.cart[item_id]['quantity'] += 1

        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def remove(self, item: Item) -> None:
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self) -> None:
        del self.session[settings.CART_SESSION_ID]
        self.save()
