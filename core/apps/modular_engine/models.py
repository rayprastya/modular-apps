from django.db import models
from core.utils.models import BaseModel

class Module(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    version = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'modules'
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
