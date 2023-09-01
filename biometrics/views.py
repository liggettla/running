import json

# Bokeh imports for plotting
from datetime import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from scipy.stats import linregress

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

    # Helper function to create plots
    def create_plot(attribute, title, biometric='Weight'):
        filtered_biometrics = [
            biometric for biometric in user_biometrics if getattr(biometric, attribute)
            ]
        weights = [getattr(biometric, attribute) for biometric in filtered_biometrics]
        dates = [
            (
            datetime.combine(biometric.date, datetime.min.time())
            - datetime(1970, 1, 1)
            ).total_seconds() * 1000
            for biometric in filtered_biometrics
            ]
        
        # don't try to run regression if there is only one data point
        if len(dates) == 0 or len(weights) == 0:
            # return a dummy plot
            p = figure(title=title, x_axis_label="Date", y_axis_label=biometric, x_axis_type="datetime",
                   width=800, height=400, tools="pan,box_zoom,reset,save")
            p.text(x=0, y=0, text=["No data available for plotting."])
            return p

        p = figure(title=title, x_axis_label="Date", y_axis_label=biometric, x_axis_type="datetime",
                   width=800, height=400, tools="pan,box_zoom,reset,save")
        p.circle(dates, weights, size=10, color="teal", alpha=0.25, legend_label=biometric)

        slope, intercept, _, _, _ = linregress(dates, weights)
        reg_line = [slope * date + intercept for date in dates]
        r = p.line(dates,
                   reg_line,
                   line_color="teal",
                   legend_label=f"Regression (y={slope:.2f}x + {intercept:.2f})")
        r.muted = True

        hover = HoverTool()
        hover.tooltips = [("Date", "@x{%F}"), ("Weight", "@y kg")]
        hover.formatters = {"@x": "datetime"}
        p.add_tools(hover)

        return p

    # Generate plots
    morning_weight_plot = create_plot("weight_morning", "Morning Weight")
    post_run_weight_plot = create_plot("weight_after_run", "Post-Run Weight")
    night_weight_plot = create_plot("weight_night", "Night Weight")
    heart_rate_plot = create_plot("heart_rate", "Heart Rate", "Heart Rate")

    # Embed plots into the template
    script_morning, div_morning = components(morning_weight_plot)
    script_postrun, div_postrun = components(post_run_weight_plot)
    script_night, div_night = components(night_weight_plot)
    script_hr, div_hr = components(heart_rate_plot)

    # Create a list of events for the calendar
    events = []
    for biometric in user_biometrics:
        extend_list = []

        if biometric.weight_morning is not None:
            extend_list.append({'title': f"Weight Morning: {biometric.weight_morning} kg",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#1d88e5'})
        if biometric.weight_after_run is not None:
            extend_list.append({'title': f"Weight After Run: {biometric.weight_after_run} kg",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#1d88e5'})
        if biometric.weight_night is not None:
            extend_list.append({'title': f"Weight Night: {biometric.weight_night} kg",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#1d88e5'})
        if biometric.heart_rate is not None:
            extend_list.append({'title': f"Heart Rate: {biometric.heart_rate}",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#e51d53'})
        if biometric.systolic_pressure is not None:
            extend_list.append({'title': f"Systolic Pressure: {biometric.systolic_pressure}",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#e51d53'})
        if biometric.diastolic_pressure is not None:
            extend_list.append({'title': f"Diastolic Pressure: {biometric.diastolic_pressure}",
                                'start': biometric.date.strftime('%Y-%m-%d'),
                                'color': '#e51d53'})
        
        events.extend(extend_list)

    # Convert the events list to JSON
    events_json = json.dumps(events)

    return render(request, 'biometrics/add_biometrics.html', {
        'form': form,
        'biometrics': user_biometrics,
        'script_morning': script_morning, 'div_morning': div_morning, 
        'script_postrun': script_postrun, 'div_postrun': div_postrun,
        'script_night': script_night, 'div_night': div_night,
        'script_hr': script_hr, 'div_hr': div_hr,
        'events_json': events_json, # Pass the JSON object to the template context
    })
