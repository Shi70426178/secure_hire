from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import BouncerProfile

from .models import BouncerProfile, Job



def bouncer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = BouncerProfile.objects.get(user=user)

                if not profile.is_active:
                    messages.error(request, "Account is inactive. Contact admin.")
                    return redirect("bouncer_login")

                login(request, user)
                return redirect("bouncer_dashboard")

            except BouncerProfile.DoesNotExist:
                messages.error(request, "You are not registered as a bouncer.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "bouncers/login.html")


@login_required
def bouncer_logout(request):
    logout(request)
    return redirect("bouncer_login")


@login_required
def bouncer_dashboard(request):
    profile = BouncerProfile.objects.get(user=request.user)

    active_jobs = profile.jobs.exclude(
        status__in=["completed", "cancelled"]
    ).order_by("start_time")

    completed_jobs = profile.jobs.filter(
        status="completed"
    ).order_by("-end_time")

    total_earnings = completed_jobs.aggregate(
        total=models.Sum("amount")
    )["total"] or 0

    return render(
        request,
        "bouncers/dashboard.html",
        {
            "profile": profile,
            "jobs": active_jobs,
            "completed_jobs": completed_jobs,
            "total_earnings": total_earnings,
        }
    )


@login_required
def toggle_online_status(request):
    profile = BouncerProfile.objects.get(user=request.user)

    active_job_exists = Job.objects.filter(
        bouncer=profile,
        status__in=["accepted", "arrived"]
    ).exists()

    if active_job_exists:
        return redirect("bouncer_dashboard")

    if profile.is_verified and profile.is_active:
        profile.is_online = not profile.is_online
        profile.save()

    return redirect("bouncer_dashboard")


@login_required
def accept_job(request, job_id):
    profile = BouncerProfile.objects.get(user=request.user)

    # 🔒 check if bouncer already has an active job
    active_job_exists = Job.objects.filter(
        bouncer=profile,
        status__in=["accepted", "arrived"]
    ).exists()

    if active_job_exists:
        # silently block (later we can show message)
        return redirect("bouncer_dashboard")

    job = Job.objects.get(
        id=job_id,
        bouncer=profile,
        status="pending"
    )

    job.status = "accepted"
    job.save()

    return redirect("bouncer_dashboard")


@login_required
def reject_job(request, job_id):
    profile = BouncerProfile.objects.get(user=request.user)

    job = Job.objects.get(
        id=job_id,
        bouncer=profile,
        status="pending"
    )

    job.status = "cancelled"
    job.bouncer = None  # free the job
    job.save()

    return redirect("bouncer_dashboard")


@login_required
def update_job_status(request, job_id, status):
    profile = BouncerProfile.objects.get(user=request.user)

    job = Job.objects.get(id=job_id, bouncer=profile)

    allowed_transitions = {
        "accepted": ["arrived"],
        "arrived": ["completed"],
    }

    if status in allowed_transitions.get(job.status, []):
        job.status = status
        job.save()

    return redirect("bouncer_dashboard")

def bouncer_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        age = request.POST.get("age")
        height = request.POST.get("height")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        BouncerProfile.objects.create(
            user=user,
            phone=phone,
            city=city.strip().lower(),
            age=age,
            height_cm=height,
            is_verified=False,  # admin approval needed
            is_active=True
        )

        login(request, user)
        return redirect("bouncer_dashboard")

    return render(request, "bouncers/signup.html")
