from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Auction
import json
import decimal
# Create your tests here.

class AuctionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user_test", email="user_test@gmail.com", password="pass_test")
        User.objects.create_user(username="user_test2", email="user_test2@gmail.com", password="pass_test")
        self.auction = Auction.objects.create(title = "Test auction", description = "This is a test auction", price = "10", deadline = "2018-12-01 11:00", seller=User.objects.all()[1])
        self.auctionId = json.loads(self.client.get(reverse("api_auctionsBrowse")).content)[0].get("id")

    def test_browse(self):
        res = self.client.get(reverse("auctionsBrowse"))
        self.assertTemplateUsed(res, "browseAuctions.html")
        self.assertEqual(res.status_code, 200)

    def test_add_logout(self):
        # We will perform an auction creation scenario. 
        title = "Test auction"
        description = "This is a test auction"
        price = "12.21"
        deadline = "2018-12-01 11:00"
        initialCount = Auction.objects.count()

        # First we create an auction
        res = self.client.post(reverse("auctionCreate"), {"title": title,
                                                        "description": description,
                                                        "price": price,
                                                        "deadline": deadline})
        # Then we confirm this auction
        res2 = self.client.post(reverse("auctionConfirm"), {"title": title,
                                                        "description": description,
                                                        "price": price,
                                                        "deadline": deadline})
        # Since we are not logged in the auction should not have been created
        self.assertEqual(Auction.objects.count(), initialCount)

    def test_add_login(self):
        # We will perform an auction creation scenario. 
        title = "Test auction"
        description = "This is a test auction"
        price = "12.21"
        deadline = "2018-12-01 11:00"
        initialCount = Auction.objects.count()

        self.client.login(username="user_test", password="pass_test")

        # First we create an auction
        res = self.client.post(reverse("auctionCreate"), {"title": title,
                                                        "description": description,
                                                        "price": price,
                                                        "deadline": deadline})
        self.assertLess(res.status_code, 400)
        
        # Then we confirm this auction
        res2 = self.client.post(reverse("auctionConfirm"), {"title": title,
                                                        "description": description,
                                                        "price": price,
                                                        "deadline": deadline})
        self.assertLess(res2.status_code, 400)

        self.assertEqual(Auction.objects.count(), initialCount + 1)

    def test_bid(self):
        # This test describes a valid bid
        self.client.login(username="user_test", password="pass_test")
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(100)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].last_bidder, self.user)
        self.assertEqual(Auction.objects.all()[0].price, 100)

    def test_bid_fail_same_user(self):
        # This bid should fail because the bidder is the seller
        self.client.login(username="user_test2", password="pass_test")
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(100)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].last_bidder, None)

    def test_bid_fail_price(self):
        # This bid should fail because the price is too low
        self.client.login(username="user_test", password="pass_test")
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(5)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].last_bidder, None)

    def test_bid_fail_price_eq(self):
        # This bid should fail because the price is equal as the current price
        self.client.login(username="user_test", password="pass_test")
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(10)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].last_bidder, None)

    def test_bid_fail_winner(self):
        # The second bid should fail because the user is already the winner of this auction
        self.client.login(username="user_test", password="pass_test")
        # First bid should be ok
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(100)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].last_bidder, self.user)
        self.assertEqual(Auction.objects.all()[0].price, 100)
        # Second bid should fail
        res = self.client.post(reverse("bid", kwargs={"id": self.auctionId}), data={"version": 0, "price": decimal.Decimal(102)})
        self.assertLess(res.status_code, 400)
        self.assertEqual(Auction.objects.all()[0].price, 100)


class AuctionsAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user_test", email="user_test@gmail.com", password="pass_test")
        self.auction = Auction.objects.create(title = "Test auction", description = "This is a test auction", price = "12.21", deadline = "2018-12-01 11:00", seller=User.objects.all()[0])
        self.auctionId = json.loads(self.client.get(reverse("api_auctionsBrowse")).content)[0].get("id")

    def test_browse(self):
        res = self.client.get(reverse("api_auctionsBrowse"))
        self.assertEqual(res.status_code, 200)
        auctions = json.loads(res.content)
        self.assertEqual(Auction.objects.count(), len(auctions))

    def test_get(self):
        res = self.client.get(reverse("api_auctionView", kwargs={"id": self.auctionId}))
        self.assertEqual(res.status_code, 200)
        

