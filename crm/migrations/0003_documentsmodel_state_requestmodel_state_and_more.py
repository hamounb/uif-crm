# Generated by Django 4.2 on 2024-04-18 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0002_rename_postcode_customermodel_postalcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentsmodel',
            name='state',
            field=models.CharField(choices=[('wait', 'در انتظار بررسی'), ('accept', 'قبول شده'), ('deny', 'رد شده')], default='wait', max_length=50, verbose_name='وضعیت'),
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='state',
            field=models.CharField(choices=[('wait', 'در انتظار بررسی'), ('accept', 'قبول شده'), ('deny', 'رد شده')], default='wait', max_length=50, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='company',
            field=models.CharField(max_length=100, verbose_name='نام تجاری/شرکت'),
        ),
        migrations.AlterField(
            model_name='documentsmodel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customermodel', verbose_name='مشارکت کننده'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='exhibition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.exhibitionmodel', verbose_name='نمایشگاه'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.CreateModel(
            name='MessagesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customermodel', verbose_name='مشارکت کننده')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'پیغام',
                'verbose_name_plural': 'پیغام\u200cها',
            },
        ),
    ]
