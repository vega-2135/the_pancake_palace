from django.shortcuts import render
from django.contrib import messages
from .models import ReachOut
from .forms import ReachOutForm


def reach_out(request):
    """
    Renders the Contact page
    """
    if request.method == "POST":
        reachout_form = ReachOutForm(data=request.POST)
        if reachout_form.is_valid():
            reachout_form.save()
            messages.add_message(request, messages.SUCCESS, 
                "Thank you for reaching out, I endeavour to respond within"
                "2-3 working days.")
            
    contact = ReachOut.objects.all()
    reachout_form = ReachOutForm()

    return render(
        request,
        "contact.html",
        {"contact": contact,
         "reachout_form": reachout_form
        },
    )
