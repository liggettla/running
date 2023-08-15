from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BiometricForm
from .models import Biometric

# Bokeh imports for plotting
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool
from scipy.stats import linregress
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
    user_biometrics = Biometric.objects.filter(user=request.user).order_by('-date')

    # Helper function to create plots
    def create_plot(attribute, title, biometric='Weight'):
        filtered_biometrics = [biometric for biometric in user_biometrics if getattr(biometric, attribute)]
        weights = [getattr(biometric, attribute) for biometric in filtered_biometrics]
        dates = [(datetime.combine(biometric.date, datetime.min.time()) - datetime(1970, 1, 1)).total_seconds() * 1000 for biometric in filtered_biometrics]

        p = figure(title=title, x_axis_label="Date", y_axis_label=biometric, x_axis_type="datetime", 
                   width=800, height=400, tools="pan,box_zoom,reset,save")
        p.circle(dates, weights, size=10, color="teal", alpha=0.25, legend_label=biometric)

        slope, intercept, _, _, _ = linregress(dates, weights)
        reg_line = [slope * date + intercept for date in dates]
        r = p.line(dates, reg_line, line_color="teal", legend_label=f"Regression (y={slope:.2f}x + {intercept:.2f})")
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

    return render(request, 'biometrics/add_biometrics.html', {
        'form': form,
        'biometrics': user_biometrics,
        'script_morning': script_morning, 'div_morning': div_morning, 
        'script_postrun': script_postrun, 'div_postrun': div_postrun,
        'script_night': script_night, 'div_night': div_night,
        'script_hr': script_hr, 'div_hr': div_hr,
    })