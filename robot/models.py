import requests
from aiopygismeteo import Gismeteo
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from robot.enums import LanguageChoices


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


class DeepLink(BaseModel):
    """Deep link model"""
    link = models.CharField(
        verbose_name=_("DeepLink name"),
        max_length=10,
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("Available variables: {userid}, {full_name}, {month_year}")
    )

    def __str__(self) -> str:
        return self.link

    class Meta:
        verbose_name = _("Deeplink")
        verbose_name_plural = _("Deep links")


def validate_gismeteo_token(value):
    """Validate token"""

    # If the token is not set, skip validation
    if not value:
        return

    # Making a request to the Gismeteo API
    url = "https://api.gismeteo.net/v2/weather/current/4956"
    headers = {
        "X-Gismeteo-Token": value,
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        raise ValidationError(
            _("Invalid Gismeteo token"),
            code="invalid",
            params={"value": value},
        )


async def validate_gismeteo_locality(value):
    """Validate the Gismeteo Locality"""
    gm = await Gismeteo().search.by_query(value)
    if not gm:
        raise ValidationError(
            _("Invalid Gismeteo locality"),
            code="invalid",
            params={"value": value},
        )


class GisMeteoWeather(BaseModel):
    """ Weather model from Gismeteo """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=150,
        unique=True,
    )

    token = models.CharField(
        verbose_name=_("Token"),
        validators=[validate_gismeteo_token],
        max_length=250,
        blank=True,
        null=True,
        help_text=_("If you don't have your own token, leave it blank")
    )

    locality = models.CharField(
        verbose_name=_("Locality"),
        max_length=250,
        validators=[validate_gismeteo_locality],
        help_text=_("City, District, Aeroport")
    )
    chat_id = models.PositiveBigIntegerField(
        verbose_name=_("Chat ID"),
        unique=True,
        blank=True,
        null=True,
    )
    language = models.CharField(
        verbose_name=_("Language"),
        max_length=6,
        default=LanguageChoices.UA,
        choices=LanguageChoices.choices,
    )
    message = models.TextField(
        verbose_name=_("Message"),
        blank=False,
        help_text=_("Additional text"),
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("Weather notification")
        verbose_name_plural = _("Weather notifications")
