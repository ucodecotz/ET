# Generated by Django 3.0.8 on 2020-07-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20200729_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionprice',
            name='sub_price_code',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
    ]
