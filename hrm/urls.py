"""hrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views 


urlpatterns = [
    path('',include('hmadmin.urls')),
    
    path('admin/', admin.site.urls),
    
    path('',views.login_request,name='login'),
    path('index/',views.index,name='index'),
    path('register/',views.register_request,name='register'),
   # path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    
    path('home/',views.index, name='hmhome') ,
    path('hm/', views.menu_hm , name='menu_hm') ,
    path('ta/', views.menu_time , name='menu_time') ,
    path('payroll/', views.menu_payroll , name='menu_payroll') ,
    #path('login/',views.login ,name='login') ,
    
    path('hm/dashboard/',views.hmdashboard,name='hmdashboard'),
    path ('hm/leave/',views.tranleave , name = 'emptranleave') ,
    path ('hm/leave/filter/',views.tranleave_filter , name = 'emptranleave_filter') ,
    path ('hm/leave/view/<int:id>/',views.tranleave_edit , name = 'emptranleave_edit') ,
    path ('hm/leave/new/',views.tranleave_add , name = 'emptranleave_new') ,
    path ('hm/leave/history/<int:id>/',views.tranleave_history , name = 'emptranleave_history') ,
    
        
    path('hm/dashboard/<str:cde>/',views.hmdashboardbydep,name='hmdashboardbydep'),
    path('hm/employee/<str:cde>/<int:depid>/list/',views.employeelist,name='employeelist'),
    path('hm/employee/<str:cde>/<int:depid>/search/',views.EmployeeSearch,name='employeesearch'),
    path('hm/employee/<str:cde>/<int:depid>/new/',views.hmaddnew,name='hm-addnew'),
    path('hm/employee/<str:cde>/<int:depid>/edit/<int:id>/',views.hmedit ,name='hm-edit'),
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/editincome/',views.hmedit_income ,name='hm-edit-income'),
    
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/exper/',views.hmexper ,name='hm-exper'),
    path('hm/employee/<int:depid>/<int:empid>/exper/edit/<int:id>',views.hmexper_edit ,name='hm-exper-edit'),
    
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/refer/',views.hmrefer ,name='hm-refer'),
    path('hm/employee/<int:depid>/<int:empid>/refer/edit/<int:id>',views.hmrefer_edit ,name='hm-refer-edit'),
    
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/education/',views.hmeducation,name='hm-education'),
    path('hm/employee/<int:depid>/<int:empid>/education/edit/<int:id>',views.hmeducation_edit ,name='hm-education-edit'),
    
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/incexp/',views.hm_inc_exp,name='hm-inc-exp'),
  # path('hm/employee/<int:depid>/<int:empid>/education/edit/<int:id>',views.hmeducation_edit ,name='hm-education-edit'),
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/timehistory/',views.hm_timedata_history ,name='hm-timedata-history'),
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/<str:period>/timehistory/',views.hm_timedata_history_by_period ,name='hm-timedata-history_by_period'),
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/<str:period>/filter/',views.hm_timedata_history_filter ,name='hm-timedata-history-filter'),
    
    path('hm/employee/<str:cde>/<int:depid>/<int:id>/deduction/',views.hm_deduction ,name='hm-deduction'),
    
    path('hm/employee/shift/<str:emptype>/<int:depid>/<int:id>/<str:period>/',views.hm_shift_data ,name='hm-shift-data'),
    
  # menu Setting
    path('hm/setting/',views.hmsetting,name='hmsetting'),
  
  # menu Daily-transaction 
    path('hm/daily/create/',views.CreateTransaction,name='createtransaction'),
    path('hm/daily/create/<str:emptype>/<str:period>/',views.RunnewTransaction,name='runnew'),
    
    path('hm/dairy/',views.hmdaily,name='hmdailymenu') ,
    path('hm/dairy/transaction/',views.hmdaily_transaction ,name='hmdailytransaction') ,
    path('hm/dairy/transaction/filter/',views.hmdaily_transaction_filter ,name='hmdailytransactionfilter') ,
    path('hm/dairy/transaction/update/<int:id>/',views.hmdaily_transaction_update ,name='hmdailytransactionupdate') ,
    path('hm/dairy/transaction/addnew/',views.hmdaily_transaction_addnew,name='hmdailytransactionaddnew') ,
    path('hm/monthend/',views.hmmonthend,name='hmmonthendmenu') ,
    
   # path('time/dashboard/' , views.hmdashboard ,name="timedashboard") ,
    
    # ALL DATA Emptime
    path('ta/import/<str:emptype>/',views.ta_import , name ='ta-import') ,  # import time data
    
    path('ta/dashboard/',views.tadashboard ,name = 'ta-dashboard') ,  #แสดง ประเภทพนักงาน
    path('ta/<str:emptype>/',views.tadashboardbyperiod ,name = 'ta_dashboard_period') , #แสดงแยกตามประเภทพนักงาน และ งวดการทำงาน
    
    path('ta/<str:emptype>/<str:period>/',views.menu_time ,name = 'menu-time') ,
    
    #time by dep
    path('ta/sumalldep/<str:emptype>/<str:period>/<str:workdate>/',views.menu_time_by_dep ,name = 'menu-time-by-dep') ,
    path('ta/<str:emptype>/<str:period>/<str:workdate>/<str:strcon>/<str:dep_id>/',views.timedata_list_bydate_dep,name='timedatalistbyworkdateAnddep') ,
    
    #   
    path('ta/all/<str:emptype>/<str:period>/',views.timedata_list ,name='timedata') ,
    
    path('ta/<str:emptype>/<str:period>/filter/',views.Timedata_filter ,name='timedata_filter') ,
    
    # specify by date Emptime
    path('ta/<str:emptype>/<str:period>/<str:workdate>/<str:strcon>/',views.timedata_list_bydate,name='timedatalistbyworkdate') ,
    path('ta/<str:emptype>/<str:period>/<str:workdate>/<str:strcon>/<int:dep_id>/filter/',views.timedata_list_filter_bydate ,name='timedata_filter_bydate') ,
    path('ta/<str:emptype>/<str:period>/<str:workdate>/<str:strcon>/<int:id>/update/',views.Timedata_update ,name='timedata_update') ,

    #for Print or Export data
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else:
    urlpatterns += staticfiles_urlpatterns()
    