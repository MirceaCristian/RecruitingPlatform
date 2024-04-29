from email.message import EmailMessage
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .forms import CVForm, UserForm, ContactForm, WorkFieldForm, EditProfileForm, ApplyJobForm
from .models import CV, CustomUser, Contact, WorkField, Job


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


@login_required
def job_search(request):
    query = request.GET.get('query')
    if query:
        jobs = Job.objects.filter(name__icontains=query) | Job.objects.filter(
            work_field__work_field__icontains=query) | Job.objects.filter(company__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})


def send_email_with_attachment(subject, message, from_email, to_email, attachment_path):
    email = EmailMessage()
    email.subject = subject
    email.body = message
    email.from_email = from_email
    email.to = to_email
    email.attach(attachment_path)

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=to_email)


@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    user = request.user
    cvs = CV.objects.filter(user=request.user)
    form = ApplyJobForm()
    if request.method == 'POST':
        form = ApplyJobForm(request.POST)
        if form.is_valid():
            selected_cv_id = form.cleaned_data['CV']
            selected_cv = CV.objects.get(id=selected_cv_id)
            subject = f'Applying for {job.name}'
            message = f'Please find attached my CV for the position of {job.name}'

            send_email_with_attachment(
                subject=subject,
                message=message,
                from_email=user.email,
                to_email=job.company_email,
                attachment_path=selected_cv.cv_file.path
            )
    return render(request, 'apply_job.html', {'form': form, 'job': job})


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


class JobView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'
