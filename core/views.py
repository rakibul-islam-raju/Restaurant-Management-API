from decimal import Decimal
from django.db.models import Q
from django.db.models import Avg
from rest_framework import status
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
    OrderItemSerializer,
    OrderSerializer,
    MenuSerializer,
    MenuCreateSerializer,
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
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Menu.objects.filter(is_active=True)
            .distinct()
            .annotate(avg_rating=Avg("review__rating"))
            .order_by("-avg_rating")[0:4]
        )


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
            order_serializer = OrderSerializer(
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
                menu = Menu.objects.get(id=i["menu"])
                item = OrderItem(
                    menu=menu,
                    order=order,
                    name=menu.name,
                    quantity=int(i["quantity"]),
                    price=Decimal(i["price"]),
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
    serializer_class = CategorySerializer
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
    serializer_class = ResarvationSerializer
    queryset = Resarvation.objects.all()

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
