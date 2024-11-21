from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field is required')

        # Format the phone number
        formatted_phone = self.format_phone_number(phone)

        user = self.model(phone=formatted_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

    def format_phone_number(self, phone):
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, phone))

        # Ensure the number starts with +998
        if not digits.startswith('998'):
            digits = '998' + digits

        # Format the number
        return f"+{digits[:3]} {digits[3:5]} {digits[5:8]}-{digits[8:10]}-{digits[10:]}"


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('admin', 'Admin'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+998 \d{2} \d{3}-\d{2}-\d{2}$',
        message="Phone number must be entered in the format: '+998 XX XXX-XX-XX'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=19, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        # Format the phone number before saving
        self.phone = UserManager.format_phone_number(self, self.phone)
        super().save(*args, **kwargs)