from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """Model definition for BaseModel."""

    # TODO: Define fields here
    state = models.BooleanField('Estado', default=True)
    created = models.DateField('Fecha de Creación', auto_now_add=True)
    modified = models.DateField('Fecha de Modificaión', auto_now=True)

    class Meta:
        """Meta definition for BaseModel."""
        abstract = True
