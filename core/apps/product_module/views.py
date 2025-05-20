from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product
from django.urls import reverse_lazy
from core.utils.mixins import ModuleRequiredMixin, RoleRequiredMixin
from core.utils.constant import ALL_ROLES, MANAGER, USER

class ProductListView(ModuleRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = "products"
    allowed_roles = ALL_ROLES
    
    # this is for if i want to add other context data
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #     return context
class ProductCreateView(ModuleRequiredMixin, RoleRequiredMixin, CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product-module') #TODO: why it has to be implemented this way?
    allowed_roles = [MANAGER, USER]

class ProductUpdateView(ModuleRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product-module')
    allowed_roles = [MANAGER, USER]

#TODO: need to check how to properly use delete view
class ProductDeleteView(ModuleRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-module')
    allowed_roles = [MANAGER]

