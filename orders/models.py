from django.db import models
from django.conf import settings

from products.models import Product


class CartItem(models.Model):

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    # — связь «многие к одному»: один пользователь может иметь много элементов в корзине.
    # on_delete=models.CASCADE — если пользователь удалён, то и его корзина удаляется (логично).
    # related_name='cart_items' — с другой стороны, user.cart_items даст QuerySet всех CartItem этого пользователя. Удобно в шаблонах и в коде.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')

    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # — ссылка на товар. on_delete=models.CASCADE означает: если товар удалён из каталога, связанные CartItem также будут удалены.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Количество единиц товара в конкретной позиции.
    # PositiveIntegerField запрещает отрицательные значения; default=1 — удобно при добавлении.
    quantity = models.PositiveIntegerField(default=1)

    # Автоматически заполнится временем добавления; полезно для истории/сортировки.
    added_at = models.DateTimeField(auto_now_add=True)

    # Важный момент: гарантирует на уровне БД, что у одного пользователя не будет двух строк с одним и тем же product.
    # То есть каждая пара (user, product) уникальна.
    # Благодаря этому логика «если добавить тот же товар — увеличиваем quantity вместо создания новой строки» станет корректной и на уровне БД (и не будет дубликатов).
    class Meta:
        unique_together = ('user', 'product')

    # Человекочитаемое представление записи (нужно для админки и логов).
    def __str__(self):
        return f'{self.user} - {self.product} x {self.quantity}'