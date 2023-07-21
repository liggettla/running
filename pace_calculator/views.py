from django.shortcuts import render
from .forms import PaceCalculatorForm

def calculate_pace(request):
    """View to calculate pace"""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = PaceCalculatorForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data['distance']
            time = form.cleaned_data['time']
            pace = form.cleaned_data['pace']
            hours, minutes, seconds = map(int, time.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            pace_in_seconds_per_km = total_seconds / distance
            pace_minutes = pace_in_seconds_per_km // 60
            pace_seconds = pace_in_seconds_per_km % 60
            pace = f'{int(pace_minutes)}:{int(pace_seconds):02d}'
            return render(request, 'pace_calculator.html', {'form': form, 'pace': pace})
    else:
        # if a GET request, create a blank form
        form = PaceCalculatorForm()
    return render(request, 'pace_calculator.html', {'form': form})


"""
in the future it might be helpful to put all of the javascript from the pace calculator
into python here so that it can be used in the pace_calculator.html template like this:

<!DOCTYPE html>
<html>
<head>
    <title>Pace Calculator</title>
</head>
<body>
    <h2>Pace Calculator</h2>
    <!-- link to admin console -->
    <a href="/">Home</a>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Calculate</button>
    </form>
    {% if pace %}
    <p>Your pace: {{ pace }} per kilometer</p>
    {% endif %}
</body>
</html>
"""