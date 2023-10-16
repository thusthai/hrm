from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from django.db.models import Q 
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from hmdb.models import Empmas,TblDepartment ,EmployeeType,EmpCtlDb,EmpDeduction,EmpExper,EmpIncExpDb,EmpTime,TblShift,EmpTranLeave
from hmdb.models import EmpPeriod,EmpPosition,EmpReference,TaxDeduction,dailyTransaction,EmpTransaction,grade,EmpEducation,gradeMajor,EmpmasIncome
from hmdb.models import empstatisticbydep, empstatistic ,TblOT ,TblLeave ,EmpmasResign ,timeshift,TimeMast

from hmadmin.models import AuthUser

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect,JsonResponse,HttpResponse
from django.db.models import Q , Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,authenticate,logout
from .forms import NewUserForm ,TransactionFormSet,TransactionModelFormset,DtransactionHead,DTransactionForm,EmployeeForm,EmployeeExperienceForm,EmpDeductionForm
from .forms import EmpReferenceForm,EmpDeductionForm,EmployeeEducationForm,EmployeeExperienceForm,EmployeeIncomeForm,IncExpForm,FrmCreateData,FrmEmpTransaction

from .forms import FrmEmpmasIncome ,TimeDataForm , EmpTranLeaveForm ,EmpmasResignForm ,TimeImportForm

from hmadmin.views import GetUserDetail,GetAppList,GetAppId
#from erpadmin.views import GetUserDetail ,GetAppList
from django.utils.dateparse import parse_datetime
 
from datetime import date ,timedelta ,datetime ,time
#import datetime 
import array 
# login request
def CalculateTime(t_h_st,t_m_st,t_hour,t_min):
    numTime = ((int(t_hour) - int(t_h_st) ) * 60) + int(t_min) - int(t_m_st)
    return (numTime)

def dayName(dayofweek):
    if dayofweek == 0 :
        dayname = "วันจันทร์"
    elif dayofweek== 1 :
        dayname = "วันอังคาร"
    elif dayofweek ==2 :
        dayname = "วันพุธ"
    elif dayofweek == 3 :
        dayname = "วันพฤหัส"
    elif dayofweek == 4 :
        dayname = "วันศุกร์"
    elif dayofweek == 5 :
        dayname = "วันเสาร์"    
    elif dayofweek == 6 :
        dayname = "วันอาทิตย์" 
    
    return (dayname)

@csrf_exempt
def create_session(request):
    request.session['username'] = ''
    request.session['is_admin'] = False
    
def custom404(request, exception=None):
    return JsonResponse( {  
        'status_code': 404 ,
        'error': 'The resource was not found'
    })
    
@login_required(login_url='login')
def index(request):
    
    #username = use

    username= request.session['username']
    if username is None:
        return redirect(reverse('login'))
    else:
        user = GetUserDetail(username)
        dep =user.dep
        department = dep.dep_code
        is_superuser = user.is_superuser
    print (user , is_superuser ,department )
    
    context = {
        'username':username,
        'department':department,
        }

    return render(request,'index.html',context)
          
# Create your views here.
def register_request(request):
    
    form = NewUserForm()
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"ลงทะเบียนเรียบร้อย")
            return redirect('index')
        else:
            messages.error(request,'Error: ลงทะเบียนไม่สำเร็จกรุณาติดต่อ admin เพื่อช่วยเหลือ')

    return render(request, 'register.html', context={"register_form":form})


def login_request(request):
    form= AuthenticationForm()

    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username} ")

                request.session['username'] = username
                request.session.set_expiry(0)

                return redirect("index")
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"invalid username or password")

    return render(request,'login.html',context={'login_form':form})

def logout_request(request):
    
    logout(request)

    #if 'username' in request.session['username']:
    #   del request.session['username']

    return redirect(reverse('login'))


## end of login

## application
""" 


def GetAppId(app):
    appid = TblAllowApp.objects.filter(Q(app = app))
    if appid.count() == 1 :
        return (appid)
    else:
        pass
        return (0)
    
def GetAppList(user,appname):
#1. ตรวจสอบสิทธิ์ในตาราง content_type ได้ค่า content_type_id 
#2. ตรวจสอบค่าในตาราง TbluserAuth ตาม userid และ content id 

    content = ContentType.objects.get(model=appname)
    print('ContentType ID:', content.id , content.app_label , content.model) 
    #appid = TblAllowApp.objects.get(app = app)
    
    try:
        app = TblUserAuth.objects.get(
                            user = user , 
                            content_type = content.id  
                        )
    except: 
        app = None 
    
    print(app)
   
    return (app)
  
def GetUserDetail(usrname):
    
    user = AuthUser.objects.get(username=usrname)

    
    return (user)
""" 

def hmhome(request):
    username= request.session['username']
    if username is None:
        return redirect(reverse('login'))
    else:
        user = GetUserDetail(username)
        department = GetUserDetail(username).dep
        is_superuser = GetUserDetail(username).is_superuser
        
        #appList = GetAppList(userid)
        
        
        print(user.id , ' ' , username,'is super user:' , is_superuser , department)
        
      #  print(grouplist)
        #print(perm_list)


    context = {'username':username,'department':department.dep_code}

    return render(request,'index.html',context)
    
    #return render(request,'index.html')

def menu_hm(request):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    department = user.dep.dep_code
    
    context = { 'username': username ,
               'department': department ,
               }
    return render(request, 'hm_menu.html',context)

def tadashboard(request):  # Fist Dashboard
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    department = user.dep.dep_code
    
    employeetype = EmployeeType.objects.all()
    
    print("RUN TADASHBOARD " , employeetype)
    
    for item in employeetype: 
            
        item_ingroup = Empmas.objects.filter(
   
                            Q(emp_type = item.cde),
                            Q(workstatus=0) 
                            )
        
        num_item_ingroup = item_ingroup.count()
        
        item.num_item = num_item_ingroup
        item.save()
   
    context = {
            'username':username,
            'department':department, 
            'employeetype': employeetype,
            'period' : None,
        }
    
    return render(request,'ta-dashboard.html',context)

def tadashboardbyperiod(request,emptype):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    department = user.dep.dep_code
    
    periods = EmpPeriod.objects.filter(
                Q(emptype__cde = emptype )
            ) 
    EmpType  = EmployeeType.objects.get(cde=emptype)
    
    print ("TA DASHBOARD BY PERIOD " , emptype )
    
    for period in periods :
        num= EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype ) ,
                Q(period__cde = period.cde)   
            ).count()
        
        period.num = num
        period.save()
     
        
        #period[i].save()
        
    #print (Period[0],Period[1],Period[2])
    periods = EmpPeriod.objects.filter(
                Q(emptype__cde = emptype ) ,
                Q(num__gt=0)
            ).order_by('-cde')
      
    context = {
            'username':username,
            'department':department, 
            'emptype': emptype,
            'periods' : periods ,
            'EmpType' : EmpType
        }
    
    return render(request,'ta-dashboard-by-period.html',context)

#แสดงรายการการทำงานประจำวัน
def menu_time(request,emptype,period): 
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    department = user.dep.dep_code
    
    EmpType = EmployeeType.objects.get(cde = emptype)
    
    fmt_date = "%Y-%m-%d"
    
    txt_work = "WORK"
    txt_leave = "ล"
    
    sdate =date.today()  # "21/07/2023"
 
    print("run Menu-time By date:" , emptype , period )
    
    # list all data Where emptype = emptype and period = period 
    alldateinperiod = EmpPeriod.objects.get(cde=period)
    startdate = alldateinperiod.work_start_date #class:datetime.datetime
    enddate = alldateinperiod.work_end_date
    
    s_date = startdate.strftime(fmt_date)
    e_date = enddate.strftime(fmt_date)
        
    #print("0" ,s_date,e_date , type(s_date) )
    
    timedata = EmpTime.objects.filter(
            Q(emp_cde__emp_type = emptype ) ,
            Q(period__cde = period )
    ).order_by('-workdate')
    
    #print('จำนวนรายการ' , timedata.count())
    
    # st_date= startdate.strftime('%Y-%m-%d') #class=str
    #end_date = enddate.strftime('%Y-%m-%d')
    st_date = startdate
    end_date = enddate
    
    #print("1" , st_date, end_date ,type(st_date) , type(end_date))

    i = 0
    while st_date <= end_date:
        
        #date_work = ได้ค่าเป็น YYYY-MM-DD จากการแปลงข้อมูลวันที่ YYYY-MM-DD HH:MM:SS 
        date_work = st_date.strftime('%Y-%m-%d')  # print("workdate=" , date_work ) # output as string= "YYYY-MM-DD" 
        d = datetime.strptime(date_work,'%Y-%m-%d')  #format as datetime  'YYYY-MM-DD HH:MM:SS
        dayofweek = d.weekday() # 1:อังคาร 2:พุธ ... 6. อาทิตย์ 7: จันทร์
        dayname = dayName(dayofweek) 
        
        timedata =EmpTime.objects.filter(
            Q(emp_cde__emp_type = emptype ) ,
            Q(period__cde = period  ), 
            Q(workdate=date_work )
            )
        
        if timedata.count() != 0 :
            num_work = timedata.filter(
                Q(timein__isnull=False)|
                Q(timeout__isnull=False)
            ).count()

            num_absent = timedata.filter(
                Q(timein__isnull=True), # เงื่อนไข ไม่มีการบันทึกเวลาเข้า ออก
                Q(timeout__isnull=True)
            ).count()
            
            num_leave =timedata.filter(
                
                Q(leavecode__isnull= False )
                ).count()
        #n_leave = data_leave.count()
        
            num_late =timedata.filter(
                Q(numlate__gt = 0 )
            ).count()
            
            #if num_absent != 0:
            #    print (date_work , num_absent )
       
        else:
            num_work = 0
            num_absent = 0
            num_late=0
            num_leave =0 
        
            
        
        if dayofweek == 6: # วันอาทิตย์
           # print(dayofweek , dayname ,date_work)
            num_absent=0
            num_leave=0
        
        try:
            Emp_statistic = empstatistic.objects.filter(
                            Q(emp_type__cde = emptype),
                            Q(workdate=date_work),
                            )
            
          #  print("data found" , Emp_statistic.count() )
        except:
            Emp_statistic = empstatistic.objects.none  #[]
            #  print("data not found")
        
        #print(Emp_statistic[0].id , Emp_statistic[0].n_work , Emp_statistic[0].n_absent )
            
        if Emp_statistic.count() != 0 :   # mean data found
            #emptran.update(num=snum,numhour=snumhour,payamt=spayamt)
          
            Emp_statistic.update(n_work=num_work ,
                                n_leave=num_leave,
                                n_absent=num_absent,
                                n_late=num_late ,
                                emp_type = EmpType,
                                dayofweek = dayname 
                        )
           
        
        else: # not found then add new data into empstatistic
            Emp_statistic= empstatistic(workdate=date_work , 
                                        n_work = num_work , 
                                        n_leave=num_leave,
                                        n_absent=num_absent,
                                        n_late=num_late,
                                        emp_type=EmpType,
                                        dayofweek = dayname
                                        )
            Emp_statistic.save() 

        st_date = st_date + timedelta(days=1) 
        i += 1
    #end loop ALL date IN PERIOD
    
    
    #s_date = startdate.strftime(fmt_date)    
    #e_date = enddate.strftime(fmt_date)
    
    #render ข้อมูลตั้งแต่วันที่ปัจจุบัน เฉพาะรายการที่มีคนมาทำงานในวันนั้น
    #print ('2 out put data between ' , s_date ,'-' , e_date )
    empstatistic_data = empstatistic.objects.filter(
                Q(emp_type__cde = emptype , n_work__gte = 1), #show only date that n_work > 0) ,
                Q(workdate__range = [s_date , e_date])
                #Q(workdate__gte = startdate , workdate__lte = end_date ),            
                ).order_by('-workdate')
    
    
    context = { 'username': username ,
                'department': department ,
                'emptype': emptype,
                'period' : period ,
                'empstatistic_data' : empstatistic_data,
             
               }
    return render(request, 'ta_menu.html' , context )

