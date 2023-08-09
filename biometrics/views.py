from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BiometricForm
from .models import Biometric

@login_required
def add_biometrics(request):
    if request.method == "POST":
        form = BiometricForm(request.POST)
        if form.is_valid():
            biometric = form.save(commit=False)
            biometric.user = request.user
            biometric.save()
            return redirect('add_biometrics')
    else:
        form = BiometricForm()

    # Query the database for the user's biometrics
    user_biometrics = Biometric.objects.filter(user=request.user).order_by('-date')

    return render(request, 'biometrics/add_biometrics.html', {'form': form, 'biometrics': user_biometrics})