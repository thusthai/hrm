from dataclasses import fields
from hmadmin.models import AuthUser
from hmdb.models import TblUserAuth,TblAllowApp
from django.contrib.auth.models import User,Group,Permission
from django import forms

class FormUser(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username','email','dep','is_superuser','is_staff','is_active']
        labels = {
            'username':'ชื่อผู้ใช้งาน ' ,
            'is_superuser' : 'Admin ',
            'dep': 'แผนก/หน่วยงาน',
            'email':'Email:',
            'first_Name' : 'First Name',
            'last_name' : 'Last NAme',
            'is_active' : 'Active',
            'is_staff' : 'User',
            
          
        }
        
class formAddUserApp(forms.ModelForm):
    class Meta:
        model = TblUserAuth
        fields= ['user','content_type','is_access','is_admin','is_add','is_edit','is_delete','is_view','is_approve','is_authorize']
        
class formEditUserApp(forms.ModelForm):
    class Meta:
        model = TblUserAuth
        fields= ['is_access','is_admin','is_add','is_edit','is_delete','is_view','is_approve','is_authorize']        
        