from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from myapp.models import Category, Group, Product, ProductImage, ProductAttribute, AttributeValue, Attribute, Comment
from import_export import resources


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class AttributeResource(resources.ModelResource):
    class Meta:
        model = Attribute


class AttributeValueResource(resources.ModelResource):
    class Meta:
        model = AttributeValue


class ProductAttributeResource(resources.ModelResource):
    class Meta:
        model = ProductAttribute


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('value',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "category", "group"]
    inlines = [ProductImageInline, ProductAttributeInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "is_prime"]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["product", "attribute", "attribute_value"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "product__name", "content")
