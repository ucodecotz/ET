# Generated by Django 3.0.8 on 2020-07-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200724_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
