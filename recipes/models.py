from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager


# Recipe post status for admin users
STATUS = ((0, "Draft"), (1, "Published"))

# Approval status options for recipes submitted by users who are not admin.
APPROVAL_STATUS = (
    ('0', 'Pending Approval'),
    ('1', 'Approved'),
    ('2', 'Rejected'),
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
    ingredients = models.TextField()
    preparation = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    approval_status = models.IntegerField(choices=APPROVAL_STATUS, default=0)
    tags = TaggableManager(blank=True)
    recipe_image = CloudinaryField('image', default='placeholder')
    likes = models.ManyToManyField(
        User, related_name='recipe_likes', blank=True)
    stars = models.ManyToManyField(
        User, related_name='recipe_stars', blank=True)
    
