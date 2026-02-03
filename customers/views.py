from django.shortcuts import render, redirect, get_object_or_404
from bouncers.models import Job, BouncerProfile
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import CustomerProfile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def customer_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        # create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # create customer profile
        CustomerProfile.objects.create(
            user=user,
            phone=phone
        )

        login(request, user)
        return redirect("book_bouncer")

    return render(request, "customers/signup.html")



def book_bouncer(request):
    if request.method == "POST":
        city = request.POST.get("city").strip().lower()

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
            customer_name=request.POST.get("customer_name"),
            customer_phone=request.POST.get("customer_phone"),
            city=city,
            location=request.POST.get("location"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            amount=request.POST.get("amount"),
            status="pending",
            bouncer=bouncer
        )

        return redirect("booking_status", job_id=job.id)

    return render(request, "customers/book.html")



def booking_success(request):
    return render(request, "customers/success.html")


def booking_status(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "customers/status.html", {"job": job})


def customer_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        # create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # create customer profile
        CustomerProfile.objects.create(
            user=user,
            phone=phone
        )

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