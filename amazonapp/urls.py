from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="home"),
    path('customers/<str:pk>/',customers,name="customers"),
    path('products/',products,name="products"),
    path('createorder/<str:pk>/',createOrder, name="createorder"),
	path('updateorder/<str:pk>/', updateOrder, name="updateorder"),
	path('deleteorder/<str:pk>/', deleteOrder, name="deleteorder"),


]
