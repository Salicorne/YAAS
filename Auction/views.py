import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.views import View
from decimal import Decimal

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

class AuctionEditView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        auction = get_auctionView(id)
        if auction.seller != request.user:
            messages.error(request, _("You can only edit your own auctions !"))
            return redirect("auctionsBrowse")
        form = forms.AuctionEditForm(instance=auction)
        return render(request, 'auctionEdit.html', {'form': form, 'title': auction.title, 'id': auction.id})

    @method_decorator(login_required)
    def post(self, request, id):
        form = forms.AuctionEditForm(request.POST)
        if form.is_valid():
            auction = get_auctionView(id)
            if auction.seller != request.user:
                messages.error(request, _("You can only edit your own auctions !"))
                return redirect("auctionsBrowse")
            auction.description = form.cleaned_data.get("description")
            auction.save()
            messages.success(request, _("Your auction has been updated !"))
            return redirect("auctionsBrowse")
        else:
            messages.error(request, _("Error during auction editing !"))
            return render(request, 'auctionEdit.html', {'form': form, 'title': auction.title, 'id': auction.id})

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
        messages.success(request, _("Your auction has been created !"))
        send_mail("YAAS Auction created !", f'Your auction {a.title} has been created for {a.price} euros. Its due date is {a.deadline}. ', "yaas@localhost", [request.user.email])
        return redirect("auctionsBrowse")
    else:
        return HttpResponse("error")

def auctionsBrowse(request):
    auctions = get_auctionsBrowse()
    return render(request, "browseAuctions.html", {"auctions": auctions})

def auctionView(request, id):
    auction = get_auctionView(id)
    form = forms.BidForm(data={'price': auction.price+Decimal(0.01), 'version': auction.bid_version})
    return render(request, "seeAuction.html", {"auction": auction, 'form': form})

def auctionsSearch(request):
    search = request.GET.get('q', '')
    auctions = get_auctionsSearch(search)
    serializer = AuctionSerializer(auctions, many=True)
    return render(request, "browseAuctions.html", { "auctions": auctions, "search": search })

@login_required
def bid(request, id):
    auction = get_auctionView(id)
    form = forms.BidForm(request.POST)
    if form.is_valid():
        try:
            exec_bid(id, form.cleaned_data.get("version", 0), form.cleaned_data.get("price", 0), request.user)
            messages.success(request, _("Your bid has been placed !"))
            return redirect("auctionView", id)
        except UpdatedAuctionException as e:
            messages.error(request, e.message)
            return redirect("auctionView", id)
        except PriceException as e:
            messages.error(request, e.detail)
            return render(request, "seeAuction.html", {"auction": auction, 'form': form})
        except OwnAuctionException as e:
            messages.error(request, e.detail)
            return render(request, "seeAuction.html", {"auction": auction, 'form': form})
        except AuctionWinnerException as e:
            messages.error(request, e.detail)
            return render(request, "seeAuction.html", {"auction": auction, 'form': form})
            
    else:
        messages.error(request, _("Error during form validation. "))
        return render(request, "seeAuction.html", {"auction": auction, 'form': form})
        