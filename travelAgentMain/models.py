from django.db import models
from django.conf import Settings, settings 
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import messages
# from PIL import Image
from django.core.exceptions import ValidationError
import re
from crum import get_current_user
from django.db.models.signals import post_save
from django.conf import settings
  
class Statuses(object):
    RECEIVED, PROCESSING, SHIPPED, CLOSED = range(0, 4)
    CHOICES = (
        (RECEIVED, 'Received'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (CLOSED, 'Closed'),
    )
list_attachments_vist = [
            ('work', 'عقد زواج'),
            ('work', 'شهادة وفاه'),
            ('work', 'رخصة قيادة'), # تطلع في نوع التاشيره العمل
            ('omrah', 'عمره'),
            ('haj', 'شهادة ميلاد'),
            ('vist', 'دفتر عائلي'),           
            ('vist', 'اذن سفر'),    
            ('vist', 'سك العزوبية'),           
            # ('other', 'اخرى'),             
    ]

def get_default_User_admin():    
    pass
    # return User.objects.get_or_create(name="admin")[0]


class Visas(models.Model):
    user = models.ForeignKey(User, verbose_name=_('المستخدم'), on_delete=models.SET_NULL, null=True,editable=False)
    modified_by = models.ForeignKey(User, verbose_name=_('اخر تعديل ب:'), on_delete=models.SET_NULL,
                                    related_name="visaEdit", blank=True, null=True, default=get_current_user,
                                    editable=False)
    # user = models.ForeignKey(User, default=get_default_User_admin,verbose_name=_('المستخدم'), on_delete=models.CASCADE)
    code_visa = models.CharField(max_length=100, verbose_name=_('رقم التأشيره'), unique=True)
    record_No = models.CharField(max_length=100, verbose_name=_('رقم السجل'))
    authorization_No = models.CharField(max_length=100, verbose_name=_('رقم التفويض'), blank=True,null=True,default=0)
    visa_type = models.CharField(max_length=100, verbose_name='نوع التأشيره',
                                 choices=(
                                     ('work', 'عمل'),
                                     ('omrah', 'عمره'),
                                     ('haj', 'حج'),
                                     ('vist', 'زياره'),
                                     # ('other', 'اخرى'),
                                 ),
                                 default=("work"))
    count_visa = models.IntegerField(verbose_name=_('عدد التأشيرات'))
    company = models.CharField(max_length=255, verbose_name=_('الشركة'))
    date_added = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'), editable=False)
    active = models.BooleanField(default=True, verbose_name=_('تفعيل'))

    def __str__(self):
        return self.code_visa

    class Meta:
        verbose_name = _('تأشيره')
        verbose_name_plural = _('التأشيرات')
        # ordering = ('pk',)
class Branch(models.Model):
    # id = models.BigAutoField(primary_key=True, verbose_name=_('رقم الفرع'))
    name = models.CharField(max_length=255, verbose_name=_('اسم الفرع'))    
    location = models.CharField(max_length=255, verbose_name=_('الموقع'))    
    active = models.BooleanField(default=True,verbose_name=_('تفعيل'))
    description = models.TextField(verbose_name=_('ملاحظة'),blank=True,)
    
    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = _('فرع')
        verbose_name_plural=_('الفروع')
        # ordering = ('pk',)
# ///////////////////////////////////
class Agent(models.Model):
    user = models.ForeignKey(User, verbose_name=_('المستخدم'), on_delete=models.SET_NULL,editable=False,null=True)
    name = models.CharField(max_length=255, verbose_name=_('الاسم'))    
    addreses = models.CharField(verbose_name=_('العنوان'), null=True, max_length=120)
    mobile = models.CharField(max_length=50 ,verbose_name=_('رقم التلفون'),null='true')
    date = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'))
    active = models.BooleanField(default=True,verbose_name=_('تفعيل')) 
    image_agreement  = models.ImageField(verbose_name='صورة الاتفاقية',  upload_to='image_id/', blank=True, null=True)
    image_id  = models.ImageField(verbose_name='صورة الهوية',upload_to='image_agreements/', blank=True, null=True)
  
    # image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    # state = models.CharField(max_length=50, verbose_name=_('Status'),
    #                          choices=(
    #                              ('pending', 'pending'),
    #                              ('active', 'activate'),
    #                              ('deactive', 'deactivate'),
    #                              ('close', 'Closed'),
    #                          ),
    #                          default=("active"))
    # type = models.CharField(max_length = 200,verbose_name='نوع النشاط',
    #         choices=(
    #         ('merchant', 'تاجر'),
    #         ('broker', 'وسيط'),
    #         ('customer', 'عميل'),
    #         ('other', 'other'),             
    #         ),
    #         default=("other"))
    # image_profile = models.ImageField(default='default.jpg',upload_to='profile_pics') 
    class Meta:
        verbose_name = _('وكيل')
        verbose_name_plural = _('الوكلاء') 
        
    def __str__(self):
        return self.name 
#  //////////// /////////////////////

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name=_('المستخدم'), on_delete=models.SET_NULL,editable=False,null=True)
    name = models.CharField(max_length=255, verbose_name=_('الاسم'))
    state = models.CharField(max_length=50, verbose_name=_('الحالة'),
                             choices=(
                                 ('process', 'تحت الاجراء'),
                                 ('murahal', 'مرحل'),
                                 ('sendTokuafel', 'تسليم قوافل'),
                                 ('moaasher', 'مؤشر'),
                                 ('receveFromkuafel', 'تم الاستلام من قوافل'),
                             ),
                             default=("process"))
    
    job= models.CharField(max_length=250, verbose_name=_('المهنة'), blank=True, null=True) 
    mobile = models.CharField(max_length=50, verbose_name=_('الموبايل'), blank=True, null=True)
    passport_No = models.CharField(max_length=200, verbose_name=_('رقم الجواز'),blank=True, null=True,unique=True)
    visa_No = models.ForeignKey(Visas, verbose_name=_('رقم التأشيره'), on_delete=models.CASCADE)    
    bond_No = models.CharField(max_length=200, verbose_name=_('رقم السند'),blank=True, null=True)
    hospital = models.CharField(max_length=255, verbose_name=_('المستشفى'),blank=True, null=True)
    examination_date  = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الفحص'),blank=True, null=True)
    cost = models.DecimalField( max_digits=8, decimal_places=2,verbose_name=_('المبلغ المتفق'),blank=True, null=True,default=0.00)
    Remaining_Amount= models.DecimalField( max_digits=8, decimal_places=2,verbose_name=_('المبلغ المتبقي'),blank=True, null=True,default=0.00)
    note = models.CharField(max_length=255, verbose_name=_('ملاحظة'),blank=True, null=True)
    branch = models.ForeignKey(Branch, verbose_name=_('الفرع'), on_delete=models.SET_NULL,blank=True,null=True)
    agent = models.ForeignKey(Agent, verbose_name=_('الوكيل'), on_delete=models.SET_NULL, blank=True, null=True)
    date_status = models.DateField(default=timezone.now,verbose_name="تاريخ الحالة", blank=True, null=True)
    murahal_date = models.DateField(verbose_name="تاريخ الترحيل", blank=True, null=True)
    sendTokuafel_date = models.DateField(verbose_name="تاريخ تسليم قوافل", blank=True, null=True)
    moaasher_date = models.DateField(verbose_name="تاريخ التأشير", blank=True, null=True)
    receveFromkuafel_date = models.DateField(help_text='تارخ الاستلام من قوافل', verbose_name="استلام قوافل",blank=True, null=True)
    order_No = models.CharField(max_length=200, verbose_name=_('رقم الطلب'),blank=True, null=True)
    vist_attachments = models.ManyToManyField('travelAgentMain.Customer_Attachments', verbose_name=_('المرفقات'), blank=True)
    health_insurance = models.DecimalField( max_digits=5, decimal_places=2,verbose_name=_('التأمين الصحيس'),blank=True, null=True,default=0.00)
    baptisms = models.CharField(max_length=255, verbose_name=_('التعميدات'),blank=True, null=True)

    date_added = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'))
    modified_by = models.ForeignKey(User,verbose_name=_('اخر تعديل بواسطة:'), on_delete=models.SET_NULL,related_name="CustomerEdit",blank=True,null=True,editable=False)

    active = models.BooleanField( default=True,verbose_name=_('تفعيل'))
    murahal_system = models.BooleanField(help_text='تمت المصادقة من قبل الادارة',default=False,verbose_name=_('مصادقة الادارة'))
    note_murahal_system = models.CharField(max_length=255, verbose_name=_('ملاحظة الادارة'),blank=True, null=True)
    
    class Meta:
        verbose_name = _('عميل')
        verbose_name_plural = _('العملاء')

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None:  # add يعني اذا فارغ الايدي  هنا عملية اضافة
            # print(self.user_id)
            # print('===============++++++++++++++++')
            visa = Visas.objects.filter(code_visa=self.visa_No)
            customer_count = Customer.objects.filter(visa_No=self.visa_No).count()
            if (customer_count >= visa[0].count_visa):
                # print('no count')
                raise ValidationError("وصلت اقصى عدد جوازات لهذة التأشيره")
        else:
            pass
