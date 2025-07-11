from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django import forms
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.core.management import call_command
from core.utils.helper import load_module_config
from apps.modular_engine.models import Module
from django.http import HttpResponse
from django.contrib import messages

class ModularView(TemplateView):
    template_name = 'module_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #TODO: why it has to be implemented this way?
        modules = [] 

        for app in apps.get_app_configs():
            if not app.name.endswith('_module'):
                continue

            metadata = load_module_config(app.label)
            if not metadata:
                continue

            metadata_db = {
                'name': metadata['name'],
                'slug': metadata['slug'],
                'description': metadata['description'],
                'is_active': False,
                'version': 1.0,
            }

            module, _ = Module.objects.get_or_create(
                defaults = metadata_db
            )

            metadata_version = float(metadata.get("version", 1.0))
            db_version = float(module.version)
            module.need_upgrade = metadata_version > db_version

            modules.append(module)

        context['modules'] = modules
        return context


class ModuleActionView(View):
    def post(self, request, slug, action):
        module = get_object_or_404(Module, slug=slug)

        actions = {
            "install": self.install_module,
            "uninstall": self.uninstall_module,
            "upgrade": self.upgrade_module,
        }

        handle_action = actions.get(action)
        if not handle_action:
            return HttpResponse("Module action failed")

        return handle_action(module)
    
    def installation_action(self, module, action):
        # to mark the of the active module
        module.is_active = action
        module.save()
    
    def install_module(self, module):
        self.installation_action(module, True)
        return redirect('modular-tools')

    def uninstall_module(self, module):
        self.installation_action(module, False)
        return redirect('modular-tools')

    def upgrade_module(self, module):
        metadata = load_module_config(module.slug)
        if not metadata:
            return HttpResponse("Metadata not found", status=400)

        # NOTE: makemigrations can be add here if want to update the model auto, but need to test further
        try:
            call_command("migrate", module.slug)
        except Exception as e:
            messages.error(self.request, f"Gagal upgrade module: {e}")
            return redirect("modular-tools")

        module.version = metadata.get("version", module.version)
        module.save()

        messages.success(self.request, f"{module.name} upgraded to version {module.version}")
        return redirect("modular-tools")

class SignUpForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'group']
    
    
class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        group = form.cleaned_data.pop('group')
        user = form.save()
        user.groups.add(group)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Errors:", form.errors)
        return super().form_invalid(form)
class UpgradeRequiredView(TemplateView):
    template_name = "upgrade_required.html"
