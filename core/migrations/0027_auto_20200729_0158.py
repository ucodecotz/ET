# Generated by Django 3.0.8 on 2020-07-28 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200729_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
        migrations.DeleteModel(
            name='Payment_response',
        ),
    ]
