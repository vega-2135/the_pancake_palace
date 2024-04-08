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
    path('remove/<slug:slug>/', views.remove_recipe, name='remove_recipe')
]