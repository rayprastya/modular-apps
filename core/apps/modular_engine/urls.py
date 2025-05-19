from django.urls import path
from . import views

urlpatterns = [
    path('modular-tools', views.index, name='modular-tools'),
]

