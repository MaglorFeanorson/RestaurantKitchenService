from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import (
    Cook,
    Dish,
    DishType
)

@login_required
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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "restaurant_kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 1


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("restaurant_kitchen:dish-type-list")
    template_name = "restaurant_kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("restaurant_kitchen:dish-type-list")
    template_name = "restaurant_kitchen/dish_type_form.html"



class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish



