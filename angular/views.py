from django.shortcuts import render


def index(request, url=None):
    return render(request, 'index.html', {})
