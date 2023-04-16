from django.db import models
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    name = models.CharField(
        _("name"),
        max_length=120
    )
    email = models.EmailField(
        _("email"),
        max_length=120,
        unique=True
    )

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return self.name
