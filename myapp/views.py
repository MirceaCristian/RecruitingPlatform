from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import CVForm
from .models import CV


def home_view(request):
    obj = CV()
    obj.title = 'titlul meu'
    obj.description = 'descrierea mea'
    dictionary = {'key': 'value', 'key2': 'value2'}
    list_ = [1, 2, 3, 4]
    return render(request, 'home_view.html', {'object': obj, 'dictionary': dictionary, 'list': list_})


def cv_list(request):
    cvs = CV.objects.all()
    return render(request, 'cv_list.html', {'cvs': cvs})


def add_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cv_list')
    else:
        form = CVForm()
    return render(request, 'add_cv.html', {'form': form})
