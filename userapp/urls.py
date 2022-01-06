from django.contrib import admin
from django.urls import path
from .views import Signup,Login,Details,clear,logout,base

urlpatterns = [
    path('',base,name='base'),
    path('signup',Signup.as_view(),name = 'signup'),
    path('login',Login.as_view(),name = 'login'),
    path('details',Details.as_view(),name = 'details'),
    path('clear',clear,name='clear'),
    path('logout',logout,name = 'logout'),
]