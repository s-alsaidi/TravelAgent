import crum
from django.contrib import admin
from crum import get_current_user
from .models import *
from django.utils import timezone
from typing import Set
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from django.db.models import Max
from django.db.models import F
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import TextInput, Textarea
from django.shortcuts import render
# Register your models here.

from django.contrib import messages
from datetime import datetime, timedelta
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.contrib.admin import ModelAdmin, SimpleListFilter
import datetime
from django.contrib.auth.models import Group
from tabular_permissions.admin import TabularPermissionsUserAdmin
from tabular_permissions.admin import TabularPermissionsGroupAdmin
from django.db.models import Count


from django.contrib import messages
from .forms import *
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from .forms import *
from admin_auto_filters.filters import AutocompleteFilter
from import_export.admin import ImportExportModelAdmin
# Register your models here. 
# user = crum.get_current_user()
# # print(user)
# if user and user.is_superuser:
#     admin.site.register(AttachedTypeAdmin, AttachedType)

admin.site.unregister(User) 
@admin.register(User) 
class CustomUserAdmin(ImportExportModelAdmin,UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
admin.site.site_header = 'ابراج مكة' 
class CustomerInline(admin.TabularInline):
    model = Customer
    fields = ('name' , 'job' , 'mobile' , 'passport_No', 'bond_No' ,'hospital', 'examination_date','vist_attachments',)

    classes = ('collapse',)
    # can_delete = True
    # extra=1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'17'})},
        # models.CharField: {'widget': Time(attrs={'size':'15'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':30})},
    }
    autocomplete_fields = ['vist_attachments'] 

class VisaComplateFilter(SimpleListFilter):
    title = "فرز التأشيرات الغير مكتملة"  # a label for our filter
    parameter_name = "visa"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("get", "عرض "), 
        ]
    def queryset(self, request, queryset): 
        if self.value() == "get":
            # print(request)
            # print(self)
            # print(dir(request))
            # result=queryset

            # for ob in  queryset:
            #     print(ob)
            #     count = Customer.objects.filter(visa_No=ob.count_visa).count()
            #     print(count)
            #     if count < ob.count_visa:
            #         pass s
            # result=none
            # result.objects.none()
        #    obj.count_visa
            # queryset.objects.annotate(count_visa=Count('visa_No')).filter(num_players__gt=10)
            # return queryset.distinct().filter(pages__isnull=True)   
            # .annotate(nb_customers=Sum('dealercontact__is_customer'))\
            # questions = Visas.objects.annotate(count_visa = Count('visa_No')  ) # annotate the queryset
            # cats = A.objects.annotate(num_b=Count('b')).filter(num_b__lt=2)
            return queryset.annotate(count_v=Count('customer')).filter(count_v=count_visa)
            # return  questions 
        
@admin.register(Visas)
class VisasAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('code_visas', 'count_visa', 'customer_count','record_No', 'authorization_No', 'visa_type', 'company',  'date_added',)
    # filter_horizontal=()
    search_fields = ('code_visa', 'record_No', 'visa_type', 'active',)
    # list_filter = ('visa_type','user','date_added')
    # exclude = ['user']
    readonly_fields = ('date_added',)
    list_per_page = 500
    # actions_on_bottom = True
    save_on_top = True
    list_filter = (
        ('date_added', DateRangeFilter), 'visa_type', 'user',
        # (VisaComplateFilter),
    ) 
    # inlines = [CustomerInline,]
    actions=('print_to_pdf',)

    def print_to_pdf(self, request, queryset): 
            return render(request,'admin/print_visa.html',context={'customers':queryset})
    print_to_pdf.short_description = 'طباعة '    
    def get_rangefilter_date_added_default(self, request):
        return (datetime.date.today, datetime.date.today) 
    # If you would like to change a title range filter  # method pattern "get_rangefilter_{field_name}_title"
    def get_rangefilter_date_added_title(self, request, field_path):
        return 'تفرير بحسب التاريخ' 
    def customer_count(self, obj):
        count = Customer.objects.filter(visa_No=obj.id).count()
        # result=Customer_Status_Date.objects.filter(customer=obj.id).order_by('-date').first()
        # print(result)
        return count   
    customer_count.short_description = 'عدد العملاء'  # Renames column head
    
         
    def code_visas(self, obj):
        count = Customer.objects.filter(visa_No=obj.id).count()
        if count == obj.count_visa:
            color_code = '447e9b'
        else:
            color_code = 'FF0000'
        html = '<span style="color: #{};">{}</span>'.format(color_code, obj.code_visa)
        return format_html(html)
    code_visas.short_description = 'رقم التأشيرة'  # Renames column head
    
 
    def save_model(self, request, instance, form, change):
        user = request.user 
        if not request.user.is_superuser:
            instance.user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

