# Generated by Django 4.2 on 2024-06-02 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_tokenmodel_user_mobilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilemodel',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='شماره موبایل'),
        ),
    ]
