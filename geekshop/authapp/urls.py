from django.urls import path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('verify_link_fail/', views.link_send_fail,
         name='verify_link_fail'),
    path('verify_link_send/', views.link_send_sucsess,
         name='verify_link_send'),
    path('verify/<email>/<activation_key>/', views.verify,
         name='verify'),
]
