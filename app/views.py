from django.shortcuts import render
from database import read_all_apps, read_app, read_top

def home_view(request):
    context = { 
        'all_apps': list(read_all_apps())
    }
    return render(request, 'index.html', context)


def application_detail_view(request, app_id):
    app = read_app(app_id)
    comments = read_top(app_id)
    context = {
        'app': app,
        'comments': comments
    }
    return render(request, "app/application/index.html", context)
