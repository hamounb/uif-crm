# Generated by Django 4.2 on 2024-08-20 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitemmodel',
            name='value_added',
            field=models.CharField(default='0', max_length=10, verbose_name='ارزش افزوده'),
        ),
    ]
