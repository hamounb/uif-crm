# Generated by Django 4.2 on 2024-08-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_invoiceitemmodel_value_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicemodel',
            name='state',
            field=models.CharField(choices=[('prepayment', 'پیش پرداخت'), ('paid', 'پرداخت شده'), ('unpaid', 'پرداخت نشده')], default='unpaid', max_length=50, verbose_name='وضعیت'),
        ),
    ]
