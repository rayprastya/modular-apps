from django.urls import path
from .views import ModularView, ModuleActionView

urlpatterns = [
    path('', ModularView.as_view(), name='modular-tools'),
    path('install/<str:slug>/<str:action>/', ModuleActionView.as_view(), name='module-action'),
]

