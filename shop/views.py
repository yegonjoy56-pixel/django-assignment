
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

from plants.models import Plant
from .cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.db.models import Sum
from decimal import Decimal


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, plant_id):
    cart = Cart(request)

    plant = get_object_or_404(
        Plant,
        id=plant_id,
        is_available=True
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart.add(plant=plant, quantity=quantity)

    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, plant_id):
    cart = Cart(request)
    plant = get_object_or_404(Plant, id=plant_id)
    cart.remove(plant)

    return redirect("shop:cart_detail")


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("shop:cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data["full_name"],
                    phone_number=form.cleaned_data["phone_number"],
                    delivery_address=form.cleaned_data["delivery_address"],
                    payment_method=form.cleaned_data["payment_method"],
                )

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        plant=item["plant"],
                        quantity=item["quantity"],
                        price=item["price"],
                    )

            request.session["cart"] = {}
            messages.success(
                request,
                f"Your order #{order.pk} has been placed successfully!"
            )
            return redirect("shop:order_success", order_id=order.pk)

    else:
        form = CheckoutForm()

    return render(
        request,
        "shop/checkout.html",
        {"form": form, "cart": cart},
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, "shop/order_success.html", {
        "order": order
    })
@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related("items__plant").order_by("-created_at")

    return render(
        request,
        "shop/my_orders.html",
        {"orders": orders},
    )


@staff_member_required
def admin_dashboard(request):
    total_plants = Plant.objects.count()

    available_plants = Plant.objects.filter(
        is_available=True
    ).count()

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    order_statuses = [
    {
        "label": label,
        "count": Order.objects.filter(status=value).count(),
    }
    for value, label in Order.STATUS_CHOICES
    ]

    recent_orders = Order.objects.select_related(
    "user"
    ).order_by("-created_at")[:5]

    inventory_plants = Plant.objects.select_related(
    "species"
    ).order_by("name")[:5]

    sales_orders = Order.objects.filter(
        status__in=["processing", "shipped", "delivered"]
    )

    total_sales = sum(
        (order.total_amount for order in sales_orders),
        Decimal("0.00")
    )

    return render(request, "shop/admin_dashboard.html", {
    "total_plants": total_plants,
    "available_plants": available_plants,
    "total_orders": total_orders,
    "pending_orders": pending_orders,
    "total_sales": total_sales,
    "recent_orders": recent_orders,
    "inventory_plants": inventory_plants,
    "order_statuses": order_statuses,
})