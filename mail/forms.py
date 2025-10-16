from django import forms

from mail.models import Recipient, Letter, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model=Recipient
        fields=["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите почту получателя:"
        })

        self.fields["full_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите Ф.И.О. получателя(необязательно):"
        })

        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите комментарий(необязательно):"
        })



class LetterForm(forms.ModelForm):
    class Meta:
        model=Letter
        fields=["subject", "letter_body"]

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите тему письма:"
        })

        self.fields["letter_body"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите содержание письма:"
        })



class MailingForm(forms.ModelForm):
    class Meta:
        model=Mailing
        fields=["letter", "recipients"]

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["letter"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Выберете письмо:"
        })

        self.fields["recipients"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Выберете получателей:"
        })


