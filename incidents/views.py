from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Incident, IncidentLog
from .forms import IncidentCreateForm, IncidentUpdateForm
from django.contrib import messages

# =====================================
# CREATE INCIDENT (USER)
# =====================================
@login_required
def create_incident(request):
    if request.method == "POST":
        form = IncidentCreateForm(request.POST)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.created_by = request.user
            incident.status = "OPEN"
            incident.save()
            return redirect("incidents:incident_list")
    else:
        form = IncidentCreateForm()

    return render(request, "incidents/create_incident.html", {"form": form})


# =====================================
# INCIDENT LIST (ROLE BASED)
# =====================================
@login_required
def incident_list(request):

    user = request.user
    role = user.role.lower()

    # ADMIN → all incidents
    if role == "admin":
        incidents = Incident.objects.all().order_by("-created_at")

    # ANALYST → only assigned incidents
    elif role == "analyst":
        incidents = Incident.objects.filter(assigned_to=user).order_by("-created_at")

    # USER → only created by him
    else:
        incidents = Incident.objects.filter(created_by=user).order_by("-created_at")

    return render(request, "incidents/incident_list.html", {
        "incidents": incidents
    })



# =====================================
# INCIDENT DETAIL
# =====================================
@login_required
def incident_detail(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    return render(request, "incidents/incident_detail.html", {"incident": incident})


# =====================================
# UPDATE INCIDENT (ANALYST + ADMIN)
# =====================================
@login_required
def incident_update(request, pk):
    incident = get_object_or_404(Incident, pk=pk)

    if request.user.role.lower() not in ["analyst", "admin"]:
        return render(request, "403.html", status=403)

    if request.method == "POST":
        form = IncidentUpdateForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect("incidents:incident_detail", pk=pk)
    else:
        form = IncidentUpdateForm(instance=incident)

    return render(request, "incidents/incident_update.html", {
        "form": form,
        "incident": incident
    })

# =====================================
# DELETE INCIDENT (REVISED & SECURE)
# =====================================
@login_required
def delete_incident(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    
    # Ensure role is a string and uppercase for a reliable comparison
    user_role = str(request.user.role).upper()
    
    # 1. PERMISSION CHECK
    is_admin = (user_role == "ADMIN")
    is_owner = (user_role == "USER" and incident.created_by == request.user)
    is_assigned = (user_role == "ANALYST" and incident.assigned_to == request.user)

    if not (is_admin or is_owner or is_assigned):
        messages.error(request, f"Permission Denied. Your role is {user_role}.")
        return redirect("incidents:incident_list")

    # 2. THE ACTUAL DELETE (Must be POST)
    if request.method == "POST":
        incident.delete()
        messages.success(request, "Incident has been permanently deleted.")
        return redirect("incidents:incident_list")

    # 3. THE CONFIRMATION STEP (GET)
    # If the code reaches here, it means permissions are OK, 
    # but we need the user to click "Confirm" in the template.
    return render(request, "incidents/delete_confirm.html", {"incident": incident})

# =====================================
# ASSIGN INCIDENT TO ANALYST
# =====================================
@login_required
def assign_to_me(request, pk):
    incident = get_object_or_404(Incident, pk=pk)

    if request.user.role.lower() != "analyst":
        return render(request, "403.html", status=403)

    old_status = incident.status

    incident.assigned_to = request.user
    incident.status = "ASSIGNED"
    incident.save()

    IncidentLog.objects.create(
        incident=incident,
        changed_by=request.user,
        old_status=old_status,
        new_status="ASSIGNED"
    )

    return redirect("incidents:incident_detail", pk=pk)


# =====================================
# CHANGE STATUS FLOW
# =====================================
@login_required
def change_status(request, pk, new_status):
    incident = get_object_or_404(Incident, pk=pk)
    role = request.user.role.lower()

    # Analyst rules
    if role == "analyst":

        if incident.assigned_to != request.user:
            return HttpResponseForbidden("Not assigned to you.")

        allowed = {
            "ASSIGNED": ["IN_PROGRESS"],
            "IN_PROGRESS": ["RESOLVED"]
        }

        if new_status not in allowed.get(incident.status, []):
            return HttpResponseForbidden("Invalid status transition.")

    # Admin rules
    elif role == "admin":
        if new_status != "CLOSED":
            return HttpResponseForbidden("Admin only closes incidents.")

    else:
        return HttpResponseForbidden("Access denied.")

    old_status = incident.status
    incident.status = new_status
    incident.save()

    IncidentLog.objects.create(
        incident=incident,
        changed_by=request.user,
        old_status=old_status,
        new_status=new_status
    )

    return redirect("incidents:incident_detail", pk=pk)

# =====================================
# VIEW LOGS (ADMIN ONLY)
# =====================================
@login_required
def incident_logs(request, pk):

    if request.user.role.lower() != "admin":
        return render(request, "403.html", status=403)

    incident = get_object_or_404(Incident, pk=pk)
    logs = IncidentLog.objects.filter(
        incident=incident
    ).order_by("-timestamp")

    return render(request, "incidents/incident_logs.html", {
        "incident": incident,
        "logs": logs
    })
@login_required
def analyst_queue(request):
    if request.user.role.lower() != "analyst":
        return HttpResponseForbidden("Only analysts allowed.")

    incidents = Incident.objects.filter(
        assigned_to=request.user
    ).order_by("created_at")

    return render(request, "incidents/analyst_queue.html", {
        "incidents": incidents
    })
@login_required
def add_note(request, pk):
    incident = get_object_or_404(Incident, pk=pk)

    if request.user.role.lower() != "analyst":
        return HttpResponseForbidden("Only analyst can add notes")

    if incident.assigned_to != request.user:
        return HttpResponseForbidden("Not your incident")

    from .forms import InvestigationNoteForm

    if request.method == "POST":
        form = InvestigationNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.incident = incident
            note.changed_by = request.user
            note.old_status = incident.status
            note.new_status = incident.status
            note.save()
            return redirect("incidents:incident_detail", pk=pk)
@login_required
def delete_incident(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    
    # Use .lower() and .strip() for the most reliable comparison
    role = str(request.user.role).strip().lower() if request.user.role else ""
    
    # 1. PERMISSION CHECK (Added superuser bypass for safety)
    is_admin = (role == "admin" or request.user.is_superuser)
    is_owner = (role == "user" and incident.created_by == request.user)
    is_assigned = (role == "analyst" and incident.assigned_to == request.user)

    if not (is_admin or is_owner or is_assigned):
        messages.error(request, f"Access Denied. Your role '{role}' cannot delete this.")
        return redirect("incidents:incident_list")

    # 2. DELETE EXECUTION (POST)
    if request.method == "POST":
        incident.delete()
        messages.success(request, "Incident deleted successfully.")
        return redirect("incidents:incident_list")

    # 3. SHOW CONFIRMATION (GET)
    return render(request, "incidents/delete_confirm.html", {"incident": incident})