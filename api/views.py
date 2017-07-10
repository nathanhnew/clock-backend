# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from api.models import AccountSettings
from api.serializers import (AccountSettingsSerializer, ClockSerializer)
from rest_framework import status
from .exceptions import SettingsDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (RetrieveUpdateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from api.renderers import (SettingsJSONRenderer)
from .models import Clock


class SettingsRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (SettingsJSONRenderer,)
    serializer_class = AccountSettingsSerializer

    def retrieve(self, request, *args, **kwargs):
        # Try to retrieve requested settings and throw exception if not fourn
        try:
            settings = AccountSettings.objects.select_related('owner').get(
                owner__email=request.user.email
            )
        except AccountSettings.DoesNotExist:
            raise SettingsDoesNotExist

        serializer = self.serializer_class(settings)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            settings = AccountSettings.objects.select_related('owner')\
                .get(owner__email=request.user.email)
        except AccountSettings.DoesNotExist:
            raise SettingsDoesNotExist

        serializer = self.serializer_class(request.user,
                                           data=request.data.get('settings'),
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
