from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    # Поля, которые сериализатор будет обрабатывать
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.pop('product_id')
        quantity = validated_data.get('quantity', 1)

        # Ключевой момент: get_or_create пытается найти существующий CartItem для данного пользователя и товара.
        # Если не найден — создаёт новый CartItem с quantity=quantity.
        # Если найден — возвращает существующий объект и created=False.
        obj, created = CartItem.objects.get_or_create(
            user=user,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        # Eсли запись уже была — просто увеличиваем quantity, вместо создания дубликата.
        # Это соответствует поведению уникального ограничения (unique_together) и интуитивно удобно:
        # если пользователь добавил 2 товара, потом ещё 1 — в корзине будет 3.
        if not created:
            obj.quantity += quantity
            obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance