from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import translation
from django.core.mail import send_mail
from .models import Email

def change_language(request, lang_code):
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    messages.add_message(request, messages.INFO, "Language changed to " + lang_code)
    return HttpResponseRedirect(reverse("main"))

def my_send_mail(subject, content, to):
    send_mail(subject, content, "yaas@localhost", to)
    mail = Email.objects.create(subject=subject, content=content, to=to)
    mail.save()

def viewEmailsHistory(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You must be an admin to view emails history !")
    else:
        return render(request, "emailsHistory.html", {"emails": Email.objects.all().order_by('-time')})
