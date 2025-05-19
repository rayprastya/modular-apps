from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product
from django.urls import reverse_lazy

class ProductListView(ListView):
    template_name = 'product_module/templates/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_module/templates/product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product_list') #TODO: why it has to be implemented this way?

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_module/templates/product_form.html'
    fields = ['name', 'barcode', 'price', 'stock']
    success_url = reverse_lazy('product_list')

#TODO: need to check how to properly use delete view
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_module/templates/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


