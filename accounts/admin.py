
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "phone_number",
        "location",
    )
    list_filter = ("role",)
    search_fields = ("user__username", "phone_number")
