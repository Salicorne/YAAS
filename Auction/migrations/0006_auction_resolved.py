# Generated by Django 2.1.1 on 2018-10-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0005_auction_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
