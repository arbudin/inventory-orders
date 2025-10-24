from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db import transaction
from .models import Order, OrderItem
from rest_framework import status, viewsets

from .serializers import CartItemSerializer
from .models import CartItem, Order, OrderItem

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save()

class CheckoutViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        GET — для отладки: показывает элементы корзины и общую сумму.
        Это НЕ делает оформлений заказа — только смотрит.
        """
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        # Если корзина пуста — возвращаем пустой список и total = 0
        if not cart_items.exists():
            return Response({"cart": [], "total_price": "0.00"})

        # Формируем удобный список позиций и считаем сумму
        items = []
        total = 0
        for it in cart_items:
            item_total = float(it.product.price) * it.quantity
            items.append({
                "product_id": it.product.id,
                "product_name": it.product.name,
                "unit_price": str(it.product.price),
                "quantity": it.quantity,
                "line_total": f"{item_total:.2f}"
            })
            total += item_total

        return Response({"cart": items, "total_price": f"{total:.2f}"})

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        cart_items = CartItem.objects.filter(user=user).select_related('product')

        if not cart_items.exists():
            return Response({"error": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        # считаем total (можно пересчитать снова внутри транзакции, для надёжности)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        try:
            with transaction.atomic():
                # Берём cart_items для блокировки строк товара в БД
                locked_items = CartItem.objects.filter(user=user).select_for_update().select_related('product')

                # Проверяем наличие на складе
                for item in locked_items:
                    if item.quantity > item.product.stock:
                        raise Exception(f"Не хватает товара: {item.product.name} (доступно {item.product.stock})")

                # Создаём заказ
                order = Order.objects.create(user=user, total_price=total_price)

                # Создаём позиции заказа и уменьшаем stock
                for item in locked_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                    # атомарное уменьшение склада — либо через save, либо через update + F()
                    item.product.stock = F('stock') - item.quantity
                    item.product.save()

                # При использовании F() нужно обновить объект из БД, если дальше используешь его в коде:
                # for p in locked_items:
                #     p.product.refresh_from_db()

                # Очищаем корзину
                locked_items.delete()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Возвращаем результат
        return Response({
            "message": "Заказ успешно оформлен",
            "order_id": order.id,
            "total_price": str(order.total_price)
        }, status=status.HTTP_201_CREATED)