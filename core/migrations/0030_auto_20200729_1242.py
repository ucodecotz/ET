# Generated by Django 3.0.8 on 2020-07-29 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20200729_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_status',
            field=models.CharField(choices=[('P', 'pending invoice'), ('A', 'Approved')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='core.UserSubscriptions'),
        ),
    ]