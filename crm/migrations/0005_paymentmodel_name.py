# Generated by Django 4.2 on 2024-08-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_paymentmodel_state_invoiceitemmodel_excus'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='مشخصات صاحب چک'),
        ),
    ]