from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from forms import getAppID
from .models import Application

def home_view(request):

    context = { 
        'all_apps': Application.objects.all()
    }

    return render(request, 'index.html', context)


def application_detail_view(request, app_name):
    context = {
        'app': Application.objects.get(name=app_name)
    }
    return render(request, "app/application/index.html", context)