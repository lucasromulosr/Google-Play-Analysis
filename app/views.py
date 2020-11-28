from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from forms import getAppID
from .models import Application

def home(request):
    '''
    if request.method == 'POST':
        form = getAppID(request.POST)

        if form.is_valid():
            text = request.POST.get('your_name', None)
            return HttpResponseRedirect('/tests/')

    else:
    '''
    form = getAppID(request.POST)
    text = request.POST.get('your_name', None)

    return render(request, 'home.html', {'form': form,
                                         'text': text})


def application_detail_view(request, app_name):
    context = {
        'app': Application.objects.get(name=app_name)
    }
    return render(request, "app/application/index.html", context)