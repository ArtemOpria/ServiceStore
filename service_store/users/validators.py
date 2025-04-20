from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator
)


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return _('Пароль занадто короткий. Він повинен містити принаймні %(min_length)d символів.') % {'min_length': self.min_length}

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                self.get_help_text(),
                code='password_too_short',
            )


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def get_help_text(self):
        return _('Цей пароль занадто поширений.')

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                self.get_help_text(),
                code='password_too_common',
            )


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return _('Пароль не може складатися тільки з цифр.')

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                self.get_help_text(),
                code='password_entirely_numeric',
            )
