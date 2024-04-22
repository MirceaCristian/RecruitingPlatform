from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('cv/', views.cv_list, name='cv_list'),
    path('add/', views.AddCvView.as_view(), name='add_cv'),
    path('create-user/', views.UserCreateView.as_view(), name='create-user'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('delete_cv/<int:cv_id>/', views.delete_cv, name='delete_cv'),
    path('work-field/add/', views.WorkFieldCreateView.as_view(), name='work-field-create'),
]
