from django.urls import path

from . import views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/',
         views.UserCreateView.as_view(),
         name='user_create'
         ),
    path('users/read/',
         views.UsersListView.as_view(),
         name='users'
         ),
    path('users/update/<int:pk>/',
         views.UserUpdateView.as_view(),
         name='user_update'
         ),
    path('users/delete/<int:pk>/',
         views.UserDeleteView.as_view(),
         name='user_delete'
         ),

    path('categories/create/',
         views.ProductCategoryCreateView.as_view(),
         name='category_create'
         ),
    path('categories/read/',
         views.ProductCategoryListView.as_view(),
         name='categories'
         ),
    path('categories/update/<int:pk>/',
         views.ProductCategoryUpdateView.as_view(),
         name='category_update'
         ),
    path('categories/delete/<int:pk>/',
         views.ProductCategoryDeleteView.as_view(),
         name='category_delete'
         ),

    path('products/create/category/<int:pk>/',
         views.ProductCreateView.as_view(),
         name='product_create'
         ),
    path('products/read/category/<int:pk>/',
         views.ProductsListView.as_view(),
         name='products'
         ),
    path('products/read/<int:pk>/',
         views.ProductDetailView.as_view(),
         name='product_read'
         ),
    path('products/update/<int:pk>/',
         views.ProductUpdateView.as_view(),
         name='product_update'
         ),
    path('products/delete/<int:pk>/',
         views.ProductDeleteView.as_view(),
         name='product_delete'
         ),
    path('orders/read/user/<int:pk>/',
         views.OrderListView.as_view(),
         name='orders_list'
         ),
    path('orders/read/<int:pk>/',
         views.OrderDetailView.as_view(),
         name='order_read'
         ),
    path('orders/update/<int:pk>/',
         views.OrderItemsUpdateView.as_view(),
         name='order_update'
         ),
    path('orders/delete/<int:pk>/',
         views.OrderDeleteView.as_view(),
         name='order_delete'
         ),
    path('forming/complete/<pk>)/',
         views.order_collect,
         name='order_collect'),
    path('payment/<pk>)/',
         views.order_send,
         name='order_send'),

]
