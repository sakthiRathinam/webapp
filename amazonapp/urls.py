from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
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
	path('reset_password/',auth_views.PasswordResetView.as_view(template_name="html/password_reset.html"),
     name="reset_password"),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="html/password_reset_sent.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="html/password_reset_form.html"), 
     name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="html/password_reset_done.html"), 
        name="password_reset_complete"),
    path('createorder/',createOrderr, name="createorderr"),
]
