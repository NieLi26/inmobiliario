from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Agent, Admin

User = get_user_model()

@receiver(post_save, sender=Agent)
def agent_post_save(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Agente')
        instance.groups.add(group)
        # if instance.tipo == "AGE":
        #     group, _ = Group.objects.get_or_create(name='Agente')
        # elif instance.tipo == "ADM":
        #     group, _ = Group.objects.get_or_create(name='Administrador')
        # instance.groups.add(group)

@receiver(post_save, sender=Admin)
def admin_post_save(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Administrador')
        instance.groups.add(group)