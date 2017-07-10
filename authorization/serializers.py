from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Account
from api.models import AccountSettings, City, Clock
from api.serializers import AccountSettingsSerializer, ClockSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    '''Serializer for registration requests to create new account'''

    # Ensure passowrds are 6 chars long and no more than 128.
    # Also ensure cannot be read by client
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True
    )

    # Client should not be able to send token. Make token read only
    token = serializers.CharField(max_length=255, read_only=True)
    settings = AccountSettingsSerializer(required=False)

    class Meta:
        model = Account

        # Fields to be included on request or response
        fields = ('email', 'username', 'password', 'token', 'settings')

    def create(self, validated_data):
        # use create_user method to create new user
        settings = validated_data.pop('settings', None)
        print(validated_data)

        account = Account.objects.create_user(**validated_data)

        if settings is not None:
            AccountSettings.objects.create(owner=account, **settings)

        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    settings = AccountSettingsSerializer(required=False)
    clock = ClockSerializer(required=False, many=True)

    class Meta:
        fields = ('email', 'username', 'password', 'token',
                  'settings', 'clock')

    def validate(self, data):
        # This method is where we ensure the curent isntance is valid
        # Meaning validating the email and password matches database
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise exception if email not provided
        if email is None:
            raise serializers.ValidationError(
                'An email is required for login.'
            )

        # Raise exception if password not provided
        if password is None:
            raise serializers.ValidationError(
                'A password is required for login.'
            )

        # Use Django's 'authenticate' method for chekcing
        # Email/password combo
        user = authenticate(username=email, password=password)

        # If no user found, authenticate return None and we will raise erro
        if user is None:
            raise serializers.ValidationError(
                'Incorrect Username and Password'
            )

        # Check to make sure user hasn't deactivated account
        if not user.is_active:
            raise serializers.ValidationError(
                'This account is deactivated.'
            )

        # This method should return a dict of validated data to be
        # used in the 'create' and 'update' methods
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'settings': user.settings,
            'clock': user.clock
        }


class AccountSerializer(serializers.ModelSerializer):
    ''' Handles serialization and deserialization of Account objects '''

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True
    )

    # Settings information handled. Account will never expose settings info
    # So set write-only
    settings = AccountSettingsSerializer(required=False)
    clock = ClockSerializer(many=True, required=False)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'token',
                  'settings', 'clock')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        '''Performs account update'''

        # Passwords should not be handled with setattr.
        # Django provides a hashing and salting function
        password = validated_data.pop('password', None)
        # Also remove the settings data
        validated_data.pop('settings', None)
        # And remove the clock data
        validated_data.pop('clock', None)

        for (key, value) in validated_data.items():
            # Remaining keys can use setattr
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        # Save changes to the database
        instance.save()

        return instance
