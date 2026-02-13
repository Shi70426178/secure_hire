from datetime import datetime
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from bouncers.models import Job, BouncerProfile
from .models import CustomerProfile


def customer_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        user = User.objects.create_user(username=username, password=password)

        CustomerProfile.objects.create(user=user, phone=phone)

        login(request, user)
        return redirect("book_bouncer")

    return render(request, "customers/signup.html")


def customer_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("book_bouncer")
        else:
            error = "Invalid username or password"

    return render(request, "customers/login.html", {"error": error})


@login_required
def book_bouncer(request):
    if request.method == "POST":
        city = request.POST.get("city").strip().lower()

        # ✅ logged in customer
        customer_profile = CustomerProfile.objects.get(user=request.user)

        # ✅ parse datetime-local
        start_time = datetime.fromisoformat(request.POST.get("start_time"))
        end_time = datetime.fromisoformat(request.POST.get("end_time"))

        # ✅ parse amount
        amount = Decimal(request.POST.get("amount"))

        # Find bouncer
        bouncer = (
            BouncerProfile.objects.filter(
                city__iexact=city,
                is_online=True,
                is_verified=True,
                is_active=True
            )
            .exclude(
                jobs__status__in=["accepted", "arrived"]
            )
            .first()
        )

        job = Job.objects.create(
            customer=customer_profile,   # ✅ IMPORTANT
            customer_name=request.POST.get("customer_name"),
            customer_phone=request.POST.get("customer_phone"),
            city=city,
            location=request.POST.get("location"),
            start_time=start_time,
            end_time=end_time,
            amount=amount,
            status="pending",
            bouncer=bouncer
        )

        return redirect("booking_status", job_id=job.id)

    return render(request, "customers/book.html")


@login_required
def booking_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, customer__user=request.user)
    return render(request, "customers/status.html", {"job": job})


@login_required
def customer_profile(request):
    profile = CustomerProfile.objects.filter(user=request.user).first()

    if not profile:
        return redirect("customer_signup")

    bookings = profile.jobs.all().order_by("-created_at")

    return render(request, "customers/profile.html", {
        "profile": profile,
        "bookings": bookings
    })

