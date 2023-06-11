from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from robot.models import TelegramUser

from common.admin import BaseAdmin


@admin.register(TelegramUser)
class TelegramUserAdmin(BaseAdmin):
    list_display = (
        "userid",
        "user",
        "phone",

    )
    list_display_links = ("user", "userid",)
    readonly_fields = ("userid", "avatar",) + BaseAdmin.readonly_fields
    fieldsets = (
                    (
                        _("Registration details"),
                        {
                            "fields": (
                                "user",
                                "userid",
                                "phone",
                                "avatar",
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
