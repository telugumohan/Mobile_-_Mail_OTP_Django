from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('validate_otp/', views.validate_otp, name='validate_otp'),
    path('login/', views.login, name='login'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('login_success/', views.login_success, name='login_success'),
]
