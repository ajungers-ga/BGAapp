from django.shortcuts import render

# Create your views here.
# Tour Legacy page (shows list of seasons)
def tour_legacy(request):
    seasons = [2019, 2020, 2021, 2022, 2023, 2024]
    return render(request, 'legacy/tour_legacy.html', {'seasons': seasons})
