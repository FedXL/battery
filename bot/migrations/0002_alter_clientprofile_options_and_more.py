# Generated by Django 5.1.5 on 2025-01-23 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientprofile',
            options={'verbose_name': 'Профиль клиента', 'verbose_name_plural': 'Профили клиентов'},
        ),
        migrations.AlterModelOptions(
            name='sellerprofile',
            options={'verbose_name': 'Профиль продавца', 'verbose_name_plural': 'Профили продавцов'},
        ),
        migrations.AlterModelOptions(
            name='usertelegram',
            options={'verbose_name': 'telegram user', 'verbose_name_plural': 'telegram users'},
        ),
        migrations.AlterModelOptions(
            name='userwhatsapp',
            options={'verbose_name': 'WhatsApp user', 'verbose_name_plural': 'WhatsApp users'},
        ),
    ]
