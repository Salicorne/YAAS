# Generated by Django 2.1.1 on 2018-10-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utils', '0002_email_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
