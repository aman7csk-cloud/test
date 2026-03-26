from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register_view, login_view, dashboard_view
from . import views


urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("assign-analyst/", views.assign_analyst_role, name="assign_analyst_role"),
    

]

