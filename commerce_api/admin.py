# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from commerce_api.models import Category, Book, Product, Cart, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    """user model fields list display"""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "verification",
    )
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "verification",
    )


class CategoryAdmin(admin.ModelAdmin):
    """user model fields list display"""

    list_display = (
            "id",
            "title"
    )

    search_fields = (
      "id",
      "title",
    )

    list_filter = (
      "title",
    )


class BookAdmin(admin.ModelAdmin):
    """user model fields list display"""

    list_display = (
            "id",
            "title",
            "category",
            "author",
            "isbn",
            "pages",
            "price",
            "stock",
            "description",
            "imageUrl",
            "user",
            "status",
            "date_created",
    )

    search_fields = (
        "id",
        "title",
        "category",
        "author",
    )

    list_filter = (
       "title",
        "category",
        "author",
    )

class ProductAdmin(admin.ModelAdmin):
    """user model fields list display"""

    list_display = (
            "id",
            "product_tag",
            "name",
            "category",
            "price",
            "stock",
            "imageUrl",
            "user",
            "status",
            "date_created",
    )

    search_fields = (
      "name",
      "category",
    )

    list_filter = (
      "name",
      "category",
      "price",
    )


class CartAdmin(admin.ModelAdmin):
    """user model fields list display"""

    list_display = (
            "cart_id_id",
            "cart_id",
            "created_at",
    )

    search_fields = (
      "cart_id_id",
    )









# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Book)
# admin.site.register(Cart)
# admin.site.register(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)


