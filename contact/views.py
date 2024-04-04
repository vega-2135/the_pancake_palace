from django.shortcuts import render
from .models import ReachOut
from .forms import ReachOutForm


def reach_out(request):
    """
    Renders the Contact page
    """
    contact = ReachOut.objects.all()
    reachout_form = ReachOutForm()

    return render(
        request,
        "contact.html",
        {"contact": contact,
         "reachout_form": reachout_form
        },
    )
