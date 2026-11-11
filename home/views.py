
from django.shortcuts import render
from plants.models import Plant


def home(request):
    featured_plants = Plant.objects.filter(
        is_available=True
    ).select_related("species")[:6]

    return render(
        request,
        "home/home.html",
        {"featured_plants": featured_plants}
    )
