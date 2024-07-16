from django.db import models


class About(models.Model):
    """
    Model representing the about section content.

    This model contains fields to describe the content of the about section
    of a website, including the title, content, and the last updated timestamp.

    Attributes:
    -----------
    title : str
        The title of the about section.
    content : str
        The content of the about section.
    updated_on : datetime
        The date and time when the about section was last updated.

    Methods:
    --------
    __str__():
        Returns the string representation of the about section, which is the
        title.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the about section,
        which is the title.
        """
        return self.title
