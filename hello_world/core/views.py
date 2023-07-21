from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

# User registration view
def register_request(request):
    # If the request is a POST validate the form
    # then save a new user object
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("core:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    # If the request is a GET or the form is invalid
    # render the template with the form
    form = NewUserForm()
    return render (request=request, template_name="core/register.html", context={"register_form":form})
