from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.bouncer_login, name="bouncer_login"),
    path("logout/", views.bouncer_logout, name="bouncer_logout"),
    path("dashboard/", views.bouncer_dashboard, name="bouncer_dashboard"),
    path("toggle-status/", views.toggle_online_status, name="toggle_status"),
    path("job/<int:job_id>/accept/", views.accept_job, name="accept_job"),
    path("job/<int:job_id>/reject/", views.reject_job, name="reject_job"),
    path("job/<int:job_id>/status/<str:status>/", views.update_job_status, name="update_job_status"),
    path("signup/", views.bouncer_signup, name="bouncer_signup"),
    path("verify/", views.verify_now, name="verify_now"),




]
