# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import generics
from commerce_api.models import Category, Product, Book, Cart, User

# from django.contrib.auth.models import User
from commerce_api.serializers import (
    ProductSerializer,
    BookSerializer,
    CategorySerializer,
    UserSerializer,
    CartSerializer,
    RegistrationSerializer,
    CategoriesSerializer,
    CustomLoginSerializer,
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import uuid
from commerce_api.tasks.send_email_celery import send_email_id_verification_email
from commerce_api.tasks.welcome_task import send_welcome_email
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from rest_auth.views import LoginView as RestLoginView


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = Token.objects.create(user=user).key
            to_email = user.email
            first_name = user.first_name
            send_email_id_verification_email.delay(uid, token, first_name, to_email)
            return Response(
                {
                    # "RequestId": str(uuid.uuid4()),
                    "Message": "Send Email for verification please verify your email...",
                    "User": serializer.data,
                    "Status": status.HTTP_201_CREATED,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(RestLoginView):
    # permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.verification = True
        login(request, user)
        return super().post(request, format=None)


class EmailValidate(APIView):
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user and Token.objects.get(user=user):
            user.verification = True
            user.save()
            user_first_name = user.first_name
            to_email = user.email
            send_welcome_email.delay(user_first_name, to_email)
            return Response({"Message": "Thank you For verifying your email address"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListBook(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Book.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BookSerializer(snippet)
        return Response(serializer.data)

    def post(self, request, format=None):

        category, created = Category.objects.get_or_create(
            title=request.data.get("category")
        )

        request.data.update({"category": category.id})
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        category, created = Category.objects.get_or_create(
            title=request.data.get("category")
        )
        request.data.update({"category": category.id})
        serializer = BookSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        category, created = Category.objects.get_or_create(
            title=request.data.get("category")
        )
        request.data.update({"category": category.id})
        serializer = BookSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCategory(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class ListBook(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class DetailBook(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class ListProduct(APIView):
    def get_object(self, pk):
        return ListProduct.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BookSerializer(snippet)
        return Response(serializer.data)

    def post(self, request, format=None):

        category, created = Category.objects.get_or_create(
            title=request.data.get("category")
        )

        request.data.update({"category": category.id})
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        category, created = Category.objects.get_or_create(
            title=request.data.get("category")
        )
        request.data.update({"category": category.id})
        serializer = ProductSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ListUser(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCart(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class DetailCart(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
