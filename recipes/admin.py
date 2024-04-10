from django.contrib import admin
from .models import Recipe, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    Register recipe model.
    """
    list_display = ('title', 'author', 'created_on', 'status', 'approved')
    search_fields = ['title', 'author']
    list_filter = ('status','created_on', 'approved')
    summernote_fields = ('ingredients', 'preparation',)
    actions = ['approve_recipe']

    # Define approve recipes action, once the admin approves a recipe
    # the status of that recipe changes from Draft to Publish
    def approve_recipe(self, request, queryset):
        queryset.update(approved=True, status= '1')




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Register comment model.
    '''
    list_display = ('author', 'created_on', 'approved')
    search_fields = ['author', 'content']
    list_filter = ('created_on', 'approved')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)