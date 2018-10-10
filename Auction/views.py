import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from . import forms, models
from .restframework_rest_api import *


class AuctionCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = forms.AuctionCreateForm()
        return render(request, 'auctionCreate.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = forms.AuctionCreateForm(request.POST)
        if form.is_valid():
            confForm = forms.ConfAuctionForm(initial={"title": form.cleaned_data.get("title"), 
                                                    "description": form.cleaned_data.get("description"), 
                                                    "price": form.cleaned_data.get("price"), 
                                                    "deadline": form.cleaned_data.get("deadline")})
            return render(request, "auctionConfirm.html", {"form": confForm, "title": form.cleaned_data.get("title")})
        else:
            return HttpResponse("error")

@login_required
def auctionConfirm(request):
    form = forms.ConfAuctionForm(request.POST)
    if(form.is_valid()):
        a = models.Auction(title=form.cleaned_data.get("title"), 
                        description=form.cleaned_data.get("description"), 
                        price=form.cleaned_data.get("price"), 
                        deadline=form.cleaned_data.get("deadline"), 
                        seller=request.user)
        a.save()
        messages.success(request, "Your auction has been created !")
        return redirect("auctionsBrowse")
    else:
        return HttpResponse("error")

def auctionsBrowse(request):
    auctions = get_auctionsBrowse()
    return render(request, "browseAuctions.html", {"auctions": auctions})

def auctionView(request, id):
    auction = get_auctionView(id)
    return render(request, "seeAuction.html", {"auction": auction})

def auctionsSearch(request):
    search = request.GET.get('q', '')
    auctions = get_auctionsSearch(search)
    serializer = AuctionSerializer(auctions, many=True)
    return render(request, "browseAuctions.html", { "auctions": auctions, "search": search })
