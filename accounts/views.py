from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, update_session_auth_hash

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import User
from accounts.serializers import (
    TokenSerializer,
    UserRegistrationSerializer,
    UserSerilizerWithToken,
    UserSerializer,
    SuperUserEditSerializer,
    UserEditSerializer,
    ChangePasswordSerializer,
)
from accounts.permissions import IsSuperAdmin

from core.permissions import IsOwner


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerilizerWithToken(user, many=False).data)


class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["=email"]


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdmin]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return SuperUserEditSerializer
        else:
            return UserSerializer


class ProfileEditView(RetrieveUpdateAPIView):
    permission_classes = [IsOwner]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UserEditSerializer
        else:
            return UserSerializer


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            user = authenticate(email=request.user.email, password=old_password)
            if user:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

                return Response(
                    {"message": "password changed"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
