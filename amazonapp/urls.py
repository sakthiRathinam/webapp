from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="home"),
    path('customers/<str:pk>/',customers,name="customers"),
    path('products/',products,name="products"),
    path('createorder/<str:pk>/',createOrder, name="createorder"),
	path('updateorder/<str:pk>/', updateOrder, name="updateorder"),
	path('deleteorder/<str:pk>/', deleteOrder, name="deleteorder"),
	path('register/',registerPage,name="register"),
	path('login/',loginPage,name="login"),
	path('logout/',logoutUser,name='logout'),
	path('user/',userPage,name='user-page'),
	path('settings/',accountSettings,name='settings'),

]
