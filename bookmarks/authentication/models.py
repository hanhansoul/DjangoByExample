from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