def menu_time_by_dep(request,emptype,period,workdate): 
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    #userdepartment = user.dep.dep_code
    
    print("RUN MENU-TIME-BY-DEP ==>" , emptype , period , workdate )
    
    EmpType = EmployeeType.objects.get(cde = emptype)
    # list all data Where emptype = emptype and period = period 
    alldeps = TblDepartment.objects.all() 
    
    timedata = EmpTime.objects.filter(
            Q(emp_cde__emp_type = emptype , workdate=workdate ,period__cde =period ) ,
             ).order_by('-workdate')
    
    n_work=0
    n_absent = 0
    n_leave = 0
    
    for item in alldeps : 
        
        n_all = Empmas.objects.filter(
            Q(emp_dep = item.dep_code , emp_type = emptype , workstatus ='0' ) 
        ).count()
        
        n_work = timedata.filter(
            Q(emp_cde__emp_dep = item.dep_code) ,
            Q(timein__isnull=False)|
            Q(timeout__isnull=False)
             
         ).count()
            
        n_leave = timedata.filter(
              
                Q(emp_cde__emp_dep = item.dep_code) ,
                Q(leavecode__isnull= False )
                
            ).count()
        #n_leave = data_leave.count()
        
        n_late =timedata.filter(
             
                Q(emp_cde__emp_dep = item.dep_code) ,
                Q(numlate__gt = 0 )
        
            ).count()
        
        n_absent = timedata.filter(
            Q(emp_cde__emp_dep = item.dep_code) ,
            Q(timein__isnull= True),
            Q(timeout__isnull=True)
             
         ).count()#n_all - n_work
             
        try:
            Emp_statistic_by_dep = empstatisticbydep.objects.filter(
                            
                            Q(emp_type__cde = emptype),
                            Q(dep = item),
                            Q(workdate=workdate),
                            )
            
          #  print("data found" , Emp_statistic.count() )
        except:
            Emp_statistic_by_dep = empstatisticbydep.objects.none  #[]
          #  print("data not found")
            
        if Emp_statistic_by_dep.count() != 0 :   # mean data found
            #emptran.update(num=snum,numhour=snumhour,payamt=spayamt)
            Emp_statistic_by_dep.update(n_work=n_work ,
                                n_leave=n_leave,
                                n_late=n_late ,
                                n_absent = n_absent ,
                                emp_type = EmpType,
                                dep = item, 
            )

        else: # not found then add new data into empstatistic
            Emp_statistic_by_dep= empstatisticbydep(workdate=workdate , 
                                        n_work = n_work , 
                                        n_leave=n_leave,
                                        n_late=n_late,
                                        n_absent = n_absent ,
                                        emp_type=EmpType,
                                        dep = item
                                        )
            Emp_statistic_by_dep.save() 


    # render ข้อมูลตั้งแต่วันที่ปัจจุบัน ย้้อนหลัง ไป 7 วัน
    data = empstatisticbydep.objects.filter(
                Q(emp_type__cde = emptype , workdate = workdate) ,
                Q(n_work__gte=1) |
                Q(n_absent__gte = 1)|
                Q(n_leave__gte=1)
                                     
                ).order_by('dep__dep_code')
    #print(data)
    
    s_work = data.aggregate(s_work=Sum("n_work"))["s_work"]
    s_absent = data.aggregate(s_absent=Sum("n_absent")) ["s_absent"]
    s_leave = data.aggregate(s_leave=Sum("n_leave")) ["s_leave"]
    s_late= data.aggregate(s_late = Sum("n_late")) ["s_late"]
    s_all = s_work + s_absent + s_leave 
        
    #print ("MENU-TIME-BY-DEP " , s_work , s_absent , s_leave , s_all )
    
    context = { 'username': username ,
                'department': user.dep.dep_code ,
                'emptype': emptype,
                'period' : period ,
                'data' : data,
                'workdate' : workdate ,
                's_all' : s_all ,
                's_work' : s_work ,
                's_absent' : s_absent,
                's_leave' : s_leave ,
                's_late' : s_late ,
               }
    return render(request, 'ta-dashboard-by-dep.html' , context )
    
def menu_payroll(request):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user=GetUserDetail(username) 
    department = user.dep.dep_code
    
    context = { 'username': username ,
               'department': department ,
               }
    return render(request, 'payroll_menu.html' ,context)

def hmdashboard(request):
    
    if request.session['username'] is not None:
       username = request.session['username']
    else:
        return redirect(reverse('login'))
    
    department = GetUserDetail(username).dep.dep_code 
    
    employeetype = EmployeeType.objects.all()
    
    #print(data)
    
    for item in employeetype: 
            
        item_ingroup = Empmas.objects.filter(
   
                            Q(emp_type = item.cde),
                            Q(workstatus=0) 
                            )
        
        num_item_ingroup = item_ingroup.count()
        
        item.num_item = num_item_ingroup
        item.save()
    
    context = {
            'username':username,
            'department':department, 
            'employeetype': employeetype,
        }
    
    return render(request,'hm-dashboard.html',context)

def hmdashboardbydep(request,cde): # cde=emptype
    
    if request.session['username'] is not None:
        username = request.session['username']
    else:
        return redirect(reverse('login'))
    
    userdepartment = GetUserDetail(username).dep.dep_code 
    
    today_workdate = date.today()  # curent date - timedelta(1)    
    workdate = today_workdate.strftime('%Y-%m-%d') 
    print("today=" ,today_workdate)
    
    #empdesc = EmployeeType.objects.get(cde=cde).desc
    # all worker by department
    #EmpGroup = TblDepartment.objects.all().order_by('dep_code')
    alldeps = TblDepartment.objects.all()
    #dep_count = alldep.count()
    #print(dep_count)
    strcon = "work"
   # print(data)
   
    nwork = array.array('f' , [])
    # นับจำนวนคนมาทำงาน ไม่มาทำงาน มาสาย แยกตามแผนก (เฉพาะวันที่่ ณ ปัจจุบัน)
    for item in alldeps: 
            
        item_ingroup = Empmas.objects.filter(
                            Q(emp_type=cde),
                            Q(workstatus=0),
                            Q(emp_dep = item.dep_code)
                            )
        
        num_item_ingroup = item_ingroup.count()  # count employee in this department
        item.num_item = num_item_ingroup 
        """ 
        emptime = EmpTime.objects.filter(
            Q(emp_cde__emp_dep__dep_code = item.dep_code) ,
            Q(emp_cde__emp_type__cde = cde ) ,
            Q(workdate = workdate))
        """
        emptime = TimeMast.objects.filter(
            Q(emp_cde__emp_dep__dep_code = item.dep_code) ,
            Q(emptype = cde ) ,
            Q(workdate = workdate))
        
        #count come to work
        ncount = emptime.filter(
            Q(inout__contains = "IN" )     
        ).count()                    
        item.num_work = ncount
        
        # late  
        ncount = emptime.filter(
            Q(remark__icontains = 'สาย')
            
        ).count()
        item.num_late = ncount  
        
        # leave by get leave from Emptranleave 
        ncount = EmpTranLeave.objects.filter(
                Q(emp_cde__emp_dep__dep_code = item.dep_code ) ,
                Q(emp_cde__emp_type = cde) ,
                Q(leavedate = workdate ) ,
            ).count()
        item.num_leave = ncount
        
        # not working
        
        item.save()
        
        #print (item, workdate , ncount)
        
        #nwork.append(ncount)
        
    #    print (item , nwork)
    #print(nwork)
    
    data = TblDepartment.objects.filter(
            Q(num_item__gte=1) ,   #num_item more than or equal 1 (start from 1 ...)
        ).order_by('dep_code',)

    #print (numofgroups['FG'])
    context = {
            'username':username,
            'userdepartment':userdepartment,
            'emptype': cde,
            'workdate' : workdate ,
           # 'empdesc':empdesc,
            'data': data,
           
            'strcon' : strcon ,
        }
    
    return render(request,'hm-dashboard-by-dep.html',context)
 
