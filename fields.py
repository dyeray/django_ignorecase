from django.db.models import CharField, TextField, EmailField


class IgnoreCaseMixin(object):

    def get_prep_value(self, value):
        if value is not None:
            value = value.lower()
        return super().get_prep_value(value)


class ICharField(IgnoreCaseMixin, CharField):
    pass


class ITextField(IgnoreCaseMixin, TextField):
    pass


class IEmailField(IgnoreCaseMixin, EmailField):
    pass
