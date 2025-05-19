from django.db import models
from core.utils.models import BaseModel
class Product(BaseModel):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
