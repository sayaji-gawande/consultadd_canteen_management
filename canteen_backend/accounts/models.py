from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, user_id, name, role, password=None, **extra_fields):
        if not user_id:
            raise ValueError("User ID is required")
        if not name:
            raise ValueError("Name is required")
        if not role:
            raise ValueError("Role is required")

        user = self.model(
            user_id=user_id,
            name=name,
            role=role,
            balance=extra_fields.get('balance', 0.0),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return f"{self.user_id} - {self.name} ({self.role})"
