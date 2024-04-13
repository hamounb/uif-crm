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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    state = models.CharField(verbose_name='نوع مشارکت کننده', max_length=50, choices=STATE_CHOICES, default=STATE_REAL)
    firstname = models.CharField(verbose_name='نام', max_length=50)
    lastname = models.CharField(verbose_name='نام خانوادگی', max_length=50)
    fathername = models.CharField(verbose_name='نام پدر', max_length=50)
    ncode = models.CharField(verbose_name='کدملی', max_length=10)
    ceoname = models.CharField(verbose_name='نام مدیرعامل', max_length=100)
    company = models.CharField(verbose_name='نام تجاری', max_length=100)
    ncode = models.CharField(verbose_name='شناسه ملی', max_length=11)
    mobile = models.CharField(verbose_name='موبایل', max_length=11)
    phone = models.CharField(verbose_name='تلفن', max_length=11, null=True, blank=True)
    fax = models.CharField(verbose_name='فکس', max_length=11, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    postcode = models.CharField(verbose_name='کد پستی', max_length=10)
    address = models.TextField(verbose_name='آدرس')

    def __str__(self):
        return f"{self.company}"
    
    class Meta:
        verbose_name = 'مشارکت کننده'
        verbose_name_plural = 'مشارکت کنندگان'

class DocumentsModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مشارکت کننده')
    file = models.FileField(verbose_name='مدرک', upload_to=documents_directory_path)

    def __str__(self):
        return f"{self.customer.company} - {self.file.name}"
    
    class Meta:
        verbose_name = 'مدرک'
        verbose_name_plural = 'مدارک'

class ExhibitionModel(BaseModel):
    title = models.CharField(verbose_name='عنوان نمایشگاه', max_length=200)
    price = models.CharField(verbose_name='قیمت', max_length=20)
    value_added = models.CharField(verbose_name='ارزش افزوده', max_length=10)
    date = models.DateField(verbose_name='تاریخ برگزاری', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.date.year}"
    
    class Meta:
        verbose_name = 'نمایشگاه'
        verbose_name_plural = 'نمایشگاه‌ها'

class InvoiceModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مشارکت کننده')
    exhibition = models.ForeignKey(ExhibitionModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='نمایشگاه')
    price = models.CharField(verbose_name='مبلغ', max_length=20)
    area = models.IntegerField(verbose_name='متراژ', default=0)
    discount = models.IntegerField(verbose_name='تخفیف', default=0)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)