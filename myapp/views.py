from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .forms import CVForm, UserForm, ContactForm, WorkFieldForm, EditProfileForm
from .models import CV, CustomUser, Contact, WorkField


class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def home_view(request):
    return render(request, 'home_view.html')


@login_required
def my_profile(request):
    profile = request.user
    return render(request, 'my_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = request.user
    form = EditProfileForm(instance=profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    return render(request, 'edit_profile.html', {"form": form})


@login_required
def cv_list(request):
    cvs = CV.objects.filter(user=request.user)
    return render(request, 'cv_list.html', {'cvs': cvs})


@login_required
def delete_cv(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id)
    if cv.user == request.user:
        cv.delete()
    return redirect('cv_list')


class AddCvView(CreateView, LoginRequiredMixin):
    form_class = CVForm
    success_url = reverse_lazy('cv_list')
    model = CV
    template_name = 'add_cv.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserCreateView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    model = CustomUser
    template_name = 'user_create.html'


class WorkFieldCreateView(CreateView, IsSuperUserMixin):
    model = WorkField
    template_name = 'domain_create.html'
    form_class = WorkFieldForm


class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    success_url = reverse_lazy('home_view')
    form_class = ContactForm