#def : รายการลาประจำวัน
def tranleave(request):
    #pass
    if request.session['username'] is not None:
        username = request.session['username']
    else:
        return redirect(reverse('login'))
    user = GetUserDetail(username) 
    print(user , user.dep.dep_code )
    
    data = EmpTranLeave.objects.filter(
            Q(emp_cde__isnull= False) 
                        
            ).order_by ('-leavedate')
    
    if data.count() != 0 :
        pagedata=Paginator(data,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    else:
        pagedata = None
        page_number=1
        page_obj = None
        
    context = {
        'username' : username ,
        'department' : user.dep.dep_code ,
        'data' : data ,
        'page_obj': page_obj,
    }
    
    return render(request,'employee-leave-list.html',context)

#ประวัติการลา
def tranleave_history(request,id):
    #pass
    if request.session['username'] is not None:
        username = request.session['username']
    else:
        return redirect(reverse('login'))
    
    user = GetUserDetail(username)
    
    data = EmpTranLeave.objects.filter(
            Q(emp_cde__id = id)                     
            ).order_by ('-leavedate')
    
    if data.count() != 0 :
        pagedata=Paginator(data,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    else:
        pagedata = None
        page_number=1
        page_obj = None
        
    context = {
        'username' : username ,
        'department' : user.dep.dep_code ,
        'data' : data ,
        'page_obj': page_obj,
    }
    
    return render(request,'employee-leave-list.html',context)


def tranleave_filter(request):
    
    if request.method == "GET":
        name = request.GET.get('q') 
    else:
        name = None 
    #print (name)
    
    data = EmpTranLeave.objects.filter(
            Q(emp_cde__emp_cde__contains = name) |
            Q(emp_cde__emp_name__contains = name) |
            Q(leavedate = name)
            ).order_by('-leavedate')

    if data.count() != 0 :
        pagedata=Paginator(data,100)
        page_number = request.GET.get('page')
        page_obj = pagedata.get_page(page_number)
    else:
        pagedata=None
        page_number = None   
        page_obj = None
    
    print (data)
    
    context = {
        'data' : data ,
        'page_obj': page_obj,
    }
    
    return render(request,'employee-leave-list.html',context)

def tranleave_edit(request , id):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    else:
        username = request.session['username']
    
    user=GetUserDetail(username)
    # department = user.dep
    data = EmpTranLeave.objects.get(id=id) 
    
    EmpmasData = data.emp_cde
    
    leaves = TblLeave.objects.all().order_by('leavecode')
    AllEmps = Empmas.objects.all()
    
    print("tranleave id: " , data)
    
    if request.method=="GET":
        form = EmpTranLeaveForm(initial=data.__dict__) 
        
    elif request.method == "POST":
        form= EmpTranLeaveForm(instance = data ,data=request.POST)

    if form.is_valid():
        newdata = form.save(commit=False)
        #emp_cde= form.cleaned_data('emp_cde')
        emp_cde = form.cleaned_data.get('emp_cde')
        leavecode = form.cleaned_data.get('leavecode')
        
        newdata.emp_cde = EmpmasData
        newdata.leavecode = leavecode
        
        newdata.save()
        
        #form.save()
        #err_msg =''
        print('SAVE NEW DATA')
        url = reverse('emptranleave',kwargs={} )
        return HttpResponseRedirect(url)
        
    else:
        print('ERR: form... Data not save') 
        
    context = {
        'username' : username,
        'department': user.dep.dep_code , 
        'data':data ,
        'form' : form ,
        'leaves' : leaves ,
        'AllEmps' : AllEmps 
    }    
    #url = reverse('emptranleave')
    #return HttpResponseRedirect(url)    
    return render(request,'employee-leave-view.html',context)

def tranleave_add (request) :
    if request.session['username'] is None:
        return redirect(reverse('login'))
    username = request.session['username']
  
    user=GetUserDetail(username)
    # department = user.dep
    newdata =  [] #EmpTranLeave.objects.none
    
    #EmpmasData = data.emp_cde
    
    leaves = TblLeave.objects.all().order_by('leavecode')
    AllEmps = Empmas.objects.all()
    
    #print(newdata)

    form = EmpTranLeaveForm()
    if request.method == 'POST':
        form = EmpTranLeaveForm(request.POST) 
        if form.is_valid():
        
            form.save()
            print('DATA OK: SAVE NEW DATA' )
            
            url = reverse('emptranleave',kwargs={} )
            return HttpResponseRedirect(url)
            
        else:
            print('ERR: form... Data not save') 
        
    context = {
        'username' : username,
        'department': user.dep.dep_code , 
        'data':newdata ,
        'form' : form ,
        'leaves' : leaves ,
        'AllEmps' : AllEmps 
    }    
     
    return render(request,'employee-leave-view.html',context)

#การลาออก
def empresignlist(request):
    pass

def empresign_add(request):
    pass

def empresign_edit (request) :
    pass


def employeelist(request,cde,depid):   # cde=emp_type depid = Department ID or Depcode
   
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']

    employeeeDep= TblDepartment.objects.get(id=depid)
   # print(employeeeDep)
    
    user=GetUserDetail(username)
    
    workdate = date.today()  # curent date - timedelta(1)    
    workdate = workdate.strftime('%Y-%m-%d') 
    
    row = Empmas.objects.filter (
            Q(emp_type = cde) ,
            Q(emp_dep__id = depid ),
            Q(workstatus = 0)      
        ).order_by('-emp_cde')
    
    row_work = TimeMast.objects.filter(
        Q(workdate= workdate) )

    #print( row_work)
    
    pagedata=Paginator(row,100)
   # print('pagedata=' , pagedata)
    page_number=request.GET.get('page')
    page_obj = pagedata.get_page(page_number)  
    
    i_count = []
    for i in row:
        
        empcde = i.emp_cde
        
        i_count= row_work.filter(Q(emp_cde=empcde)).count()
        
    print (i_count)  # mean come to work today
        
    context={
    'emptype':cde,
    'depid': depid,
    'employeeDep':employeeeDep.dep_name ,
    'data':row,
    'page_obj': page_obj,
    'username':username,
    'department':user.dep.dep_code,
   
    }
    
    return render(request,'employeelist.html',context)

# for search
def EmployeeSearch(request,cde,depid): #cde = emp_type
    
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user = GetUserDetail(username)
    
    #dep = TblDepartment.objects.get(id=depid).dep_code
    if request.method == "GET" :
        name = request.GET.get('q')
    else:
        name = None
           
    # multiple search criteria Base on Emptype & Emp_dep 
    data = Empmas.objects.filter(
            Q(emp_type=cde),
            Q(emp_dep = name )|  
            Q(emp_cde = name)|
            Q(emp_name__contains = name )|
            Q(shift = name )

        ).order_by('-id')
   
    if data.count() != 0 :   
        pagedata=Paginator(data,100)
        page_number = request.GET.get('page')
        page_obj = pagedata.get_page(page_number)
    else:
        pagedata = None
        page_number=1
        page_obj = None
    
    context = {'username':username, 
                   'department':user.dep.dep_code,
                   'page_obj': page_obj ,
                   'emptype':cde ,
                   'depid':depid,
                   'data': data,
                   }
        
    return render(request,'employeelist.html',context)
    
def hmsetting(request):
    pass
    
    return render(request,'hm-home-setting.html')
# def for daily process menu
def hmdaily(request):
    
    workdate = date.today()
    print ("TODAY: " ,  workdate)
    
    d1 = workdate.strftime('%d-%m-%Y')
    print("d1 =", d1)
    
    
    

    data_work = EmpTime.objects.filter(
                            Q(ta_date = d1 ),
                            Q(pay="Y")
                            )
    n_work = data_work.count()
    
    context = {
        'workdate': workdate ,
        'n_work': n_work,    
    }
    
    return render(request,'ta_menu.html',context)

def hmdaily_created(request):
    pass
def hmdaily_time(request):
    pass

def hmdaily_transaction_filter(request):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    
    if request.method == "GET":
        name = request.GET.get('q') 
    else:
        name = None 
    print (name , type(name))
    
    dtransaction = dailyTransaction.objects.filter(
               # Q(workdate__icontains= datetime.strptime(name,'%d/%m/%Y').date()) |
                
                Q(doc_no__startswith= name)|
                Q(emp_cde__emp_cde__contains = name )|
                Q(emp_cde__emp_name__contains = name )|
                Q(period__cde__icontains = name)  
                
               
               # Q(workdate = date(name))
                ).order_by('-id')
    
    if dtransaction.count() != 0 :
        pagedata=Paginator(dtransaction,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    else:
        pagedata=None
        page_number = 0
        page_obj = None
    
    context={
     
        'data':dtransaction,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep.dep_code,
        
    }
  
    return render(request,'hm-daily-transaction.html',context)

def hmdaily_transaction(request):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)

    
    dtransaction = dailyTransaction.objects.all().order_by('-id')
  
    pagedata=Paginator(dtransaction,100)
    page_number=request.GET.get('page')
    page_obj = pagedata.get_page(page_number)  
  
    
    context={
     
        'data':dtransaction,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep.dep_code,
        
    }
  
    return render(request,'hm-daily-transaction.html',context)

def hmdaily_transaction_addnew(request):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    
    dtransaction = dailyTransaction.objects.none() 
    periods  = EmpPeriod.objects.filter(
                Q(status='0')).order_by('cde')
    
    employees = Empmas.objects.all().order_by('emp_type','emp_cde')
    codes = EmpCtlDb.objects.filter(Q(dailyrecord=True)).order_by('cde')
    err_msg = None
    
    formset = TransactionModelFormset(queryset=dtransaction)
    docform = DtransactionHead(request.GET or None)  
    
    if request.method == "POST":
     #   docform =DTransactionForm(instance=dtransaction,dtransaction=request.POST)
        
        docform = DtransactionHead(request.POST)

        formset= TransactionModelFormset(request.POST)
        
        if docform.is_valid() and formset.is_valid():
            docno = docform.cleaned_data.get('docno')
            period = docform.cleaned_data.get('period')
            docdate = docform.cleaned_data.get('docdate')

            print(docno , period , docdate)
            
            for form in formset:
    
                
                dtransaction=form.save(commit=False)
                dtransaction.docno = docno
                dtransaction.docdate=docdate
                dtransaction.period=period
               # dtransaction.workdate = workdate 
               # dtransaction.workstartdate = workstartdate 
               
               # dtransaction.workenddate = workenddate 
               
                emp_cde = form.cleaned_data.get('emp_cde').emp_cde
                code = form.cleaned_data.get('code').cde
                workstarttime = form.cleaned_data.get('workstarttime')
                workendtime = form.cleaned_data.get('workendtime')
                
                print(emp_cde , code )
                
                IncExpDb = EmpIncExpDb.objects.filter(
                            Q(emp_cde = emp_cde),
                            Q(code=code)
                )
                print(IncExpDb)
                
                if IncExpDb.count() != 0 :
                    amtPerMinute = IncExpDb[0].emp_amt / 60  # คิดเป็น นาที
                    
                else:
                    amtPerMinute= 0
                    
                Ctldb = EmpCtlDb.objects.get(cde=code)
                if Ctldb.onetime == True :
                    NuminHour = 1
                    NuminMinute = 1
                    dtransaction.num = 1
                    pay_amt = form.cleaned_data.get('payamt')
                else:
                    NuminHour = workendtime - workstarttime #show in hour:miniute
                    NuminMinute = (NuminHour.seconds)/60  #เก็บเป็นนาที
                    dtransaction.num = NuminMinute/60
                    
                    dtransaction.numhour = NuminMinute 
                    pay_amt = round( amtPerMinute * NuminMinute  ,2) 
                
                #pay_amt = dtransaction.num * emp_amt
                     
                print(amtPerMinute , pay_amt)
                # EmpAmt = IncExpDb.emp_amt 
                #if Ctldb.calhour == True:  
                #    numhour = dtransaction.num * 60 
                    
                dtransaction.payamt = pay_amt
                
                print(Ctldb.calday,Ctldb.calhour,Ctldb.onetime,NuminHour)
                dtransaction.save()  # SAVE NEW DATA INTO DAILYTRANSACTION
               
                print  ('SAVE NEW DATA ' , docno )

                # step: update to emp_transaction 
                alltran_code = dailyTransaction.objects.filter(
                    Q(emp_cde=emp_cde),
                    Q(code = code )
                )
            
                snum = alltran_code.aggregate(snum=Sum("num"))["snum"]
                snumhour = alltran_code.aggregate(snumhour=Sum("numhour"))["snumhour"]
                spayamt = alltran_code.aggregate(spayamt=Sum("payamt"))["spayamt"]

                emptran = EmpTransaction.objects.filter(
                    Q(emp_cde=emp_cde),
                    Q(code =code)
                )

                if emptran.count() == 1 :

                    emptran.update(num=snum,numhour=snumhour,payamt=spayamt)
                    
                    #print(emptran[0].emp_cde,emptran[0].code,emptran[0].numhour,emptran[0].payamt)
                    messages.success(request,'Update Complete')
                else:
                    print('Data not found')
                
            return redirect('hmdailytransaction') 
        else:
            err_msg ="ข้อมูลไม่ถูกต้อง"
            print('form is not valid ')
            print(formset.errors)
            
    context={
        'docform':docform,
        'formset':formset ,
        'data':dtransaction,
        'periods':periods,
        'employees': employees,
        'codes':codes,
        'username':username,
        'department':user.dep.dep_code,
        'err_msg' : err_msg
        
    }
  
    return render(request,'hm-daily-transaction-add.html',context)

def hmdaily_transaction_update(request,id):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    
    data = dailyTransaction.objects.get(id=id )
    
    print(1, data)
    code = data.code.cde
    empcde= data.emp_cde
    
    ctldb = EmpCtlDb.objects.filter(Q(cde=data.code.cde)) 
    print (2, ctldb)
    if ctldb.count() != 0:
        cal1time = ctldb[0].onetime
        calhour = ctldb[0].calhour 
        
    
    #cal1time =EmpCtlDb.objects.get(cde=code).onetime
    #calhour = EmpCtlDb.objects.get(cde=code).calhour
    """ 
      try:
        data = dailyTransaction.objects.get(id=id )
        empcde= data.emp_cde
        code = data.code
        cal1time =EmpCtlDb.objects.get(cde=code).onetime
        calhour = EmpCtlDb.objects.get(cde=code).calhour
        
    except:
        data = dailyTransaction.objects.none()
        empcde= None 
        code = None
        cal1time = False
        calhour = False
        
    """
  
    print (3, id, empcde.emp_cde , code )
    
    #if data.status == "9" :
    #    return HttpResponse("Error. .. ไม่อนุญาติให้แก้ไขรายการที่ สถานะรายการเป็น POST แล้ว")
    #print (id)
    if empcde is not None:
        EmpmasData = Empmas.objects.get(emp_cde = empcde.emp_cde)
        emptype = EmpmasData.emp_type
        empname = empcde 
        
        employees = Empmas.objects.filter(
                Q(emp_type=emptype),
                Q(workstatus='0')
                ).order_by('emp_type','emp_cde')
    
    # periods equivalent with EMP_TYPE abd OPEN STATUS 
        periods  = EmpPeriod.objects.filter(
            Q(status='0'),
            Q(emptype= emptype )).order_by('cde')
    else:
        EmpmasData = None
        emptype = None
        empname =None
        employees = Empmas.objects.filter(
                Q(workstatus='0')
                ).order_by('emp_cde')
        periods  = EmpPeriod.objects.filter(
            Q(status='0'),
            ).order_by('cde')
   
    #print(employees.count())
   
    codes = EmpCtlDb.objects.filter(Q(
                dailyrecord= True )).order_by('cde')
    
    if request.method=="GET":
        form = DTransactionForm(initial=data.__dict__) 
        
        
    elif request.method == "POST":
     #   docform =DTransactionForm(instance=dtransaction,dtransaction=request.POST)
        form= DTransactionForm(instance = data ,data=request.POST)
        
        print('DATA' , request.POST)
        
        if form.is_valid():
           
            emp_cde = empcde #form.cleaned_data.get('emp_cde').emp_cde
            docno = form.cleaned_data.get('docno')
            docdate = form.cleaned_data.get('docdate')
            code= form.cleaned_data.get('code').cde
            period = form.cleaned_data.get('period')
            num = form.cleaned_data.get('num')
            payamt= form.cleaned_data.get('payamt')
            workdate = form.cleaned_data.get('workdate')
            workstarttime = form.cleaned_data.get('workstarttime')
            workendtime = form.cleaned_data.get('workendtime')
            print  ('SAVE' , id , empcde, code ,num , payamt , period,workstarttime,workendtime )    
            data=form.save(commit=False)
            
          
            # update payamt in dtransaction with true condition 
            ctlcde = EmpCtlDb.objects.get(cde=code)
            calhour = ctlcde.calhour
            calday = ctlcde.calday
            cal1time = ctlcde.onetime
  
            if cal1time == False:  # จ่ายหรือหักเป็นงวด เป็นจำนวนเงิน
                amt = EmpIncExpDb.objects.filter(
                        Q(emp_cde= empcde),
                        Q(code = code )
                        )
                
                if amt.count() != 0 :
                    empamt = amt[0].emp_amt
                    amtPerMinute = empamt / 60  # คิดต่อนาที
                else:
                    amtPerMinute = 0 
                
                NuminHour = workendtime - workstarttime #show in hour:miniute
                NuminMinute = (NuminHour.seconds)/60  #เก็บเป็นนาที
                
                data.numhour = NuminMinute 
                data.num = NuminMinute/60
                payamt = round( amtPerMinute * NuminMinute  ,2) 
                             
                print('in hour', NuminHour , 'in minute' ,NuminMinute)
            else:
                data.num=1    
                                    
            print (code , calhour, calday, cal1time ,payamt,workstarttime,workendtime)    
            #  data.emp_cde.emp_cde = empcde         
            data.workstarttime = workstarttime
            data.workendtime = workendtime
            #data.num = num
            data.payamt = payamt
            
            data.save()  # update data in dailytransaction
                        
            # step: update to emp_transaction 
            alltran_code = dailyTransaction.objects.filter(
                Q(emp_cde=empcde),
                Q(code = code )
            )
           
            snum = alltran_code.aggregate(snum=Sum("num"))["snum"]
            snumhour = alltran_code.aggregate(snumhour=Sum("numhour"))["snumhour"]
            spayamt = alltran_code.aggregate(spayamt=Sum("payamt"))["spayamt"]
            
           # print(alltran_code )
            
            emptran = EmpTransaction.objects.filter(
                Q(emp_cde=empcde),
                Q(code =code)
            )
            print(emptran)
           # print(emptran.count(), emptran[0].emp_cde,emptran[0].code,emptran[0].num)
            if emptran.count() == 1 :

                emptran.update(num=snum,numhour=snumhour,payamt=spayamt)
                
                #print(emptran[0].emp_cde,emptran[0].code,emptran[0].numhour,emptran[0].payamt)
                messages.success(request,'Update Complete')
            else:
                print('Data not found')

            # return redirect('hmdailytransaction')   
        else:
            print('form is not valid ')
    
    context={
        
        'form': form,
        'data':data,
        'codes':codes,
        'periods':periods ,
        'username':username,
        'department':user.dep.dep_code,
        'empname' : empname ,
        'cal1time' : cal1time,
        'calhour'  : calhour ,
        
    }
  
    return render(request,'hm-daily-transaction-update.html',context)

def hmdaily_process(request):
    pass
# def for month-end process menu 
def hmmonthend(request):
    pass    
    return render(request,'hm-monthend-menu.html')
def hmmonthend_transaction(request):
    pass
def hmmonthend_process(request):
    pass
def hmmonthend_report(request):
    pass 
def hmmonthend_closed(request):
    pass 


#Add new Emp-Code
def hmaddnew(request,cde,depid):
    appname ="HumanResourcePlanning"
    if request.session['username'] is None:
            return redirect(reverse('login'))
    
    username = request.session['username'] 
    user=GetUserDetail(username)
    department = user.dep.dep_code
     
    auth = GetAppList(user.id,appname)
    
    if auth is None :
        print('query set== None')
        return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานระบบ')
    else:
        is_access = auth.is_access
        is_admin = auth.is_admin
    err_msg=""    
    emp_positions = EmpPosition.objects.all()
    emp_departments = TblDepartment.objects.all()
    emp_types = EmployeeType.objects.all()
    head_msg = "New"
    data = {'id':None}
    
    print (username, is_admin)
    
    form=EmployeeForm()
    if request.method == 'POST':
        form=EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            newdata = form.save(commit=False)
            newdata.emp_taxid = newdata.emp_cardid
            newdata.emp_socialid = newdata.emp_cardid
            
            newdata.save()
            
            #form.save()
            err_msg =''
            print('SAVE NEW DATA')
            
            url = reverse('employeelist',kwargs={'emptype':cde,'depid':depid} )
            return HttpResponseRedirect(url)
        
        else:
            err_msg='Data Error.'
            print('Error data not save')
        
    context = {
        'err_msg':err_msg,
        'username':username,
        'department':department,
        'form':form, 
        'emp_departments': emp_departments,
        'emp_positions':emp_positions,
        'emp_types':emp_types,
        'head_msg':head_msg,
        'emptype':cde,
        'depid' : depid ,
        'data':data,
    }
    
    return render(request,'employeehome.html',context)

def hmedit(request,cde,depid,id):  #cde = emptype , depid = department id , id = empmas id       
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    emp_positions = EmpPosition.objects.all()
    alldeps = TblDepartment.objects.all()
    emp_types = EmployeeType.objects.all()
    shifts = TblShift.objects.all()
    
    data= Empmas.objects.get(id=id) # get all data from empmas (id = id)
    
    print (data.emp_imageurl)
    
    form=EmployeeForm(initial=data.__dict__)
    if request.method =="POST":
        form=EmployeeForm(instance=data,data=request.POST,files=request.FILES)
        if form.is_valid():
            #file = request.FILES['emp_imageurl']
            #print(file)
            
            cardid = form.cleaned_data['emp_cardid']
            data=form.save(commit=False)
            data.emp_taxid = cardid
            data.emp_socialid = cardid 
            
            data.save()
            
            print("SAVE DATA " , cardid)
           # print(cardid)
            
           # url = reverse('employeelist',kwargs={'depid':depid} )
           # return HttpResponseRedirect(url)
            
    context = {
        'form':form,
        'data':data ,
        'alldeps': alldeps,
        'emp_positions':emp_positions,
        'emp_types':emp_types,
        #'details':details,
        'username':username,
        'department':user.dep.dep_code,
        'emptype':cde,
        'depid':depid,
        'shifts' : shifts
       # 'head_msg':head_msg,
    }

    return render(request,'employeehome.html',context )

#class for HM_income 
# class for HM Experience 
def hmexper(request,cde,depid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    
    empid = id
    
    data = EmpExper.objects.filter(
                Q(empmas = id )
            ).all()
    
    if request.method == "POST" :
        form = EmployeeExperienceForm(request.POST)
        if form.is_valid():
            newexper = form.save(commit = False)
            newexper.empmas_id = empid 
            newexper.save()
    else:
        form =  EmployeeExperienceForm()        
            
    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'form':form,
            
    }
    
    return render(request,'hm-experience.html',context )

def hmexper_edit(request,depid,empid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    
    data = EmpExper.objects.get(id = id)
            
    form =  EmployeeExperienceForm(initial=data.__dict__) 
    
    if request.method == "POST" :
        form = EmployeeExperienceForm(instance=data, data = request.POST)
        if form.is_valid():
            newexper = form.save(commit = False)
            newexper.empmas_id = empid 
            newexper.save()

            url = reverse('hm-exper',kwargs={'depid':depid,'id':empid} )
            return HttpResponseRedirect(url)
               
            
    context = {
        'username' : username,
        'department' : department,
        'depid': depid ,
        'empid' : empid ,
        'data': data,
        'form':form,
            
    }
    
    return render(request,'hm-exper-edit.html',context )
# class for HM reference 
def hmrefer(request,cde,depid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    
    empid = id
    
    data = EmpReference.objects.filter(
                Q(empmas = id )
            ).all()
    
    if request.method == "POST" :
        form = EmpReferenceForm(request.POST)
        if form.is_valid():
            newdata = form.save(commit = False)
            newdata.empmas_id = empid 
            newdata.save()
            
            messages.success(request, 'emp id  {}  added.'.format(newdata.p_name))
        else:
            err=form.errors 
            a = list(err.as_data() ["p_name"][0])
            print (a[0])
            #print (form.errors.as_data())
            
    else:
        form =  EmpReferenceForm()        
            
    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'form':form,
            
    }
    
    return render(request,'hm-refer.html',context )

def hmrefer_edit(request,depid,empid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    
    data = EmpReference.objects.get(id = id)
            
    form =  EmpReferenceForm(initial=data.__dict__) 
    
    if request.method == "POST" :
        form = EmpReferenceForm(instance=data, data = request.POST)
        if form.is_valid():
            newdata = form.save(commit = False)
            newdata.empmas_id = empid 
            newdata.save()

            url = reverse('hm-refer',kwargs={'depid':depid,'id':empid} )
            return HttpResponseRedirect(url)
               
            
    context = {
        'username' : username,
        'department' : department,
        'depid': depid ,
        'empid' : empid ,
        'data': data,
        'form':form,
            
    }
    
    return render(request,'hm-refer-edit.html',context )

# class for HM Education History 
def hmeducation(request,cde,depid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    
    empid = id
    
    data = EmpEducation.objects.filter(
                Q(empmas = id )
            ).all()
    
    if request.method == "POST" :
        form = EmployeeEducationForm(request.POST)
        if form.is_valid():
            newexper = form.save(commit = False)
            newexper.empmas_id = empid 
            newexper.save()
    else:
        form =  EmployeeEducationForm()        
            
    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'form':form,
            
    }
    
    return render(request,'hm-education.html',context )

def hmeducation_edit(request,depid,empid,id):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code
    # data for p_level and p_major
    p_levels = grade.objects.all() 
    p_majors = gradeMajor.objects.all()
    
    data = EmpEducation.objects.get(id = id)
            
    form =  EmployeeEducationForm(initial=data.__dict__) 
    
    if request.method == "POST" :
        form = EmployeeEducationForm(instance=data, data = request.POST)
        if form.is_valid():
            newdata = form.save(commit = False)
            newdata.empmas_id = empid 
            newdata.save()
            #form.save()
            print('Save Data OK')
            url = reverse('hm-education',kwargs={'depid':depid,'id':empid} )
            return HttpResponseRedirect(url)
               
            
    context = {
        'username' : username,
        'department' : department,
        'depid': depid ,
        'empid' : empid ,
        'data': data,
        'form':form,
        'p_levels' : p_levels ,
        'p_majors' : p_majors ,
            
    }
    
    return render(request,'hm-education-edit.html',context )

# CHECK is_admin# ถ้าไม่ใช่ Admin ของแผนก หรือ หัวหน้า ไม่สามารถเข้าบางเมนูที่สำคัญได้
def hmedit_income(request,cde,depid,id):
    appname ="HumanResourcePlanning"
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    auth = GetAppList(user.id,appname)
    
    if auth is None :
        print('query set== None')
        return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานระบบ')
    else:
        is_access = auth.is_access
        is_admin = auth.is_admin
        if is_admin == 0 :  # ไม่ใช่ Admin ของแผนก หรือ หัวหน้า
             return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานหน้านี้ ')
    
    data= Empmas.objects.get(id=id)
    empcde = data.emp_cde
    
    print ('IS ADMIN:' , is_admin)
    """
     try: 
        data = Empmas.objects.get(empmas_id=id)
    except:
        data = Empmas.objects.none()
    
    print(data)
    
    """
    #data=Empmas.objects.get(id=id)
   
    #if data.count()==0:
    #    data=None
    #    emptype= cde
    #    depid = depid
    #    id = id 
    
    try:
        IncExpdata = EmpIncExpDb.objects.filter(
                    Q(emp_cde=data.emp_cde)
                ) 
    except:
        IncExpdata = EmpIncExpDb.objects.none    
        
    emptype = cde
    
    # get infomation from Tbl_employeetype
    EmpType = EmployeeType.objects.get(cde=emptype)
    
    #filter data from tbl_inc_exp_db Where emp_cde=data.emp_cde
     
    
    form= FrmEmpmasIncome(initial=data.__dict__)
    if request.method=="POST":
        #form=EmployeeIncomeForm(instance=data,data=request.POST)
        form=FrmEmpmasIncome(instance=data, data= request.POST)
        if form.is_valid():
            newincome = form.cleaned_data['emp_income']
            newdata = form.save(commit=False)
          #  newdata.empmas_id= id 
          #  newdata.emp_cde = empmas.emp_cde
            #newdata.emp_income = newincome
            
           
            newdata.save()  # save data into EmpmasIncome 
            
            
            # update emp_amt in tbl_inc_exp_db (EmpIncExpDb)
            # process = 1. check data in tbl_inc_exp_db
            
            
            if EmpType.cde== "W" :  #คำนวณ เงินได้/ชม. เพื่อเป็นฐานสำหรับการคำนวณเงินได้ เงินหัก ตามจริง 
                amt_hour = newincome/EmpType.workhour
            else:
                amt_hour = newincome/(EmpType.workday * EmpType.workhour)
            
            if IncExpdata.count()  !=  0 : # mean found in system (data Exist in model: EmpIncExpDb)
                
                for incexp in IncExpdata:
                    code = incexp.code
                    
                    print (code)
                    
                    try:
                        ctldb = EmpCtlDb.objects.get(cde=code)
                        if ctldb.onetime== True:
                            emp_amt = 0
                    
                        else:
                            if ctldb.calday == True:
                                emp_amt = amt_hour * EmpType.workhour
                            
                            else:
                                if ctldb.calhour == True:
                                    emp_amt=amt_hour * ctldb.multiby
                                
                        print (code , emp_amt )            
                        
                        incexp.emp_amt = emp_amt 
                        incexp.save(update_fields=['emp_amt'])
                    except:
                        ctldb = []
                    
                    
            else:  # Not Found Just Add new all item From model EMPCTLDB that default Value=1
                
                EmpIncExp = [] 
                #EmpIncExpDb()
                
                ctldb = EmpCtlDb.objects.filter(Q(defaultvalue = True)).order_by('cde')
                
                print(ctldb)
                
                for item in ctldb:
                    code=item.cde
                    print(item.cde)
                    
                    if item.onetime == True:
                            emp_amt = 0
                    else:
                        if item.calday == True:
                            emp_amt = amt_hour * EmpType.workhour
                        else:
                            if item.calhour == True:
                                emp_amt=amt_hour * item.multiby
                                
                    EmpIncExp.append(EmpIncExpDb(
                        emp_cde= empcde,
                        code = item ,  #instance data from EmpCtlDb
                        detail = item.desc ,
                        emp_amt = emp_amt
                    ))
                    
                EmpIncExpDb.objects.bulk_create(EmpIncExp)
                
                #ตรวจสอบข้อมูลการลดหย่อนในตาราง Emp_less_Deduction ถ้าไม่มีให้เพิ่มเข้าไปใหม่ จากตาราง TaxDeduction ตามค่า default = True
                EmpLessDeduction = EmpDeduction.objects.filter(Q(emp_cde = empcde))
                if EmpLessDeduction.count() == 0: 
                    
                    empdeduct=[] # declare array for empdeduct data
                    
                    Taxdeduct = TaxDeduction.objects.filter(Q(defaultvalue=True))
                    for item in Taxdeduct:
                        print (item)
                        
                        empdeduct.append(EmpDeduction(
                                emp_cde=empcde ,
                                deduct_cde = item,
                                desc = item.desc,
                                num=1 ,
                              
                        ))
                        
                    EmpDeduction.objects.bulk_create(empdeduct) 
                
                
            print('save income data')

          #  url = reverse('hm-edit',kwargs={'depid':depid,'id':id} )
          #  return HttpResponseRedirect(url)
    
    #print(is_admin  , id)
    #pass 
    context = {
        'form':form ,
        'username' : username ,
        'department' : department ,
        'emptype':cde,
        'depid': depid ,
        'id' : id,
        'empmas':data,
        'data':data,
        'is_admin' : is_admin,
        'incexpdata': IncExpdata,
        
    }
    
    return render(request,'hm-income.html',context)

    """
    if ctl.onetime == 1 or ctl.calauto == 1 :
                        emp_amt = 0
                    else:
                        if ctl.calday == 1:
                            emp_amt = amt_hour * EmpType.workhour
                        else:
                            if ctl.calhour == 1:
                                emp_amt=amt_hour * ctl.multiby
    """
 
                                

# CHECK is_admin# ถ้าไม่ใช่ Admin ของแผนก หรือ หัวหน้า ไม่สามารถเข้าบางเมนูที่สำคัญได้
def hm_inc_exp(request,cde,depid,id):
    appname ="HumanResourcePlanning"
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    auth = GetAppList(user.id,appname)
    
    if auth is None :
        print('query set== None')
        return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานระบบ')
    else:
        is_access = auth.is_access
        is_admin = auth.is_admin
        if is_admin == 0 :  # ไม่ใช่ Admin ของแผนก หรือ หัวหน้า
             return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานหน้านี้ ')

    print (is_admin)
    emp_cde=Empmas.objects.get(id=id).emp_cde
    
    #filter data from tbl_inc_exp_db Where emp_cde=data.emp_cde
    try:
        data = EmpIncExpDb.objects.filter(
                    Q(emp_cde=emp_cde)
                ).order_by('code')    
    except:
        data = None
    
    print (emp_cde)

    if request.method=="POST":
        form=IncExpForm(request.POST)
        if form.is_valid():
            datanew = form.save(commit=False)
            datanew.emp_cde = emp_cde
            datanew.save()    
    else:
        form=IncExpForm()
           
    #print(is_admin  , id)
    #pass 
    context = {
        'form':form ,
        'username' : username ,
        'department' : department ,
        'emptype':cde,
        'depid': depid ,
        'is_admin' : is_admin,
        'data': data,
        'emp_cde': emp_cde ,
        'emp_id' : id ,
    }
    
    return render(request,'hm-inc-exp.html',context)


# class for HM - Deduction 
def hm_deduction(request,cde,depid,id):
    appname ="HumanResourcePlanning"
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    auth = GetAppList(user.id,appname)
    
    if auth is None :
        print('query set== None')
        return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานระบบ')
    else:
        is_access = auth.is_access
        is_admin = auth.is_admin
       # if is_admin == 0 :  # ไม่ใช่ Admin ของแผนก หรือ หัวหน้า
       #      return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานหน้านี้ ')

    print (is_admin)
    emp_cde=Empmas.objects.get(id=id).emp_cde
    
    #filter data from tbl_inc_exp_db Where emp_cde=data.emp_cde
    try:
        data = EmpDeduction.objects.filter(
                    Q(emp_cde=emp_cde)
                ).order_by('deduct_cde')    
    except:
        data = None
    
    print (emp_cde)
  
    
    if request.method=="POST":
        form=EmpDeductionForm(request.POST)
        if form.is_valid():
            datanew = form.save(commit=False)
            datanew.emp_cde = emp_cde
            datanew.save()
            #form.save()]
    else:
        form=EmpDeductionForm()  
                  
    #print(is_admin  , id)
    #pass 
    context = {
        'form':form ,
        'username' : username ,
        'department' : department ,
        'emptype':cde,
        'depid': depid ,
        'is_admin' : is_admin,
        'data': data,
        'emp_cde': emp_cde ,
        'emp_id' : id ,
        
    }
    
    return render(request,'hm-deduction.html',context)

# emptime data history 
def hm_timedata_history(request,cde,depid,id):  # cde= emptype , depid = department id , id = empmas id
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    emp_cde  = Empmas.objects.get(id=id).emp_cde
    
    strcon = "all"
    #print(emp_cde)
    periods = EmpPeriod.objects.filter(
                Q(emptype = cde )
                
            ).order_by('-cde')
    for item in periods:
        emptime = EmpTime.objects.filter(Q(period=item.cde))
        n_emptime = emptime.count()
       # print(item.cde , n_emptime)
        item.num = n_emptime
        item.save
    
    #print(periods)
    period = None
    data = None 
    #EmpTime.objects.filter(
    #Q(emp_cde = emp_cde)
    #        ).order_by('-ta_date')
    
    periods = EmpPeriod.objects.filter(
                Q(emptype = cde ) ,
                Q(num__gte = 1)
                
            ).order_by('-cde')
    try:    
        pagedata=Paginator(data,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    except:
        pagedata=None
        page_number=1
        page_obj = None 

    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'empmas' : Empmas.objects.get(id=id) ,  # return only emp_cde & emp_name & emp_surname
        'page_obj' : page_obj ,
        'strcon' : strcon ,    
        'periods' : periods , # all periods
        'period' : period ,
        'workdate' : None,       
    }
    
    return render(request,'hm-timedata-history.html',context )

def hm_timedata_history_by_period(request,cde,depid,id,period ): #cde:emptype
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    #emp_cde  = Empmas.objects.get(id=id).emp_cde
    
    empmas = Empmas.objects.get(id=id)
    
    strcon = "all"
    
    periods = EmpPeriod.objects.filter(
                Q(emptype = cde ), 
                Q(num__gte = 1)
            ).order_by('-cde') 
    
    #data = EmpTime.objects.filter(
    #            Q(emp_cde = empmas.emp_cde),
    #            Q(period = period) 
    #            
    #        ).order_by('-ta_date')
    data = TimeMast.objects.filter(
        Q(emp_cde__id = id ) ,
        Q(period = period ) 
    ).order_by('workdate' , 'worktime')
    
    pagedata=Paginator(data,100)
   # print('pagedata=' , pagedata)
    page_number=request.GET.get('page')
    page_obj = pagedata.get_page(page_number)  
    

    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'empmas' : empmas ,  # return only emp_cde & emp_name & emp_surname
        'page_obj' : page_obj ,
        'strcon' : strcon ,    
        'periods' : periods , 
        'period' : period ,
        'workdate' : None,
       
    }
    
    return render(request,'hm-timedata-history.html',context )

def hm_timedata_history_filter(request,cde,depid,id,period):
    if request.session['username'] is None:
        return redirect('login')
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    emp_cde  = Empmas.objects.get(id=id).emp_cde
    
    print(emp_cde)
    if request.method == "GET":
        name = request.GET.get('q') 
    else:
        name = None 
    strcon ='all'
    print (name , type(name))
    
    
   # data = EmpTime.objects.filter(
   #         Q(emp_cde = emp_cde , period = period),
   #         Q(workdate__contains= name)|
   #         Q(remarks_other__contains = name )|
   #         Q(shift=name) 
   #     
   #     ).order_by('-id')   
        
    data = TimeMast.objects.filter(
        Q(emp_cde = emp_cde , period = period ) ,
        Q(workdate=name )|
        Q(inout__contains = name )|
        Q(remark__contains= name)
    )        
    
    pagedata=Paginator(data,100)
   # print('pagedata=' , pagedata)
    page_number=request.GET.get('page')
    page_obj = pagedata.get_page(page_number)  
    

    context = {
        'username' : username,
        'department' : department,
        'emptype':cde,
        'depid': depid ,
        'empid' : id ,
        'data': data,
        'page_obj' : page_obj ,
        'period' : period ,    
        'strcon' : strcon ,
        'workdate' : None,
    }
    
    return render(request,'hm-timedata-history.html',context )
#TIME SHIFT DATA กะการทำงานของพนักงาน

def hm_shift_data(request, emptype,depid,id,period):
    
    emp_cde = Empmas.objects.get(id=id).emp_cde
    
    periods = EmpPeriod.objects.filter(
                Q(emptype = emptype ),
               
                
            ).order_by('-cde') 
    
    data = timeshift.objects.filter(
        Q(emp_cde=emp_cde) ,
        Q(period = period )
        
    ).order_by('workdate')
    
    try:
        pagedata=Paginator(data,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    except: 
        pagedata = None 
        page_number = 1
        page_obj = None
        
    context= { 
            'data' :data,
            'periods': periods ,
            'emptype' : emptype,
            'depid' : depid,
            'empid' : id ,
            'emp' : emp_cde ,
            'page_obj' : page_obj ,      
    }
    
    return render(request , 'hm-timeshift.html' ,context)
   
# setup EmpCtlDb data
def setupCtlDb(request):
    appname ="HumanResourcePlanning"
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    user = GetUserDetail(username)
    department= user.dep.dep_code 
    
    auth = GetAppList(user.id,appname)
    
    if auth is None :
        print('query set== None')
        return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานระบบ')
    else:
        is_access = auth.is_access
        is_admin = auth.is_admin
        if is_admin == 0 :  # ไม่ใช่ Admin ของแผนก หรือ หัวหน้า
             return HttpResponse('user นี้ไม่ได้กำหนดสิทธิ์ในการเข้าใช้งานหน้านี้ ')
    data= EmpCtlDb.objects.all().order_by('cde')
    
    
    context={
        'data':data ,
        
    }
    
    return render(request,'setting-ctldb.html',context)

# ----- section : สร้างข้อมูลประจำงวด ---
def CreateTransaction(request):
    
    emptypes = EmployeeType.objects.all()
    periods = EmpPeriod.objects.all()
    form= FrmCreateData()
    
    context = { 
        'form':form ,
        'emptypes':emptypes,
        'periods':periods,
        
    }
    
    return render(request,'create-transaction.html',context)

def RunnewTransaction(emptype,period) :
    
    print (emptype , period )    
    pass
#-- section Monthly --

def MonthlyDashboard(request):
    if request.session['username'] is not None:
            username = request.session['username']
    else:
        return redirect(reverse('login'))
    
    department = GetUserDetail(username).dep 
    # all worker by department
    #EmpGroup = TblDepartment.objects.all().order_by('dep_code')
    data = EmployeeType.objects.all()    
    for item in data: 
            
        item_ingroup = Empmas.objects.filter(
   
                            Q(emp_type = item.cde)
                            )
        
        num_item_ingroup = item_ingroup.count()
        
        item.num_item = num_item_ingroup
        item.save()
   
    context = {
            'username':username,
            'department':department, 
            'emptypes': data,
        }
    
    return render(request,'hm-monthend-dashboard.html',context)

def MonthendEmployeeList(request,emptype):
    
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    department = user.dep
    depid=1
    #employeeeDep= TblDepartment.objects.get(id=depid)
    #print(employeeeDep)
    
    row = Empmas.objects.filter (
            Q(emp_type = emptype) ,
            Q(workstatus = 0)
            
        ).order_by('-id')
    
    pagedata=Paginator(row,100)
   # print('pagedata=' , pagedata)
    page_number=request.GET.get('page')
    page_obj = pagedata.get_page(page_number)  
    
    context={
        'emptype': emptype,
        'depid' : depid,
        'data':row,
        'page_obj': page_obj,
        'username':username,
        'department':department,
        
    }
    
    return render(request,'hm-monthend-employeelist.html',context)

def MonthendTransaction(request,emptype,id):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    department = user.dep
    depid=1
    
    EmpmasData = Empmas.objects.get(id=id)

    row = EmpTransaction.objects.filter (
            Q(emp_cde = EmpmasData.emp_cde )
        ).order_by('code')
    
    
    if request.method=="POST":
        
        form=FrmEmpTransaction(request.POST)
        
        if form.is_valid():    
            #step process 1. check duplicate code if not then save new data else if exist update data
            
            pass
    else: 
        form=FrmEmpTransaction()
    
    context = {
        'form':form ,
        'data' : row ,
        'empcde': EmpmasData.emp_cde,
        'empname':EmpmasData.emp_name ,
        'emptype':emptype,
        'depid':depid ,
        'usernanme':username ,
        'department': department,
        
    }
    return render(request,'hm-monthend-transaction.html', context)

def MonthendEditTransaction(request,emptype,empcde,id):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    department = user.dep
    depid=1
    
    periods = EmpPeriod.objects.filter(
            Q(emptype=emptype ) ,
            Q(status = 0 )
    )
    
    EmpmasData = Empmas.objects.get(emp_cde=empcde)

    row = EmpTransaction.objects.get (id=id)
    try:
        code = row.code.cde
        period = row.period.cde
    except:
        code = None
        period = None
        
    print(code,period)    
    
    dtransaction = dailyTransaction.objects.filter(
        Q(emp_cde=empcde ) ,
        Q(code = code ) ,
        Q(period = period )
    )
    
    if request.method=="POST":
        
        form=FrmEmpTransaction(instance=row , data=request.POST)
        
        if form.is_valid():    
            #step process 1. check duplicate code if not then save new data else if exist update data
            
            pass
    else: 
        form=FrmEmpTransaction(initial=row.__dict__)
    
    context = {
        'form':form ,
        'data' : row ,
        'empcde': empcde,
        'empname':EmpmasData.emp_name ,
        'emptype':emptype,
        'depid':depid ,
        'usernanme':username ,
        'periods':periods,
        'department': department,
        'empid' : EmpmasData.id ,
        'dtransaction':dtransaction 
        
        
    }
    
    return render(request,'hm-monthend-edit-transaction.html', context)

#time Data Models
def ta_import(request,emptype):
    # step of process 
    """ 
    0. ควรจะเลือก period ในการทำงานก่อนหรือไม่  
    1. add New All Empmas data into Emptime_mast (condition emp_type = emptype, workstatus = '0' )
    2. loop emptime_mast then just look in TA_MAST (in/out) 
    3. update data in emptime_mast 
        
    """

    # กำหนดค่าข้อมูลหลักพนักงาน
    EmpmasData = Empmas.objects.filter(
        Q(emp_type = emptype , workstatus ='0') 
    ).order_by('emp_cde')
    
    # กำหนดค่าเริ่มต้นในฟอร์ม 
    EmpType = EmployeeType.objects.get(cde=emptype) #ส่งค่ามาจาก url
    period = None
    enddate = date.today()
    startdate = enddate - timedelta(days = 1 )
    #กำหนดค่าตัวเลือกในฟอร์ม
    periods = EmpPeriod.objects.filter(Q(emptype=emptype,status=0)).order_by('cde')
    # emptypes = EmployeeType.objects.all()
    
    print(emptype , 'period:', period ,startdate, enddate ,type(startdate) )
   # print(periods)
    
    data = {
        'emptype' :EmpType ,
        'startdate' : startdate ,
        'enddate' : enddate ,
        'period' : period ,
        'periods' : periods ,
    }
    
    fmt = '%H:%M:%S' # format time
    fmt_date = '%Y-%m-%d' #format Date
    
    if request.method == 'GET' :
        form = TimeImportForm(initial = data )
    else: 
        if request.method =='POST' :
            form = TimeImportForm(data=request.POST)
            
            if form.is_valid():
                
                startdate = form.cleaned_data.get('startdate')
                enddate =form.cleaned_data.get('enddate')
                #emptype = form.cleaned_data.get('emptype')
                period = form.cleaned_data.get('period')
                print('Form is valid' , form.cleaned_data ,type(startdate) , period )
                Period = EmpPeriod.objects.get(cde=period)
                
                st_date =  datetime.strptime(startdate,fmt_date)
                end_date = datetime.strptime(enddate,fmt_date)
                
              #  print("start date=" , st_date , type(st_date) , "end date=" , end_date )
                
                while st_date <= end_date:
                    
                    date_work = st_date #datetime.strptime(st_date,fmt_date)  # output = "YYYY-MM-DD 00:00:00" format datetime
                    # d = datetime.strptime(date_work,'%Y-%m-%d')
                    workdate = date_work.strftime('%Y-%m-%d') # output format ==> STRING as :YYYY-MM-DD
                    dayofweek = date_work.weekday() #output 1:อังคาร 2:พุธ ... 6. อาทิตย์ 7: จันทร์
                    dayname = dayName(dayofweek) 
                    
                    
                    #date_work = st_date.strftime('%Y-%m-%d')  # print("workdate=" , date_work ) # output as string= "YYYY-MM-DD" 
                    #d = datetime.strptime(date_work,'%Y-%m-%d')  #format as datetime  'YYYY-MM-DD HH:MM:SS
                    #dayofweek = d.weekday() # 1:อังคาร 2:พุธ ... 6. อาทิตย์ 7: จันทร์
                    #dayname = dayName(dayofweek) 
                    
                    print(dayname, date_work ,  "workdate:" , workdate ) #==> output date_work= YYYY-MM-DD:00:00:00 workdate = YYYY-MM-DD
                    
                    for item in EmpmasData:   # all employee Master
                        empcde = item.emp_cde
                        
                        Emptime_Mast = EmpTime.objects.filter(
                            Q(emp_cde__emp_cde = empcde , workdate = workdate)
                        )

                        #print (Emptime_Mast , Emptime_Mast.count())
                         
                        nrec = Emptime_Mast.count()
                        #print(nrec)
                        if nrec == 0 :  # mean Data not found in emptime_mast Then add new data into emptime_mast
                            print ('Add new Emptime_Mast ' , empcde, workdate )
                            emptime = []
                            emptime.append(EmpTime(
                                emp_cde = item ,
                                shift = TblShift.objects.get(shift=item.shift.shift) ,
                                period = Period , 
                                ta_date = workdate , # date_work ,
                                workdate = workdate ,
                                remarks = dayname 
                            ))
                            
                            EmpTime.objects.bulk_create(emptime)
                        #endif 
                           # print ('data found in emptime_mast' , Emptime_Mast  )

                            # get update data from ta_mast that emp_cde= empcde and workdate = st_date 
                            
                        emptimedata = EmpTime.objects.get(
                                        emp_cde__emp_cde = empcde , workdate = workdate
                                    )
                        
                        ta = TimeMast.objects.filter(
                            Q(emp_cde = empcde , workdate = workdate),
                            )
                        ta_count = ta.count()
                        
                        if ta_count > 0 :
                            
                            #print('TA_MAST  DATA ' ,'จำนวน' , ta_count)
                            
                            for ta_item in ta: 
                                # print(ta_item.id)
                                
                                sht_code = ta_item.shift.shift
                                # update time data into Emptime_mast
                                ta_item.period = period  # update period into ta_mast
                                ta_item.save(update_fields=['period'])
                                
                                
                                Shiftdata = TblShift.objects.get(shift = sht_code)
                                #print(ta_item.emp_cde, ta_item.workdate , ta_item.inout, ta_item.worktime  , Shiftdata.shift ,Shiftdata.starttime)                                    
                                shiftCrossDay = Shiftdata.shift_cross_day
                                shiftStart = datetime.strptime(Shiftdata.starttime,fmt)
                                shiftEnd = datetime.strptime(Shiftdata.endtime,fmt)
                                shiftOtStart = datetime.strptime(Shiftdata.ot_st,fmt)
                                shiftOtEnd = datetime.strptime(Shiftdata.ot_end,fmt) 
                                #print ('SHIFT-CODE:' , sht_code , shiftCrossDay, shiftStart, shiftEnd, shiftOtStart , shiftOtEnd)
                                        
                                pay="Y"
                                ot=""   
                                remarks_other=''
                                msg='' 
                                numot =0
                                numbf =0
                                numlate=0
                                #print (shiftStart )  # interval between start and end
                                
                                if ta_item.inout == "IN" :
                                    time_in = ta_item.worktime
                                    remarks = ta_item.remark
                                    worktime = datetime.strptime(time_in,fmt) #แปลง Str ให้เป็นรูปแบบของเวลา เพื่อ ทำการเปรียบเทียบค่า กับ shift information
                                    
                                    t_h_st = Shiftdata.starttime[:2]
                                    t_m_st = Shiftdata.starttime[4:5]
                                    #print (worktime , shiftStart )
                                    
                                    if worktime > shiftStart :
                                        msg = msg + ' **สาย'
                                        t_min = time_in[4:5] 
                                        t_hour= time_in[:2]

                                        numlate = CalculateTime(t_h_st,t_m_st,t_hour,t_min)
                                        
                                        
                                        #  print (t_hour , t_min ,type(t_hour) , type(t_min) , tt )
                                        # late 
                                        # numlate= tt #shiftStart - worktime 
                                        
                                    else:
                                        msg = msg + "เข้างานปกติ"
                                        numlate = 0     
                                        
                                    print(msg ,numlate ,type(numlate))
                                                                            
                                    # print ('LATE =' , numlate)
                                    emptimedata.period = Period
                                    emptimedata.shift = Shiftdata 
                                    emptimedata.timein=time_in
                                    emptimedata.remarks_other =  msg
                                    emptimedata.pay = pay
                                    emptimedata.ot = ot
                                    emptimedata.numlate = numlate 
                                    
                                    emptimedata.save(update_fields=['period','shift','timein','remarks_other','pay' ,'ot' ,'numlate'])
                                    
                                elif ta_item.inout=="OUT" :
                                    time_out = ta_item.worktime
                                    remarks = ta_item.remark
                                    
                                    worktime = datetime.strptime(time_out,fmt)
                                    t_min = time_out[4:5] 
                                    t_hour= time_out[:2]
                                    if worktime > shiftEnd :
                                        msg = msg + 'ออกงานปกติ'
                                        numot=0
                                        if worktime > shiftOtStart :
                                            t_h_st = Shiftdata.ot_st[:2] #18
                                            t_m_st = Shiftdata.ot_st[4:5] #00
                                            t_h_en = Shiftdata.ot_end[:2] #20
                                            t_m_en = Shiftdata.ot_end[4:5] #00
                                            
                                            # print('*** OT')
                                            if worktime > shiftOtEnd :
                                                msg= msg + ' * OT 2 ชม.'
                                                numot = CalculateTime(t_h_st,t_m_st, t_h_en,t_m_en)
                                                    
                                            else:
                                                
                                                msg = msg + ' * OT ไม่เกิน 2 ชม.'
                                                numot = CalculateTime(t_h_st,t_m_st, t_hour,t_min)
                                                
                                            ot ='Y'
                                        
                                        print("**OT " , ot , msg ,  numot)
                                            
                                        #numlate= shiftStart - worktime 
                                    else:
                                        msg= msg + 'ออกงานก่อนเวลา'
                                        t_h_st = Shiftdata.endtime[:2]
                                        t_m_st = Shiftdata.endtime[4:5]
                                        numbf =  CalculateTime(t_h_st,t_m_st,t_hour,t_min)
                                        print(msg , numbf)
                                        numot = 0     
                                        
                                    emptimedata.period = Period
                                    emptimedata.numot = numot    
                                    emptimedata.shift = Shiftdata 
                                    emptimedata.timeout=time_out
                                    emptimedata.remarks_other =  msg #remarks
                                    emptimedata.pay = pay
                                    emptimedata.ot = ot
                                        
                                    emptimedata.save(update_fields=['period','shift','timeout','remarks_other','pay' ,'ot' , 'numot'])
                        
                    #loop for Next Date
                    st_date = st_date + timedelta(days=1)  
                                                    
            else:
                print ("form is not valid " ,emptype , period , startdate ,enddate)
                form = TimeImportForm()
            #print(emptype)
            
            data = {
                'form':form ,
                'emptype': EmpType ,
                'startdate' : startdate ,
                'enddate' : enddate,
                'period' : period ,
                    }
            
            print('NEW VALUE ' , emptype, period , startdate ,enddate)
            #url = reverse('timedatalistbyworkdate',kwargs={'emptype': emptype , 'period': speriod , 'workdate': workdate , 'strcon':strcon } )
            #return HttpResponseRedirect(url)
            
            url = reverse('ta_dashboard_period' ,kwargs = {'emptype': emptype})
            return HttpResponseRedirect(url)
        
    context= {
        'emptype' : EmpType , 
        'periods' : periods ,
        'data' : data ,
        'form' : form ,
        
    }
    
    return render(request,'ta-import.html',context )

def timedata_list(request,emptype,period):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']    
    user=GetUserDetail(username)
    # print (strcon)
    #strcon = "all"
    
   # if strcon == 'all':
    print("module:timedata_list", emptype , period )
    

    timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype),
                Q(period = period )
                ).order_by('-workdate')
    if timedata.count() != 0:
        ncount = timedata.count()

    print('จำนวนรายการ'  , ncount)
    
    
    
    pagedata=Paginator(timedata,100)
    
    try:
        page_num =request.GET.get('page')
        page_obj = pagedata.get_page(page_num)  
        page_number = page_obj.number
    except:
        page_num = None
        page_obj = None
        page_number = None

    context={
     
        'data':timedata,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep,
        'workdate':None ,
        'emptype' : emptype,
        'period':period,
        'strcon': None,
        'dep_id' : None,
    }
  
    return render(request,'timedata_list.html',context)

# filter all data condition = emptype , period
def Timedata_filter(request,emptype,period):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)

    if request.method == "GET":
        name = request.GET.get('q') 
    else: 
        if request.method == "POST" :
            name =strcon
    print ("RUN Def : Timedata_filter " ,emptype , period , "look up word: " , name )
    
    timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype , period__cde = period ),
                Q(workdate = name)|
                Q(emp_cde__emp_cde = name )|
                Q(emp_cde__emp_name__contains = name )|
                Q(emp_cde__emp_dep = name )|
                Q(remarks_other__contains=name)
                    
                ).order_by('-workdate')
    pagedata=Paginator(timedata,100)  
    try:  
        page_num =int(request.GET.get('page' ,'1'))
    except ValueError:
        page_num = 1 
    
    strcon = name 
     
    try:          
      page_obj = pagedata.get_page(page_num)  
    except PageNotAnInteger:
        page_obj = pagedata.page(1)
    except EmptyPage:
        page_obj = pagedata.page(pagedata.num_pages)
    
    page_number = page_obj.number
   
    context={
     
        'data':timedata,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep,
        'workdate': None,
        'emptype' : emptype,
        'period' : period ,
        'strcon' : strcon
    }
  
    return render(request,'timedata_list.html',context)

