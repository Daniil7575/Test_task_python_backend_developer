from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from payment.models import Item
from .cart import Cart
from .models import OrderItem
from .forms import OrderCreationForm


def order_create(request: HttpRequest):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['item'],
                    price=item['price'],
                    quantity=item['quantity'])
            # request.session['order_id'] = order.id
            return redirect('create-checkout-session', pk=order.id)

    else:
        form = OrderCreationForm()
    return render(request, 'order/create.html',
                  {'cart': cart, 'form': form})


@require_POST
def add_item_to_cart(request: HttpRequest, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = Cart(request)
    cart.add(item=item)
    return redirect('item-list')


def clear_cart(request: HttpRequest):
    cart = Cart(request)
    cart.clear()
    return redirect('item-list')
