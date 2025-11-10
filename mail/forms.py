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
        fields=["letter", "recipients", "first_send", "end_send", "cycle"]
        widgets = {
            "first_send": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Начало отправки",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "end_send": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Конец отправки",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)
        self.fields["letter"].queryset = Letter.objects.filter(owner=user)

        self.fields["letter"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Выберете письмо:"
        })

        self.fields["recipients"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Выберете получателей:"
        })

        self.fields["first_send"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["first_send"].widget.format="%Y-%m-%dT%H:%M"
        self.fields["first_send"].widget.attrs.update({
            "type": "datetime-local",
            "class": "form-control",
            "placeholder": "Начало отправки:"
        })

        self.fields["end_send"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_send"].widget.format = "%Y-%m-%dT%H:%M"
        self.fields["end_send"].widget.attrs.update({
            "type": "datetime-local",
            "class": "form-control",
            "placeholder": "Конец отправки:"
        })

        self.fields["cycle"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Периодичность отправки:"
        })


