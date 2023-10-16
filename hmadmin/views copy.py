from django.shortcuts import render,redirect
from django.http.response import HttpResponse,HttpResponseRedirect
from erpadmin.models import AuthUser
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User,Group,Permission
from erpadmin.forms import FormUser ,formAddUserApp,formEditUserApp
from erpdb.models import TblDepartment,TblUserAuth,TblAllowApp

from django.contrib.auth import login ,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
# Create your views here.
# appname = adminMenu
def appname():
    appname = 'adminMenu'
    return appname 

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
    """ 
    if app is not None :
        #app = app 
        is_admin = app.is_admin  
    else:
        #app = None
        is_admin = None
    
    print('2.APPLICATION:' , app ,'is_admin=' , is_admin)
    """
    return (app)
  
def GetUserDetail(usrname):
    
    user = AuthUser.objects.get(username=usrname)
 #   print ("1.USER: ",user) 
    
    
    #apps = TblUserAuth.objects.filter(Q(user = user.id)).order_by('app')
    #if apps.count() != 0 : 
    #    print (apps)
        
    #appList = GetAppList(userDetail.id)
     
    # return Allow application list 
    # return department-id  
   # department = userDetail.dep
   # print(department)
    
    return (user)

@login_required(login_url='login')
def adminhome(request):
    appname()
    print(appname())
    
    username = request.session['username']
    department=GetUserDetail(username).dep
    user = GetUserDetail(username)
    
    auth = GetAppList(user.id,appname())
    print(auth)
    if user.is_superuser == 0:  # only admin 
        if auth is None:
            return HttpResponse('Error.. Menu Not Authorized Please contact Admin.. ')
    
    #department = AuthUser.objects.get(username=username).dep
    
    context = {'username' : username ,
               'department':department }
    
    return render(request,'admin-home.html',context)
  
def userlist(request):  #display all vendor
    username = request.session['username']
    department=GetUserDetail(username).dep
    
    context = {'username' : username }
    title_msg= 'ข้อมูลผู้ใช้งานระบบ'
    users =AuthUser.objects.all().order_by('username')
    #dep = TblDepartment.objects.get(users.user_id)

    context = {'users':users,'title_msg':title_msg,'username':username,'department':department }
    
    return render(request,'user-list.html',context)

def useredit(request,id):
    username = request.session['username']
    department=GetUserDetail(username).dep
    #user = AuthUser.objects.get(username=username)
    if GetUserDetail(username).is_superuser == 1 :
        print(username, 'is system administrator or superuser')
    else:
        print ('err: you are not authorize', GetUserDetail(username).is_superuser)
        messages.error(request,"you are not authorized...")
        return redirect('userlist')
    
    row = AuthUser.objects.get(id=id)
    alldep = TblDepartment.objects.all()
    try:
        applist = TblUserAuth.objects.filter(Q
                    (user = id)
                ).all().order_by('content_type')
    except:
        applist = None
        pass
 
    data=row
    print('edit userid' , id , row.username , row.dep)
    print('App list',applist)
    
    if request.method=="POST":
        form = FormUser(instance =row, data=request.POST)
        if form.is_valid():
            form.save()
            
        return HttpResponseRedirect(reverse('userlist'))  
    else:
        form=FormUser(initial= row.__dict__)
        data=row
        
    context= {'form':form,
              'data':data,
              'deps':alldep,
              'applist':applist,
              'username':username,
              'department':department}
    
    return render(request,'user-edit.html',context)

def useradd(request):
    username = request.session['username']
    department=GetUserDetail(username).dep
    #user = AuthUser.objects.get(username=username)
    if GetUserDetail(username).is_superuser == 1 :
        print(username)
    else:
        print ('err: you are not authorize', GetUserDetail(username).is_superuser)
        return redirect('userlist')


    #row = AuthUser.objects.get(id=id)
    alldep = TblDepartment.objects.all()
   # applist = TblAllowApp.objects.all()
   
    username = '' 
    email = '' 
    dep = ' '
    is_superuser= False
    is_active= False
    is_staff = True
    
    form = FormUser()
    
    if request.method=="POST":
       
        form = FormUser(request.POST)
         
        if form.is_valid():
            
           # username = form.cleaned_data.get('username')
           # email = form.cleaned_data.get('email')
          
            
         #   if not is_user_exist(username):
            form.save()

    
            context= {'form':form,        
                    }
            
            return HttpResponseRedirect(reverse('userlist'))
         #   else:
         #       messages.error (request ,'Error .. User Name มีอยู่แล้ว')
            
    context= {'form':form,
                        'deps':alldep,        
                        'username':username,'department':department,
                        'email':email,
                        'dep': dep,
                        'is_superuser': is_superuser,
                        'is_staff': is_staff ,
                        'is_active': is_active}    
    return render(request,'user-add.html',context)

def is_user_exist(usr_name):
    
    print(usr_name)
    
    newuser = User.objects.filter(Q(username=usr_name))
    if newuser.count() == 0 : # mean Not found
        return False
    else:
        return True 
def applist_exist(userid,appid):
    print(userid, appid)
    appexist = TblUserAuth.objects.filter(
                Q(user= userid) , Q(app = appid)
                )
    #appexist = appexist[0] 
    print (appexist)
    
    if appexist.count() == 0 :
        return False
    else:
        return True
    
    
def adduserapp(request,user):
    print('Add auth user:' , user)
    
    apps = TblAllowApp.objects.all()
    alluser = AuthUser.objects.all()
    content_types  = ContentType.objects.all()
    """  
    row = TblAllowApp.objects.filter(
        Q(user_id=id),
        Q(app_id = appid ))
    """
    err_msg = None 
    selectuser = AuthUser.objects.get(id=user)
    
    print(apps)
    
    form= formAddUserApp()
    
    if request.method == 'POST' :
        form=formAddUserApp(request.POST)
        
        if form.is_valid():
            # must be check dupplicate app-list before save
            newapp = form.cleaned_data['app'] 
            if not applist_exist(user,newapp): 
               
                form.save()
                
                print('SAVE NEW DATA')
                url = reverse('useredit',kwargs= {'id':user})
                return redirect(url)
            else:
                # display error massage : error this app already register by this user id 
                err_msg = "Error.. duplicate app in list "
               # print(err_msg)
                pass                 
        else:
            err_msg = "Error..กรุณาตรวจสอบข้อมูลอีกครั้ง "
            print('DATA NOT SAVE')
            
    context = {'form':form,
                'apps':apps,
                'user':selectuser,
                'err_msg':err_msg,    
                'content_types': content_types,           
            }
    return render(request,'add-user-app.html',context)

def edituserapp(request,user,content_type):
    print('Edit user:' , user , content_type)
    
    apps = TblAllowApp.objects.all()
    
    row = TblUserAuth.objects.get(
            user= user , content_type = content_type
             
            )
    
    data=row
    
    print('App:', data)

    if request.method=='POST' :
        form=formEditUserApp(instance=row, data=request.POST)
        
        if form.is_valid():
            r=form.save()
            r.save()
            
         #   q=row
        #  q.user = user  # save user id into row  
        #    q.save()
        
            print('Save data OK' , user , content_type)
            
            url=reverse('useredit',kwargs={'id':user})
            return HttpResponseRedirect(url)
            #return HttpResponseRedirect(reverse('useredit',user))  
    
    else:
        form= formEditUserApp(initial=row.__dict__)
        data=row
    
    context = {'form':form,
                'apps':apps,
                'data': data,
                'edituser':user,
                'editapp': content_type,               
    }
    
    return render(request,'edit-user-app.html',context)
