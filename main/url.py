from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home , name = 'home'),
    path('login',views.login_view , name="login"),
    path('login/authenticate', views.login_handle , name='login_handle'),
    path('logout',views.logout_handle, name="logout"),
    path('create_acc',views.create_user, name='create_user')
]