################################ 
class Customer_Attachments(models.Model):     
    name = models.CharField(max_length=255, verbose_name=_('نوع المرفق'))   
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = _('مرفق')
        verbose_name_plural=_('انواع المرفقات')
        # ordering = ('pk',)
# ///////////////////////////////////
class Customer_Status(models.Model):     
    name = models.CharField(max_length=255, verbose_name=_('نوع الحالة'))   
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = _('الحالة')
        verbose_name_plural=_('انواع الحالة')
        # ordering = ('pk',)
# ///////////////////////////////////
class Customer_Status_Date(models.Model):    # نوع التاشيره 
    customer_status = models.ForeignKey(Customer_Status, verbose_name=_('جالة الجواز'), on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, verbose_name=_('المستخدم'), on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'))
    user = models.ForeignKey(User, verbose_name=_('المستخدم'), on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_status.name

    class Meta:
        verbose_name = _('متابعة التأشيره')
        verbose_name_plural=_('تتبع التأشيرات')
        # ordering = ('pk',)
# ///////////////////////////////////
# ///////////////////////////////////
class News(models.Model):
    content = models.CharField(blank=True,max_length=500,verbose_name=_('النص'))     
    date = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'))
    Status = models.BooleanField(default=False, verbose_name=_('المستخدم'))
    # date_start = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ البدء')) 
    user = models.ForeignKey(User, verbose_name=_('المستخدم'), on_delete=models.CASCADE)
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = _('اضافة خبر')
        verbose_name_plural=_('الاخبار')

    
class Mandate(models.Model):    # جدول التفويضات
    name = models.CharField(max_length=255, verbose_name=_('الاسم'))
    job= models.CharField(max_length=250, verbose_name=_('المهنة'), blank=True, null=True) 
    mobile = models.CharField(max_length=50, verbose_name=_('الموبايل'), blank=True, null=True)
    passport_No = models.CharField(max_length=200, verbose_name=_('رقم الجواز'),blank=True, null=True)
    visa_No = models.CharField(max_length=50, verbose_name=_('رقم التأشيره'))    
    bond_No = models.CharField(max_length=200, verbose_name=_('رقم السجل'),blank=True, null=True)    
    date_added = models.DateTimeField(default=timezone.now, verbose_name=_('تاريخ الاظافة'))
    # modified_by = models.ForeignKey(User,verbose_name=_('اخر تعديل بواسطة:'), on_delete=models.SET_NULL,related_name="CustomerEdit",blank=True,null=True,editable=False)  
    class Meta:
        verbose_name = _('تفويض')
        verbose_name_plural = _('التفويضات')
    def __str__(self):
        return self.name 
################################
class Profile(models.Model):
    # image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='اسم المستخدم')
    branch = models.ForeignKey('travelAgentMain.Branch', on_delete=models.SET_NULL, verbose_name='الفرع', blank=True, null=True)
    tel = models.CharField(max_length=20, verbose_name='رقم الهاتف')

    class Meta:
        verbose_name = _('بروفايل المستخدم')
        verbose_name_plural = _('بروفايل المستخدمين')

    def __str__(self):
        return '{} profile.'.format(self.user.username)

    def save(self, *args, **kwarg):  #
        super().save(*args, **kwarg)  #

        # img = Image.open(self.image.path)
        # if img.width > 300 or img.height > 300:
        #         output_siae = (300, 300)
        #         img.thumbnail(output_siae)
        #         img.save(self.image.path)
def create_profile(sender, **kwarg):  #
    if kwarg['created']:
        user_profile = Profile.objects.create(user=kwarg['instance'])  #

post_save.connect(create_profile, sender=User)

################################
class PrintSetting(models.Model):
    # image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    # table = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='اسم المستخدم')
    branch = models.ForeignKey('travelAgentMain.Branch', on_delete=models.SET_NULL, verbose_name='الفرع', blank=True, null=True)
    table_Name = models.CharField(max_length=20, verbose_name='')

    class Meta:
        verbose_name = _('بروفايل المستخدم')
        verbose_name_plural = _('بروفايل المستخدمين')