# module timedatalistbyworkdate
def timedata_list_bydate(request,emptype,period,workdate,strcon):  #strcon :เงื่อนไข all:all data , work : only who is time stamp ,absent:Absent 
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']    
    user=GetUserDetail(username)
    
    print('Run Def: timedata_list_by_date: condition: ' , workdate , strcon )
  
    timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype , workdate= workdate ),
                ).order_by('-id')
    
    if strcon == 'work' : 
        data = timedata.filter(
                Q(timein__isnull=False)|
                Q(timeout__isnull=False)
            ).order_by('-id')
    
    if strcon == 'absent' : 
        data = timedata.filter(
                Q(timein__isnull=True),
                Q(timeout__isnull=True)
            ).order_by('-id')
    if strcon == 'leave' : 
        data = timedata.filter(    
                Q(leavecode__isnull=False)
            ).order_by('-id')       
    
    if strcon == 'late' :  #late and outbf
        data = timedata.filter(
                Q(numlate__gt=0)
               
            ).order_by('-id')
    try:
        pagedata=Paginator(data,500)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    except:
        pagedata=None
        page_number=0
        page_obj = None
    
    context={
     
        'data':data,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep,
        'workdate': workdate,
        'emptype' : emptype,
        'period' :period ,
        'strcon' : strcon ,
        'dep_id' : None ,
    }
  
    return render(request,'timedata_list.html',context)

