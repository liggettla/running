from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RunForm
from .models import Run

@login_required  # The view requires the user to be logged in.
def run_log(request):
    """View to add a run and list runs."""
    if request.method == 'POST':  # If the form has been submitted...
        # Create a form instance and populate it with data from the request.
        form = RunForm(request.POST)

        # Check if the form is valid.
        if form.is_valid():
            # Save the form data but don't commit to the database yet (because we haven't added the user).
            run = form.save(commit=False)

            # Add the current user to the run.
            run.user = request.user

            # Save the run to the database.
            run.save()

            # Redirect to the running log after a run is added.
            return redirect('run_log')

    else:  # If the form has not been submitted (i.e., the page is just being loaded)...
        # Create an empty form.
        form = RunForm()

    # Get all runs for the current user, ordered by date asscending.
    runs = Run.objects.filter(user=request.user).order_by('date')

    # Create a dictionary of lists containing the run data.
    # this is just so things can be easily accessed in running_log.html
    run_data = {
        'distances': [run.distance for run in runs],
        'dates': [run.date for run in runs],
        'times': [run.time for run in runs],
        'total_times': [run.total_time for run in runs],
        # Add more fields as needed.
    }

    # Render the template with the form and runs.
    return render(request, 'running_log.html', {'form': form, 'runs': runs, 'run_data': run_data})
