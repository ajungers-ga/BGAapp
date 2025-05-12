# File Purpose = This file defines the views (functions responding to user requests) \
# for the Tour Results section of BGAapp

# These views allow users to:
# - View all events
# - Create new events
# - Edit or delete existing events
# This connects to the Event model (models.py), the EventForm (forms.py), and template files inside templates/bgaapp/.


# ------IMPORTS BELOW -------#
from django.shortcuts import redirect 
# ABOVE = manUally redirect users after a form is submitted so theyre not stuck at deadlink

from django.views.generic import ListView, UpdateView, DeleteView
# ABOVE = Built in class views that make it easier to: List items, Edit Items & Delete items

from django.urls import reverse_lazy # refer to a URL by name insead of hardcoding - redirect after edit/delete
from .models import Event # importing the EVENT model, so it can be used in views
from .forms import EventForm # importing the form connected to the event model, used for create & edit
#-------IMPORTS ABOVE-----------#


# BELOW = List all events and show a form to add a new one
class EventListView(ListView):
    model = Event # telling Django which model
    template_name = 'bgaapp/event_list.html'
    context_object_name = 'events' # the name used in the template to access all events

    # When the page loads (user GET request)
    def get_context_data(self, extra_context=None):
        context = super().get_context_data() # super refers to parent class(listview) now I can reuse default logic
        context['form'] = EventForm() # form to be filled and returned by user
        return context

    # when the user submits form (user POST request)
    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save() # if form filled out properly, save the event to the DB
        return redirect('event_list') # sending the user back to the Event List page


# Edit an existing event
class EventUpdateView(UpdateView):
    model = Event  # telling Django which model
    form_class = EventForm  # use the same form as the create view
    template_name = 'bgaapp/event_form.html'  # page where the edit form will be displayed
    success_url = reverse_lazy('event_list')  # after saving, redirect user back to the Event List page

# Delete an event
class EventDeleteView(DeleteView):
    model = Event  # tell Django which model to delete from
    template_name = 'bgaapp/event_confirm_delete.html'  # confirmation page
    success_url = reverse_lazy('event_list')  # after deletion, send user back to the Event List page
