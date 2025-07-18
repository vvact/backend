from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()



# products/tests/test_products.py
from django.test import TestCase
from products.models import Category

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Test", slug="test")
        self.assertEqual(category.name, "Test")


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes", slug="shoes")
        self.product = Product.objects.create(
            name="Test Shoe",
            slug="test-shoe",
            sku="SKU-001",
            category=self.category,
            base_price=1000,
            description="A nice shoe"
        )

    def test_list_products(self):
        url = reverse('product-list')  # adjust this to match your URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Test Shoe")

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product.slug])  # adjust if slug-based
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Shoe")
