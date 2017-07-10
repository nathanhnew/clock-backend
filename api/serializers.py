from rest_framework import serializers
from .models import AccountSettings, Clock, City


class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = ('theme', 'alerts', 'fullDay', 'metric')

    def update(self, instance, validated_data):
        settings = instance.settings

        settings.theme = validated_data.get(
            'theme',
            settings.theme
        )
        settings.alerts = validated_data.get(
            'alerts',
            settings.alerts
        )
        settings.fullDay = validated_data.get(
            'fullDay',
            settings.fullDay
        )
        settings.metric = validated_data.get(
            'metric',
            settings.metric
        )

        instance.settings.save()

        return instance.settings


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('name', 'country', 'lat', 'lon', 'tz')

    def getCity(self, instance, data):
        city, created = City.objects\
            .get_or_create(place_id=data['place_id'],
                           defaults={'name': data.get('name', None),
                                     'country': data.get('country', None),
                                     'lat': data.get('lat', None),
                                     'lon': data.get('lon', None),
                                     'tz': data.get('tz', None)})
        return city, created


class ClockSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Clock
        fields = ('city', 'fullDay', 'arrIndex', 'clock_id')
        # read_only_fields = ('owner',)
