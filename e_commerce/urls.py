"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from commerce_api.views import RegistrationAPIView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_auth.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("commerce_api.urls")),
    # path('api/v1/auth/auth-token', obtain_auth_token, name='obtain-auth-token')
    path("auth/register/", RegistrationAPIView.as_view(), name="register"),
    # path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path("api-auth/", include("rest_framework.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("login/", LoginView.as_view(), name="login")
    # path('auth/refresh-token', TokenRefreshView.as_view(), name='refreshtoken'),
]
