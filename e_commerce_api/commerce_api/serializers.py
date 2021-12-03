from rest_framework import serializers
from .models import Category, Book, Product, Cart

# from django.contrib.auth.models import User
from rest_auth.serializers import LoginSerializer
from commerce_api.models import User
from rest_auth.serializers import LoginSerializer


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)
    # username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password")

    def validate(self, args):
        email = args.get("email", None)
        username = args.get("username", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        # if User.objects.filter(username=username).exists():
        #     raise serializers.ValidationError({"username": ("username already exists")})

        return super().validate(args)

    def create(self, validated_data):
        user = super(RegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("user").verification:
            return attrs
        raise serializers.ValidationError("Please verify your email to login")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title")
        model = Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title",)
        model = Category


class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source="created_by.username", read_only=False
    )

    class Meta:
        fields = (
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
            "status",
            "date_created",
        )
        model = Book


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source="created_by.username", read_only=False
    )

    class Meta:
        fields = (
            "id",
            "product_tag",
            "name",
            "category",
            "price",
            "stock",
            "imageUrl",
            "status",
            "date_created",
        )
        model = Product


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all()
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "books",
            "products",
            "verification",
        )


class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class CartSerializer(serializers.ModelSerializer):

    cart_id = CartUserSerializer(read_only=True, many=False)
    books = BookSerializer(read_only=True, many=True)
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ("cart_id", "created_at", "books", "products")
