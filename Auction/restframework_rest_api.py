import datetime

from django.shortcuts import get_object_or_404
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes, renderer_classes)
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from Utils.views import my_send_mail

from .models import Auction
from .serializers import AuctionSerializer, BidSerializer


class OwnAuctionException(APIException):
    status_code = 403
    default_detail = "An user can not bid on his own auctions"
    default_code = "Forbidden"

class PriceException(APIException):
    status_code = 403
    default_detail = "The bidding price must be higher than the current price"
    default_code = "Forbidden"

class AuctionWinnerException(APIException):
    status_code = 403
    default_detail = "You are already the winner of this auction"
    default_code = "Forbidden"

class BannedAuctionException(APIException):
    status_code = 403
    default_detail = "You can not bid on a banned auction"
    default_code = "Forbidden"

class ResolvedAuctionException(APIException):
    status_code = 403
    default_detail = "You can not bid on a resolved auction"
    default_code = "Forbidden"

class UpdatedAuctionException(Exception):
    def __init__(self):
        self.message = "This auction has been updated before your request, please refresh !"



def get_auctionsBrowse():
    return Auction.objects.filter(banned=False, resolved=False)

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def api_auctionsBrowse(request):
    auctions = get_auctionsBrowse()
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)


def get_auctionView(id):
    return get_object_or_404(Auction, id=id)

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def api_auctionView(request, id):
    auction = get_auctionView(id)
    serializer = AuctionSerializer(auction)
    return Response(serializer.data)


def get_auctionsSearch(search):
    return Auction.objects.filter(title__icontains=search, banned=False, resolved=False)

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def api_auctionsSearch(request):
    search = request.GET.get('q', '')
    auctions = get_auctionsSearch(search)
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)


def exec_bid(id, version, price, bidder):
    auction = get_object_or_404(Auction, id=id)
    # Bid validity verification
    if auction.seller == bidder:
        raise OwnAuctionException()
    if auction.last_bidder == bidder:
        raise AuctionWinnerException()
    if auction.bid_version != version:
        raise UpdatedAuctionException()
    if auction.banned:
        raise BannedAuctionException()
    if auction.resolved:
        raise ResolvedAuctionException()
    if(auction.price >= price):
        raise PriceException()
    # Bid registration
    auction.price = price
    auction.bid_version = auction.bid_version + 1
    if auction.last_bidder is not None:
        my_send_mail("Someone else placed a bid on an auction", f'Hi ! Your bid on auction {auction.title} is no longer valid, because someone placed a higher bid on it.', [auction.last_bidder.email])
    auction.last_bidder = bidder
    auction.bidders.add(bidder)
    # Soft deadlines
    if(auction.deadline.replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None) < datetime.timedelta(minutes=5)):
        auction.deadline += datetime.timedelta(minutes=5)
    auction.save()
    my_send_mail("A new bid has been placed on your auction", f'A new bid has been placed on your auction {auction.title} by {bidder.username}. The new price of your auction is now {auction.price} euros. ', [auction.seller.email])
    return auction

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer,])
def api_bid(request, id):
    in_serializer = BidSerializer(data=request.data)
    if in_serializer.is_valid():
        try:
            auction = exec_bid(id, in_serializer.validated_data.get("version", 0), in_serializer.validated_data.get("price", 0), request.user)
        except UpdatedAuctionException as e:
            return Response({'detail': e.message})

        out_serializer = AuctionSerializer(auction, many=False)
        return Response(out_serializer.data)
