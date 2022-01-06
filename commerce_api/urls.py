from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListCategory,
    DetailCategory,
    ListBook,
    ListProduct,
    ListUser,
    ListCart,
    EmailValidate,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    EmployeeApiView
    # UserView
)


router = DefaultRouter()
router.register(r"users", ListUser, basename="user")
router.register(r"carts", ListCart, basename="carts")

urlpatterns = [
    path("categories/", ListCategory.as_view(), name="categorie"),
    path("categories/<int:pk>/", DetailCategory.as_view(), name="singlecategory"),
    path("books/", ListBook.as_view(), name="books"),
    # path('books', ListBook.as_view(), name='books'),
    path("books/<int:pk>/", ListBook.as_view(), name="singlebook"),
    path("products/", ListProduct.as_view(), name="products"),
    path("products/<int:pk>/", ListProduct.as_view(), name="singleproduct"),
    # path("users/", ListUser.as_view(), name="users"),
    # path("users/<int:pk>/", DetailUser.as_view(), name="singleuser"),
    path("routers_urls/", include(router.urls)),
    # path("carts/", ListCart.as_view(), name="allcarts"),
    # path("carts/<int:pk>/", DetailCart.as_view(), name="cartdetail"),
    path("activate/<uidb64>/<token>/", EmailValidate.as_view(), name="activate"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView().as_view(),
        name="password_reset_confirm",
    ),
    path("emp/",EmployeeApiView.as_view(),name="emp"),
    path("emp/<int:pk>/",EmployeeApiView.as_view(),name="emp"),
    # path("users-list",UserView.as_view(),name="users-list")
]
