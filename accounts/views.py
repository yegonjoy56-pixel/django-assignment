
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from shop.models import Order


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:home")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home:home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("home:home")

@login_required
def dashboard_view(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "orders": orders,
            "total_orders": total_orders,
        },
    )
