
from django.shortcuts import render, get_object_or_404
from .models import Plant
from care.models import PlantCare


def plant_list(request):
    plants = Plant.objects.filter(is_available=True).select_related("species")

    return render(
        request,
        "plants/plant_list.html",
        {"plants": plants}
    )


def plant_detail(request, plant_id):
    plant = get_object_or_404(
        Plant.objects.select_related("species"),
        id=plant_id,
        is_available=True
    )

    try:
        care_guide = plant.care_guide
    except PlantCare.DoesNotExist:
        care_guide = None

    return render(
        request,
        "plants/plant_detail.html",
        {
            "plant": plant,
            "care_guide": care_guide,
        }
    )
