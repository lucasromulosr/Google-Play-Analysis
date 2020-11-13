from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from forms import getAppID

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


def tests(request):

    return HttpResponse('---suave')