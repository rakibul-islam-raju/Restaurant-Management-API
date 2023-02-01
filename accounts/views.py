from accounts.models import User

from rest_framework.exceptions import APIException
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.serializers import (
    TokenSerializer,
    UserRegistrationSerializer,
    UserSerilizerWithToken,
    UserSerializer,
)


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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_staff:
            return User.objects.filter(is_superuser=False)
        else:
            return User.objects.none()


# class UserDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated | ]

#     def get_permissions(self):
#         if self.request.user.is_
#             self.permission_classes = [AllowAny]
#         else:
#             self.permission_classes = [IsAdminUser]

#         return super(CategoryListCreateView, self).get_permissions()
