from django.urls import path
from . import views


app_name = 'mainapp'

urlpatterns = [
    path('', views.hot_product, name='index'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<int:pk>/page/<int:page>/',
         views.products_list,
         name='category'),
]
