import json
import time
import datetime
import random
import requests
from decimal import Decimal
from threading import Thread

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from Utils.views import my_send_mail

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
            if form.cleaned_data.get("deadline").replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None) < datetime.timedelta(hours=72):
                messages.error(request, "The minimum duration of an auction is 72h")
                return render(request, 'auctionCreate.html', {'form': form})
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
        auction = get_auctionView(id)
        if form.is_valid():
            if auction.seller != request.user:
                messages.error(request, _("You can only edit your own auctions !"))
                return redirect("auctionsBrowse")
            auction.description = form.cleaned_data.get("description")
            auction.bid_version += 1
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
        if form.cleaned_data.get("deadline").replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None) < datetime.timedelta(hours=72):
            messages.error(request, "The minimum duration of an auction is 72h")
            form = forms.AuctionCreateForm()
            return render(request, 'auctionCreate.html', {'form': form})
        a = models.Auction(title=form.cleaned_data.get("title"), 
                        description=form.cleaned_data.get("description"), 
                        price=form.cleaned_data.get("price"), 
                        deadline=form.cleaned_data.get("deadline"), 
                        seller=request.user)
        a.save()
        messages.success(request, _("Your auction has been created !"))
        my_send_mail("YAAS Auction created !", f'Your auction {a.title} has been created for {a.price} euros. Its due date is {a.deadline}. ', [request.user.email])
        return redirect("auctionsBrowse")
    else:
        return HttpResponse("error")

def auctionsBrowse(request):
    auctions = get_auctionsBrowse()
    return render(request, "browseAuctions.html", {"auctions": auctions})

def getRate(cur):
    key = "37c17a3674def739416f5e9a653a166a"
    if cur == "EUR":
        return 1
    r = requests.get(f'http://data.fixer.io/api/latest?access_key={key}&base=EUR')
    if r.status_code != 200:
        return 1
    res = r.json()
    try:
        return res.get("rates", None).get(cur, 1)
    except Exception:
        return 1

def getSymbol(cur):
    table = {
        "EUR": "&euro;",
        "USD": "&dollar;",
        "GBP": "&pound;",
        "JPY": "&yen;",
        "RUB": "&#8381;",
    }
    return table.get(cur, '&euro;')

def auctionView(request, id):
    auction = get_auctionView(id)
    form = forms.BidForm(data={'price': auction.price+Decimal(0.01), 'version': auction.bid_version})
    cur = request.GET.get('cur', 'EUR')
    auction.price = '%.2f' % (auction.price * Decimal(getRate(cur)))
    symbol = getSymbol(cur)
    return render(request, "seeAuction.html", {"auction": auction, 'symbol': symbol, 'form': form})

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
        except BannedAuctionException as e:
            messages.error(request, e.detail)
            return render(request, "seeAuction.html", {"auction": auction, 'form': form})
        except AuctionWinnerException as e:
            messages.error(request, e.detail)
            return render(request, "seeAuction.html", {"auction": auction, 'form': form})
            
    else:
        messages.error(request, _("Error during form validation. "))
        return render(request, "seeAuction.html", {"auction": auction, 'form': form})

@login_required
def auctionBan(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You must be an admin to ban an auction !")
    else:
        auction = get_auctionView(id)
        auction.banned = True
        auction.save()
        my_send_mail("Auction banned", f'Your auction {auction.title} has been banned by an administrator, it will not appear in the system anymore. ', [auction.seller.email])
        my_send_mail("Auction banned", f'The auction {auction.title} on which you had a bid has been banned by an administrator. It will no longer appear in the system. ', list(map(lambda u: u.email, auction.bidders.all())))
        return redirect('auctionsBrowse')

@login_required
def viewBannedAuctions(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You must be an admin to view the list of banned auctions !")
    else:
        return render(request, "bannedAuctions.html", {"auctions": Auction.objects.filter(banned=True)})
        
class AutionsResolution(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True      # https://docs.python.org/3/library/threading.html
        print(" --- Launching auctions resolution thread ---")

    def run(self):
        while(True):
            for a in Auction.objects.filter(resolved=False, banned=False):
                a.testResolve()
            time.sleep(60)


# Data generation program :

def getRandomUser(sampleSize):
    return User.objects.all()[random.randint(0, sampleSize - 1)]

def getRandomAuction(sampleSize):
    return Auction.objects.all()[random.randint(0, sampleSize - 1)]

def createAuction(sampleSize):
    u = getRandomUser(sampleSize)
    Auction(seller=u,
            title=f'Sample auction created by {u.username}',
            description=f'This is a sample random auction. It has been created via GET /generatedata !',
            price=random.randint(10, 100),
            # This deadline respects the 72h limit, but can be changed to create shorter auctions. 
            deadline=datetime.datetime.now() + datetime.timedelta(days=random.randint(4, 10))).save()

def createBid(sampleSize):
    a = getRandomAuction(sampleSize)
    u = getRandomUser(sampleSize)
    Auction.restframework_rest_api.exec_bid(id=a.id,
                                        version=a.bid_version,
                                        price=a.price + 1,
                                        bidder=u)

def generateData(request):
    Auction.objects.all().delete()
    User.objects.all().delete()

    User.objects.create_superuser(username="admin", password="admin2018", email="admin@localhost")
    User.objects.create_user(username="user", password="user", email="user@localhost")

    sampleSize = 51
    for i in range(0, sampleSize):
        User.objects.create_user(username=f'user{i}', password=f'user{i}', email=f'user{i}@localhost')

    for i in range(0, sampleSize):
        createAuction(sampleSize)

    for i in range(0, sampleSize * 3):
        try:
            createBid(sampleSize)
        except Exception:
            pass

    messages.success(request, "Sample data has been generated !")
    return redirect("main")