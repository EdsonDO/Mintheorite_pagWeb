from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Perfil

@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=Usuario)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except Perfil.DoesNotExist:
        Perfil.objects.create(usuario=instance)
