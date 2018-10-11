from rest_framework import serializers
from .models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'seller', 'last_bidder', 'title', 'description', 'price', 'deadline')

class BidSerializer(serializers.Serializer):
    version = serializers.IntegerField()
    price = serializers.FloatField()
