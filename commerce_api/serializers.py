from rest_framework import serializers
from .models import Category, Book, Product, Cart
from django import forms
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore

# from django.contrib.auth.models import User
from rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from commerce_api.models import User
from rest_auth.serializers import LoginSerializer
from commerce_api.tasks.passeord_reset_task import send_password_reset_email


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "verification",
        )


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("user").verification:
            return attrs
        raise serializers.ValidationError("Please verify your email First to login")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title")
        model = Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title",)
        model = Category


class BookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
            "user",
            "status",
            "date_created",
        )
        model = Book


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        fields = (
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
        model = Product
        read_only_fields = ("user",)


class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)


class CartSerializer(serializers.ModelSerializer):
    cart_id = CartUserSerializer(read_only=True, many=False)
    books = BookSerializer(read_only=True, many=True)
    products = ProductSerializer(read_only=True, many=True)
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.cart_id_id

    class Meta:
        model = Cart
        fields = ("id", "cart_id", "created_at", "books", "products")


class PasswordResetForm(PasswordResetFormCore):
    """custom password reset form for send email with celery"""

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "email", "placeholder": "Email"}
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        context["user"] = context["user"].id
        send_password_reset_email.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """Password Reset Serializer"""

    def get_email_options(self):
        return {"email_template_name": "commerce_api/password_reset_email.txt"}

    def validate_email(self, value):
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError("Error")

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid e-mail address")
        return value
