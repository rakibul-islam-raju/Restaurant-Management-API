from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import LoginView, UserRegistrationView, UserListView

app_name = "accounts"

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", LoginView.as_view(), name="login"),
    path("registration", UserRegistrationView.as_view(), name="registration"),
    path("users", UserListView.as_view(), name="user-list"),
]
