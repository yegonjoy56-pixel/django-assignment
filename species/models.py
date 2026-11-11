
from django.db import models


class Species(models.Model):
    common_name = models.CharField(max_length=150)
    scientific_name = models.CharField(max_length=200, unique=True)
    plant_family = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    native_region = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Species"
        ordering = ["common_name"]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"
