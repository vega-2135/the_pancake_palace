from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Recipe, Comment
import re
import json
from .forms import CommentForm
from .forms import (
    RecipeForm,
    IngredientsFormset,
    PreparationFormset,
    CommentForm)
from .forms import RatingForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

    saved_recipe = False

    if recipe.saved.filter(id=request.user.id).exists():
        saved_recipe = True
  
    # Set liked to false by default
    recipe_liked = False
    
    if recipe.likes.filter(id=request.user.id).exists():
        recipe_liked = True
    
    # Display only approved comments
    comments = recipe.comments.all().order_by("-created_on")
    comment_count = recipe.comments.filter(approved=True).count()

    # Display a form to users, so they can add comments and rate a recipe post
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        rating_form = RatingForm(data=request.POST)
        
        if comment_form.is_valid() and rating_form.is_valid():
            # Process comment
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.recipe = recipe
            comment.save()

            # Process rating
            rating = rating_form.cleaned_data['rating']
            current_rating = recipe.rating if recipe.rating else 0
            num_of_ratings = recipe.number_of_ratings if recipe.number_of_ratings else 0
            new_average_rating = ((current_rating * num_of_ratings) + int(rating)) / (num_of_ratings + 1)
            recipe.rating = round(new_average_rating, 2)
            recipe.number_of_ratings = num_of_ratings + 1
            recipe.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your comment and rating will be submitted once approved.'
            )
            return redirect('recipe_detail', slug=slug)
        else:
            messages.warning(
                        request,
                        ('You must rate the recipe if you want to leave a comment')
                    )

    else:
        comment_form = CommentForm()
        rating_form = RatingForm()
        # Uncomment next line to raise a 400 error
        # raise SuspiciousOperation("Title and ingredients are required.")
        # Uncomment next line to raise a 403 error
        # raise PermissionDenied
        # Uncomment next line to raise a 500 error
        #raise Exception("This is a deliberate exception to trigger a 500 error")
    

    return render(
        request,
        "recipe_detail.html",
        {"recipe": recipe,
        "recipe_title": recipe_title,
        "saved_recipe": saved_recipe,
        "recipe_liked": recipe_liked,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "rating_form": rating_form, 
        },
    )

@login_required
def comment_edit(request, slug, comment_id):
    """
    Function to edit comments
    """
    if request.preparation == "POST":

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

@login_required
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

#### Share recipe view ####
class ShareRecipe(LoginRequiredMixin, CreateView):
    '''
    Allow authenticated user to access create recipe form to submit recipes.
    '''
    model = Recipe
    form_class = RecipeForm
    template_name = 'share_recipe.html'
    success_url = reverse_lazy('submitted_recipes')

    def get_context_data(self, **kwargs):
        # Add ingredients formset, preparation formset and page title to context.
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients_formset'] = IngredientsFormset(
                self.request.POST,
                prefix='ingredients'
            )
            context['preparation_formset'] = PreparationFormset(
                self.request.POST,
                prefix='preparation'
            )
            context['page_title'] = 'Share Recipe'
        else:
            context['ingredients_formset'] = IngredientsFormset(
                prefix='ingredients'
            )
            context['preparation_formset'] = PreparationFormset(prefix='preparation')
            context['page_title'] = 'Create Recipe'
        return context
    
    def form_valid(self, form):
        # Validate submitted form.
        context = self.get_context_data()
        ingredients_formset = context['ingredients_formset']
        preparation_formset = context['preparation_formset']

        if ingredients_formset.is_valid() and preparation_formset.is_valid():
            # get cleaned data from ingredients formset
            ingredients_input = ingredients_formset.cleaned_data
            # convert ingredients input data into json string
            ingredients_json = json.dumps(ingredients_input)
            preparation_input = preparation_formset.cleaned_data
            preparation_json = json.dumps(preparation_input)
            # set author as current user
            form.instance.author = self.request.user
            # set ingredients as ingredients json string
            form.instance.ingredients = ingredients_json
            form.instance.preparation = preparation_json
            # if publish request check box is checked
            if form.instance.make_public:
                # if recipe does not include ingredients or preparation,
                # save but don't submit for publication
                if (form.instance.ingredients == "[]" or
                        form.instance.preparation == "[]"):
                    form.instance.make_public = False
                    # display message informing user recipe requires
                    # ingredients and preparation for publication
                    messages.warning(
                        self.request,
                        ('Recipe saved but requires ingredients and '
                            'preparation for publication')
                    )
                else:
                    # set approval status to 'pending approval'
                    form.instance.approved = False
                    messages.success(
                        self.request,
                        'Recipe successfully created and awaiting approval'
                    )
            else:
                # approval status will be set to 'unpublished' by default
                messages.success(self.request, 'Recipe saved in your recipes')
            return super().form_valid(form)
        

class RecipeOwnership(UserPassesTestMixin):
    '''
    If the user is the recipe author, they will have permission
    to perform an action.
    If the user does not match the recipe author the user will be
    redirected to 403 error page.
    '''
    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user
    

