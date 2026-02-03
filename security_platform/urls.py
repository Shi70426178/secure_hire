from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import home, login_choice, signup_choice


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("bouncer/", include("bouncers.urls")),
    path("customer/", include("customers.urls")),
    path("login/", login_choice, name="login_choice"),
    path("signup/", signup_choice, name="signup_choice"),


]
