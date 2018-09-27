from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from . import forms

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get("username"), form.cleaned_data.get("email"), form.cleaned_data.get("password"))
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.save()
            return HttpResponse("ok")
        return HttpResponse("POST")

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form, 'next': request.GET.get("next", reverse("main"))})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                # Success !
                # return HttpResponseRedirect(reverse('main'))
                return HttpResponseRedirect(self.request.GET.get("next", reverse("main")))
            else:
                return HttpResponse("No such user...")
        return HttpResponse('Error')

class UserEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.UserEditForm(instance=request.user)
        return render(request, 'userEdit.html', {'form': form, 'username': request.user.username})

    def post(self, request):
        form = forms.UserEditForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data.get("email")
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            if(password is not None and password != ""):
                user.set_password(password)
                update_session_auth_hash(request, user) # Used to not disconnect the user
            user.save()
            return HttpResponseRedirect(reverse('main'))
        return HttpResponse("POST")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
