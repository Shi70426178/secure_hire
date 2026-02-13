from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.book_bouncer, name="book_bouncer"),
    path("status/<int:job_id>/", views.booking_status, name="booking_status"),
    path("signup/", views.customer_signup, name="customer_signup"),
    path("login/", views.customer_login, name="customer_login"),
    path("profile/", views.customer_profile, name="customer_profile"),


]
