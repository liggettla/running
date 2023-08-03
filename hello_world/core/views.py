from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def register_request(request):
    # Check if the request method is POST
    if request.method == "POST":
        # If it is POST, create a form instance and populate it with data from the request
        form = NewUserForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # If the form is valid, save the data (this also saves it to the database)
            user = form.save()
            # Log in the user
            login(request, user)
            # Send a success message
            messages.success(request, "Registration successful." )
            # Redirect to the index page
            return redirect("index")
        # If the form is not valid, send an error message
        messages.error(request, "Unsuccessful registration. Invalid information. " + str(form.errors))

    # If the request method is not POST (i.e., it's GET), create a new empty form
    form = NewUserForm()
    # Render the registration page with the form
    return render(request=request, template_name="register.html", context={"register_form":form})
