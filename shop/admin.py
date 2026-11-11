
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("plant", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    list_editable = ("status",)

    search_fields = (
        "full_name",
        "phone_number",
        "delivery_address",
        "user__username",
    )

    readonly_fields = ("created_at", "updated_at")
    inlines = [OrderItemInline]
    list_per_page = 20
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
