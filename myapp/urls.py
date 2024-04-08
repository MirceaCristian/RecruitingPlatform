from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('cv/', views.cv_list, name='cv_list'),
    path('add/', views.add_cv, name='add_cv'),
]
