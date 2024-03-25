from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager


# Recipe post status for admin users
STATUS = ((0, "Draft"), (1, "Published"))

CATEGORY = (
    (0, "Popular Pancakes"),
    (1, "Healthy Pancakes for Kids"),
    (3, "Vegan Pancakes")
)



class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resources_added")
    servings = models.IntegerField(
        help_text='Please enter the number of portions that result from your recipe.'
    )
    cooking_duration = models.IntegerField(
        help_text = 'Please enter how many minutes is required for the preparation of your recipe')
    ingredients = models.JSONField(null=False)
    preparation = models.JSONField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.IntegerField(choices=CATEGORY, default=0)
    recipe_image = CloudinaryField('image', default='placeholder')
    likes = models.ManyToManyField(
        User, related_name='recipe_likes', blank=True)


    class Meta:
        ordering = ['-created_on']

    
    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()
    
