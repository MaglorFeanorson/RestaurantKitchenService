from django.urls import path, include

from restaurant_kitchen.views import (
    index,
    DishTypeListView,
    DishTypeCreateView,
    DishListView,
    CookListView,
    CookDetailView,
    DishDetailView,


)

urlpatterns = [
    path("", index, name="index"),

    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),

]

app_name = "restaurant_kitchen"
