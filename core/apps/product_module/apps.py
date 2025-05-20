from django.apps import AppConfig


class ProductModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.product_module'
    app_label = 'product_module'
