
from django.db import models
from species.models import Species


class Plant(models.Model):
    name = models.CharField(max_length=150)
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name="plants"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to="plants/",
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


