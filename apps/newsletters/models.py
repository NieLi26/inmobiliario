from django.db import models
from django.urls import reverse
# Create your models here.

class TimeStampedModel(models.Model):
    '''Model definition for Base.'''
    created = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    modified = models.DateTimeField('Fecha de Actualización', auto_now=True)

    class Meta:
        '''Meta definition for Base.'''

        abstract = True

class NewsletterUser(TimeStampedModel):
    """Model definition for NewsletterUser."""

    # TODO: Define fields here
    email = models.EmailField('Correo', null=False, blank=False, unique=True)

    class Meta:
        """Meta definition for NewsletterUser."""

        verbose_name = 'NewsletterUser'
        verbose_name_plural = 'NewsletterUsers'

    def __str__(self):
        """Unicode representation of NewsletterUser."""
        return str(self.email)

class Newsletter(TimeStampedModel):
    """Model definition for Newsletter."""

    EMAIL_STATUS_CHOICES=(
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )

    class Status(models.TextChoices):
        DRAFT = 'dr', 'Borrador'
        PUBLISHED = 'pu', 'Publicado'

    # TODO: Define fields here
    name = models.CharField('Nombre', max_length=250)
    subject = models.CharField('Asunto', max_length=250)
    body = models.TextField(blank=True)
    email = models.ManyToManyField(NewsletterUser)
    status = models.CharField('Status', max_length=2, choices=Status.choices)

    class Meta:
        """Meta definition for Newsletter."""

        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        ordering = ('-created',)

    def __str__(self):
        """Unicode representation of Newsletter."""
        return self.name

    # def get_absolute_url(self):
    #     return reverse('dashboard:detail,', args=[str(self.id)])