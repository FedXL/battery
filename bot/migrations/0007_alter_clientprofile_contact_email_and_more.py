# Generated by Django 5.1.5 on 2025-01-31 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_clientprofile_language_sellerprofile_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofile',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Город'),
        ),
    ]
