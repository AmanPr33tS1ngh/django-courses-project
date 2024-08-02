"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import About, ContactUs, Index, MyTokenObtainPairView, SignIn, SignUp, LogOut

urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('sign_in/', SignIn.as_view(), name='users'),
    path('sign_up/', SignUp.as_view(), name='users'),
    path('sign_out/', LogOut.as_view(), name='users'),

    path("about", About.as_view(), name="about"),
    path("contact", ContactUs.as_view(), name="contact"),
    path('admin/', admin.site.urls),
    path('course/', include('course.urls')),
    path("user/", include('user.urls')),
    path("appointment/", include('appointment.urls')),
]
