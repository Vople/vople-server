from django.contrib.auth.models import AbstractUser
from django.db.models import TextField, CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-choice', 'Non-Choice')
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    bio = TextField(null=True)
    gender = CharField(max_length=80, choices=GENDER_CHOICES, null=True)

    def __str__(self):
        return str(self.username)
