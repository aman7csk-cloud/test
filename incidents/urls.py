from django.urls import path
from . import views

app_name = "incidents"

urlpatterns = [

    # list + detail
    path("", views.incident_list, name="incident_list"),
    path("<int:pk>/", views.incident_detail, name="incident_detail"),

    # create
    path("create/", views.create_incident, name="create_incident"),

    # update
    path("update/<int:pk>/", views.incident_update, name="incident_update"),

    # delete (admin)
    path("delete/<int:pk>/", views.delete_incident, name="delete_incident"),

    # assign analyst
    path("assign/<int:pk>/", views.assign_to_me, name="assign_to_me"),

    # change status
    path("status/<int:pk>/<str:new_status>/", views.change_status, name="change_status"),

    # logs
    path("logs/<int:pk>/", views.incident_logs, name="incident_logs"),
    path("<int:pk>/add-note/", views.add_note, name="add_note"),
    path("my-queue/", views.analyst_queue, name="analyst_queue"),
    path("delete/<int:pk>/", views.delete_incident, name="delete_incident"),


]
