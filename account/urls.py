from django.urls import path
from .import views


urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/',views.user_logout, name='logout'),

    path('register/',views.register, name='register'),

    path('password_change/',views.password_change, name='password_change'),

    path('password_reset_request/',views.password_reset_request,
         name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/',views.password_reset_confirm,
         name='password_reset_confirm'),

     path('edit/',views.edit,name='edit'),
     path('users/',views.user_list, name='user_list'),
     path('users/<username>/',views.user_detail, name='user_detail'),
]

