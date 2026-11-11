
from django.contrib import admin
from .models import Species


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "plant_family",
        "native_region",
    )

    search_fields = (
        "common_name",
        "scientific_name",
        "plant_family",
    )

    list_filter = ("plant_family",)
    list_per_page = 20
