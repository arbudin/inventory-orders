import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from products.models import Product


@pytest.mark.django_db
def test_create_product_api():
    client = APIClient()
    url = reverse('products-list')

    data = {
        "name": "API продукт",
        "description": "Описание продукта",  # обязательно!
        "price": 50.0,
        "stock": 5
    }

    response = client.post(url, data, format='json')

    print(response.data)  # чтобы видеть ошибки, если будут

    assert response.status_code == 201
    assert Product.objects.filter(name="API продукт").exists()
