from django.db import models


class Contact(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"title: {self.title}\ncontent: {self.content}"

class ReachOut(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"