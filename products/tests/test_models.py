import pytest
from products.models import Product


@pytest.mark.django_db  # нужен для работы с базой данных
def test_create_product():
    product = Product.objects.create(name="Тестовый продукт", price=99.99, stock=10)

    # Проверяем, что продукт реально добавился в базу
    assert Product.objects.count() == 1
    assert product.name == "Тестовый продукт"