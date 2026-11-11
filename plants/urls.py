
from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("", views.plant_list, name="plant_list"),
    path("<int:plant_id>/", views.plant_detail, name="plant_detail"),
]
