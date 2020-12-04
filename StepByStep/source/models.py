from django.db import models


SOURCES = (("sdut", "sdut"), ("poj", "poj"))
RESULTS = (("ac", "Accepted"), ("wa", "WrongAnswer"))
LANGUAGES = (("c", "C"), ("cpp", "CPP"), ("py", "Python"))


class Source(models.Model):
    name = models.CharField(max_length=32, choices=SOURCES)

    def __str__(self):
        return self.name


class Problem(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class SourceUser(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    username = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Solution(models.Model):
    source_user = models.ForeignKey(SourceUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    result = models.CharField(max_length=32, choices=RESULTS)
    language = models.CharField(max_length=32, choices=LANGUAGES)
    time_used = models.IntegerField()
    memory_used = models.IntegerField()
    length = models.IntegerField()
    run_id = models.CharField(max_length=32)
    submitted_at = models.DateTimeField()
