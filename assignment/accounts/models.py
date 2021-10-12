from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from random import randint
import datetime
from django.utils import timezone
from model_utils.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, name, phone, password=None):
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            name=name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, name, phone, password=None):
        user = self.create_user(
            email, nickname, name, phone, password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, null=False,
                              blank=False, unique=True, validators=[EmailValidator()])
    nickname = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=11, null=False,
                             unique=True, validators=[PhoneValidator()])

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname


class EmailValidator(RegexValidator):
    regex = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
    message = 'Invalid Email'


class PhoneValidator(RegexValidator):
    regex = r'^[0-9]{9,14}$'
    message = 'Invalid Phone'


class SmsAuthentication(TimeStampedModel):
    phone = models.CharField(
        max_length=11, primary_key=True, validators=[PhoneValidator()])
    auth_number = models.CharField(max_length=4)
    auth_key = models.CharField(max_length=4)

    class Meta:
        db_table = 'sms_auth'

    def save(self, *args, **kwargs):
        self.auth_number = '0000'  # test auth number
        self.auth_key = randint(1000, 9999)  # anything hash id
        # need send sms function
        super().save(*args, **kwargs)

    @classmethod
    def check_sms_auth(cls, check_phone, check_number):
        time_limit = timezone.now() - datetime.timedelta(minutes=3)
        try:
            result = cls.objects.get(
                phone=check_phone,
                auth_number=check_number,
                modified__gte=time_limit
            )
            if result:
                return result.auth_key
        except cls.DoesNotExist:
            return False

    @classmethod
    def check_auth_key(cls, check_phone, check_key):
        time_limit = timezone.now() - datetime.timedelta(minutes=10)
        result = cls.objects.filter(
            phone=check_phone,
            auth_key=check_key,
            modified__gte=time_limit
        )
        if result:
            return True
        return False
