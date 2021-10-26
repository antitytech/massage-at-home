from auth_module import views
from knox import views as knox_views
from django.urls import include, path
from django_email_verification import urls as email_urls


urlpatterns = [
     path('', views.home, name='home'),
     path('email/', include(email_urls)),
     path('user/login/', views.LoginView.as_view(), name='login'),
     path('user/logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('user/recover/', include('django.contrib.auth.urls')),
     path('user/register/', views.register, name='register'),
     path('user/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
     path('user/view_profile/', views.view_profile, name='view_profile'),
     path('user/verify_email/', views.verify_email, name='verify_email'),
     path('user/update_profile/', views.update_profile, name='update_profile'),
     path('user/update_password/', views.update_password, name='update_password'),
]
