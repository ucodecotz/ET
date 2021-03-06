# Generated by Django 3.0.8 on 2020-08-14 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0032_auto_20200730_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='amount',
            field=models.FloatField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='reference_id_from_ISP',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='success_type',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
