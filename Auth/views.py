from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from . import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

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
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                # Success !
                return HttpResponse("Login successful")
            else:
                return HttpResponse("No such user...")
        return HttpResponse('Error')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
