
from django.contrib import admin
from .models import PlantCare


@admin.register(PlantCare)
class PlantCareAdmin(admin.ModelAdmin):
    list_display = (
        "plant",
        "sunlight_requirements",
        "temperature_range",
        "updated_at",
    )

    search_fields = (
        "plant__name",
        "watering_instructions",
        "sunlight_requirements",
    )

    list_filter = ("sunlight_requirements",)
    list_per_page = 20
