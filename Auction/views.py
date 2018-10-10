import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from . import forms, models
from .restframework_rest_api import *

# Create your views here.

class AuctionCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = forms.AuctionCreateForm()
        return render(request, 'auctionCreate.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = forms.AuctionCreateForm(request.POST)
        if form.is_valid():
            a = models.Auction(title=form.cleaned_data.get("title"), 
                        description=form.cleaned_data.get("description"), 
                        price=form.cleaned_data.get("price"), 
                        deadline=form.cleaned_data.get("deadline"), 
                        seller=request.user)
            a.save()
            return redirect("auctionsBrowse")
        else:
            return HttpResponse("error")

def auctionsBrowse(request):
    try:
        auctions = json.loads(get_auctionsBrowse())
    except json.JSONDecodeError:
        return HttpResponse("error")
    return render(request, "browseAuctions.html", {"auctions": auctions})
