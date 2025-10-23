from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Название товара", max_length=100)
    description = models.TextField("Описание товара")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Количество штук на складе")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

