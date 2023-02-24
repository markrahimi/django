from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    profile = models.ImageField(verbose_name='پروفایل', upload_to='media/images/profile/',default='static/images/default/default-profile.jpg')
    mobile = models.CharField(verbose_name='شماره موبایل',max_length=11, blank=False, db_index=True, null=False)
    nationalcode = models.CharField(verbose_name='کد ملی',max_length=10, blank=True, db_index=True, null=True)
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    address = models.TextField(verbose_name='آدرس', null=True)
    bio = models.TextField(verbose_name='بیوگرافی', null=True)
    SEX = (
        ('male', 'مرد'),
        ('female', 'زن')
    )
    sex = models.CharField(verbose_name='جنسیت', max_length=6, choices=SEX, null=True)
    birthday = models.DateField(verbose_name='تاریخ تولد',null=True,default=None)
    state = models.CharField(verbose_name='استان', max_length=120, null=True)
    city = models.CharField(verbose_name='شهر', max_length=120, null=True)
    

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username
