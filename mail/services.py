from smtplib import SMTPDataError, SMTPSenderRefused, SMTPRecipientsRefused

from django.core.mail import EmailMessage

from mail.models import MailingTry


def mailing_letter(subject, recipients, message, from_email):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to = recipients
    )
    mail_code = None
    try:
        email.send(fail_silently=False)
    except SMTPDataError as e:
        # Здесь код и текст ответа сервера
        mail_code = e.smtp_error.decode()
        print(f"Код(1): {e.smtp_code}")
        print(f"Ответ сервера: {e.smtp_error.decode()}")
    except SMTPSenderRefused as e:
        mail_code = e.smtp_error.decode()
        print(f"Код(2): {e.smtp_code}")
        print(f"Ответ сервера: {e.smtp_error.decode()}")
    except SMTPRecipientsRefused as e:
        mail_code = e.recipients
        print(f"Ответ сервера: {e.recipients}")  # тут dict с кодами и ответами
    return mail_code

def create_try(mailing, status_code ):
    status = "defeat"
    if status_code == None:
        status_code = "None"
        status = "success"

    MailingTry.objects.create(
        mailing=mailing,
        status=status,
        smtp_response=status_code
    )
    return None