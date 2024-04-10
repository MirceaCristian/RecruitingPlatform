"""
URL configuration for proiect_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from myapp.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, PasswordSetForm

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(form_class=LoginForm), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(form_class=ChangePasswordForm),
         name='password_change'),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(form_class=ResetPasswordForm),
         name="password_reset"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class=PasswordSetForm),
         name="password_reset_confirm", ),
    path('accounts/', include('django.contrib.auth.urls')),

]
