from django.db import models
from django.contrib.auth.models import AbstractUser
from kombu.abstract import MaybeChannelBound
from e_commerce.manager import UserManager
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
User = settings.AUTH_USER_MODEL


class User(AbstractUser):
    """User model"""

    username = None
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    verification = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, related_name="books_category", on_delete=models.CASCADE
    )
    author = models.CharField(max_length=100, default="John Doe")
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField()
    imageUrl = models.URLField()
    user = models.ForeignKey(
        "User",
        related_name="books_user",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title


class Product(models.Model):
    product_tag = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    price = models.IntegerField()
    stock = models.IntegerField()
    imageUrl = models.URLField()
    user = models.ForeignKey(
        User, related_name="products", blank=True, null=True, on_delete=models.CASCADE
    )
    status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "{} {}".format(self.product_tag, self.name)

    # product = models.ForeignKey(Product, related_name='products',blank=True,,on_delete=models.CASCADE)
    # book = models.ForeignKey(Book, related_name='books', on_delete=models.CASCADE)


class Cart(models.Model):
    cart_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    books = models.ManyToManyField(Book)
    products = models.ManyToManyField(Product)

    class Meta:
        ordering = ["cart_id", "-created_at"]

    def __str__(self):
        return f"{self.cart_id}"


class DocumentManager(models.QuerySet):

    def first_name(self):
        return self.filter(first_name='Pr')

    def last_name(self):
        return self.filter(last_name__startswith='d')


class Comment(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField()

    # the required fields to enable a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.author


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.IntegerField()
    comments = GenericRelation(Comment)
    objects = DocumentManager.as_manager()


    def __str__(self):
        return self.email


