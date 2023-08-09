from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BiometricForm
from .models import Biometric

# Bokeh imports for plotting
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, Span, Label
from bokeh.layouts import column
from scipy.stats import linregress
import numpy as np
from datetime import datetime

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
    # order by date in reverse order (most recent first)
    user_biometrics = Biometric.objects.filter(user=request.user).order_by('-date')

    #########
    # Plots #
    #########

    # Filter the user_biometrics to only include entries where weight_morning is not None
    filtered_biometrics = [biometric for biometric in user_biometrics if biometric.weight_morning]

    # Now, derive weights and dates from this filtered list
    weights = [biometric.weight_morning for biometric in filtered_biometrics]
    dates = [(datetime.combine(biometric.date, datetime.min.time()) - datetime(1970, 1, 1)).total_seconds() * 1000 for biometric in filtered_biometrics]

    # Create the plot
    p = figure(title="Weight Over Time", x_axis_label="Date", y_axis_label="Weight (kg)", x_axis_type="datetime", 
           width=800, height=400, tools="pan,box_zoom,reset,save")
    
    # Scatter plot
    p.circle(dates, weights, size=10, color="blue", alpha=0.5, legend_label="Weight")

    # Regression line
    slope, intercept, r_value, p_value, std_err = linregress(dates, weights)

    reg_line = [slope * date + intercept for date in dates]

    p.line(dates, reg_line, line_color="red", legend_label=f"Regression (y={slope:.2f}x + {intercept:.2f})")
    
    # Add hover tool for better user experience
    hover = HoverTool()
    hover.tooltips = [("Date", "@x{%F}"), ("Weight", "@y kg")]
    hover.formatters = {"@x": "datetime"}
    p.add_tools(hover)

    # Get components to embed in template
    script, div = components(p)

    # return render(request, 'biometrics/add_biometrics.html', {'form': form, 'biometrics': user_biometrics})

    return render(request, 'biometrics/add_biometrics.html', {'form': form, 'biometrics': user_biometrics, 'script': script, 'div': div})
