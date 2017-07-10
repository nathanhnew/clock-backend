from django.db import models

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from api.models import AccountSettings
import jwt
from datetime import datetime, timedelta


class AccountManager(BaseUserManager):
    """
    Manager class for custom user to be used by Django

    Will override the default create_user function that will
    be used to create new 'user' objects
    """

    def create_user(self, username, email, password=None):
        '''Create and return a "User" with an email, username, and pw'''
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        ''' Create and return user with admin permissions '''

        if password is None:
            raise TypeError('Administrators must have password')

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ''' Each user must have human-readable unique ID to represent
    in the UI. Indexing the username column improves lookup speed
    '''
    username = models.CharField(db_index=True, max_length=255, unique=True)

    ''' Also need a way to contact user and have a way to identify at login.
    will use email for login purposes as write_only_fields
    '''
    email = models.EmailField(db_index=True, unique=True)

    ''' Offer users a way to deactivate account instead of deleting it
    I love keeping peoples data :)
    '''
    is_active = models.BooleanField(default=True)

    ''' The is_staff flag is expected by django to determin who can
    and cannot log into the django admin site. False by default
    '''
    is_staff = models.BooleanField(default=False)

    ''' Timestamp to show account creation
    '''
    created_at = models.DateTimeField(auto_now_add=True)

    ''' Timestamp to show last update
    '''
    updated_at = models.DateTimeField(auto_now=True)

    ''' DJANGO REQUIRED FIELDS

    the USERNAME_FIELD property tells us which field used to login
    '''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    ''' tells Django to use userManager class to Define
    objects of this Type
    '''
    objects = AccountManager()

    def __str__(self):
        ''' Returns string representation of 'user' '''
        return self.email

    @property
    def token(self):
        ''' Allows call of user.token insead of user.generate_jwt_token()
        '''

        return self._generate_jwt_token()

    def get_full_name(self):
        ''' Method required by django for things like emails
        '''
        return self.username

    def get_short_name(self):
        ''' Method required by django for stuff like emails
        '''
        return self.username

    def _generate_jwt_token(self):
        ''' Generate JWT that stores user ID and an expiry date
        set 5 days in the future
        '''

        dt = datetime.now() + timedelta(days=5)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
