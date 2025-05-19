from django.urls import path
from .views import ModularView, install_module

urlpatterns = [
    path('modular-tools', ModularView, name='modular-tools'),
    path('install/<str:slug/', install_module, name='module-list'),
]

