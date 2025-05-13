from django.contrib import admin
from .models import Player

# Registering the player model so it appears in the admin panel
admin.site.register(Player)
