from django.contrib.auth import authenticate, login
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status, mixins
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from cf_core.api.views import PageNumberPaginator
from .serializers import (
    ProfileSerializer, UserChangePasswordSerializer,
    ShareRegistrationSerializer, ProfileListSerializer
)
from cf_users.models import Profile


class UserProfileViewSet(ModelViewSet):
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)

    def get_object(self):
        return self.request.user.profile

    @list_route(methods=['post'],
                serializer_class=UserChangePasswordSerializer)
    @transaction.atomic
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data, user=user)
        serializer.is_valid(raise_exception=True)
        serializer.update()
        user = authenticate(request, username=user.email,
                            password=serializer.validated_data)
        login(request, user)
        return Response({'detail': _("Your password successfully changed")})


class PublishedProfileVewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPaginator
    serializer_class = ProfileListSerializer
    queryset = Profile.objects.filter(
        is_available=True,
        base_type=Profile.TYPE_CHOICES.NCO
    ).order_by('title')
