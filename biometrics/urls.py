from django.urls import path
from . import views

urlpatterns = [
    path('add_biometrics/', views.add_biometrics, name='add_biometrics'),
]
