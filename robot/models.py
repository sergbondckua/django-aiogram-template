from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class TelegramUser(BaseModel):
    user = models.OneToOneField(
        verbose_name=_("User"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="telegram_user",
    )
    avatar = models.CharField(
        verbose_name=_("Avatar"),
        max_length=255,
        blank=True,
        null=True,
    )
    userid = models.BigIntegerField(
        verbose_name=_("Userid"),
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_("Phone number in the format: '+380999999'. "
                  "Up to 15 digits allowed."),
    )
    phone = models.CharField(
        verbose_name=_("Phone number"),
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
    )
    language_code = models.CharField(
        verbose_name=_("Language code"),
        max_length=8,
        null=True,
        blank=True,
        help_text=_("Telegram client's lang"),
    )
    is_blocked_bot = models.BooleanField(verbose_name=_("Is blocked"), default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.userid)

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
        self.save()
