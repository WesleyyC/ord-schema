from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('small', views.small, name='small'),
]