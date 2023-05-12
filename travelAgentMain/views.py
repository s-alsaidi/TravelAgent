from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    custormer_state=''
    try:

        if request.method == 'POST':

            id = request.POST['id']
            custormer_state=Customer.objects.filter(passport_No=id)[0]
            print('====================')
            print(id)
            print(custormer_state)
            print('====================')  
    except:
         print('not found')
   
    news=News.objects.filter(Status=True)
    context={
        'title': ' الصفحة الرئيسية',
        'news':news,
        'state':custormer_state
    }
    return   render(request, 'travelAgentMain/index.html', context)
def family(request):
    return   render(request, 'travelAgentMain/family.html', {'title': 'متطلبات الزياره العائلية'})
def work(request):
    return   render(request, 'travelAgentMain/work.html', {'title': 'مطلبات فيزة العمل'})
def ekamah(request):
    return   render(request, 'travelAgentMain/ekamah.html', {'title': 'مطلبات الاقامة'})
def mandate(request):
    if request.method == 'POST':
        name = request.POST['name']
        job = request.POST['job']
        mobile = request.POST['mobile']
        passport_No = request.POST['passport_No']
        visa_No = request.POST['visa_No']
        bond_No = request.POST['bond_No'] 
        mandate = Mandate.objects.create(name=name,job=job,mobile=mobile,passport_No=passport_No,visa_No=visa_No,bond_No=bond_No)
        print(mandate) 
        # print('====================')
        if mandate:
            messages.success(request,'تم اضافة التفويض بنجاح')
        else:
            messages.warning(request,'هناك خطا')
    return   render(request, 'travelAgentMain/mandate.html', {'title': 'اضافة تفويض'})
def add_mandate(request,id):
    print("mandate[[[[[[[[") 

    if request.method == 'POST':
        name = request.POST['name']
        job = request.POST['job']
        mobile = request.POST['mobile']
        passport_No = request.POST['passport_No']
        visa_No = request.POST['visa_No']
        bond_No = request.POST['bond_No'] 
        mandate = Mandate.objects.create(name=name,job=job,mobile=mobile,passport_No=passport_No,visa_No=visa_No,bond_No=bond_No)
        print(mandate) 
        # print('====================')
        if mandate:
            messages.success(request,'تم اضافة التفويض بنجاح')
        else:
            messages.warning(request,'هناك خطا')
    return   render(request, 'travelAgentMain/mandate.html', {'title': 'اضافة تفويض'})
