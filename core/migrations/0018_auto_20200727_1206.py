# Generated by Django 3.0.8 on 2020-07-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200727_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
    ]
