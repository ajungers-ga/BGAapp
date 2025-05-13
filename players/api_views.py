# File Purpose: API endpoint to return all BGA Tour players in JSON format

from django.http import JsonResponse
from .models import Player

def players_api(request):
    players = Player.objects.all().order_by('last_name')  # Adjust if your model has no last_name

    data = [
        {
            'id': player.id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'nickname': player.nickname,
            'years_of_service': player.years_active,
        }
        for player in players
    ]

    return JsonResponse(data, safe=False)



 