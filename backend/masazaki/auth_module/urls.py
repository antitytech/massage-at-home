from django.urls import include, path
from rest_framework import routers
from auth_module import views
from rest_framework.authtoken.views import obtain_auth_token
from knox import views as knox_views


urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('update_password/', views.update_password, name='update_password'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

