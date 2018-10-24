from django.apps import AppConfig

class AuctionConfig(AppConfig):
    name = 'Auction'

    def ready(self):
        from Auction.views import AutionsResolution
        print(" --- AuctionConfig ready ! ---")
        AutionsResolution().start()