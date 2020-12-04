from django.conf import settings
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from user.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

# TODO: 通过 Github 登录
print('client id', settings.CLIENT_ID)
print('client secret', settings.CLIENT_SECRET)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
