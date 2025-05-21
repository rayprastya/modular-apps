from django.urls import path
from apps.modular_engine.views import ModularView, ModuleActionView, UpgradeRequiredView

urlpatterns = [
    path('', ModularView.as_view(), name='modular-tools'),
    path('install/<str:slug>/<str:action>/', ModuleActionView.as_view(), name='module-action'),
    path('upgrade-required/', UpgradeRequiredView.as_view(), name='upgrade-required'),
]

