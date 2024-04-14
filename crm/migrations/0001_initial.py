# Generated by Django 4.2 on 2024-04-14 15:01

import crm.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('sid', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد معین')),
                ('state', models.CharField(choices=[('real', 'حقیقی'), ('legal', 'حقوقی')], default='real', max_length=50, verbose_name='نوع مشارکت کننده')),
                ('firstname', models.CharField(max_length=50, verbose_name='نام')),
                ('lastname', models.CharField(max_length=50, verbose_name='نام خانوادگی')),
                ('fathername', models.CharField(max_length=50, verbose_name='نام پدر')),
                ('code', models.CharField(max_length=10, verbose_name='کدملی')),
                ('ceoname', models.CharField(max_length=100, verbose_name='نام مدیرعامل')),
                ('company', models.CharField(max_length=100, verbose_name='نام تجاری')),
                ('ncode', models.CharField(max_length=11, verbose_name='شناسه ملی')),
                ('mobile', models.CharField(max_length=11, verbose_name='موبایل')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='تلفن')),
                ('fax', models.CharField(blank=True, max_length=11, null=True, verbose_name='فکس')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('postcode', models.CharField(max_length=10, verbose_name='کد پستی')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'مشارکت کننده',
                'verbose_name_plural': 'مشارکت کنندگان',
            },
        ),
        migrations.CreateModel(
            name='ExhibitionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('sid', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد معین')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان نمایشگاه')),
                ('price', models.CharField(max_length=20, verbose_name='قیمت')),
                ('value_added', models.CharField(max_length=10, verbose_name='ارزش افزوده')),
                ('date', models.DateField(blank=True, null=True, verbose_name='تاریخ برگزاری')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'نمایشگاه',
                'verbose_name_plural': 'نمایشگاه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('area', models.IntegerField(default=0, verbose_name='متراژ')),
                ('rules', models.BooleanField(verbose_name='قوانین')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.customermodel', verbose_name='مشارکت کننده')),
                ('exhibition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.exhibitionmodel', verbose_name='نمایشگاه')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'درخواست',
                'verbose_name_plural': 'درخواست\u200cها',
            },
        ),
        migrations.CreateModel(
            name='InvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('price', models.CharField(max_length=20, verbose_name='مبلغ')),
                ('area', models.IntegerField(default=0, verbose_name='متراژ')),
                ('value_added', models.IntegerField(default=0, verbose_name='متراژ')),
                ('discount', models.CharField(blank=True, max_length=20, null=True, verbose_name='تخفیف')),
                ('total_price', models.CharField(max_length=20, verbose_name='مبلغ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.customermodel', verbose_name='مشارکت کننده')),
                ('exhibition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.exhibitionmodel', verbose_name='نمایشگاه')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'فاکتور',
                'verbose_name_plural': 'فاکتورها',
            },
        ),
        migrations.CreateModel(
            name='DocumentsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('file', models.FileField(upload_to=crm.models.documents_directory_path, verbose_name='مدرک')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.customermodel', verbose_name='مشارکت کننده')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ایجاد')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user_modified', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ویرایش')),
            ],
            options={
                'verbose_name': 'مدرک',
                'verbose_name_plural': 'مدارک',
            },
        ),
    ]