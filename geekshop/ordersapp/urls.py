from django.urls import path
from . import views

app_name="ordersapp"

urlpatterns = [
   path('',
        views.OrderList.as_view(),
        name='orders_list'),
   path('forming/complete/<pk>)/',
        views.order_forming_complete,
        name='order_forming_complete'),
   path('create/',
        views.OrderItemsCreate.as_view(),
           name='order_create'),
   path('read/<pk>/',
        views.OrderRead.as_view(),
        name='order_read'),
   path('update/<pk>/',
        views.OrderItemsUpdate.as_view(),
        name='order_update'),
   path('delete/<pk>/',
        views.OrderDelete.as_view(),
        name='order_delete'),
]