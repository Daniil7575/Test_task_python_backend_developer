from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import Item

import stripe
from django.db.models import Sum
from order.models import Order
from order.cart import Cart


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        order.is_formed = True
        order.save()
        item_quantities = order.items.values('item_id') \
            .annotate(quantity=Sum('quantity'))

        items = {
            Item.objects.values('name').get(pk=group['item_id'])['name']:
            group['quantity']
            for group in item_quantities
        }

        domain = f'http://127.0.0.1:8000/{order.id}'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': int(order.get_total_cost() * 100),
                    'product_data': {
                        'name': f'Заказ номер {order.id}',
                        'description': '; '.join(
                            [f'{name} x{cnt}' for name, cnt in items.items()]
                        ),
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url, order_id=self.kwargs['pk'])


class SuccessView(TemplateView):
    template_name = "payment/success.html"

    def get(self, request, pk):
        cart = Cart(request)
        cart.clear()
        order = Order.objects.get(pk=pk)
        order.paid = True
        order.save()
        query = self.request.GET.get('session_id')
        context = {'session_id': query, 'order_id': order.id}
        return render(request, self.template_name, context)


class CancelView(TemplateView):
    template_name = "payment/cancel.html"

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.save()
        return render(request, self.template_name)


class ItemDetailView(TemplateView):
    template_name = 'payment/item_detail.html'

    def get_context_data(self, item_id, **kwargs):
        item = Item.objects.get(id=item_id)
        # prices = OrderItem.objects.filter(product=product)
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
        })
        return context


class ItemListView(ListView):
    template_name = 'payment/items.html'
    model = Item
    context_object_name = 'items'
    queryset = Item.objects.all()
