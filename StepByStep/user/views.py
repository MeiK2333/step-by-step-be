import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import GitHubUser
from source.models import Source, SourceUser
from source.serializers import SourceUserSerializer
from user.serializers import GitHubUserSerializer, GroupSerializer, UserSerializer


class LoginAPIView(APIView):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return Response(GitHubUserSerializer(request.user.github_user).data)
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        code = request.GET.get("code")

        if not code:
            return HttpResponseRedirect(
                f"https://github.com/login/oauth/authorize?client_id={client_id}"
            )

        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            json={"client_id": client_id, "client_secret": client_secret, "code": code},
        )
        access_token = resp.json().get("access_token")
        if not access_token:
            return Response(
                {"errmsg": "github token error"}, status=status.HTTP_403_FORBIDDEN
            )

        resp = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        username = resp.json().get("login")
        if not username:
            return Response(
                {"errmsg": "github token error"}, status=status.HTTP_403_FORBIDDEN
            )
        github_user = GitHubUser.objects.filter(username=username)
        if not github_user:
            user = User.objects.create_user(username=username)
            github_user = GitHubUser.objects.create(
                user=user,
                username=username,
                avatar_url=resp.json().get("avatar_url"),
                url=resp.json().get("url"),
                html_url=resp.json().get("html_url"),
            )
            github_user.save()
        else:
            github_user = github_user[0]
        user = github_user.user
        login(request, user)
        return Response(GitHubUserSerializer(request.user.github_user).data)


class LogoutAPIView(APIView):
    @staticmethod
    def get(request):
        logout(request)
        return Response({"success": True})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
