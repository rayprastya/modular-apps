from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.core.management import call_command
from models import Module
class ModularView(TemplateView):
    template_name = 'modular_engine/templates/modular_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #TODO: why it has to be implemented this way?

        app_config = [
            app for app in apps.get_app_configs()
            if app.name.startswith('core.apps')
        ]

        modules = [] 

        for app in app_config:
            # sync to db if not exists
            module, created = Module.objects.get_or_create(
                slug = app.name,
                defaults = {
                    'name': app.name,
                    'is_active': True,
                }
            )

            module_object = {
                'name': module.name,
                'slug': module.slug,
                'is_active': module.is_active,
            }

            modules.append(module_object)

        context['modules'] = Module.objects.all()
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
            return False #TODO: return error message

        return handle_action(module)
    
    def installation_action(self, module, action):
        # to mark the of the active module
        module.is_active = action
        module.save()
    
    def install_module(self, module):
        self.installation_action(module, True)
        return redirect('module_list')

    def uninstall_module(self, module):
        self.installation_action(module, False)
        return redirect('module_list')

    def upgrade_module(self, module):
        # running migrations for updating the data
        # TODO: to check if it doesnt need to add the version up
        call_command('makemigrations', module.slug) #param : command, app_label
        call_command('migrate', module.slug)

        # version upgrade tracking
        major, minor= map(int, module.version.split('.'))
        minor += 1
        module.version = f"{major}.{minor}"
        module.save()