class AgentFilter(AutocompleteFilter):
    title = 'الوكيل' # display title
    field_name = 'agent' # name of the foreign key field

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
   
    list_display = ('name' , 'passport_No' ,'visa_No','mobile','job' ,'agent','bond_No','health_insurance','cost','Remaining_Amount','state','date_added',)    
    search_fields = ('name','mobile' , 'passport_No','visa_No__code_visa', 'bond_No',) 
    list_filter = (
        ('date_added', DateRangeFilter), 'state','branch','visa_No__visa_type', 'user','murahal_system' ,AgentFilter)
    list_per_page = 500
    # actions_on_bottom = True
    # save_on_top = True
    autocomplete_fields = ['vist_attachments', 'visa_No', 'agent', 'branch']
    readonly_fields =('branch','user','modified_by','date_added',)
    actions=('set_customer_as_process','set_customer_as_murahal','set_customer_as_sendTokuafel','set_customer_as_moaasher',
                 'set_customer_as_receveFromkuafel','print_to_pdf','set_customer_as_murahal_From_Sys',)
    # filter_horizontal = ()
    action_form = UpdateScoreForm 
   
    def get_actions(self, request):
            actions = super(CustomerAdmin, self).get_actions(request)
            if not request.user.is_superuser:
               del actions['set_customer_as_murahal_From_Sys']
            #    del actions[reject_art]
            return actions

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        self.readonly_fields=[] 
        if not request.user.is_superuser:
            # self.exclude.append('murahal_system') #here!
            self.readonly_fields.append('murahal_system') #here!
            self.readonly_fields.append('note_murahal_system')

        return super(CustomerAdmin, self).get_form(request, obj, **kwargs)
   
    def print_to_pdf(self, request, queryset): 
        return render(request,'admin/print_report.html',context={'customers':queryset})
    print_to_pdf.short_description = 'طباعة '    
 
    def get_visa_type(self, obj):
        return obj.visa_No.get_visa_type_display()  # get  قبل الحقل 
        # return obj.visa_No.visa_type
    get_visa_type.admin_order_field = 'visa_type'  # Allows column order sorting
    get_visa_type.short_description = 'نوع التأشيره'  # Renames column head

    def get_rangefilter_date_added_default(self, request):
        return (datetime.date.today, datetime.date.today)
    def get_rangefilter_date_added_title(self, request, field_path):
        return 'تفرير بحسب التاريخ'
    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:  # add new
            instance.user = request.user
            instance.modified_by = request.user
            branch = Profile.objects.filter(user=request.user)
            instance.branch = branch[0].branch
            # instance.save()
            # form.save_m2m()
            # print('----not change-----')
        if form.changed_data:
            instance.modified_by = request.user
            # instance.save()
            # form.save_m2m()
            print('---- changeed-----')
            # return instance
        if 'state' in form.changed_data:
            # print('status change-----------------')
            if (instance.state == "process"):
                instance.date_status = datetime.date.today()
            elif (instance.state == "murahal"):
                instance.date_status = instance.murahal_date
            elif (instance.state == "sendTokuafel"):
                instance.date_status = instance.sendTokuafel_date
            elif (instance.state == "moaasher"):
                instance.date_status = instance.moaasher_date
            elif (instance.state == "receveFromkuafel"):
                instance.date_status = instance.receveFromkuafel_date

        instance.save()
        form.save_m2m()
        return instance
    def set_customer_as_murahal(self,request,queryset):
        
        if request.POST['state_date'] : 
            murahal_date = (request.POST['state_date'])
            print(murahal_date)
            # count = queryset.update(state='murahal')
            count = queryset.update(state='murahal',murahal_date=murahal_date,date_status=murahal_date)
            self.message_user(request, '   {}عملاء تم تعديل الحالة الي مرحل '.format(count))
         
       
        
        # if request.POST.get('post'):
        #     print('aaaaaaaaaarequest.POST[]')
        # else:
        #         print(helpers.ACTION_CHECKBOX_NAME)
        #         context = {
        #             'title': ("Are you sure?"),
        #             'queryset': queryset,
        #             'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        #         }
        #         return TemplateResponse(request, 'admin/change_state_customer.html',context)
    set_customer_as_murahal.short_description = 'تعديل الحالة الى مرحل'  # Renames column head
    
    def set_customer_as_process(self,request,queryset):        
        if request.POST['state_date'] : 
            state_date = (request.POST['state_date'])
            print(state_date) 
            count = queryset.update(state='process',date_status=state_date)
            self.message_user(request, '   {}عملاء تم تعديل الحالة الي تحت الاجراء '.format(count))
    set_customer_as_process.short_description = 'تعديل الحالة الى تحت الاجراء'  # Renames column head
    def set_customer_as_sendTokuafel(self,request,queryset):        
        if request.POST['state_date'] : 
            state_date = (request.POST['state_date'])
            # print(state_date) 
            count = queryset.update(state='sendTokuafel',date_status=state_date,sendTokuafel_date=state_date)
            self.message_user(request, '   {}عملاء تم تعديل الحالة الي   تسليم قوافل '.format(count))
    set_customer_as_sendTokuafel.short_description = 'تعديل الحالة الى  تسليم قوافل'  # Renames column head
    def set_customer_as_moaasher(self,request,queryset):        
        if request.POST['state_date'] : 
            state_date = (request.POST['state_date']) 
            count = queryset.update(state='moaasher',date_status=state_date,moaasher_date=state_date)
            self.message_user(request, '   {}عملاء تم تعديل الحالة الي  مؤشر'.format(count))
    set_customer_as_moaasher.short_description = 'تعديل الحالة الى مؤشر'  # Renames column head
    def set_customer_as_receveFromkuafel(self,request,queryset):        
        if request.POST['state_date'] : 
            state_date = (request.POST['state_date']) 
            count = queryset.update(state='receveFromkuafel',date_status=state_date,receveFromkuafel_date=state_date)
            self.message_user(request, '   {}عملاء تم تعديل الحالة الي استلام من قوافل'.format(count))
    set_customer_as_receveFromkuafel.short_description = 'تعديل الحالة الى استلام من قوافل'  # Renames column head

    def set_customer_as_murahal_From_Sys(self,request,queryset):        
        if request.POST['state_date'] : 
            # state_date = (request.POST['state_date']) 
            count = queryset.update(murahal_system=True)
            self.message_user(request, '   {}عملاء تمت المصادقة     '.format(count))
    set_customer_as_murahal_From_Sys.short_description = 'ترحيل العملاء والمصادقة عليهم'  # Renames column head
     


