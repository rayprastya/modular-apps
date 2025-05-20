from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-module'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
]

