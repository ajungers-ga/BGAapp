# File Purpose = Seed all scheduled 2025 BGA events into the database using Django ORM

import os
import django
from datetime import datetime

# Set up Django environment so this file can access models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from results.models import Event

# This list contains every scheduled event from the 2025 season
events = [
    {"date": "2025-04-12", "course": "Oak Glen", "type": "2-Man Scramble", "notes": "$52, cart — 10-10:50 (28ppl) — Sydney & Jason"},
    {"date": "2025-04-19", "course": "River Oaks", "type": "2-Man Scramble", "notes": "$xx — 10-10:50 (28ppl) — Dennis Neitz"},
    {"date": "2025-04-26", "course": "Loggers Trail", "type": "2-Man Scramble", "notes": "$xx — 9:00-9:50 (28ppl) — Tim"},
    {"date": "2025-05-03", "course": "Loggers Trail", "type": "2-Man Scramble", "notes": "$xx — 9:00-9:50 (28ppl) — Tim"},
    {"date": "2025-05-10", "course": "Eagle Valley", "type": "2-Man Scramble", "notes": "$69, cart, range — 10:30-11:30 (28ppl) — Josh Schroetter"},
    {"date": "2025-05-17", "course": "Troy Burne", "type": "Major Tournament", "notes": "$110, cart, range — 10-11:30 (40ppl) — Dave Tentis"},
    {"date": "2025-05-31", "course": "Jungle Juice Open", "type": "2-Man Scramble", "notes": ""},
    {"date": "2025-06-14", "course": "Victory Links", "type": "2-Man Scramble", "notes": "$89, cart — 8:30-9:20 (28ppl) — Tom Kirkland"},
    {"date": "2025-06-21", "course": "The Wilds", "type": "Major Tournament", "notes": "$95, cart, range — 1:00-2:20 (36ppl) — Pierson Pass"},
    {"date": "2025-06-28", "course": "Oak Marsh", "type": "2-Man Scramble", "notes": "$xx — 9:10-10:10 (28ppl) — Steve Whillock"},
    {"date": "2025-07-12", "course": "White Eagle", "type": "2-Man Scramble", "notes": "$xx — 8:50-9:50 (28ppl) — Scott Landin"},
    {"date": "2025-07-19", "course": "Bellwood Oaks", "type": "2-Man Scramble", "notes": "$xx — ????? — Mike Krug"},
    {"date": "2025-07-26", "course": "Matty D Invitational", "type": "2-Man Scramble", "notes": ""},
    {"date": "2025-08-02", "course": "Links at Northfork", "type": "2-Man Scramble", "notes": "$xx — 9:00-9:50 (28ppl) — Nicki Maling"},
    {"date": "2025-08-09", "course": "Clifton Highlands", "type": "2-Man Scramble", "notes": "$67, cart, range — 10-10:50 (28ppl) — Pete Law"},
    {"date": "2025-08-16", "course": "Meadows at Mystic Lake", "type": "Major Tournament", "notes": "$110, cart, prepay — 12:00-1:00 (28ppl) — Chris Olson"},
    {"date": "2025-08-23", "course": "River Falls Golf Club", "type": "2-Man Scramble", "notes": "$65, cart, range — 9:00-9:50 (28ppl) — Eric Ciupik"},
    {"date": "2025-09-06", "course": "Willingers", "type": "2-Man Scramble", "notes": "$85, cart, range — 9:00-9:50 (28ppl) — Eddie Dennis"},
    {"date": "2025-09-13", "course": "Hidden Greens", "type": "2-Man Scramble", "notes": "$xx — 9:00-9:50 (28ppl) — Andy Gerber"},
    {"date": "2025-09-20", "course": "BGA British Open", "type": "Major Tournament", "notes": "TBD"},
    {"date": "2025-10-04", "course": "Loggers Trail", "type": "2-Man Scramble", "notes": "$75, cart, range — 8:30am shotgun (40ppl) — Tim"},
    {"date": "2025-10-11", "course": "Loggers Trail", "type": "2-Man Scramble", "notes": "$xx — 10-10:50 — Tim"},
    {"date": "2025-10-18", "course": "Loggers Trail", "type": "2-Man Scramble", "notes": "$xx — 10-10:50 — Tim"},
]

for e in events:
    Event.objects.get_or_create(
        date=datetime.strptime(e["date"], "%Y-%m-%d").date(),
        course_name=e["course"],
        name=e["type"],
        is_team_event=True,
        season=2025,
        defaults={"notes": e["notes"]}
    )

print("2025 schedule inserted.")
