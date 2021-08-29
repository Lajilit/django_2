from django.urls import path
# from django.views.decorators.cache import cache_page
from . import views


app_name = 'mainapp'

urlpatterns = [
    path('', views.hot_product, name='index'),
    path('product/<int:pk>/',
         views.product,
         name='product'
         ),
    path('category/<int:pk>/',
         views.products_list,
         name='category'
         ),
    path('category/<int:pk>/page/<int:page>/',
         views.products_list,
         name='category'
         ),
    # path('category/<int:pk>/ajax/',
    #      cache_page(3600)(views.products_ajax)
    #      ),
    # path('category/<int:pk>/page/<int:page>/ajax/',
    #      cache_page(3600)(views.products_ajax)
    #      ),
]
