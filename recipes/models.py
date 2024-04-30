from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models

# Recipe post status for admin users
STATUS = ((0, "Draft"), (1, "Published"))

CATEGORY = (
    (0, "Popular Pancakes"),
    (1, "Pancakes for Kids"),
    (2, "Vegan Pancakes")
)


# Recipe Model
class Recipe(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resources_added")
    servings = models.IntegerField(
        help_text="Please enter the number of portions that result"
        "from your recipe."
    )
    cooking_duration = models.IntegerField(
        help_text="Please enter how many minutes is required for"
        "the preparation of your recipe")
    ingredients = models.TextField()
    preparation = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.IntegerField(choices=CATEGORY, default=0)
    recipe_image = CloudinaryField('image', default='placeholder')
    saved = models.ManyToManyField(
        User, related_name="saved_recipes", default=None, blank=True)
    likes = models.ManyToManyField(
        User, related_name='recipe_likes', blank=True)
    saved_boolean = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    number_of_ratings = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    make_public = models.BooleanField(
        default=False,
        help_text='Check this box to allow your recipe to be published online.'
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()


# Comment Model
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='commenter')
    content = models.TextField(help_text="Remember to also rate the recipe"
                               "before submitting a comment.")
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.content} by {self.author}'

    def recipe_title(self):
        return self.recipe.title

    def recipe_rating(self):
        return self.recipe.rating

    def recipe_number_of_ratings(self):
        return self.recipe.number_of_ratings
