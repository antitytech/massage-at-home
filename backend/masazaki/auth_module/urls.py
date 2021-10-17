from django.urls import include, path
from rest_framework import routers
from auth_module import views
from rest_framework.authtoken.views import obtain_auth_token
from knox import views as knox_views


urlpatterns = [
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
     path('register/', views.register, name='register'),
]

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('register/', views.register),
#     path('login/', obtain_auth_token)
# ]