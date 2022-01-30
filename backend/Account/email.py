from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage
from django.conf import settings


class EmailManager(BaseEmailMessage):
    def send(self, to, *args, **kwargs):
        self.render()
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email',
            'DRFJWT認証テスト <' + settings.DEFAULT_FROM_EMAIL + '>'
        )
        super(BaseEmailMessage, self).send(*args, **kwargs)


class ActivationEmail(EmailManager):
    template_name = 'Account/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["ACTIVATION_URL"].format(**context)
        return context


class ConfirmationEmail(EmailManager):
    template_name = 'Account/confirmation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        return context


class PasswordResetEmail(BaseEmailMessage):
    template_name = 'Account/password_reset.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["PASSWORD_RESET_CONFIRM_URL"].format(**context)
        return context


class PasswordChangedConfirmationemail(BaseEmailMessage):
    template_name = 'Account/password_changed_confirmation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        return context


class UsernameResetEmail(BaseEmailMessage):
    template_name = 'Account/username_reset.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["USERNAME_RESET_CONFIRM_URL"].format(**context)
        return context


class UsernameChangedConfirmationEmail(BaseEmailMessage):
    template_name = 'Account/username_changed_confirmation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.name
        return context
