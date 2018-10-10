import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from . import forms, models

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

def get_auctionsBrowse():
    def build_dict(x):
        i = x.get("fields")
        i["id"] = x.get("pk")
        return i
    try:
        a = models.Auction.objects.all()
        orm_json = serializers.serialize("json", a)
        return json.dumps(list(map(build_dict, list(json.loads(orm_json)))))
        
    except Exception:
        return "[]"

def api_auctionsBrowse(request):
    return HttpResponse(get_auctionsBrowse())

def auctionsBrowse(request):
    try:
        a = json.loads(get_auctionsBrowse())
    except json.JSONDecodeError:
        return HttpResponse("error")
    return render(request, "browseAuctions.html", {"auctions": a})
