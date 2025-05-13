# File Purpose = 
# Create your models here.
from django.db import models
from decimal import Decimal


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, blank=True)
    hometown = models.CharField(max_length=50, blank=True)
    years_active = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)

    career_events_played = models.PositiveIntegerField(default=0)
    career_wins = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"
