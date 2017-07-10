from .serializers import (RegistrationSerializer,
                          LoginSerializer,
                          AccountSerializer)
from api.serializers import (AccountSettingsSerializer,
                             CitySerializer,
                             ClockSerializer)
from rest_framework import status
# from api.permissions import IsStaffOrTarget
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (RetrieveUpdateDestroyAPIView,
                                     RetrieveAPIView)
from api.renderers import (AccountJSONRenderer)
from api.models import Clock, City
from .models import Account


class RegistrationAPIView(APIView):

    # Allow any user (authenticated or not) to hit this endpoint
    permission_classes = (AllowAny,)
    renderer_classes = (AccountJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):

    # Allow anyone to hit the endpoint to login
    permission_classes = (AllowAny,)
    renderer_classes = (AccountJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Call serialzer to validate data. No need to save anything
        # Just verify everything is correct
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # Return user data
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AccountJSONRenderer,)
    serializer_class = AccountSerializer

    city_serializer_class = CitySerializer()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Update any user information
        user_data = request.data.get('account', {})
        serializer = self.serializer_class(
            request.user, data=user_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update any settings information
        settings_data = request.data.get('settings', None)
        if settings_data is not None:
            settings_serializer = AccountSettingsSerializer(
                request.user, data=settings_data, partial=True
            )
            settings_serializer.is_valid(raise_exception=True)
            settings_serializer.save()

        # Update any clock information
        clock_data = request.data.get('clock', None)
        if clock_data is not None:
            if isinstance(clock_data, list):
                for clock in clock_data:
                    city_data = clock.pop('city', None)
                    try:
                        clockObj = Clock.objects.get(owner=request.user,
                                                     arrIndex=clock.get
                                                     ('arrIndex', None))
                    except Clock.DoesNotExist:
                        clockObj = Clock(owner=request.user,
                                         arrIndex=clock.get('arrIndex', None),
                                         city=City(),
                                         fullDay=clock.get('fullDay', None))

                    if city_data is not None:
                        city, created = CitySerializer().getCity(request.user,
                                                                 data=city_data)
                        clockObj.city = city

                    clockObj.fullDay = clock.get('fullDay', clockObj.fullDay)

                    clockObj.save()
            else:
                clock = clock_data
                city_data = clock.pop('city', None)
                try:
                    clockObj = Clock.objects.get(owner=request.user,
                                                 arrIndex=clock.get
                                                 ('arrIndex', None))
                except Clock.DoesNotExist:
                    clockObj = Clock(owner=request.user,
                                     arrIndex=clock.get('arrIndex', None),
                                     city=City(),
                                     fullDay=clock.get('fullDay', None))

                if city_data is not None:
                    city, created = CitySerializer().getCity(request.user,
                                                             data=city_data)
                    clockObj.city = city

                clockObj.fullDay = clock.get('fullDay', clockObj.fullDay)

                clockObj.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        clock_data = request.data.get('clock')
        if isinstance(clock_data, list):
            for clock_datum in clock_data:
                clockId = clock_datum.get('clock_id', None)
                clock = Clock.objects.get(clock_id=clockId)
                clock.delete()
        else:
            clockId = clock_data.get('clock_id', None)
            clock = Clock.objects.get(clock_id=clockId)
            clock.delete()

        return Response(request.data, status=status.HTTP_204_NO_CONTENT)


class AccountRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        email = request.GET['email']

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response(data={'exists': False})
        else:
            return Response(data={'exists': True})
