# Generated by Django 3.0.8 on 2020-07-24 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200724_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='service_provider_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ServiceProvider'),
        ),
    ]