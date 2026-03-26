from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('incidents/', include('incidents.urls')),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

]

