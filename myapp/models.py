from django.db import models
from decimal import Decimal

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(models.Model):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.CharField(max_length=20, default="Not Available")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    model = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return (self.price * (1 - Decimal(self.discount) / 100)).quantize(Decimal("0.01"))
        return self.price

    def save(self, *args, **kwargs):
        self.stock = "Available" if self.quantity > 0 else "Sold Out"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.name