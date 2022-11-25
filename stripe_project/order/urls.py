from django.urls import path
from . import views


urlpatterns = [
    path(
        'add-to-cart/<int:item_id>/',
        views.add_item_to_cart, name='add-to-cart',
    ),
    path('create/', views.order_create, name='order-create'),
    path('clear-cart/', views.clear_cart, name='clear-cart')
]
