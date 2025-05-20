from django.urls import path
from .views import ModularView, ModuleActionView

urlpatterns = [
    path('module/', ModularView.as_view(), name='modular-tools'),
    path('module/install/<str:slug>/', ModuleActionView.as_view(), name='module-action'),
]

