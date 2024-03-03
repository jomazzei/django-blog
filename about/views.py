# Http needs to be imported before render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import About
from .forms import CollaborateForm


# Create your views here.
def about_me(request):
    """
    Renders the most recent information on the website author
    and allows user collaboration requests.

    Displays an individual instance of :model:`about.About`.

    **Context**
    ``about``
        The most recent instance of :model:`about.About`.
        ``collaborate_form``
            An instance of :form:`about.CollaborateForm`.
    
    **Template**
    :template:`about/about.html`
    """
    # POST req check above empty instance call so that form clears on submission
    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(request, messages.SUCCESS, "Collaboration request received! I endeavour to respond within 2 working days.")
            # return redirect makes it so the page is automatically reloaded with a fresh form on submission. 
            # This prevents the form resubmitting twice when page is refreshed manually through browser
            return HttpResponseRedirect(request.path_info)

    about = About.objects.all().order_by('-updated_on').first()
    # Creates empty form instance
    collaborate_form = CollaborateForm()

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form,
        },
    )
