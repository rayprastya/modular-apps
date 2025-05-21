# Mixins for expandable view action

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from apps.modular_engine.models import Module
from core.utils.constant import PUBLIC
from core.utils.helper import load_module_config
from django.shortcuts import redirect, render
class RoleRequiredMixin(AccessMixin):
    """limit user access based on role."""
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if PUBLIC in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
                
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        user_roles = request.user.groups.values_list('name', flat=True)
        if not set(user_roles).intersection(self.allowed_roles):
            return HttpResponseForbidden("You do not have permission for this action")
        
        return super().dispatch(request, *args, **kwargs)
    
class ModuleRequiredMixin(AccessMixin):
    model_slug = None
    def dispatch(self, request, *args, **kwargs):
        print("model_slug", self.model_slug)
        try:
            module = Module.objects.get(slug=self.model_slug)
        except Module.DoesNotExist:
            return render(request, "errors/module_not_found.html", status=404)
        
        if not module.is_active:
            return render(request, "errors/module_inactive.html", status=403)
        
        return super().dispatch(request, *args, **kwargs)

class UpgradeRequiredMixin(AccessMixin):
    model_slug = None

    def dispatch(self, request, *args, **kwargs):
        slug = self.model_slug
        if not slug:
            return super().dispatch(request, *args, **kwargs)

        # ambil versi dari DB & metadata
        db_module = Module.objects.filter(slug=slug).first()
        metadata = load_module_config(slug)

        if db_module and metadata:
            db_version = float(db_module.version)
            metadata_version = float(metadata.get("version", db_version))

            if db_version < metadata_version:
                return redirect("upgrade-required")

        return super().dispatch(request, *args, **kwargs)
