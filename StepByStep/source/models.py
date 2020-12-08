from django.db import models

SOURCES = (("sdut", "sdut"), ("poj", "poj"))
RESULTS = (("ac", "Accepted"), ("wa", "WrongAnswer"))
LANGUAGES = (("c", "C"), ("cpp", "CPP"), ("py", "Python"), ("java", "Java"), ("c#", "C#"))


class Source(models.Model):
    name = models.CharField(max_length=32, choices=SOURCES)

    def __str__(self):
        return self.name


class Problem(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    problem_id = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class SourceUser(models.Model):
    user = models.ForeignKey("auth.user", related_name="source_users", on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    username = models.CharField(max_length=128)
    nickname = models.CharField(max_length=128)

    last_solution_id = models.IntegerField(default=0)

    class Meta:
        unique_together = ('source', 'user')

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

    class Meta:
        unique_together = ('source_user', 'run_id')
