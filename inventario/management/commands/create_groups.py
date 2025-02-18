from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventario.models import Producto, Movimiento

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Crear grupo Administradores
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Crear grupo Empleados
        empleado_group, created = Group.objects.get_or_create(name='Empleados')
        empleado_permissions = Permission.objects.filter(content_type__model='movimiento')
        empleado_group.permissions.set(empleado_permissions)

        self.stdout.write(self.style.SUCCESS("Grupos creados con éxito."))
