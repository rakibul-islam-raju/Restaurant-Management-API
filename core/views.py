from decimal import Decimal
from django.db.models import Q
from django.db.models import Avg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core.permissions import IsOwner, IsStaffOrOwnerAuthenticated
from core.serializers import (
    CampaignSerializer,
    ContactSerializer,
    CategorySerializer,
    CategoryCreateSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    MenuSerializer,
    MenuCreateSerializer,
    ResarvationCreateSerializer,
    ResarvationSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from core.models import (
    Category,
    Menu,
    Campaign,
    Order,
    OrderItem,
    Contact,
    Resarvation,
    Review,
)
from accounts.models import User
from accounts.serializers import UserSerializer


class SummaryStatistics(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        pending_orders = Order.objects.filter(is_served=False).count()
        registered_users = User.objects.filter(is_staff=False).count()
        pending_reservations = Resarvation.objects.filter(status="pending").count()
        runnig_campaigns = Campaign.objects.filter(is_active=True).count()

        results = {
            "pending_orders": pending_orders,
            "registered_users": registered_users,
            "pending_reservations": pending_reservations,
            "runnig_campaigns": runnig_campaigns,
        }

        return Response({"results": results})


class CategoryListCreateView(ListCreateAPIView):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Category.objects.all()
        else:
            return Category.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategoryCreateSerializer
        else:
            return CategorySerializer

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


class TopRatedMenus(ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        return (
            Menu.objects.filter(is_active=True)
            .distinct()
            .annotate(avg_rating=Avg("review__rating"))
            .order_by("-avg_rating")[0:6]
        )


class MenuListCreateView(ListCreateAPIView):
    filterset_fields = ["category"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Menu.objects.all()
        else:
            return Menu.objects.filter(is_active=True)

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

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return MenuCreateSerializer
        else:
            return MenuSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]

        return super(MenuDetailView, self).get_permissions()


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filterset_fields = ["is_active", "is_paid", "is_served", "user__email"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsStaffOrOwnerAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(OrderListCreateView, self).get_permissions()

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        order_items = data.get("order_items")

        if order_items and len(order_items) == 0:
            return Response(
                {"detail": "No Order Items"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            order_serializer = OrderCreateSerializer(
                data={
                    "user": user.pk,
                    "tax": data.get("tax"),
                    "total_price": data.get("total_price"),
                }
            )
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save()

            # create order items and add to order
            for i in order_items:
                price = 0
                if i["offer_price"]:
                    price = i["offer_price"]
                else:
                    price = i["price"]
                menu = Menu.objects.get(id=i["id"])
                item = OrderItem(
                    menu=menu,
                    order=order,
                    name=menu.name,
                    quantity=int(i["quantity"]),
                    price=Decimal(price),
                    image=menu.image,
                )
                item.save()

                menu.save()

            serializer = OrderDetailSerializer(order, many=False)
            return Response(serializer.data)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrOwnerAuthenticated]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


class CampaignListCreateView(ListCreateAPIView):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Campaign.objects.all()
        else:
            return Campaign.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]

        return super(CampaignListCreateView, self).get_permissions()


class CampaignDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()
    permission_classes = [IsAdminUser]


class ContactListCreateView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]

        return super(ContactListCreateView, self).get_permissions()


class ContactDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [IsAdminUser]


class ResarvationListCreateView(ListCreateAPIView):
    queryset = Resarvation.objects.all()
    filterset_fields = ["is_active", "user__email"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ResarvationCreateSerializer
        else:
            return ResarvationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return super(ResarvationListCreateView, self).get_permissions()


class ResarvationDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ResarvationSerializer
    queryset = Resarvation.objects.all()
    permission_classes = [IsAdminUser]


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        else:
            return ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]

        return super(ReviewListCreateView, self).get_permissions()


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Resarvation.objects.all()
    permission_classes = [IsOwner]
