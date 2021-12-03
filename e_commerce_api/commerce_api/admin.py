# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from commerce_api.models import Category, Book, Product, Cart, User

# Register your models here.


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(User)
