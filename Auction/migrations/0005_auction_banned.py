# Generated by Django 2.1.1 on 2018-10-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0004_auction_bidders'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='banned',
            field=models.BooleanField(default=False),
        ),
    ]
