# File Purpose: Route requests for /legacy/ pages like the main season archive

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_legacy, name='tour_legacy'),
]
