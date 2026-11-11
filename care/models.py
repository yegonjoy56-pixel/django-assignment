
from django.db import models
from plants.models import Plant


class PlantCare(models.Model):
    plant = models.OneToOneField(
        Plant,
        on_delete=models.CASCADE,
        related_name="care_guide"
    )
    watering_instructions = models.TextField()
    sunlight_requirements = models.CharField(max_length=200)
    soil_requirements = models.CharField(max_length=200, blank=True)
    temperature_range = models.CharField(max_length=100, blank=True)
    fertilizing_instructions = models.TextField(blank=True)
    additional_tips = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plant Care Guide"
        verbose_name_plural = "Plant Care Guides"

    def __str__(self):
        return f"Care guide for {self.plant.name}"
