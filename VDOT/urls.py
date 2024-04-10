from django.urls import path
from . import views

urlpatterns = [
    path('vdot/', views.vdot, name='vdot')
]