from django.contrib.auth.models import Group, User
from rest_framework import serializers
from user.models import GitHubUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class GitHubUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitHubUser
        fields = ["username", "avatar_url", "url", "html_url"]
