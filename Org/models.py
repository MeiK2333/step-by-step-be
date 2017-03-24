from django.db import models

class Org(models.Model):
    name = models.CharField(max_length = 30)
    shortName = models.CharField(max_length = 30)