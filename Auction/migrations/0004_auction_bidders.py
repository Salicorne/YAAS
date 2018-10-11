# Generated by Django 2.1.1 on 2018-10-11 11:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Auction', '0003_auto_20181011_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bidders',
            field=models.ManyToManyField(related_name='auctions', to=settings.AUTH_USER_MODEL),
        ),
    ]
