from django.db import models
from django.utils.translation import gettext_lazy as _


class LanguageChoices(models.TextChoices):
    """ Language choices for Weather """

    EN = "en", _("English")
    UA = "ua", _("Ukrainian")
    RU = "ru", _("Russian")
