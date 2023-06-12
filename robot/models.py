from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class TelegramUser(BaseModel):
    """ User model for Telegram users """
    user = models.OneToOneField(
        verbose_name=_("User"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="telegram_user",
    )
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=25,
        default="None",
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=50,
        null=True,
        blank=True,
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=32,
        blank=True,
        null=True,
    )
    userid = models.BigIntegerField(
        verbose_name=_("Userid"),
        unique=True,
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
    birthday = models.DateField(
        verbose_name=_("Date of Birth"),
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
    is_blocked_bot = models.BooleanField(
        verbose_name=_("Is blocked"),
        default=False,
    )
    is_banned = models.BooleanField(
        verbose_name=_("Is banned"),
        default=False,
    )
    is_admin = models.BooleanField(
        verbose_name=_("Is admin"),
        default=False,
    )
    is_moderator = models.BooleanField(
        verbose_name=_("Is moderator"),
        default=False,
    )

    def __str__(self) -> str:
        return f"@{self.username}" if self.username is not None else f"{self.userid}"

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
        self.save()

    @admin.display(description=_("Full name"))
    def full_name(self):
        return f"{self.first_name} {self.last_name}" \
            if self.last_name else f"{self.first_name}"

    class Meta:
        verbose_name = _("Telegram user")
        verbose_name_plural = _("Telegram users")
