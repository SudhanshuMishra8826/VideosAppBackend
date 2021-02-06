from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password):
        if not email:
            raise ValueError('Users must have a username')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            password=password,
            email=email,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    date_joined				= models.DateTimeField(verbose_name='date joined',default=timezone.now)
    last_login				= models.DateTimeField(verbose_name='last login', default=timezone.now)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
