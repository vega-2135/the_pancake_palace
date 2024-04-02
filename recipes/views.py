from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe
import re


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1)
    template_name = "index.html"
    paginate_by = 6


def recipe_detail(request, slug):
    """
    Display an individual recipe post.

    **Context**

    ``recipe``
        An instance of :model:`recipe.Post`.

    **Template:**

    :template:`recipes/recipe_detail.html`
    """
    # Return all objects of the class Recipe
    queryset = Recipe.objects.filter(status=1)

    # Return recipe with the correct slug
    recipe = get_object_or_404(queryset, slug=slug)
  
    recipe_title = recipe.title

    # Split ingredients and preparation steps into several strings 
    ingredients = recipe.ingredients.split('<br>')
    preparation = recipe.preparation.split('<br>')
    # Remove any HTML tags 
    ingredients = [re.sub('<[^<]+?>', '', ingredient) for ingredient in ingredients]
    preparation = [re.sub('<[^<]+?>', '', step) for step in preparation]

    
    # set liked to false by default
    recipe_liked = False
    
    if recipe.likes.filter(id=request.user.id).exists():
        recipe_liked = True
    

    return render(
        request,
        "recipe_detail.html",
        {"recipe": recipe,
        "recipe_title": recipe_title,
        "ingredients": ingredients,
        "preparation": preparation,
        "recipe_liked": recipe_liked },
    )