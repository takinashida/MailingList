from django.urls import path, include
from mail.apps import MailConfig

from django.views.decorators.cache import cache_page

from mail.views import Index, RecipientCreateView, RecipientListView, RecipientDetailView, RecipientUpdateView, \
    RecipientDeleteView, LetterCreateView, LetterUpdateView, LetterListView, LetterDetailView, LetterDeleteView, \
    MailingCreateView, MailingUpdateView, MailingListView, MailingDetailView, MailingDeleteView, DoMailingView, \
    MailingTryListView

app_name = MailConfig.name

urlpatterns = [
    path("", Index.as_view(), name="index"),

    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),

    path("letter/create/", LetterCreateView.as_view(), name="letter_create"),
    path("letter/update/<int:pk>/", LetterUpdateView.as_view(), name="letter_update"),
    path("letter/list/", LetterListView.as_view(), name="letter_list"),
    path("letter/<int:pk>/", LetterDetailView.as_view(), name="letter_detail"),
    path("letter/delete/<int:pk>/", LetterDeleteView.as_view(), name="letter_delete"),

    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),

    path("mailing/do/<int:pk>/", DoMailingView.as_view(), name="mailing_do"),
    path("mailing/trys/<int:pk>/", MailingTryListView.as_view(), name="mailing_trys")

]