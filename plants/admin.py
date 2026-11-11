from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "species",
        "price",
        "is_available",
        "created_at",
    )

    list_filter = ("is_available", "species")
    search_fields = ("name", "description", "species__common_name")
    list_editable = ("price", "is_available")
    list_per_page = 20
