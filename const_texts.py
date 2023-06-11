from django.utils.translation import gettext_lazy as _


def c_get_hello(full_name: str) -> str:
    return f"Привіт, {full_name}!\nВи новачок у нас, " "тому введіть свої дані."


def c_get_hello_back(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name} ми раді бачити вас знову!"


c_register = "Реєстрація 📝"
c_cancel = "Відмовитись ❌"
c_share_phone_number = "Надіслати номер телефону"
c_input_phone_number = "Введіть свій номер телефону:"
c_input_first_name = "Введіть ім'я:"
c_input_last_name = "Введіть своє прізвище:"
c_input_password = "Введіть пароль:"
c_input_password_again = _(
    "Довжина пароля має бути від 8 символів і містити в собі: "
    "цифри, великі та малі літери")
c_successfully_register = _(
    "Вітаю 🎉\n"
    "<b>Ви успішно зареєструвалися.</b>")
c_registration_failed = _("Під час реєстрації сталася помилка 🫤\n")

c_about_us = "Про нас 👁️"
