from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import forms
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


