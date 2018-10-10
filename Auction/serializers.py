from rest_framework import serializers
from .models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'seller', 'title', 'description', 'price', 'deadline')
