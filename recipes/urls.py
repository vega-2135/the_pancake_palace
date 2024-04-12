from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('recipe/<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
    path('save/<slug:slug>/', views.save_recipe, name='save_recipe'),
    path('saved-recipes/', views.saved_recipes, name='saved_recipes'),
    path('remove/<slug:slug>/', views.remove_recipe, name='remove_recipe'),
    path('like/<slug:slug>/', views.like_recipe, name='like_recipe'),
    path('share/', views.ShareRecipe.as_view(), name='share_recipe'),
    path('edit/<slug:slug>/', views.EditRecipe.as_view(), name='edit_recipe'),
    path('submitted-recipes/', views.SubmittedRecipes.as_view(), name='submitted_recipes'),
    path('delete_submitted/<slug:slug>/', views.delete_submitted_recipe, name='delete_submitted_recipe'),
    path('popular-pancakes/', views.popular_pancakes, name='popular_pancakes'),
    path('pancakes-kids/', views.pancakes_kids, name='pancakes_kids'),
    path('vegan-pancakes/', views.vegan_pancakes, name='vegan_pancakes'),
]