from django.urls import path,include
from . import views

urlpatterns = [
  
    
    path('adminhome/',views.adminhome,name='adminhome'),
    path('adminhome/userlist/',views.userlist,name='userlist'),
    path('adminhome/edit/<int:id>/',views.useredit,name='useredit'),
    path('adminhome/addnew/',views.useradd,name='useraddnew'),
    path('adminhome/applist/<int:user>/',views.adduserapp,name='adduserapp'),
    path('adminhome/applist/<int:user>/<int:content_type>/',views.edituserapp,name='edituserapp'),
]