class EditRecipe(LoginRequiredMixin, RecipeOwnership, UpdateView):
    '''
    Allow authenticated user that passes RecipeOwnership to edit recipes.
    Display create recipe form populated with values from the
    recipe being edited.
    '''
    model = Recipe
    form_class = RecipeForm
    template_name = 'share_recipe.html'
    success_url = reverse_lazy('submitted_recipes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients_formset'] = IngredientsFormset(
                self.request.POST,
                initial=json.loads(self.object.ingredients),
                prefix='ingredients'
            )
            context['preparation_formset'] = PreparationFormset(
                self.request.POST,
                initial=json.loads(self.object.preparation),
                prefix='preparation'
            )
            context['page_title'] = 'Edit Recipe'
        else:
            context['ingredients_formset'] = IngredientsFormset(
                initial=json.loads(self.object.ingredients),
                prefix='ingredients'
            )
            context['preparation_formset'] = PreparationFormset(
                initial=json.loads(self.object.preparation),
                prefix='preparation'
            )
            context['page_title'] = 'Edit Recipe'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients_formset = context['ingredients_formset']
        preparation_formset = context['preparation_formset']

        if ingredients_formset.is_valid() and preparation_formset.is_valid():
            ingredients_input = ingredients_formset.cleaned_data
            ingredients_json = json.dumps(ingredients_input)
            preparation_input = preparation_formset.cleaned_data
            preparation_json = json.dumps(preparation_input)
            form.instance.author = self.request.user
            form.instance.ingredients = ingredients_json
            form.instance.preparation = preparation_json
            if form.instance.make_public:
                # if recipe does not include ingredients or preparation,
                # save but don't submit for publication
                if (form.instance.ingredients == "[]" or
                        form.instance.preparation == "[]"):
                    form.instance.make_public = False
                    form.instance.status = 0
                    # display message informing user recipe requires
                    # ingredients and preparation for publication
                    messages.warning(
                        self.request,
                        ('Recipe saved but requires ingredients and '
                            'preparation for publication')
                    )
                else:
                    # set approval status to 'pending approval'
                    form.instance.status = 1
                    messages.success(
                        self.request,
                        'Recipe successfully created and awaiting approval'
                    )
            else:
                form.instance.status = 0
                messages.success(self.request, 'Recipe successfully edited')
            return super().form_valid(form) 
        
@login_required
def delete_submitted_recipe(request, slug):
    """
    view to delete submitted recipe
    """
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)

    if recipe.status == 1:

        if recipe.author == request.user:
            recipe.delete()
            messages.add_message(request, messages.SUCCESS, 'Recipe deleted!')
        else:
            messages.add_message(request, messages.ERROR, "You can only" 
                                 "delete your own recipes!")

    else:
        messages.add_message(request, messages.ERROR, "You can only delete " 
                "published recipes, wait for approval to delete the recipe")
    
    return HttpResponseRedirect(reverse('submitted_recipes'))


class SubmittedRecipes(LoginRequiredMixin, ListView):
    '''
    Display recipes that the user has shared.
    '''
    template_name = 'submitted_recipes.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Submitted Recipes'
        return context

    def get_queryset(self):
        # Return all recipes that user has written,
        # in reverse order of created date.
        shared_recipes = Recipe.objects.filter(
            author=self.request.user
        ).order_by('-created_on')
        return shared_recipes
    
@login_required
def saved_recipes(request):
    queryset = Recipe.objects.filter(status=1)
    new_added_recipe = queryset.filter(saved=request.user)
    return render(request, "saved_recipes.html", {"new_added_recipe": new_added_recipe})


@login_required
def save_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if not recipe.saved.filter(id=request.user.id).exists():
        recipe.saved.add(request.user)
    recipe.saved_boolean = True
    recipe.save()
    redirect_url = request.META.get('HTTP_REFERER', reverse('saved_recipes'))
    return HttpResponseRedirect(redirect_url)


@login_required
def remove_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.saved.filter(id=request.user.id).exists():
        recipe.saved.remove(request.user)
    recipe.saved_boolean = False
    recipe.save()
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

#### Search recipes ####
class RecipeSearch(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'search.html'
    paginate_by = 6

    def get_queryset(self):
        if self.request.method == 'GET':
            search_query = self.request.GET.get('search_query')
            recipes = Recipe.objects.filter(title__icontains=search_query)
            return recipes
        else:
            return Recipe.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search_query')
        return context


#### Recipes categories ####
def popular_pancakes(request):
    recipe_list = Recipe.objects.filter(category=0)
    return render(request, 'popular_pancakes.html', {'recipe_list': recipe_list})

def pancakes_kids(request):
    recipe_list = Recipe.objects.filter(category=1)
    return render(request, 'pancakes_kids.html', {'recipe_list': recipe_list})

def vegan_pancakes(request):
    recipe_list = Recipe.objects.filter(category=2)
    return render(request, 'vegan_pancakes.html', {'recipe_list': recipe_list})