
from django.db import models
from django.contrib.auth.models import User
from plants.models import Plant


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="plant_orders"
    )
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    delivery_address = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    PAYMENT_METHOD_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("cash_on_delivery", "Cash on Delivery"),
        ("card", "Card Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash_on_delivery"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

    @property
    def total_amount(self):
        return sum(
            item.price * item.quantity
            for item in self.items.all()
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    plant = models.ForeignKey(
        Plant,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.plant.name} x {self.quantity}"
