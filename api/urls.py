from django.conf.urls import url
from .views import (SettingsRetrieveUpdateAPIView)

urlpatterns = [
    url(r'^settings/?$',
        SettingsRetrieveUpdateAPIView.as_view())
]
