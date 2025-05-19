from django.db import models
from core.utils.models import BaseModel
class Module(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name



