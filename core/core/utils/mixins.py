# Mixins for expandable view action

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from apps.modular_engine.models import Module
from core.utils.constant import PUBLIC

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
        try:
            module = Module.objects.get(slug=self.model_slug)
        except Module.DoesNotExist:
            return HttpResponseForbidden("Module does not exist", status=404)
        
        if not module.is_active:
            return HttpResponseForbidden("Module is not active", status=403)
        
        return super().dispatch(request, *args, **kwargs)
