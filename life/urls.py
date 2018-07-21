from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('cart/', views.cart, name='cart'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('update/', views.update, name='update')
]