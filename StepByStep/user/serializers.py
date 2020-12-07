from django.contrib.auth.models import Group, User
from rest_framework import serializers
from user.models import GitHubUser
from source.serializers import SourceUserSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    source_users = SourceUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["url", "username", "email", "groups", "source_users"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class GitHubUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitHubUser
        fields = ["username", "avatar_url", "url", "html_url"]
