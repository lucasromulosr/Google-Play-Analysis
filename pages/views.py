from django.shortcuts import render
from app.models import Application

# Create your views here.
def home_view(request):

    context = { 
        'all_apps': Application.objects.all()
    }

    return render(request, 'index.html', context)