from autoslug import AutoSlugField
from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import (  # noqa: F401
    FileExtensionValidator,
    MinValueValidator,
)
from django.db import models
from django.forms import ValidationError

# Recipe post status for admin users
STATUS = ((0, "Draft"), (1, "Published"))

CATEGORY = (
    (0, "Popular Pancakes"),
    (1, "Pancakes for Kids"),
    (2, "Vegan Pancakes"),
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 1.2 * 1024 * 1024
VALID_FILE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def file_validation(file):
    if isinstance(file, CloudinaryImage):
        if file.metadata["bytes"] > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 1.2MB.")
        if file.format.lower() not in VALID_FILE_EXTENSIONS:
            raise ValidationError(
                f"File should be of type: {VALID_FILE_EXTENSIONS}"
            )


# Recipe Model
class Recipe(models.Model):
    """
    Model representing a recipe.

    This model contains all the necessary fields to describe a recipe,
    including title, author, servings, cooking duration, ingredients,
    preparation steps, and additional metadata like creation and update
    timestamps, status, category, image, likes, and ratings.

    Attributes:
    -----------
    title : str
        The title of the recipe. Must be unique.
    slug : str
        A unique slug automatically generated from the title.
    author : ForeignKey
        The user who created the recipe.
    servings : int
        The number of portions the recipe yields.
    cooking_duration : int
        The cooking duration in minutes.
    ingredients : str
        The ingredients required for the recipe.
    preparation : str
        The preparation steps for the recipe.
    created_on : datetime
        The date and time when the recipe was created.
    updated_on : datetime
        The date and time when the recipe was last updated.
    status : int
        The publication status of the recipe.
    category : int
        The category of the recipe.
    recipe_image : CloudinaryField
        The image of the recipe.
    saved : ManyToManyField
        Users who have saved the recipe.
    likes : ManyToManyField
        Users who have liked the recipe.
    saved_boolean : bool
        Boolean flag indicating if the recipe has been saved.
    rating : int
        The rating of the recipe.
    number_of_ratings : int
        The number of ratings the recipe has received.
    approved : bool
        Boolean flag indicating if the recipe is approved.
    make_public : bool
        Boolean flag indicating if the recipe should be published online.

    Methods:
    --------
    __str__():
        Returns the string representation of the recipe.
    likes_count():
        Returns the count of likes for the recipe.
    """

    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resources_added"
    )
    servings = models.IntegerField(
        help_text="Please enter the number of portions that result"
        "from your recipe.",
        validators=[MinValueValidator(1)],
    )
    cooking_duration = models.IntegerField(
        help_text="Please enter how many minutes is required for"
        "the preparation of your recipe",
        validators=[MinValueValidator(1)],
    )
    ingredients = models.TextField()
    preparation = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.IntegerField(choices=CATEGORY, default=0)
    recipe_image = CloudinaryField(
        null=True,
        validators=[file_validation],
    )
    saved = models.ManyToManyField(
        User, related_name="saved_recipes", default=None, blank=True
    )
    likes = models.ManyToManyField(
        User, related_name="recipe_likes", blank=True
    )
    rating = models.IntegerField(default=0)
    number_of_ratings = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    make_public = models.BooleanField(
        default=False,
        help_text="Check this box to allow your recipe to"
        "be published online.",
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns the string representation of the recipe, which is the title.
        """
        return self.title

    def likes_count(self):
        """
        Returns the count of likes for the recipe.
        """
        return self.likes.count()


# Comment Model
class Comment(models.Model):
    """
    Model representing a comment on a recipe.

    This model contains fields to describe a comment made by a user on a
    recipe,including the content of the comment, the user who made the comment,
    the recipe being commented on, and metadata like creation time, approval
    status and likes.

    Attributes:
    -----------
    recipe : ForeignKey
        The recipe that the comment is associated with.
    author : ForeignKey
        The user who made the comment.
    content : str
        The content of the comment.
    likes : ManyToManyField
        Users who have liked the comment.
    created_on : datetime
        The date and time when the comment was created.
    approved : bool
        Boolean flag indicating if the comment is approved.

    Methods:
    --------
    __str__():
        Returns the string representation of the comment.
    recipe_title():
        Returns the title of the recipe associated with the comment.
    recipe_rating():
        Returns the rating of the recipe associated with the comment.
    recipe_number_of_ratings():
        Returns the number of ratings of the recipe associated with the
        comment.
    """

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    content = models.TextField()
    likes = models.ManyToManyField(
        User, related_name="comment_likes", blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        """
        Returns the string representation of the comment, including its content
        and the author.
        """
        return f"Comment {self.content} by {self.author}"

    def recipe_title(self):
        """
        Returns the title of the recipe associated with the comment.
        """
        return self.recipe.title

    def recipe_rating(self):
        """
        Returns the rating of the recipe associated with the comment.
        """
        return self.recipe.rating

    def recipe_number_of_ratings(self):
        """
        Returns the number of ratings of the recipe associated with the
        comment.
        """
        return self.recipe.number_of_ratings
