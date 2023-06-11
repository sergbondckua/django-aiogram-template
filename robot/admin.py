from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "userid",
    )
    list_display_links = ("user",)
    readonly_fields = ("userid",)
    fields = (
        "user",
        "language_code",
        (
            "is_admin",
            "is_blocked_bot",
            "is_moderator",
            "is_banned",
        ),
    )
