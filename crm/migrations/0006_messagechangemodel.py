# Generated by Django 4.2 on 2024-05-30 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0005_alter_invoicemodel_total_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageChangeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.messagesmodel', verbose_name='پیغام اصلی')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'پیغام ویرایش شده',
                'verbose_name_plural': 'پیغام\u200cهای ویرایشی',
            },
        ),
    ]
