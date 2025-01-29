from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from core.models import Profile  # Importar el modelo personalizado

@receiver(post_save, sender=Profile)
def add_user_to_groups(sender, instance, created, **kwargs):
    if created:  # Solo se ejecuta al crear un nuevo usuario
        # Obtener o crear los grupos
        cliente_group, _ = Group.objects.get_or_create(name='Cliente')
        empresa_group, _ = Group.objects.get_or_create(name='Empresa')
        
        # Verificar si el usuario quiere registrarse como empresa
        if instance.is_empresa:  # Si is_empresa es True
            instance.groups.add(empresa_group)  # Agregar a ambos grupos
        else:  # Si is_empresa es False
            instance.groups.add(cliente_group)  # Agregar solo al grupo Cliente
