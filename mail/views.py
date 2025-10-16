from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from config.settings import EMAIL_HOST_USER
from mail.forms import RecipientForm, LetterForm, MailingForm
from mail.models import Recipient, Letter, Mailing, MailingTry
from mail.services import mailing_letter, create_try


# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, "mail/index.html")


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mail/recipient/recipient_list.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "mail/recipient/recipient_detail.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")

class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name ="mail/recipient/recipient_confirm_delete.html"
    success_url = reverse_lazy("mail:recipient_list")



class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "mail/letter/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class LetterListView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = "mail/letter/letter_list.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(owner=self.request.user)

class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter
    template_name = "mail/letter/letter_detail.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(owner=self.request.user)

class LetterUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = "mail/letter/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")

class LetterDeleteView(LoginRequiredMixin, DeleteView):
    model = Letter
    template_name ="mail/letter/letter_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")



class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mail/mailing/mailing_list.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(owner=self.request.user)

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mail/mailing/mailing_detail.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(owner=self.request.user)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name ="mail/mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:mailing_list")

class DoMailingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        mailing = Mailing.objects.get(pk=kwargs["pk"])
        mailing.status = "started"
        mailing.save()
        status_code = mailing_letter(
            subject=mailing.letter.subject,
            recipients=[rec.email for rec in mailing.recipients.all()],
            message=mailing.letter.letter_body,
            from_email=EMAIL_HOST_USER,
        )
        create_try(mailing,status_code)

        return redirect(reverse_lazy("mail:mailing_detail", kwargs=kwargs))

class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry
    template_name = "mail/mailingtry/mailingtry_list.html"

    def get_queryset(self):
        mailing=get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if mailing.owner == self.request.user:
            return MailingTry.objects.filter(mailing=mailing)
        else:
            raise PermissionDenied("Ты не можешь смотреть информацию о чужих рассылках!")
