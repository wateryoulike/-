from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Engineer
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    cateId = 1
    context = {
        'cateId': cateId
    }
    return render(request, 'index.html', context=context)

def sort(request):
    now_page = int(request.GET.get('page', '1'))
    sex_sort = int(request.POST.get('sex_sort', '-1'))
    education_sort = int(request.POST.get('education_sort', '-1'))
    basic_wage_sort = int(request.POST.get('basic_wage_sort', '-1'))
    seniority_sort = int(request.POST.get('seniority_sort', '-1'))
    print(sex_sort, education_sort, basic_wage_sort, seniority_sort)


    cateId = 2
    datas = Engineer.objects.all()
    if sex_sort != -1 and sex_sort != -2:
        if education_sort != -1 and education_sort != -2:
            datas = Engineer.objects.filter(Q(education=education_sort) & Q(sex=sex_sort))
        else:
            datas = Engineer.objects.filter(sex=sex_sort)
    else:
        if education_sort != -1 and education_sort != -2:
            datas = Engineer.objects.filter(education=education_sort)

    if basic_wage_sort == 0:
        datas = datas.order_by('-basic_wage')
    else:
        datas = datas.order_by('basic_wage')

    if seniority_sort == 0:
        datas = datas.order_by('-seniority')
    else:
        datas = datas.order_by('seniority')

    datas = datas.values()
    all_num = len(datas)
    datas = datas[(now_page-1) * 8: now_page * 8]

    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))

    sort = {
        'sex_sort': sex_sort,
        'education_sort': education_sort,
        'seniority_sort': seniority_sort,
        'basic_wage_sort': basic_wage_sort,
    }
    context = {
        'cateId': cateId,
        'datas': datas,
        'all_years': all_years,
        'num': all_num,
        'sort': sort,
        'is_sort': 1,
        'now_page': now_page
    }
    return render(request, 'workerList.html', context=context)

def workerList(request):
    now_page = int(request.GET.get('page', '1'))
    cateId = 2
    datas = Engineer.objects.filter().values()
    all_num = len(datas)
    datas = datas[(now_page-1) * 8: now_page * 8]
    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))
    print(all_years)

    sort = {
        'sex_sort': -1,
        'education_sort': -1,
        'seniority_sort': -1,
        'basic_wage_sort': -1,
    }

    context = {
        'cateId': cateId,
        'datas': datas,
        'all_years': all_years,
        'num': all_num,
        'sort': sort,
        'now_page': now_page
    }
    return render(request, 'workerList.html', context=context)

def calculation(request):
    cateId = 3
    context = {
        'cateId': cateId
    }
    return render(request, 'calculation.html', context=context)

def engineer_detail(request):
    if request.is_ajax():
        data = json.loads(request.body)
        id = int(data['id'])
        datas = Engineer.objects.filter(id=id).values()[0]
        datas['birth_date'] = datas['birth_date'].strftime("%Y-%m-%d")
        print(id, datas)

        context = {
            'datas': datas,
        }
        return JsonResponse(context, safe=False)


def hand_calculation(request):
    cateId = 3
    context = {
        'cateId': cateId
    }
    return render(request, 'calculation.html', context=context)

def aboutUs(request):
    cateId = 4
    context = {
        'cateId': cateId
    }
    return render(request, 'aboutUs.html', context=context)

def login(request):
    return render(request, 'login.html')

def handLogin(request):
    data = json.loads(request.body)
    account = data['account']
    password = data['password']
    print(account, password)
    if account == 'root' and password == 'password':
        loginStatus = 1
        request.session['loginStatus'] = True
    else:
        loginStatus = 0
    cateId = 1
    context = {
        'cateId': cateId,
        'loginStatus': loginStatus,
    }
    return JsonResponse(context, safe=False)

def update_message(request):
    ID = int(request.POST.get('ID', '1'))
    print(ID, type(ID))
    name = request.POST.get('name', '')
    number = request.POST.get('number', '')
    sex = request.POST.get('sex', '')
    birth_date = request.POST.get('birth_date', '')
    education = request.POST.get('education', '')
    hometown = request.POST.get('hometown', '')
    address = request.POST.get('address', '')
    telphone = request.POST.get('telphone', '')
    seniority = request.POST.get('seniority', '')
    basic_wage = request.POST.get('basic_wage', '')
    print(ID, name, number, sex, birth_date, education, hometown, address, telphone, seniority, basic_wage)
    human = Engineer.objects.get(pk=ID)
    human.name = name
    human.number = number
    human.sex = sex
    human.birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    human.education = education
    human.hometown = hometown
    human.address = address
    human.telphone = telphone
    human.seniority = seniority
    human.basic_wage = basic_wage
    human.save()

    datas = Engineer.objects.filter().values()
    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))
    print(all_years)
    cateId = 2

    context = {
        'cateId': cateId,
        'datas': datas,
        'all_years': all_years,
    }

    return render(request, 'workerList.html', context=context)


def add_message(request):
    name = request.POST.get('name', '')
    number = request.POST.get('number', '')
    sex = request.POST.get('sex', '')
    birth_date = request.POST.get('birth_date', '')
    education = request.POST.get('education', '')
    hometown = request.POST.get('hometown', '')
    address = request.POST.get('address', '')
    telphone = request.POST.get('telphone', '')
    seniority = request.POST.get('seniority', '')
    basic_wage = request.POST.get('basic_wage', '')
    print(name, number, sex, birth_date, education, hometown, address, telphone, seniority, basic_wage)
    human = Engineer(name=name, number=number, sex=sex, birth_date=birth_date, education=education, hometown=hometown, address=address, telphone=telphone, seniority=seniority, basic_wage=basic_wage)
    human.save()

    datas = Engineer.objects.filter().values()
    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))
    cateId = 2

    context = {
        'cateId': cateId,
        'datas': datas,
        'all_years': all_years,
    }

    return render(request, 'workerList.html', context=context)


def delete_message(request):
    id = int(request.POST.get('delete_id', '0'))
    human = Engineer.objects.filter(pk=id)
    print(human, id)
    if human.exists():
        human.delete()
    else:
        print("kongkongkongkong")

    cateId = 2
    datas = Engineer.objects.filter().values()
    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))

    context = {
        'cateId': cateId,
        'datas': datas,
        'all_years': all_years,
    }
    return render(request, 'workerList.html', context=context)

def select_message(request):
    search = request.POST.get('search', '')
    cateId = 2
    datas = Engineer.objects.filter(Q(number__icontains=search) | Q(name__icontains=search)).values()
    for key, data in enumerate(datas):
        datas[key]['birth_date'] = datas[key]['birth_date'].strftime("%Y-%m-%d")
    all_years = list(range(1, 51))

    context = {
        'cateId': cateId,
        'searchResult': 0,
        'searchContent': search,
        'datas': datas,
        'all_years': all_years,
    }
    return render(request, 'workerList.html', context=context)

