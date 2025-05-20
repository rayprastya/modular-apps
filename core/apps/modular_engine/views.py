from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.core.management import call_command
from core.utils.helper import load_module_config
from apps.modular_engine.models import Module

class ModularView(TemplateView):
    template_name = 'module_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #TODO: why it has to be implemented this way?
        modules = [] 

        for app in apps.get_app_configs():
            if not app.name.endswith('_module'):
                continue

            metadata = load_module_config(app)
            if not metadata:
                continue

            metadata_db = {
                'name': metadata['name'],
                'slug': metadata['slug'],
                'description': metadata['description'],
                'is_active': False,
            }

            module, _ = Module.objects.get_or_create(
                defaults = metadata_db
            )

            modules.append(module)

        context['modules'] = modules
        return context


class ModuleActionView(View):
    def post(self, request, slug, action):
        print("got here")
        module = get_object_or_404(Module, slug=slug)

        actions = {
            "install": self.install_module,
            "uninstall": self.uninstall_module,
            "upgrade": self.upgrade_module,
        }

        handle_action = actions.get(action)
        if not handle_action:
            return False #TODO: return error message

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
        # running migrations for updating the data
        # TODO: to check if it doesnt need to add the version up
        call_command('makemigrations', module.slug) #param : command, app_label
        call_command('migrate', module.slug)

        # version upgrade tracking
        # TODO: the version upgrade will update to the metadata.json file
