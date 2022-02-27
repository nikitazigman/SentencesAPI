from django.db import models


class Content(models.Model):
    content = models.CharField(max_length=200)
