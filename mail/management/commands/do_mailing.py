from django.core.management import BaseCommand
from config.settings import EMAIL_HOST_USER
from mail.models import Mailing
from mail.services import mailing_letter, create_try


class Command(BaseCommand):
    def handle(self):
        mailing = Mailing.objects.get(pk=3)
        status_code = mailing_letter(
            subject=mailing.letter.subject,
            recipients=[rec.email for rec in mailing.recipients.all()],
            message=mailing.letter.letter_body,
            from_email=EMAIL_HOST_USER,
        )
        create_try(mailing, status_code)
        if status_code:
            self.stdout.write(self.style.WARNING(f'Возникла ошибка: {status_code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully send mail: {mailing.letter.subject}'))