def timedata_list_filter_bydate(request,emptype,period,workdate,strcon , dep_id): #name = timedatalistbyworkdate
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    
    if request.method == "GET":
        name = request.GET.get('q') 
    else:
        name = None 
    print("RUN Def: timedata_list_filter_bydate" , emptype ,period,workdate ,strcon ,dep_id)
        
    print ('name=' , name , type(name) , 'timedata_filter_bydate=' ,emptype , period , workdate ,strcon )
    
    
    timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype ,workdate = workdate ,emp_cde__emp_dep__id = dep_id ),
                Q(emp_cde__emp_cde = name )|
                Q(emp_cde__emp_name__contains = name )|
                Q(remarks_other__contains=name)
                
                
            ).order_by('-ta_date')
    
    if timedata.count() != 0 :
        pagedata=Paginator(timedata,100)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    else:
        pagedata=None
        page_number = 0
        page_obj = None
    
    context={
     
        'data':timedata,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep,
        'workdate': workdate, 
        'strcon' : strcon ,
        'period' : period ,
        'emptype' : emptype,
        'dep_id' : dep_id ,
    }
  
    return render(request,'timedata_list.html',context)

#time data list by workdate and department  รายการข้อมูลเวลาแสดงตามวันที่และแผนก
def timedata_list_bydate_dep(request,emptype,period,workdate,strcon,dep_id):  #strcon :เงื่อนไข all:all data , work : only who is time stamp ,absent:Absent 
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']    
    user=GetUserDetail(username)
   # depcode= TblDepartment.objects.get(id=dep_id).dep_code
    print('RUN timedata_list_bydate_dep: ' ,emptype , workdate , strcon, "dep=", dep_id  )
    
    if dep_id != None:
        #d = TblDepartment.objects.get(id=dep_id)
        #depcode = d.dep_code 
        
        timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype , workdate = workdate , emp_cde__emp_dep__id = dep_id )
                ).order_by('-id')
    else: 
        timedata = EmpTime.objects.filter(
                Q(emp_cde__emp_type = emptype , workdate = workdate )
                ).order_by('-id')
        
    if strcon == 'all' : 
        data = timedata
        
    if strcon == 'work' : 
        data = timedata.filter(
                Q(timein__isnull=False)|
                Q(timeout__isnull=False) )
          
    if strcon == 'absent' : 
        data = timedata.filter(
                Q(timein__isnull=True , timeout__isnull=True ) )
       
    if strcon == 'leave' : 
        data = timedata.filter(
                Q(leave__isnull=False)
            )
    if strcon == 'late' : 
        data = timedata.filter(
                Q(numlate__gte=1)
            )
    try:
        pagedata=Paginator(data,500)
        page_number=request.GET.get('page')
        page_obj = pagedata.get_page(page_number)  
    except:
        pagedata=None
        page_number=0
        page_obj = None
    
    context={
     
        'data':data,
        'page_obj': page_obj,
        'username':username,
        'department':user.dep.dep_code,
        'workdate': workdate,
        'emptype' : emptype,
        'period' :period ,
        'strcon' : strcon ,
        'dep_id' : dep_id ,
    }
  
    return render(request,'timedata_list.html',context)

