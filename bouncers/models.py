from django.db import models
from django.contrib.auth.models import User


class BouncerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=100)

    age = models.PositiveIntegerField()
    height_cm = models.PositiveIntegerField()
    experience_years = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.city})"


class Job(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("arrived", "Arrived"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    bouncer = models.ForeignKey(
        BouncerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs"
    )
    customer = models.ForeignKey(
        "customers.CustomerProfile",
        on_delete=models.CASCADE,
        related_name="jobs",
        null=True,
        blank=True
    )

    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)

    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
class BouncerVerificationRequest(models.Model):
    bouncer = models.OneToOneField(
        BouncerProfile,
        on_delete=models.CASCADE,
        related_name="verification_request"
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    aadhar_photo = models.ImageField(upload_to="aadhar_photos/")

    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.bouncer.user.username})"
