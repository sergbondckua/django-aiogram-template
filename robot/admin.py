from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common.admin import BaseAdmin
from robot.models import TelegramUser, DeepLink, GisMeteoWeather


@admin.register(TelegramUser)
class TelegramUserAdmin(BaseAdmin):
    list_display = (
        "userid",
        "full_name",
        "username",
        "phone",
        "birthday",
        "user",

    )
    list_display_links = ("userid",)
    empty_value_display = _("-empty-")
    readonly_fields = ("userid", "username",) + BaseAdmin.readonly_fields
    fieldsets = (
                    (
                        _("Registration details"),
                        {
                            "fields": (
                                "user",
                                "first_name",
                                "last_name",
                                "birthday",
                                "userid",
                                "username",
                                "phone",
                                "language_code",
                            )
                        },
                    ),
                    (
                        _("Status and Role"),
                        {
                            "fields": (
                                (
                                    "is_admin",
                                    "is_moderator",
                                    "is_blocked_bot",
                                    "is_banned",
                                ),
                            )
                        },
                    )
                ) + BaseAdmin.fieldsets


@admin.register(DeepLink)
class DeepLinkAdmin(BaseAdmin):
    list_display = ("id", "link",)
    list_display_links = ("link",)
    fieldsets = (
                    (
                        _("Set info"),
                        {
                            "fields": (
                                "link",
                                "message",
                            )
                        },
                    ),
                ) + BaseAdmin.fieldsets


@admin.register(GisMeteoWeather)
class GisMeteoWeatherAdmin(BaseAdmin):
    list_display = ("title", "chat_id", "locality_code")
    list_display_links = ("title",)
    fieldsets = (
                    (
                        _("Set info"),
                        {
                            "fields": (
                                "title",
                                "token",
                                "chat_id",
                                "locality_code",
                                "language",
                                "message",
                            )
                        },
                    ),
                ) + BaseAdmin.fieldsets
