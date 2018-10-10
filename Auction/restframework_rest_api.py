from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404

from .serializers import AuctionSerializer
from .models import Auction


def get_auctionsBrowse():
    return Auction.objects.all()

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
    return Auction.objects.filter(title__icontains=search)

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def api_auctionsSearch(request):
    search = request.GET.get('q', '')
    auctions = get_auctionsSearch(search)
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)