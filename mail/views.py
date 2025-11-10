from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django_apscheduler.jobstores import register_job

from config.settings import EMAIL_HOST_USER
from mail.forms import RecipientForm, LetterForm, MailingForm
from mail.models import Recipient, Letter, Mailing, MailingTry
from mail.services import mailing_letter, create_try, mailing_letters
from mail.tasks import scheduler
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# Create your views here.
class Index(View):
    def get(self, request):
        all_mailings=len(Mailing.objects.filter(owner=request.user))
        active_mailings=len(Mailing.objects.filter(owner=request.user, status="started"))
        recipients=len(Recipient.objects.filter(owner=request.user))
        context={"all_mailings":all_mailings,
        "active_mailings":active_mailings,
        "recipients":recipients}
        return render(request, "mail/index.html", context)


class RecipientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")
    permission_required = "mail.add_recipient"



    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    template_name = "mail/recipient/recipient_list.html"
    permission_required = "mail.view_recipient"

    def get_queryset(self):
        queryset = cache.get('recipient_list_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('recipient_list_queryset', queryset, 60 * 15)
        if self.request.user.has_perm("mail.can_manage_recipient"):
            return queryset
        return  queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recipient
    template_name = "mail/recipient/recipient_detail.html"
    permission_required = "mail.view_recipient"

    def get_queryset(self):
        queryset = cache.get('recipient_detail_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('recipient_detail_queryset', queryset, 60 * 15)
        if self.request.user.has_perm("mail.can_manage_recipient"):
            return queryset
        return queryset.filter(owner=self.request.user)


class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mail/recipient/recipient_form.html"
    success_url = reverse_lazy("mail:recipient_list")
    permission_required = "mail.change_recipient"

class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Recipient
    template_name ="mail/recipient/recipient_confirm_delete.html"
    success_url = reverse_lazy("mail:recipient_list")
    permission_required = "mail.delete_recipient"



class LetterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "mail/letter/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")
    permission_required = "mail.add_letter"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(cache_page(60 * 15), name='dispatch')
class LetterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Letter
    template_name = "mail/letter/letter_list.html"
    permission_required = "mail.view_letter"

    def get_queryset(self):
        queryset = cache.get('letter_list_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('letter_list_queryset', queryset, 60 * 15)
        return  queryset.filter(owner=self.request.user)

@method_decorator(cache_page(60 * 15), name='dispatch')
class LetterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Letter
    template_name = "mail/letter/letter_detail.html"
    permission_required = "mail.view_letter"
    def get_queryset(self):
        queryset = cache.get('letter_detail_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('letter_detail_queryset', queryset, 60 * 15)
        return  queryset.filter(owner=self.request.user)

class LetterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = "mail/letter/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")
    permission_required = "mail.change_letter"

class LetterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Letter
    template_name ="mail/letter/letter_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")
    permission_required = "mail.delete_letter"



class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")
    permission_required = "mail.add_mailing"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"]=self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.instance.cycle == "now":
            mailing_letters(mailing=form.instance)
            form.instance.status = "finished"
        if form.instance.cycle == "everyday":
            @register_job(scheduler, "cron", hour=8, minute=0, start_date=form.instance.first_send,end_date=form.instance.end_send)
            def everyday_mailing():
                mailing_letters(mailing=form.instance)
        if form.instance.cycle == "everyweek":
            @register_job(scheduler, "cron", day_of_week="mon", hour=8, start_date=form.instance.first_send,end_date=form.instance.end_send)
            def everyweek_mailing():
                mailing_letters(mailing=form.instance)
        if form.instance.cycle == "everymonth":
            @register_job(scheduler, "cron", day=1, hour=8, start_date=form.instance.first_send,end_date=form.instance.end_send)
            def everymonth_mailing():
                mailing_letters(mailing=form.instance)
        else:
            print("Что-то пошло не так")

        return super().form_valid(form)

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = "mail/mailing/mailing_list.html"
    permission_required = "mail.view_mailing"

    def get_queryset(self):
        queryset = cache.get('mailing_list_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('mailing_list_queryset', queryset, 60 * 15)
        if self.request.user.has_perm("mail.can_manage_mailing"):
            return queryset
        return  queryset.filter(owner=self.request.user)

class MailingBlock(View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.status= "finished"
        mailing.save()
        return redirect("mail:mailing_list")

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = "mail/mailing/mailing_detail.html"
    permission_required = "mail.view_mailing"

    def get_queryset(self):
        queryset = cache.get('mailing_detail_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('mailing_detail_queryset', queryset, 60 * 15)
        if self.request.user.has_perm("mail.can_manage_mailing"):
            return queryset
        return  queryset.filter(owner=self.request.user)

class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail/mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")
    permission_required = "mail.change_mailing"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"]=self.request.user
        return kwargs

class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name ="mail/mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:mailing_list")
    permission_required = "mail.delete_mailing"


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

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry
    template_name = "mail/mailingtry/mailingtry_list.html"

    def get_queryset(self):
        queryset = cache.get('mailingtry_queryset')
        if not queryset:
            mailing=get_object_or_404(Mailing, pk=self.kwargs["pk"])
            queryset = MailingTry.objects.filter(mailing=mailing)
            cache.set('mailingtry_queryset', queryset, 60 * 15)
        if mailing.owner == self.request.user:
            return queryset
        else:
            raise PermissionDenied("Ты не можешь смотреть информацию о чужих рассылках!")
