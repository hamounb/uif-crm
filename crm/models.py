from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def documents_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"{instance.user.id} - {instance.customer.company}/{filename}"
    # "{0}/{1}".format(instance.user.id, filename)


class BaseModel(models.Model):
    user_modified = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_modified',
        null=True,
        blank=True,
        verbose_name='کاربر ویرایش'
        )
    user_created = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_created',
        null=True,
        blank=True,
        verbose_name='کاربر ایجاد'
        )
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ تغییرات', auto_now=True)

    class Meta:
        abstract = True


class CustomerModel(BaseModel):
    STATE_REAL = 'real'
    STATE_LEGAL = 'legal'
    STATE_CHOICES = (
        (STATE_REAL, 'حقیقی'),
        (STATE_LEGAL, 'حقوقی')
    )
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    sid = models.CharField(verbose_name='کد معین', max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    state = models.CharField(verbose_name='نوع مشارکت کننده', max_length=50, choices=STATE_CHOICES, default=STATE_REAL)
    firstname = models.CharField(verbose_name='نام', max_length=50)
    lastname = models.CharField(verbose_name='نام خانوادگی', max_length=50)
    fathername = models.CharField(verbose_name='نام پدر', max_length=50)
    code = models.CharField(verbose_name='کدملی', max_length=10)
    ceoname = models.CharField(verbose_name='نام مدیرعامل', max_length=100, null=True, blank=True)
    company = models.CharField(verbose_name='نام تجاری/شرکت', max_length=100)
    ncode = models.CharField(verbose_name='شناسه ملی', max_length=11, null=True, blank=True)
    mobile = models.CharField(verbose_name='موبایل', max_length=11)
    phone = models.CharField(verbose_name='تلفن', max_length=11, null=True, blank=True)
    fax = models.CharField(verbose_name='فکس', max_length=11, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    postalcode = models.CharField(verbose_name='کد پستی', max_length=10)
    address = models.TextField(verbose_name='آدرس')

    def __str__(self):
        return f"{self.company}"
    
    class Meta:
        verbose_name = 'مشارکت کننده'
        verbose_name_plural = 'مشارکت کنندگان'


class DocumentsModel(BaseModel):
    STATE_WAIT = 'wait'
    STATE_ACCEPT = 'accept'
    STATE_DENY = 'deny'
    STATE_CHOICES = (
        (STATE_WAIT, 'در انتظار بررسی'),
        (STATE_ACCEPT, 'قبول شده'),
        (STATE_DENY, 'رد شده')
    )
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    state = models.CharField(verbose_name='وضعیت', max_length=50, choices=STATE_CHOICES, default=STATE_WAIT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مشارکت کننده')
    file = models.FileField(verbose_name='مدرک', upload_to=documents_directory_path)

    def __str__(self):
        return f"{self.customer.company} - {self.file.name}"
    
    class Meta:
        verbose_name = 'مدرک'
        verbose_name_plural = 'مدارک'


class ExhibitionModel(BaseModel):
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    sid = models.CharField(verbose_name='کد معین', max_length=50, null=True, blank=True)
    title = models.CharField(verbose_name='عنوان نمایشگاه', max_length=200)
    price = models.CharField(verbose_name='قیمت', max_length=20)
    value_added = models.CharField(verbose_name='ارزش افزوده', max_length=10)
    date = models.DateField(verbose_name='تاریخ برگزاری', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.date.year}"
    
    class Meta:
        verbose_name = 'نمایشگاه'
        verbose_name_plural = 'نمایشگاه‌ها'


class RequestModel(BaseModel):
    STATE_WAIT = 'wait'
    STATE_ACCEPT = 'accept'
    STATE_DENY = 'deny'
    STATE_CHOICES = (
        (STATE_WAIT, 'در انتظار بررسی'),
        (STATE_ACCEPT, 'قبول شده'),
        (STATE_DENY, 'رد شده')
    )
    state = models.CharField(verbose_name='وضعیت', max_length=50, choices=STATE_CHOICES, default=STATE_WAIT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, verbose_name='مشارکت کننده')
    exhibition = models.ForeignKey(ExhibitionModel, on_delete=models.CASCADE, verbose_name='نمایشگاه')
    area = models.IntegerField(verbose_name='متراژ', default=0)
    rules = models.BooleanField(verbose_name='قوانین')
    is_active = models.BooleanField(verbose_name='فعال', default=True)

    def __str__(self):
        return f"{self.customer.company} - {self.exhibition.title}"
    
    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست‌ها'


class MessagesModel(BaseModel):
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, verbose_name='مشارکت کننده')
    text = models.TextField(verbose_name='متن پیام')

    def __str__(self):
        return f"{self.customer.company} - ({self.customer.firstname} {self.customer.lastname})"
    
    class Meta:
        verbose_name = 'پیغام'
        verbose_name_plural = 'پیغام‌ها'


class InvoiceModel(BaseModel):
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مشارکت کننده')
    exhibition = models.ForeignKey(ExhibitionModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='نمایشگاه')
    price = models.CharField(verbose_name='مبلغ', max_length=20)
    area = models.IntegerField(verbose_name='متراژ', default=0)
    value_added = models.IntegerField(verbose_name='متراژ', default=0)
    discount = models.CharField(verbose_name='تخفیف', max_length=20, null=True, blank=True)
    total_price = models.CharField(verbose_name='مبلغ', max_length=20)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)

    def __str__(self):
        return f"{self.customer.company} - {self.exhibition.title} - {self.price}"
    
    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتورها'