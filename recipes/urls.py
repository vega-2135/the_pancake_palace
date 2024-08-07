"""
Recipes URL Configuration
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path("recipe/<slug:slug>/", views.recipe_detail, name="recipe_detail"),
    path(
        "recipe/<slug:slug>/edit_comment/<int:comment_id>",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "recipe/<slug:slug>/delete_comment/<int:comment_id>",
        views.comment_delete,
        name="comment_delete",
    ),
    path("save/<slug:slug>/", views.save_recipe, name="save_recipe"),
    path("saved-recipes/", views.saved_recipes, name="saved_recipes"),
    path("remove/<slug:slug>/", views.remove_recipe, name="remove_recipe"),
    path("like/<slug:slug>/", views.like_recipe, name="like_recipe"),
    path("share/", views.ShareRecipe.as_view(), name="share_recipe"),
    path("edit/<slug:slug>/", views.EditRecipe.as_view(), name="edit_recipe"),
    path(
        "submitted-recipes/",
        views.SubmittedRecipes.as_view(),
        name="submitted_recipes",
    ),
    path(
        "recipe/<slug:slug>/delete_submitted_recipe/<int:recipe_id>",
        views.delete_submitted_recipe,
        name="delete_submitted_recipe",
    ),
    path("search/", views.RecipeSearch.as_view(), name="search_recipe"),
    path(
        "popular-pancakes/",
        views.PopularPancakes.as_view(),
        name="popular_pancakes",
    ),
    path("pancakes-kids/", views.PancakesKids.as_view(), name="pancakes_kids"),
    path(
        "vegan-pancakes/", views.VeganPancakes.as_view(), name="vegan_pancakes"
    ),
]
