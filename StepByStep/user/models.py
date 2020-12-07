from django.db import models


class GitHubUser(models.Model):
    user = models.OneToOneField(
        "auth.user", related_name="github_user", on_delete=models.CASCADE
    )
    username = models.CharField(max_length=128)
    avatar_url = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    html_url = models.CharField(max_length=256)
