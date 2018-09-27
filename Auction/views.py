import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.core import serializers

from . import forms, models

# Create your views here.

class AuctionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.AuctionCreateForm()
        return render(request, 'auctionCreate.html', {'form': form})

    def post(self, request):
        form = forms.AuctionCreateForm(request.POST)
        if form.is_valid():
            a = models.Auction(title=form.cleaned_data.get("title"), 
                        description=form.cleaned_data.get("description"), 
                        price=form.cleaned_data.get("price"), 
                        deadline=form.cleaned_data.get("deadline"), 
                        seller=request.user)
            a.save()
            return redirect("main")
        else:
            return HttpResponse("error")

def get_auctionsBrowse():
    try:
        a = models.Auction.objects.all()
        orm_json = serializers.serialize("json", a)
        res = list(map(lambda x: x.get("fields"), list(json.loads(orm_json))))
        
    except Exception:
        return "[]"
    
    return json.dumps(res)

def api_auctionsBrowse(request):
    return HttpResponse(get_auctionsBrowse())

def auctionsBrowse(request):
    try:
        a = json.loads(get_auctionsBrowse())
    except json.JSONDecodeError:
        return HttpResponse("error")
    return render(request, "browseAuctions.html", {"auctions": a})