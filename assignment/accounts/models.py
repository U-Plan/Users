from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
