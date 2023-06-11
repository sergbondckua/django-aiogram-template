from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _

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
    userid = models.BigIntegerField(
        verbose_name=_("Userid"),
    )
    language_code = models.CharField(
        verbose_name=_("Language code"),
        max_length=8,
        null=True,
        blank=True,
        help_text="Telegram client's lang",
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
