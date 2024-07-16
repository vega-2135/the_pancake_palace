from django.db import models


class Contact(models.Model):
    """
    Model representing the contact section content.

    This model contains fields to describe the content of the contact section
    of a website, including the title and content.

    Attributes:
    -----------
    title : str
        The title of the contact section.
    content : str
        The content of the contact section.

    Methods:
    --------
    __str__():
        Returns the string representation of the contact section, which is the
        title.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """
        Returns the title of the contact section.
        """
        return self.title


class ReachOut(models.Model):
    """
    Model representing a message sent through the reach out form.

    This model contains fields to describe a message sent by a user, including
    the sender's name, email, message content, and a flag indicating if the
    message has been read.

    Attributes:
    -----------
    name : str
        The name of the sender.
    email : EmailField
        The email address of the sender.
    message : str
        The content of the message.
    read : bool
        A boolean flag indicating if the message has been read. Defaults to
        False.

    Methods:
    --------
    __str__():
        Returns the string representation of the message, including the
        sender's name.
    """

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the message sent through the reach out form, including the
        sender's name.
        """
        return f"Message from {self.name}"
