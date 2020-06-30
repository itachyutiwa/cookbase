from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('dashboard/', home, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('customer/<str:pk_test>/', customer, name='customer'),
    path('create-customer/', createCustomer, name='create-customer'),
    path('products/', products, name='products'),
    path('create-order/<str:pk>/', createOrder, name='create-order'),
    path('update-order/<str:pk>/', updateOrder, name='update-order'),
    path('delete-order/<str:pk>/', deleteOrder, name='delete-order'),
    path('update-customer/<str:pk>/', updateCustomer, name='update-customer'),
    path('delete-customer/<str:pk>/', deleteCustomer, name='delete-customer'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('user/', userPage, name='user'),
    path('settings/', accountSettings, name='settings'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),


    
]