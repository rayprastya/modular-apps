from django.urls import path
from . import views

urlpatterns = [
    path('product-module/', views.ProductListView.as_view(), name='product-module'),
    path('product-module/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product-module/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('product-module/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
]

