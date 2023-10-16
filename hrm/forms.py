from unicodedata import decimal
#from erpdb.models import Bom,Bomdetails
from django import forms
from django.forms import formset_factory ,modelformset_factory,inlineformset_factory

from hmdb.models import Empmas,EmpExper,EmpHealth,EmpReference,EmpEducation,EmpIncExpDb,EmpDeduction,EmpmasIncome,EmpTranLeave
from hmdb.models import EmpCtlDb , EmpIncExpDb , TaxDeduction ,TaxRate ,EmployeeType,dailyTransaction,EmpTransaction
#from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hmdb.models import EmpTime  ,EmpmasResign

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        
    def save(self,commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
        labels = {
            'username': 'ชื่อผู้ใช้',
            'password': 'รหัสผ่าน',
        }


class DateTimeHelper():    
    @staticmethod
    def human_readable_to_sql(docdate):
        d = datetime.strptime(docdate, '%d/%m/%Y').date()
        return str(d)
    
class DateInput(forms.DateInput):
    input_type='date'
   # format= '%d/%m/%Y %H:%M:%S'
   # widget = forms.DateTimeInput(attrs= {
   #          'class':'form-control datetimepicker-input' ,
   #          'data-target': '#datetimepicker1'
   #      })
    
class TimeInput(forms.TimeInput):
    input_type='time'
    format= '%H:%M:%S'

class DateForm(forms.Form):
     date=forms.DateTimeField(
         input_formats = ['%d/%m/%Y %H:%M'],
         widget = forms.DateTimeInput(attrs= {
             'class':'form-control datetimepicker-input' ,
             'data-target': '#datetimepicker1'
         })
     )     
      
class DtransactionHead(forms.Form):
    docno = forms.CharField(max_length = 30)
    docdate = forms.DateField()
    period = forms.CharField(max_length=20 )
    
    widgets = {
            'docno' : forms.TextInput(attrs= {
                'class' : 'form-control' ,
                'placeholder' : 'Enter Document No' ,
            
            }) ,
            
            'docdate':forms.DateInput(format='%d/%m/%Y')
        }
    
class DTransactionForm(forms.ModelForm):

    class Meta:
        model= dailyTransaction
        fields= ['code','num','payamt','docno','docdate','period','workdate','work_starttime','work_endtime',
                 'workstarttime', 'workendtime']
        labels = {
            'emp_cde':'พนักงาน',
            'period':'งวดบัญชี',
            'docno': 'เอกสารเลขที่' ,
            'docdate' : 'วันที่เอกสาร' ,
            'code': 'รายการ ',
            'num' : 'จำนวน (หน่วย: วัน/ชม.)' ,
            'payamt' : 'คิดเป็นเงิน' ,
            'workdate': 'วันที่ทำรายการ',
            'workstarttime' : 'เวลาเริ่มต้น' ,
            'workendtime' : 'เวลาสิ้นสุด' ,
            
        }
        widgets = {  
          'docdate':forms.DateInput(attrs= {
              'class': 'form-control datetimepicker-input' ,
                    'data-target' : 'workdatepicker'
              }
            ),
                
          'workdate' : forms.DateInput( attrs={
                    'class': 'form-control datetimepicker-input' ,
                    'data-target' : 'workdatepicker'
                }
            ),
          'workstarttime' : forms.TimeInput(attrs={
             
              'data-target' : 'workstarttime'
          }),
          'workendtime' : forms.TimeInput(attrs={
              'data-target' : 'workendtime',
              'format' : 'H:i',
          })
            
           
        
        }
   

TransactionFormSet = formset_factory(DTransactionForm,extra=1 )

TransactionModelFormset = modelformset_factory(dailyTransaction,
                        fields= ('item','emp_cde','code','num','payamt','workdate','work_starttime','work_endtime','workstarttime','workendtime'),
                        extra=1 ,
                        
                        )


class EmployeeIncomeForm(forms.ModelForm):
    class Meta:
        model = Empmas
        fields = ['emp_income','emp_cum_income','emp_cum_soc','emp_cum_tax',
                  'em_bf_inc','em_bf_soc','em_bf_tax' 
                
                  ]

        labels = {
            'emp_cde' : 'รหัสพนักงาน:',
            'emp_income' : 'เงินได้:', 
            'emp_cum_income' : 'สะสมเงินได้', 
            'emp_cum_soc' : 'สะสมประกันสังคม', 
            'emp_cum_tax' : 'สะสมภาษีเงินได้', 
            'em_bf_inc' : 'รายได้ยกมา',
            'em_bf_soc': 'ประกันสังคมยกมา' ,
            'em_bf_tax': 'ภาษีเงินได้ยกมา' ,
        }
        

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Empmas
        fields = ['emp_cde','emp_name','emp_surname','emp_name_eng','emp_add1','emp_add2','emp_mobile','emp_email',
                  'emp_position','emp_dep','emp_type','emp_cardid','emp_birthdate','emp_taxid','emp_socialid' ,'shift' ,
                  
                  'workstatus' , 'emp_startworkdate','emp_prodate','emp_hiredate','emp_pf','emp_sex','emp_imageurl'
                  ]

        labels = {
            'emp_cde' : 'รหัสพนักงาน:',
            'emp_pf' : 'คำนำหน้า:', 
            'emp_sex' : 'เพศ:', 
            'emp_name' : 'ชื่อ (ภาษาไทย)' ,
            'emp_surname': 'นามสกุล' , 
            'emp_name_eng' : 'ชื่อ-สกุล(ภาษาอังกฤษ)', 
            'emp_add1' : 'ที่อยู่:เลขที่ หมู่ที่ อาคาร ถนน ', 
            'emp_add2' : 'แขวง/ตำบล เขต/อำเภอ จังหวัด รหัสไปรษณีย์', 
            'emp_mobile' : 'เบอร์ติดต่อ(มือถือ)',
            'emp_email': 'อีเมลล์' ,
            'emp_position' :'ตำแหน่ง','emp_dep':'หน่วยงาน/แผนก','emp_type':'ประเภทพนักงาน',
            'emp_cardid': 'เลขบัตรประชาชน',
            'emp_birthdate':'วันเดือนปีเกิด' ,
            'emp_taxid' : 'เลขประจำตัวผู้เสียภาษี',
            'emp_socialid' : 'เลขประจำตัวผู้ประกันตน',
            'workstatus' : 'สถานะพนักงาน', 
            'emp_startworkdate': 'วันที่เริ่มงาน','emp_prodate':'วันที่ผ่านงาน' ,'emp_hiredate': 'วันที่ลาออก' ,
            'emp_imageurl' : 'รูปประจำตัว',
            'shift' : 'กะทำงาน'
                }
        
        widgets = {
            'emp_birthdate': forms.DateInput(format='%d/%m/%Y') ,
            'emp_startworkdate' :  forms.DateInput(format='%d/%m/%Y') ,
            'emp_prodate' :  forms.DateInput(format='%d/%m/%Y') ,
            'emp_hiredate' :  forms.DateInput(format='%d/%m/%Y') ,
          
            
           # 'emp_cardid' : forms.CharField(format="9-9999-99999-9-99")
        }
class FrmEmpmasIncome(forms.ModelForm):
     class Meta:
        model = Empmas
        fields = ['emp_income','emp_income_d','emp_income_h','emp_cum_income','emp_cum_soc','emp_cum_tax',
                  'em_bf_inc','em_bf_soc','em_bf_tax' 
                
                  ]

        labels = {
            'emp_cde' : 'รหัสพนักงาน:',
            'emp_income' : 'เงินได้:', 
            'emp_income_d' : 'เงินได้/วัน:',
            'emp_income_h' : 'เงินได้/ชม.:',  
          
            'emp_cum_income' : 'สะสมเงินได้', 
            'emp_cum_soc' : 'สะสมประกันสังคม', 
            'emp_cum_tax' : 'สะสมภาษีเงินได้',
             
            'em_bf_inc' : 'รายได้ยกมา',
            'em_bf_soc': 'ประกันสังคมยกมา' ,
            'em_bf_tax': 'ภาษีเงินได้ยกมา' ,
        }
        
class EmployeeExperienceForm(forms.ModelForm):
    class Meta:
        model= EmpExper
        fields='__all__'
    
        labels ={
        'p_seq' : 'ลำดับ',
        'p_company' : 'บริษัทฯ' ,
        'p_position' : 'ตำแหน่ง',
        'p_duty':'หน้าที่',
        'p_startdte' : 'วันที่เรื่มงาน' ,
        'p_enddte' : 'วันที่สิ้นสุด' ,
        
            }
        widgets = {
            'p_duty' : forms.Textarea(attrs= {'rows':3 , 'cols':70} ),
            'p_startdte' :  forms.DateInput(format='%m/%d/%Y') ,
            'p_enddte' :  forms.DateInput(format='%m/%d/%Y') ,
             
        }
    def __init__(self,*args,**kwargs):
        super(EmployeeExperienceForm,self).__init__(*args,**kwargs)
        
        self.fields['p_company'].error_messages.update({
            'required': 'กรุณาระบุชื่อบริษัท..',
            
        })
        
        self.fields['p_seq'].error_messages.update({
            'required': 'ระบุ SEQ.',
            
        })
    
class EmployeeEducationForm(forms.ModelForm):
    class Meta:
        model= EmpEducation
        fields='__all__'
    
        labels ={
        'p_seq' : 'ลำดับ',
        'p_institue' : 'สถานศึกษา' ,
        'p_level' : 'วุฒิการศึกษา',
        'p_major':'คณะหรือสาขาวิชา',
        'p_year' : 'ปีที่จบการศึกษา' ,
        'p_gpa' : 'เกรด' ,
        
        
            }
        
class EmployeeHealthForm(forms.ModelForm):
    class Meta:
        model= EmpHealth
        fields='__all__'
    
        labels ={
    
        'p_hieght' : 'น้ำหนัก(kg.)' ,
        'p_weight' : 'ส่วนสูง (cm)',
        'p_blood':'กรุ๊ปเลือด',
        'p_disease' : 'โรคประจำตัว' ,
        'p_hiv' : 'HIV DEFECTED' ,
        'p_vdrl' : 'ตรวจพบโรคซิฟิลิส',
        'p_drug' :'ยาใช้ประจำ',
        
        
            }
class EmpReferenceForm(forms.ModelForm):
  #  p_seq = forms.CharField(error_messages={'required': 'กรุณาระบุลำดับที่..'})
  #  p_name = forms.CharField(error_messages={'required': 'กรุณาระบุชื่อ..'})
    
    class Meta:
        model  = EmpReference
        fields = ['p_seq','p_name','p_address','p_tel','p_career'
        ]
        
        labels ={
        'p_seq' : 'ลำดับ',
        'p_name' : 'ชื่อ-สกุล',
        'p_tel' : 'เบอร์ติดต่อ',
        'p_career':'อาชีพ',
        'p_address' : 'ที่อยู่' ,
        }
        
    
        widgets = {
            'p_address' : forms.Textarea(attrs= {'rows':3 , 'cols':70} ),
               
        }
    def __init__(self,*args,**kwargs):
        super(EmpReferenceForm,self).__init__(*args,**kwargs)
        
        self.fields['p_name'].error_messages.update({
            'required': 'กรุณาระบุชื่อ..',
            
        })
        
        self.fields['p_seq'].error_messages.update({
            'required': 'ระบุ SEQ..',
            
        })
class IncExpForm(forms.ModelForm):
    class Meta:
        model= EmpIncExpDb
        fields=[
        
            'code',
            'emp_amt',
          
]
    
        labels ={
           
            'code': 'รายการ', 
            'emp_amt': 'ฐานคำนวน',
          
        
        
            }
class EmpDeductionForm(forms.ModelForm):
    class Meta:
        model= EmpDeduction
        fields=[
            
            'deduct_cde',
            'num',
       
]   
        labels ={
           
            'deduct_cde': 'รายการ', 
            'num': 'จำนวน',

            }

class CtlDbForm(forms.ModelForm):
    class Meta:
        model= EmpCtlDb
        fields = '__all__' 


class FrmCreateData(forms.Form):
    emptype = forms.CharField(max_length=20 )
    period = forms.CharField(max_length=20)
    
    labels = {
        'emptype': 'ประเภทพนักงาน',
        'period' : 'งวดทำงาน' ,
    }

class FrmEmpTransaction(forms.ModelForm):
    class Meta:
        model = EmpTransaction 
        fields= ['emp_cde','code','numhour','numday','num','period','payamt']
        
        labels= {
            'code':'รายการ' ,
            'numhour' : 'จำนวนนาที' ,
            'numday': 'จำนวนวัน' ,
            'num' : 'จำนวนชม.',
            'period' : 'งวด' ,
            'payamt' : 'จำนวนเงิน'
        }
        
       
# form บันทึกเวลาเข้า ออก
class TimeImportForm(forms.Form):
    period = forms.CharField(max_length = 20)
    #emptype = forms.CharField(max_length=20 )
    # period = forms.CharField(max_length=20)
    startdate = forms.CharField(max_length=20)
    enddate = forms.CharField(max_length=20 )
    
    class Meta:
        labels = {
            'period' : 'ระบุงวดบัญชี' ,
            #'emptype': 'ประเภทพนักงาน',
            'period' : 'งวดทำงาน' ,
            'startdate' : 'เริ่มวันที่' ,
        }
    widgets = {
       # 'startdate' : forms.DateInput(format='%d-%m-%Y'),
       # 'enddate' :   forms.DateInput(format='%d-%m-%Y'),
    } 
    

class TimeDataForm(forms.ModelForm):
    class Meta:
        model = EmpTime 
        fields= ['emp_cde','ta_date','timein','timeout','shift','period' , 
                 'pay','holiday','leavecode','ot','ot_type','numlate','numoutbf', 
                 'numot' , 'remarks_other','workdate'  ]
        labels = {
            'emp_cde':'พนักงาน' ,
            'ta_date' : 'วันที่' ,
            'pay' : 'คิดเงินได้' ,
            'leavecode' : 'ลา' ,
            'holiday' : 'วันหยุด' ,
            'timein': 'เข้างาน' ,
            'timeout' : 'ออกงาน',
            'period' : 'งวด' ,
            'shift' : 'กะงาน' ,
            'remarks_other' : 'หมายเหตุ' ,
            'ot' : 'ล่วงเวลา' ,
            'ot_type' : 'ประเภท OT' ,
            'numot' :'ล่วงเวลา(นาที)' , 
            'numlate' : 'มาสาย(นาที)' ,
            'numoutbf' : 'ออกก่อน(นาที)'
            
        }
        
        widgets={
            'ta_date' :  forms.DateInput(format='%d/%m/%Y') ,
          
            'remarks_other' :forms.Textarea(attrs= {'rows':3,'cols':75})
            #Textarea(attrs= {'rows':3 , 'cols':70} ),
        }
# Form การลาประจำวัน
class EmpTranLeaveForm(forms.ModelForm):
    
    class Meta:
        model=EmpTranLeave
        fields= ['emp_cde','leavedate','leavecode','starttime','endtime','reason','pay' , 
                 'approved_by','authorized_by','leave_type']
      
        
        labels = {
            'emp_cde' :'พนักงาน' ,
            'leavedate' : 'วันที่ลา' ,
            'leavecode' : 'รหัสการลา',
            'leave_type' : 'ประเภทการลา',
            'starttime' : 'เริมเวลา',
            'endtime': 'สิ้นสุด',
            'reason': 'เหตุผล',
            'pay' : 'จ่ายเงินได้',
            'approved_by': 'อนุมัติการลาโดย',
            'authorized_by': 'Auhorized By'
            
        }
        widgets = {
            'reason' : forms.Textarea(attrs={'rows':3 ,'cols': 50})
        }
#Form สำหรับการแจ้งลาออก        
class EmpmasResignForm(forms.ModelForm):
    class Meta:
        model = EmpmasResign
        fields = ['emp_cde','require_date','effective_date','reason',
                'status', 
                'approved_by',
            
        ]
        labels = {
            'emp_cde' :'พนักงาน' ,
            'require_date' : 'วันที่แจ้งขอลาออก' ,
            'effective_date' : 'วันที่มีผล',
           
            'reason': 'เหตุผล',
        
            'approved_by': 'อนุมัติโดย',
        }   
        widgets = {
            'reason' : forms.Textarea(attrs={'rows':3 ,'cols': 50})
        }
        