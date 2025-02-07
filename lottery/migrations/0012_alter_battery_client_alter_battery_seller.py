# Generated by Django 5.1.5 on 2025-02-07 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_alter_clientprofile_client_and_more'),
        ('lottery', '0011_alter_battery_client_alter_battery_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='battery',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.seller', verbose_name='Продавец'),
        ),
    ]
