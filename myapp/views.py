from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import CVForm, UserForm
from .models import CV, CustomUser


def home_view(request):
    return render(request, 'home_view.html')


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


class UserCreateView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    model = CustomUser
    template_name = 'user_create.html'
