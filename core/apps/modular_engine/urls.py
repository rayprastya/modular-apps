from django.urls import path
from .views import ModularView, ModuleActionView

urlpatterns = [
    path('modular-tools', ModularView, name='modular-tools'),
    path('install/<str:slug/', ModuleActionView, name='module-action'),
]

