from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from forms import getAppID
from .models import Application
from database import read_all_apps, read_app

def home_view(request):
    context = { 
        'all_apps': list(read_all_apps())
    }
    return render(request, 'index.html', context)


def application_detail_view(request, app_id):
    context = {
        'app': read_app(app_id)
    }
    return render(request, "app/application/index.html", context)