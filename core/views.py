from django.db.models import Avg
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core.serializers import (
    CampaignSerializer,
    ContactSerializer,
    CategorySerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
    MenuSerializer,
    MenuCreateSerializer,
    ResarvationSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from core.models import (
    Campaign,
    Category,
    Menu,
    Order,
    OrderItem,
    Contact,
    Resarvation,
    Review,
)


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Category.objects.all()
        else:
            return Category.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]

        return super(CategoryListCreateView, self).get_permissions()


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class MenuListCreateView(ListCreateAPIView):
    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = Menu.objects.filter(Q(name__icontains=keyword))
        else:
            queryset = Menu.objects.all()

        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MenuCreateSerializer
        else:
            return MenuSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(MenuListCreateView, self).get_permissions()


class MenuDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Menu.objects.all()
        else:
            return Menu.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]

        return super(ProductDetailView, self).get_permissions()
