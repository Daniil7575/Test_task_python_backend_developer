from django.urls import path
from . import views


urlpatterns = [
    path(
        'item/<int:item_id>/',
        views.ItemDetailView.as_view(),
        name='item-detail'
    ),
    path(
        'buy/<int:pk>/',
        views.CreateCheckoutSessionView.as_view(),
        name='create-checkout-session'
    ),
    path('<int:pk>/cancel/', views.CancelView.as_view(), name='cancel'),
    path('<int:pk>/success/', views.SuccessView.as_view(), name='success'),
    path('item/', views.ItemListView.as_view(), name='item-list'),

]
