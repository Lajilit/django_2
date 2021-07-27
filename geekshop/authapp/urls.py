from django.urls import path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('verify/<email>/<activation_key>/', views.verify,
         name='verify'),
]
