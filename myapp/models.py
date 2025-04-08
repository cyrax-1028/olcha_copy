from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from django.db.models import Avg
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = "groups"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.CharField(max_length=20, default="Not Available")
    like = models.ManyToManyField(User, related_name="liked_products", blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return (self.price * (1 - Decimal(self.discount) / 100)).quantize(Decimal("0.01"))
        return self.price

    @property
    def get_rating(self):
        avg_rating = self.comments.aggregate(average=Avg("rating"))["average"]
        return round(avg_rating) if avg_rating is not None else 1

    @property
    def is_new(self):
        return (now() - self.created_at).total_seconds() < 86400

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
    is_prime = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True,
                                blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)


class Comment(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE)
    image = models.FileField(upload_to='comment_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user} => {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=255)
    phone = PhoneNumberField(region='UZ')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')],
        default='pending'
    )

    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity:
            self.total_price = self.product.price * self.quantity
            self.product.quantity -= self.quantity
            self.product.save(update_fields=["quantity"])
            super().save(*args, **kwargs)
        else:
            print("Yetarli mahsulot mavjud emas!")
