import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail as core_send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserChangeForm, UserAuthForm
from users.models import User

from django.contrib.auth.models import Group



class RegistrationView(CreateView):
    model=User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        url = f"http://{self.request.get_host()}/users/email_confirm/{token}/"
        core_send_mail(
            subject='Подтверждение почты',
            message=f"Для подтверждения почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

class EmailVerification(View):
    def get(self, request, token):
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.token = None
        group = Group.objects.get(name="Users")
        user.groups.add(group)
        user.save()
        
        return redirect('users:login')

class ProfileList(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model=User
    template_name = "users/user_list.html"
    permission_required = "users.can_manage_users"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class ProfileBlock(View):
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect("users:profile_list")


class ProfileView(LoginRequiredMixin, DetailView):
    model=User
    template_name = "users/user_detail.html"



class ChangeProfileView(LoginRequiredMixin, UpdateView):
    model=User
    form_class = UserChangeForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        return self.request.user

# class MyPasswordResetView(PasswordResetView):
#     model=User
#     template_name = "users/password_reset.html"
#     success_url = reverse_lazy("users:login")
#     def send_mail(self,
#                   subject_template_name, email_template_name,
#                   context, from_email, to_email,
#                   html_email_template_name=None):
#         subject = "Восстановление пароля"
#
#         message = (
#             f"Привет, {context['user'].username}!\n\n"
#             f"Для подтверждения перейди по ссылке:\n"
#             f"{context['protocol']}://{context['domain']}"
#             f"/users/password_reset_confirm/{context['uid']}/{context['token']}/\n\n"
#             f"Если это был не ты — игнорируй письмо."
#         )
#
#         recipient_list=[to_email] if isinstance(to_email, str) else to_email
#
#         core_send_mail(
#             subject=subject,
#             message=message,
#             from_email=EMAIL_HOST_USER,
#             recipient_list=recipient_list
#         )