@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name' , 'location' , 'active' , 'description',)
    # list_display = [field.name for field in Branch._meta.get_fields()]
    search_fields=('name',) 
    list_filter = ()
    
    # readonly_fields =('user',)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs    
    #     return qs.filter(user=request.user)

@admin.register(Agent)
class AgentAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display = ('name' , 'addreses' , 'mobile' , 'date', 'active' ,)
    # list_display = [field.name for field in Agent._meta.get_fields()]
    search_fields=('name',) 
    # list_filter = ()
    
    readonly_fields =('user',)

# @admin.register(Statuses)
# class StatusesAdmin(admin.ModelAdmin):
#     list_display = ('name',)   
#     search_fields=('name',) 
#     list_filter = ()
# @admin.register(Customer_Status)
# class Customer_StatusAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields=('name',)
#     list_filter = ()
@admin.register(Customer_Attachments)
class Customer_AttachmentsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name',)   
    search_fields=('name',) 
    list_filter = ()
# @admin.register(Customer_Status_Date)
# class Customer_Status_DateAdmin(admin.ModelAdmin):
#     list_display = ('customer_status','customer','date')
#     search_fields=('customer',)
#     list_filter = ()

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('status',)
#     list_filter = (StatusListFilter,)

@admin.register(Profile)
class AgentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('user', 'branch', 'tel',)
    # list_display = [field.name for field in Agent._meta.get_fields()]
    # search_fields=('name',)
    list_filter = ()

    # readonly_fields =('user',)
@admin.register(Mandate)
class MandateAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name','mobile','job','passport_No','visa_No','bond_No','date_added')
    # list_display = [field.name for field in Mandate._meta.get_fields()]
    search_fields=('name','mobile','passport_No','visa_No','bond_No')
    list_filter = ()
@admin.register(News)
class NewsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('content','date','Status',)
    # list_display = [field.name for field in Mandate._meta.get_fields()]
    # search_fields=('name','mobile','passport_No','visa_No','bond_No')
    list_filter = ()
 


# admin.site.unregister(Group)

class ExtendUserAdmin(TabularPermissionsUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', )
    # list_select_related = ('userprofile',)
    readonly_fields = ('last_login', 'date_joined',)
    raw_id_fields = ('user_permissions',)
    autocomplete_fields=('groups',)
    filter_horizontal = ()
    fieldsets = (
        (None,
        {'fields': ('username', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),

        (_('Permissions'),
        {'fields': ('is_active', 'is_staff',),
                                'classes':("col-md-12", '& col-md-12'),
                            }),
        (_('ادارة صلاحيات المستخدم'), {'fields': ('user_permissions',),
                                 'classes':("col-md-12" , ' & col-md-12'),
                             }),
        (_('Groups'), {'fields': ('groups',),
                                 'classes':("col-md-12", "collapse" , " & col-md-12"),
                            }),
         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # def get_profile(self, instance):
    #     return instance.userprofile.display_name

    # get_profile.short_description = _('Profile')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, ExtendUserAdmin)
class ExtendGroupAdmin(TabularPermissionsGroupAdmin):
    list_display = ('name',)
    # raw_id_fields = ('groups',)
    filter_horizontal = ()
    fieldsets = (
        (None, {
            'fields': (
                'name',
            ),
            'classes':("col-md-12", '& col-md-12'),
        }),
        (None, {
            'fields': (
                'permissions',
            ),
            'classes':("col-md-12", '& col-md-12'),
        }),
    )
admin.site.unregister(Group)
admin.site.register(Group,ExtendGroupAdmin)

