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
    auctions = Auction.objects.all()
    serializer = AuctionSerializer(auctions, many=True)
    return serializer.data

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def api_auctionsBrowse(request):
    return Response(get_auctionsBrowse())
