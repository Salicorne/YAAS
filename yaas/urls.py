"""yaas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Utils.views import *
from Auth.views import *
from Auction.views import *
from Auction.restframework_rest_api import *

urlpatterns = [
    path('admin', admin.site.urls),

    path('', index, name="main"),
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout_view, name="logout"),
    path('edit-user', UserEditView.as_view(), name="userEdit"),
    
    path('auctions/create', AuctionCreateView.as_view(), name="auctionCreate"),
    path('auctions/edit/<int:id>', AuctionEditView.as_view(), name="auctionEdit"),
    path('auctions/confirm', auctionConfirm, name="auctionConfirm"),
    
    path('api/auctions', api_auctionsBrowse, name="api_auctionsBrowse"),
    path('auctions', auctionsBrowse, name="auctionsBrowse"),
    path('api/auctions/<int:id>', api_auctionView, name="api_auctionView"),
    path('auctions/<int:id>', auctionView, name="auctionView"),
    path('api/auctions/search', api_auctionsSearch, name="api_auctionSearch"),
    path('auctions/search', auctionsSearch, name="auctionSearch"),
    path('auctions/ban/<int:id>', auctionBan, name="auctionBan"),
    path('auctions/banned', viewBannedAuctions, name="bannedAuctions"),

    path('api/bid/<int:id>', api_bid, name="api_bid"),
    path('bid/<int:id>', bid, name="bid"),

    path('language/<slug:lang_code>/', change_language, name="language"),
    path('emailsHistory', viewEmailsHistory, name="emailsHistory"),
    path('generatedata', generateData, name="generateData")
]
