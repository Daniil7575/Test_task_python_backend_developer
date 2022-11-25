from django.http import HttpRequest
from typing import Dict
from order.cart import Cart


def cart(request: HttpRequest) -> Dict[str, Cart]:
    return {'cart': Cart(request)}
