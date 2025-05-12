from django.shortcuts import render

# Home page
def home(request):
    return render(request, 'core/home.html')

