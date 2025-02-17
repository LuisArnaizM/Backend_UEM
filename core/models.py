from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Se cambia el related_name para evitar conflicto
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Se cambia el related_name para evitar conflicto
        blank=True
    )
class Preference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="preferences")
    favorite_genre = models.CharField(max_length=100)
    notifications = models.BooleanField(default=True)
