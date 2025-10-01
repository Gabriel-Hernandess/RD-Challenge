from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import LoginPageView
from apps.probes.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("login/", LoginPageView.as_view(), name="login_page"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path('api/', include("apps.probes.urls")),
    path('auth/', include("apps.authentication.urls")),
]