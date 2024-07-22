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
    paginate_by = 5


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


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


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "restaurant_kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("restaurant_kitchen:dish-type-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    paginate_by = 5

class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = ["username", "first_name", "last_name", "years_of_experience"]
    success_url = reverse_lazy("restaurant_kitchen:cook-list")
    template_name = "restaurant_kitchen/cook_form.html"

class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ["username", "first_name", "last_name", "years_of_experience"]
    success_url = reverse_lazy("restaurant_kitchen:cook-list")
    template_name = "restaurant_kitchen/cook_form.html"

class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("restaurant_kitchen:cook-list")
    template_name = "restaurant_kitchen/cook_confirm_delete.html"


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish

class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = ["name", "description", "price", "dish_type", "cooks"]
    success_url = reverse_lazy("restaurant_kitchen:dish-list")
    template_name = "restaurant_kitchen/dish_form.html"

class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = ["name", "description", "price", "dish_type", "cooks"]
    success_url = reverse_lazy("restaurant_kitchen:dish-list")
    template_name = "restaurant_kitchen/dish_form.html"

class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant_kitchen:dish-list")
    template_name = "restaurant_kitchen/dish_confirm_delete.html"


