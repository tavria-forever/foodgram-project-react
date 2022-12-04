from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly)
from users.models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import UserPermissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={
            'user': request.user
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
