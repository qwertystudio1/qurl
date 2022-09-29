from django.urls import path
from .views import *

urlpatterns =[
    path('',Home.as_view(),name='home'),
    path('register',signup,name='register'),
    path('login',signin,name='login'),
    path('logout',logout,name='logout'),
    path('about',Home.as_view(),name='about'),
    path('account',myAccount,name='account'),
    path('delete/<str:id>',deleteUrl,name='delete'),
    path('<str:pk>', go,name="go"),
]