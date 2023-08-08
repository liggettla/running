"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Django provides a built-in view to handle registration
from .core.views import register_request

# Django provides a built-in view to handle login/logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from hello_world.core import views as core_views
# Import the view from pace_calculator app
from pace_calculator.views import calculate_pace
from running_log.views import run_log  # Import the run_log view from the running_log app 



urlpatterns = [
    path("", core_views.index, name="index"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    path("register/", core_views.register_request, name="register"), # Register new users page
    path("login/", LoginView.as_view(template_name='login.html'), name="login"), # Login page
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"), # Logout page

    path("pace_calculator/", calculate_pace, name="pace_calculator"), # Pace calculator page
    path("running_log/", run_log, name="run_log"),
    

]
