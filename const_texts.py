from django.utils.translation import gettext_lazy as _


def c_get_hello(full_name: str) -> str:
    return f"Привіт, {full_name}!\nВи новачок у нас, " "тому введіть свої дані."


def c_get_hello_back(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name} ми раді бачити вас знову!"


c_register = "Реєстрація 📝"
c_cancel = "Скасувати ❌"
c_share_phone_number = "Надіслати номер телефону"
c_share_phone_number_again = _(
    "Цей номер телефону не належить Вашому обліковому запису Telegram. "
    "Спробуйте знову."
)
c_input_birthday = _("Вкажіть вашу дату народження в форматі: дд.мм.рррр")
c_input_birthday_again = _("Невірний формат дати. Спробуйте ще раз.")
c_input_birthday_incorrect = _("Некоректна дата. Спробуйте ще раз")
c_input_phone_number = _("Введіть свій номер телефону:")
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

c_about_us = "Про нас 👁️"
