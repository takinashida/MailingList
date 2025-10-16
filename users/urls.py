from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.messages import success
from django.urls import path, include, reverse_lazy

from config import settings
from users.apps import UsersConfig

from django.views.decorators.cache import cache_page

from users.views import ChangeProfileView, ProfileView, RegistrationView, EmailVerification

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('email_confirm/<str:token>/', EmailVerification.as_view(), name='email_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change/', ChangeProfileView.as_view(), name='change_profile'),

    path('password_reset/', PasswordResetView.as_view(template_name = "users/password_reset.html",
                                                      email_template_name = "users/password_reset_email.html",
                                                      from_email=settings.EMAIL_HOST_USER,
                                                      success_url = reverse_lazy("users:password_reset_done")), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = "users/password_reset_confirm.html",
                                                                                               success_url = reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name = "users/password_reset_complete.html"), name='password_reset_complete'),

]