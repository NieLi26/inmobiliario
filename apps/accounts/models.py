from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class CustomUser(AbstractUser):
    class Tipos(models.TextChoices):
        SUPER = "SUP", "Super"
        ADMIN = "ADM", "Admin"
        AGENT = "AGE", "Agent"

    base_type = Tipos.SUPER

    tipo = models.CharField(max_length=3, choices=Tipos.choices,
                            default=Tipos.SUPER)
    rut = models.CharField(max_length=12, null=True)
    phone = models.CharField('Telefono', max_length=10, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.tipo = self.base_type

        return super().save(*args, **kwargs)
    

# Managers
class SuperManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs) \
                      .filter(tipo=CustomUser.Tipos.SUPER)


class AdminManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs) \
                      .filter(tipo=CustomUser.Tipos.ADMIN)
    

class AgentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs) \
                      .filter(tipo=CustomUser.Tipos.AGENT)


# Proxy Models
class Super(CustomUser):
    base_type = CustomUser.Tipos.SUPER
    objects = SuperManager()

    class Meta:
        proxy = True


class Admin(CustomUser):
    base_type = CustomUser.Tipos.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True


class Agent(CustomUser):
    base_type = CustomUser.Tipos.AGENT
    objects = AgentManager()

    class Meta:
        proxy = True


# Profiles
class SuperProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class AgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    start_contract = models.DateField('Inicio Contrato')
    end_contract = models.DateField('Termino Contrato')
    zone = models.TextField('Zona')

    def __str__(self) -> str:
        return self.user.username
