from django.contrib import admin
from .models import BouncerProfile
from .models import Job

@admin.register(BouncerProfile)
class BouncerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'city',
        'is_verified',
        'is_active',
        'is_online',
        'created_at',
    )

    list_filter = ('is_verified', 'is_active', 'city')
    search_fields = ('user__username', 'phone', 'city')
    ordering = ('-created_at',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "city",
        "bouncer",
        "status",
        "amount",
        "start_time",
    )

    list_filter = ("status", "city")
    search_fields = ("customer_name", "customer_phone", "location")