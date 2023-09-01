from django.urls import path
from . import views

urlpatterns = [
    path('add_biometrics/', views.add_biometrics, name='add_biometrics'),
    path('delete_biometric/', views.delete_biometric, name='delete_biometric'),
]
