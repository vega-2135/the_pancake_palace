from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Recipe, Comment
import re
from .forms import CommentForm
from .forms import RatingForm

import logging


LOGGER = logging.getLogger('django')


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
    recipe = get_object_or_404(queryset, slug=slug, status='1')
    recipe_title = recipe.title

    saved_recipe = bool

    if recipe.saved.filter(id=request.user.id).exists():
        saved_recipe = True
    

    # Split ingredients and preparation steps into se#veral strings 
    ingredients = recipe.ingredients
    preparation = recipe.preparation.split('<br>')
    LOGGER.info(type(ingredients))
    # Remove any HTML tags 
    ingredients_parts = []
    for i in range(len(ingredients)):
        ingredients_items = f"{ingredients[i]['name']}, {ingredients[i]['quantity']}"
        ingredients_parts.append(ingredients_items)
        LOGGER.info(ingredients_parts)

    preparation = [re.sub('<[^<]+?>', '', step) for step in preparation]

    
    # Set liked to false by default
    recipe_liked = False
    
    if recipe.likes.filter(id=request.user.id).exists():
        recipe_liked = True
    
    # Display only approved comments
    comments = recipe.comments.all().order_by("-created_on")
    comment_count = recipe.comments.filter(approved=True).count()

    # Display a form to users, so they can add comments to a recipe post
    # Make form functinal by adding POST method
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.recipe = recipe
            print(comment_form)
            print(recipe)
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your comment will be submitted once approved.'
            )

    comment_form = CommentForm()
    

    return render(
        request,
        "recipe_detail.html",
        {"recipe": recipe,
        "recipe_title": recipe_title,
        "saved_recipe": saved_recipe,
        "ingredients": ingredients_parts,
        "preparation": preparation,
        "recipe_liked": recipe_liked,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        },
    )

def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if form.is_valid():
            rating = form.cleaned_data['rating']
            # Calculate the new average rating
            current_rating = recipe.rating if recipe.rating else 0
            num_of_ratings = recipe.num_of_ratings if recipe.num_of_ratings else 0
            new_average_rating = ((current_rating * num_of_ratings) + int(rating)) / (num_of_ratings + 1)
            recipe.rating = round(new_average_rating, 2)
            recipe.num_of_ratings = num_of_ratings + 1
            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RatingForm()
    
    return render(request, 'rate_recipe.html', {'form': form})


def comment_edit(request, slug, comment_id):
    """
    Function to edit comments
    """
    if request.method == "POST":

        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Recipe.objects.filter(status=1)
    recipe = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


@login_required
def saved_recipes(request):
    queryset = Recipe.objects.filter(status=1)
    new_added_recipe = queryset.filter(saved=request.user)
    return render(request, "saved_recipes.html", {"new_added_recipe": new_added_recipe})


@login_required
def save_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.saved.filter(id=request.user.id).exists():
        recipe.saved.remove(request.user)
    else:
        recipe.saved.add(request.user)

    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


@login_required
def remove_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.saved.filter(id=request.user.id).exists():
        recipe.saved.remove(request.user)
    # Redirect the user back to the referring page, or to a default page if the 
    # referring page is not available
    redirect_url = request.META.get('HTTP_REFERER', reverse('saved_recipes'))
    return HttpResponseRedirect(redirect_url)

@login_required
def like_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))
