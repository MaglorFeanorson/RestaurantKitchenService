from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import (
    Cook,
    Dish,
    DishType
)


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dish = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dish": num_dish,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "restaurant_kitchen/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "restaurant_kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")

class CookListView(generic.ListView):
    model = Cook

def dish_detail_view(request: HttpRequest, pk=int) -> HttpResponse:
    dish = Dish.objects.get(id=pk)
    context = {
        "dish": dish,
    }
    return render(request, "restaurant_kitchen/dish_detail.html", context=context)
