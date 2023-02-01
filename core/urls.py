from django.urls import path

from core.views import (
    CategoryListCreateView,
    CategoryDetailView,
    MenuListCreateView,
    MenuDetailView,
)

app_name = "core"

urlpatterns = [
    # categories
    path("categories", CategoryListCreateView.as_view(), name="categories"),
    path("categories/<pk>", CategoryDetailView.as_view(), name="category-details"),
    # menus
    path("menus", MenuListCreateView.as_view(), name="categories"),
    path("menus/<pk>", MenuDetailView.as_view(), name="menu-details"),
]
