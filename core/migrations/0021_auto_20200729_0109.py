# Generated by Django 3.0.8 on 2020-07-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200729_0102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='number_service_selected',
            new_name='number_subscription_selected',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
    ]
