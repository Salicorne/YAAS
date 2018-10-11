from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    last_bidder = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="bids")
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deadline = models.DateTimeField()
    bid_version = models.IntegerField(default=0)
