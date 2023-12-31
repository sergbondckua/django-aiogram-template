from aiogram.utils.markdown import text, hbold, quote_html
from loader import _


def c_get_hello(name: str) -> str:
    msg = text(
        text("👋🏻", hbold(_("Привіт,")), hbold(quote_html(name) + "!")),
        text(
            _("   • В мене відсутня деяка інформація про тебе."),
            _("   • Ти погоджуєшся надати інформацію?"),
            sep="\n"
        ),
        sep="\n\n"
    )
    return msg


def c_get_hello_back(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}, 😉"


c_register = _("✍️ Реєстрація")
c_cancel = _("❌ Скасувати")
c_cancel_msg = _(
    "🧹 Надання даних скасовано. "
    "Попередньо введена інформація видалена."
)
c_share_phone_number = _("📲 Надіслати номер телефону")
c_share_phone_number_again = _(
    "📵 Цей номер телефону не належить Вашому обліковому запису Telegram. "
    "Спробуйте знову."
)
c_share_phone_number_not_valid = _(
    "📇 Це не є контакт! Для надсилання свого номера телефона "
    "скористайся кнопкою, що нижче."
)


def c_share_phone_number_thx(first_name: str) -> str:
    msg = text(
        text(hbold("🙏 ", _("Дякую!"))),
        text(
            "   •", "🔐 ",
            hbold(first_name + ","),
            _(
                "твій номер телефону надійно збережено та буде "
                "використаний лише в організаційних питаннях клубу на "
                "твою користь і НЕ буде переданий третім особам."
            ),
        ),
        sep="\n\n"
    )
    return msg


c_input_birthday = _("Напиши та відправ мені свою дату народження в відповідному форматі - дд.мм.рррр ("
                     "31.12.2000)\n\n• Для правильної організації тренувального процесу та участі в змаганнях - "
                     "необхідно знати твій вік.\n"
                     "• І ще, я хочу вітати тебе з Днем народження 🙂")
c_input_birthday_again = _("Невірний формат дати. Спробуйте ще раз.")
c_input_birthday_incorrect = _("Некоректна дата. Спробуйте ще раз")
c_input_phone_number = _("Для повноцінного контакту, надай свій номер телефону.\n\n• Його будуть бачити тільки "
                         "адміністрація клубу 📲")
c_input_first_name = _("Введіть ім'я:")
c_input_last_name = _("Введіть своє прізвище:")
c_input_password = _("Введіть пароль:")
c_input_password_again = _(
    "Довжина пароля має бути від 8 символів і містити в собі: "
    "цифри, великі та малі літери")
c_successfully_register = _(
    "Вітаю 🎉\n"
    "<b>Ви успішно зареєструвалися.</b>")
c_registration_failed = _("Під час реєстрації сталася помилка 🫤\n")
c_yes = _("✅ Так")
c_take_approval = _("Натисніть кнопку згоди або скасування")

c_about_us = _("Про нас 👁️")
