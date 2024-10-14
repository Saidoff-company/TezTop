import datetime
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from accounts.managers import CustomUserManager


class User(AbstractUser, BaseModel):
    USER_ROLE = (
        ('WORKER', 'WORKER'),
        ('COMPANY', 'COMPANY')
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=250)
    user_role = models.CharField(max_length=250, choices=USER_ROLE)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('foydalanuvchi')
        verbose_name_plural = _('foydalanuvchilar')

    def create_verify_code(self):
        code = ''.join([str(random.randint(0, 100) % 10) for _ in range(5)])
        Confirmation.objects.create(
            user=self,
            code=code,
            type=Confirmation.Type.PHONE,
            expires=timezone.now() + datetime.timedelta(minutes=2)
        )
        return code


class Category(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('soha')
        verbose_name_plural = _('sohalar')


class Company(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=250)
    company_employees = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='companies')
    admin_name = models.CharField(max_length=250)
    admin_phone_number = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = _('kompaniya')
        verbose_name_plural = _('kompaniyalar')

    def create_verify_code(self):
        code = ''.join([str(random.randint(0, 100) % 10) for _ in range(5)])
        Confirmation.objects.create(
            company=self,
            code=code,
            type=Confirmation.Type.EMAIL,
            expires=timezone.now() + datetime.timedelta(minutes=5)
        )
        return code


class Confirmation(BaseModel):
    class Type(models.TextChoices):
        PHONE = 'PHONE', _('phone')
        EMAIL = 'EMAIL', _('email')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmations', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='confirmations', null=True, blank=True)
    code = models.CharField(max_length=5)
    type = models.CharField(max_length=250, choices=Type.choices)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'Code: {self.code}, code type: {self.type}'

    class Meta:
        verbose_name = _('confirmation')
        verbose_name_plural = _('confirmations')



