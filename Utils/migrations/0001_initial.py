# Generated by Django 2.1.1 on 2018-10-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150)),
                ('content', models.CharField(max_length=500)),
                ('to', models.CharField(max_length=150)),
            ],
        ),
    ]
