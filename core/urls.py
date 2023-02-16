from django.urls import path

from core.views import (
    CategoryListCreateView,
    CategoryDetailView,
    MenuListCreateView,
    MenuDetailView,
    TopRatedMenus,
    OrderListCreateView,
    OrderDetailView,
    CampaignListCreateView,
    CampaignDetailView,
    ContactListCreateView,
    ContactDetailView,
    ResarvationListCreateView,
    ResarvationDetailView,
    ReviewListCreateView,
    ReviewDetailView,
)

app_name = "core"

urlpatterns = [
    # categories
    path("categories", CategoryListCreateView.as_view(), name="categories"),
    path("categories/<pk>", CategoryDetailView.as_view(), name="category-details"),
    # menus
    path("menus", MenuListCreateView.as_view(), name="categories"),
    path("menus/<pk>", MenuDetailView.as_view(), name="menu-details"),
    path("menus/top-rated", TopRatedMenus.as_view(), name="menu-top-rated"),
    # orders
    path("orders", OrderListCreateView.as_view(), name="orders"),
    path("orders/<pk>", OrderDetailView.as_view(), name="order-details"),
    # campaigns
    path("campaigns", CampaignListCreateView.as_view(), name="campaigns"),
    path("campaigns/<pk>", CampaignDetailView.as_view(), name="campaign-details"),
    # contact
    path("contacts", ContactListCreateView.as_view(), name="contacts"),
    path("contacts/<pk>", ContactDetailView.as_view(), name="contact-details"),
    # resarvations
    path("resarvations", ResarvationListCreateView.as_view(), name="resarvations"),
    path(
        "resarvations/<pk>", ResarvationDetailView.as_view(), name="resarvation-details"
    ),
    # reviews
    path("reviews", ReviewListCreateView.as_view(), name="reviews"),
    path("reviews/<pk>", ReviewDetailView.as_view(), name="review-details"),
]
