from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta

from incidents.models import Incident, IncidentLog
from .forms import CustomUserCreationForm, AssignAnalystForm

User = get_user_model()


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can login now.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# =========================
# DASHBOARD (ROLE BASED)
# =========================
@login_required
def dashboard_view(request):
    user = request.user
    role = (user.role or "user").lower()

    # Base queryset for everyone
    if role == "admin":
        incidents = Incident.objects.all()
    elif role == "analyst":
        incidents = Incident.objects.filter(assigned_to=user)
    else:
        incidents = Incident.objects.filter(created_by=user)

    # Standardized Count Logic
    # Standardized Count Logic - Using __iexact to fix the "0" count issue
    context = {
        "total_count": incidents.count(),
        "open_count": incidents.filter(status__iexact="OPEN").count(),
        "progress_count": incidents.filter(status__iexact="IN_PROGRESS").count(),
        "resolved_count": incidents.filter(status__iexact="RESOLVED").count(),
        "closed_count": incidents.filter(status__iexact="CLOSED").count(),
    }

    # ================= ADMIN DASHBOARD =================
    if role == "admin":
        overdue_time = timezone.now() - timedelta(hours=24)
        context.update({
            "overdue_incidents": incidents.filter(created_at__lt=overdue_time, status__in=["OPEN", "IN_PROGRESS"]),
            "recent_incidents": incidents.order_by("-created_at")[:8],
            "recent_logs": IncidentLog.objects.order_by("-timestamp")[:8],
        })
        return render(request, "accounts/admin_dashboard.html", context)

    # ================= ANALYST DASHBOARD =================
    elif role == "analyst":
        context.update({
            "assigned_incidents": incidents.order_by("-created_at"),
            "assigned_count": incidents.filter(status="ASSIGNED").count(),
            "recent_logs": IncidentLog.objects.filter(changed_by=user).order_by("-timestamp")[:5],
        })
        return render(request, "accounts/analyst_dashboard.html", context)

    # ================= USER DASHBOARD =================
    else:
        context.update({
            "my_incidents": incidents.order_by("-created_at"),
        })
        return render(request, "accounts/user_dashboard.html", context)



# =========================
# ADMIN: ASSIGN ANALYST ROLE BY EMAIL
# =========================
@login_required
def assign_analyst_role(request):

    # Only admin allowed
    if (request.user.role or "").lower() != "admin":
        return HttpResponseForbidden("Only admin can assign analyst role.")

    if request.method == "POST":
        form = AssignAnalystForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)

                if (user.role or "").lower() == "analyst":
                    messages.warning(request, "User is already an analyst.")
                else:
                    user.role = "analyst"
                    user.save()

                    # Audit Log
                    IncidentLog.objects.create(
                        action=f"Admin promoted {user.username} to Analyst",
                        changed_by=request.user
                    )

                    messages.success(request, f"{user.username} is now an Analyst.")

            except User.DoesNotExist:
                messages.error(request, "No user found with this email.")

            return redirect("assign_analyst_role")

    else:
        form = AssignAnalystForm()

    return render(request, "accounts/assign_analyst.html", {"form": form})
