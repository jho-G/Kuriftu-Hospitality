from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from bookings.models import Booking

from .forms import SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account is ready.")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(
        request,
        "registration/signup.html",
        {"form": form, "nav_active": "account"},
    )


@login_required
def dashboard_view(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("room")
        .order_by("-check_in")[:20]
    )
    return render(
        request,
        "dashboard.html",
        {
            "bookings": bookings,
            "nav_active": "dashboard",
        },
    )
