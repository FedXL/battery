# Generated by Django 5.1.5 on 2025-01-23 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_client_options_alter_seller_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertelegram',
            name='phone_from_telegram',
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='phone_from_telegram',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон привязанный к телеграм аккаунту'),
        ),
        migrations.AddField(
            model_name='sellerprofile',
            name='phone_from_telegram',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон привязанный к телеграм аккаунту'),
        ),
    ]