from django.db import models

# Модель (типа База данных) для товаров
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Название товара", max_length=100)
    description = models.TextField("Описание товара")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Количество штук на складе")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

