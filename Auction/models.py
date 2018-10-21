from django.db import models
from django.contrib.auth.models import User
from Utils.views import my_send_mail
import datetime
import time

# Create your models here.

class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    bidders = models.ManyToManyField(User, related_name="auctions")
    last_bidder = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="bids")
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deadline = models.DateTimeField()
    bid_version = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    def getTimeLeft(self):
        diff = self.deadline.replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)
        return str(diff)

    def testResolve(self):
        print(f' -- Trying {self.title}')
        if datetime.datetime.now().replace(tzinfo=None) > self.deadline.replace(tzinfo=None) and not self.resolved and not self.banned:
            print(f'Resolving auction {self.title} !')
            self.resolved = True
            my_send_mail("Auction resolved", f'The auction {self.title} on which you had a bid has been resolved. It will no longer appear in the system. ', list(map(lambda u: u.email, self.bidders.all())))
            if self.last_bidder is not None:
                my_send_mail("Auction resolved", f'Your auction {self.title} has been resolved. It has been sold to {self.last_bidder.username}. ', [self.seller.email])
            else:
                my_send_mail("Auction resolved", f'Your auction {self.title} has been resolved, unfortunately nobody has placed any bid on it. ', [self.seller.email])
            self.save()
