from django.db import models

class Step(models.Model):
    title = models.CharField(max_length = 60)
    userCount = models.IntegerField()
    problemCount = models.IntegerField()
    allAcCount = models.IntegerField()
    orgId = models.IntegerField()
    source = models.CharField(max_length = 30)