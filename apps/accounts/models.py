from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    rut = models.CharField(max_length=12, null=True)
    phone = models.CharField('Telefono', max_length=10, null=True)

#     def has_paid(self, current_day=datetime.date.today()):
#         if not self.paid_until:
#             return False
#         return current_day < self.paid_until


# class Pricing(TimeStampedModel):

#     class Currencys(models.TextChoices):
#         UF = 'uf', 'UF'
#         USD = 'usd', 'USD'
#         CLP = 'clp', 'CLP'

#     '''Model definition for Pricing.'''
#     name = models.CharField('Nombre', max_length=50)
#     slug = models.SlugField(unique=True)
#     # price = models.DecimalField('Precio', decimal_places=1, max_digits=5)
#     price = models.PositiveIntegerField('Precio')
#     allowed_property = models.IntegerField()
#     currency = models.CharField(
#         'Divisa',
#         max_length=3,
#         choices=Currencys.choices
#     )

#     class Meta:
#         '''Meta definition for Pricing.'''

#         verbose_name = 'Pricing'
#         verbose_name_plural = 'Pricings'

#     def __str__(self):
#         return self.name

