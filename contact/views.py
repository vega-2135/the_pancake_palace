from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from contact.models import Contact
from .forms import ReachOutForm


def contact_me(request):
    """
    Renders the Contact page
    """
    if request.method == "POST":
        reachout_form = ReachOutForm(data=request.POST)
        if reachout_form.is_valid():
            reachout_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Thank you for reaching out, I endeavour to respond within"
                "2-3 working days.")

    queryset = Contact.objects.all()
    contact = get_object_or_404(queryset)
    reachout_form = ReachOutForm()

    return render(
        request,
        "contact.html",
        {
            "contact": contact,
            "reachout_form": reachout_form
        },
    )