def Timedata_update(request,emptype,period,workdate,strcon,id):
    if request.session['username'] is None:
        return redirect(reverse('login'))
    
    username = request.session['username']
    
    user=GetUserDetail(username)
    
    speriod = period 
    
    #print(workdate)
    
    data =EmpTime.objects.get(id=id )
    
    print(1, data)
    emp_cde = data.emp_cde.emp_cde

    if emp_cde is not None:
        EmpmasData = Empmas.objects.get(emp_cde = emp_cde)
        dep = EmpmasData.emp_dep
    else:
        EmpmasData = None
    
    print (3, id, emp_cde , workdate , strcon ,period , dep )
    
    periods  = EmpPeriod.objects.filter(
            Q(status='0'),
            Q(emptype= emptype) ,
            ).order_by('cde')
    shifts = TblShift.objects.all()
    
    ot_types = TblOT.objects.all().order_by('cde') 
    
    
    
    #print(employees.count())

    if request.method=="GET":
        form = TimeDataForm(initial=data.__dict__) 
        
        
    elif request.method == "POST":
     #   docform =DTransactionForm(instance=dtransaction,dtransaction=request.POST)
        form= TimeDataForm(instance = data ,data=request.POST)
        
        print('DATA' , request.POST)
        
        if form.is_valid():
            
            data= form.save(commit=False)
            
            data.emp_cde = EmpmasData
            
            #emp_cde = EmpmasData.emp_cde #form.cleaned_data.get('emp_cde')
          
            ta_date = form.cleaned_data.get('ta_date')
            data.workdate = ta_date.strftime('%Y-%m-%d')
            print ( ta_date , data.workdate )

            newperiod = form.cleaned_data.get('period').cde
            newshift = form.cleaned_data.get('shift').shift
            #print('period:' ,newperiod , 'shift:', newshift)  ==>output OK
            
            PeriodData= EmpPeriod.objects.get(cde=newperiod)  #intance of period 
            data.period = PeriodData  
            
            ShiftData = TblShift.objects.get(shift=newshift)  #intance of Shift
            data.shift = ShiftData
            
            #num = form.cleaned_data.get('num')
            #payamt= form.cleaned_data.get('payamt')
            #workdate = form.cleaned_data.get('workdate')
            timein = form.cleaned_data.get('timein')
            timeout = form.cleaned_data.get('timeout')
            
            print  ('SAVE' , id , emp_cde, ta_date,data.period,timein,timeout , workdate ,data.shift ) 
            #print(speriod , period )   
            
            data.save()
            
            
            # update payamt in dtransaction with true condition 
            
        else:
            print('form is not valid ')
        
        url = reverse('timedatalistbyworkdate',kwargs={'emptype': emptype , 'period': speriod , 'workdate': workdate , 'strcon':strcon } )
        return HttpResponseRedirect(url)
        #return render(request,'timedata_list.html',context)
    
    context={
        'username' : username ,
        'department' : user.dep ,
        'form': form,
        'data':data,
        'periods' : periods ,
        'shifts' : shifts,
        'ot_types' : ot_types,
        'workdate' : workdate,
        'emptype' : emptype,
        'strcon' : strcon,
        'period' : speriod 
        
    }
    
    return render(request,'timedata_update.html',context)

