from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.product_module.models import Product
from django.urls import reverse_lazy
from core.utils.mixins import ModuleRequiredMixin, RoleRequiredMixin, UpgradeRequiredMixin
from core.utils.constant import ALL_ROLES, MANAGER, USER

class ProductListView(ModuleRequiredMixin, RoleRequiredMixin, UpgradeRequiredMixin, ListView):
    model_slug = 'product_module'
    template_name = 'product_list.html'
    model = Product
    context_object_name = "products"
    allowed_roles = ALL_ROLES
    
    # this is for if i want to add other context data
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #     return context
class ProductCreateView(ModuleRequiredMixin, RoleRequiredMixin, UpgradeRequiredMixin, CreateView):
    model_slug = 'product_module'
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product-module') #TODO: why it has to be implemented this way?
    allowed_roles = [MANAGER, USER]

class ProductUpdateView(ModuleRequiredMixin, RoleRequiredMixin, UpgradeRequiredMixin, UpdateView):
    model_slug = 'product_module'
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product-module')
    allowed_roles = [MANAGER, USER]

#TODO: need to check how to properly use delete view
class ProductDeleteView(ModuleRequiredMixin, RoleRequiredMixin, UpgradeRequiredMixin, DeleteView):
    model_slug = 'product_module'
    model = Product
    template_name = 'product_list.html'
    success_url = reverse_lazy('product-module')
    allowed_roles = [MANAGER]

