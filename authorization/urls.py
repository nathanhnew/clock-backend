from django.conf.urls import url
from .views import (RegistrationAPIView,
                    LoginAPIView,
                    AccountRetrieveUpdateAPIView,
                    AccountRetrieveAPIView)

urlpatterns = [
    url(r'^register/?$', RegistrationAPIView.as_view()),
    url(r'^login/?$', LoginAPIView.as_view()),
    url(r'^account/?$', AccountRetrieveUpdateAPIView.as_view()),
    url(r'^check/?$', AccountRetrieveAPIView.as_view())
]
