from django.db import models

# Create your models here.
#from django.db import models
#from erpdb.models import TblDepartment
#from django.db import connections

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class TblAllowApp(models.Model): 
    app = models.CharField(max_length=30 ,null=True,blank=True)
    class Meta:
        db_table = 'erpdb_tblallowapp'
    def __str__(self):
            return '{}'.format(self.app)

class TblUserAuth(models.Model):
    #user : is a user id related with django USER models (class= AuthUser(models.Model):)
    #content_type : related with django ContentType Model (class = DjangoContentType(models.Model):)
    
    choice = [
        (0,'NO'),
        (1,'YES')
       
    ]
    
    user = models.ForeignKey(User,null=True,on_delete= models.SET_NULL)
   # app = models.ForeignKey(TblAllowApp,null=True,on_delete=models.SET_NULL)
    
    content_type = models.ForeignKey(ContentType,null=True,on_delete=models.CASCADE)
    
    is_access = models.IntegerField(null=True,choices=choice,default=True)  #กำหนดว่าเข้าระบบได้หรือไม่
    
    is_admin = models.IntegerField(null=True, choices=choice,default=False) #กำหนดว่ามีสิทธิ์ ในการเป็น admin ของระบบ หรือไม่
    is_add = models.IntegerField(null=True,choices=choice,default=False)
    is_edit = models.IntegerField(null=True,choices=choice,default=False)
    is_delete = models.IntegerField(null=True,choices=choice,default=False)
    is_view = models.IntegerField(null=True,choices=choice,default=True)
    is_approve = models.IntegerField(null=True,choices=choice,default=False)
    is_authorize = models.IntegerField(null=True,choices=choice,default=False)
    
   # dep = models.ForeignKey('TblDepartment', on_delete= models.CASCADE) 
    class Meta:
        db_table = 'erpdb_tbluserauth'
        
    def __str__(self):
        return '{} {} '.format(self.user,self.content_type)
    
class TblDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    dep_code = models.CharField(unique=True,max_length=20, blank=True, null=True)
    dep_name = models.CharField(max_length=30, blank=True, null=True)
    num_item = models.IntegerField(blank=True,null=True)
    num_work = models.IntegerField(blank=True,null=True)
    num_leave = models.IntegerField(blank=True,null=True)
    num_late = models.IntegerField(blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_department'
    def __str__(self):
            return '{} {}'.format(self.dep_code,self.dep_name) 
    
    @property
    def num_absent(self):
        return int(self.num_item) - int(self.num_work) - int(self.num_leave)
    
    

 
class Company(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=200,blank=True,null=True)
    companynameeng = models.CharField(max_length=200,blank=True,null=True)
    companyadd = models.CharField(max_length=250,blank=True,null=True)
    companyemail = models.CharField(max_length=100,blank=True,null=True)
    companywww = models.CharField(max_length=100,blank=True,null=True)
    companytaxid = models.CharField(max_length=20,blank=True,null=True)
    companyvat = models.CharField(max_length=10,blank=True,null=True)
    companysoc = models.IntegerField(blank=True,null=True)
    minsoc = models.FloatField()
    maxsoc=models.FloatField()
    socialid = models.CharField(max_length=20,blank=True,null=True)
    no13 = models.CharField(max_length=20,blank=True,null=True)
    soc_loc = models.CharField(max_length=20,blank=True,null=True)
    soc_br = models.CharField(max_length=20,blank=True,null=True)
    postid = models.CharField(max_length=20,blank=True,null=True)
    emp_deduct = models.FloatField(blank=True,null=True)
    emp_deduct_max = models.FloatField(blank=True,null=True)
    com_soc_rate = models.FloatField(blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_hm_config'
    def __str__(self):
        return '{}{}'.format(self.companyid,self.companyname)
    
class Acyear(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=20,blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_accyear'
    def __str__(self):
        return '{}'.format(self.desc)
class Acmonth(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=20,blank=True,null=True)
    dateclosed = models.DateField(blank=True,null=True)
    acyear = models.ForeignKey(Acyear,to_field="cde",db_column="acyear",blank=True,null=True,on_delete=models.SET_NULL)
    
    class Meta:
        managed = False
        db_table = 'tbl_accper'
    def __str__(self):
        return '{} {} {}'.format(self.cde,self.desc,self.acyear)
    
#กำหนดการจ่ายเงินได้ของแต่ละประเภทพนักงาน เช่น S:รายเดือน 12 ครั้ง/ปี  W:รายวัน 2 งวด/เดือนหรือ 24ครั้ง/ปี        
class PaymentPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    payterm = models.CharField(max_length=20,blank=True,null=True)
    class Meta:
        managed=False
        db_table = 'tbl_paymentperiod'
    def __str__(self):
        return '{} {}'.format(self.cde,self.desc)
#ประเภทพนักงาน เช่น S:รายเดือน W:รายวัน 
class EmployeeType(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    workday = models.IntegerField(blank=True,null=True)
    workhour = models.IntegerField(blank=True,null=True)
    #paymentperiod = models.CharField(max_length=20,blank=True,null=True)
    paymentperiod = models.ForeignKey(PaymentPeriod,to_field='cde',db_column='paymentperiod', blank=True,null=True,on_delete=models.CASCADE)
    
    paymentterm = models.IntegerField(blank=True,null=True)
    pnd1 = models.BooleanField(blank=True,null=True)
    pnd3= models.BooleanField(blank=True,null=True)
    sso = models.BooleanField(blank=True,null=True)
    pnd3rate = models.FloatField(blank=True,null=True)
    num_item = models.IntegerField(blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_employeetype'
    def __str__(self):
        return '{}-{}'.format(self.cde,self.desc)

#กำหนดงวดการทำงานของพนักงานแต่ละประเภท เช่น S:รายเดือน W:รายวัน     
class EmpPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,db_column="CDE",max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    ptdate = models.DateField(blank=True,null=True)
    socdate = models.DateField(blank=True,null=True)
    status = models.CharField(max_length=1,blank=True,null=True,default='0')
    acyear = models.CharField(max_length=20,blank=True,null=True)
    work_start_date= models.DateField(blank=True,null=True)
    work_end_date = models.DateField(blank=True,null=True)
    acmonth = models.ForeignKey(Acmonth,to_field="cde",db_column="acmonth" ,blank=True,null=True,on_delete=models.SET_NULL)
    emptype = models.ForeignKey(EmployeeType,to_field="cde",db_column="Emptype",blank=True,null=True,on_delete=models.SET_NULL)
    period_no = models.CharField(max_length=20,blank=True,null=True)
    total_day_work = models.CharField(max_length=20,blank=True,null=True)
    #new fields 
    num = models.CharField(max_length=10 ,blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_emp_period'
    def __str__(self):
        return '{} {}'.format(self.cde,self.desc)

class EmpPosition(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        db_table = 'tbl_position'
    def __str__(self):
        return '{}-{}'.format(self.cde,self.desc)

class TaxRate(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    maxincome = models.FloatField()
    maxtax = models.FloatField()
    taxrate = models.FloatField()
    maxtaxcum=models.FloatField()
    minincome = models.FloatField()    
    class Meta:
        db_table = 'taxrate'
    def __str__(self):
        return '{}{}'.format(self.cde,self.desc)
# ตารางค่าลดหย่อนต่างๆ 
class TaxDeduction(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True)
    defaultvalue  = models.BooleanField()    
    amt = models.FloatField()
    max = models.FloatField()
    percent = models.FloatField()
    calamt=models.BooleanField()
    calpercent = models.BooleanField()
        
    class Meta:
        db_table = 'tax_deduction'
        managed=False
    def __str__(self):
        return '{} {}'.format(self.cde,self.desc)

class EmpCtlDb(models.Model):
    id = models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=20)
    desc = models.CharField(max_length=100,blank=True,null=True)
    calauto = models.BooleanField(db_column="CAL_AUTO",blank=True,null=True)
    calday = models.BooleanField(db_column="CalDay",blank=True,null=True)
    calhour = models.BooleanField(db_column="CallHours",blank=True,null=True)
    calmonth = models.BooleanField(db_column="CalMonth",blank=True,null=True)
    type=models.CharField(max_length=30,db_column="TYPE",blank=True,null=True)
    typeset= models.IntegerField(db_column="TYPESET",blank=True,null=True)
    multiby = models.IntegerField(db_column="MULTIBY",blank=True,null=True)
    calsoc = models.BooleanField(db_column="CALSOC",blank=True,null=True)
    caltax= models.BooleanField(db_column="CALTAX",blank=True,null=True)
    defaultvalue= models.BooleanField(blank=True,null=True)
    onetime = models.BooleanField(db_column="1Time",blank=True,null=True)
    dailyrecord = models.BooleanField(db_column="RecordDaily",blank=True,null=True)
    fldupd = models.CharField(max_length=50,blank=True,null=True)
    class Meta:
        db_table = 'emp_ctl_db'
        managed = False
    def __str__(self):
        return '{} {}'.format(self.cde,self.desc)
    
# class for ค่าลดหย่อนต่างๆ ของแต่ละคน
class EmpDeduction(models.Model):
    id = models.AutoField(primary_key=True)
    emp_cde = models.CharField(max_length=20,db_column="EMP_CDE",blank=True,null=True)
    deduct_cde = models.ForeignKey(TaxDeduction,to_field="cde" ,max_length=20,db_column="DEDUCT_CDE",blank=True,null=True,on_delete=models.SET_NULL)
    desc = models.CharField(max_length=100,blank=True,null=True)
    amt = models.FloatField(db_column="AMT",blank=True,null=True)
    num= models.FloatField(db_column="NUM",blank=True,null=True,default=1)
    max= models.FloatField(db_column="MAX",blank=True,null=True)
    percent = models.FloatField(db_column="PERCENT",blank=True,null=True)
    class Meta:
        db_table = 'emp_less_deduction'
        managed = False
    def __str__(self):
        return '{} {}'.format(self.emp_cde,self.deduct_cde)

# ตารางรายได้ รายการหักต่างๆ ของแต่ละคน
class EmpIncExpDb(models.Model):
    id = models.AutoField(primary_key=True)
    emp_cde = models.CharField(max_length=20,blank=True,null=True)
    
    code = models.ForeignKey(EmpCtlDb,to_field="cde",db_column="Code", max_length=20,blank=True,null=True,on_delete=models.SET_NULL)
   # code = models.CharField(max_length=30,blank=True,null=True)
    
    detail = models.CharField(max_length =100,blank=True,null=True)
    emp_amt = models.FloatField(db_column="EMP_AMT",blank=True,null=True)
    amtmth = models.FloatField(db_column="AMTMTH",blank=True,null=True)
    c_numhour = models.FloatField(db_column="C_numHours",blank=True,null=True)
    c_numday = models.FloatField(db_column="C_numDay",blank=True,null=True)
    emp_cum_amt = models.FloatField(db_column="emp_cum_amt",blank=True,null=True)
    class Meta:
        db_table = 'emp_inc_exp_db'
        managed = False
    def __str__(self):
        return '{}{}'.format(self.emp_cde,self.code)    

class WorkStatus(models.Model):
    cde = models.CharField(unique=True,max_length=20,blank=True)
    desc = models.CharField(max_length=50,blank=True,null=True)
    class Meta:
      #  using = ' hmdb' 
        db_table = 'tbl_work_status'
        managed = False
    def __str__(self):
        return '{}'.format(self.desc) 
    
class TblShift(models.Model) :
    id= models.AutoField(primary_key=True)
    shift = models.CharField(max_length=20,db_column="shiftcode",unique=True,blank=True,null=True)
    shiftname = models.CharField(max_length=50,blank=True,null=True)
    starttime = models.CharField(max_length=20,blank=True,null=True)
    endtime = models.CharField(max_length=20,blank=True,null=True)
    ot_st = models.CharField(max_length=20,blank=True,null=True)
    ot_end = models.CharField(max_length=20,blank=True,null=True)
    in_shift_st= models.CharField(max_length=20,blank=True,null=True)
    in_shift_end= models.CharField(max_length=20,blank=True,null=True)
    out_shift_st = models.CharField(max_length=20,blank=True,null=True)
    out_shift_end =models.CharField(max_length=20,blank=True,null=True)
    break_st = models.CharField(max_length=20,blank=True,null=True)
    break_end = models.CharField(max_length=20,blank=True,null=True)
    shift_cross_day = models.CharField(max_length=10,db_column="crossday",blank=True,null=True)
    
    class Meta:
        db_table = "tbl_shift"
    def __str__(self):
        return '{}-{}'.format(self.shift,self.shiftname)
class TblLeave(models.Model):
    id = models.AutoField(primary_key=True)
    leavecode = models.CharField(unique=True,max_length=20,blank=True,null=True)
    leavename = models.CharField(max_length=150,blank=True,null=True)
    pay = models.CharField(max_length=10,blank=True,null=True)
    class Meta:
        db_table="tbl_leave"
    def __str__(self):
        return '{} {}'.format(self.leavecode , self.leavename)

# table Ot-type contains Overtime Ratio     
class TblOT(models.Model):
    id = models.AutoField(primary_key=True) 
    cde = models.CharField(unique=True, max_length=10,blank=True,null=True)
    desc = models.CharField(max_length=100,blank=True,null=True,db_column='Desc')
    num = models.CharField(max_length=10,blank=True,null=True)
    #ref_code = models.CharField(max_length=10,blank=True,null=True)  # return this value for Empctldb
    refcode = models.ForeignKey(EmpCtlDb,to_field='cde',db_column='ref_code' ,blank=True,null=True,on_delete=models.SET_NULL)
    defaultvalue= models.CharField(max_length=1,blank=True,null=True)
    class Meta:
        db_table = 'tbl_ot_type'
    def __str__(self) :
        return '{} {}'.format(self.cde,self.desc)
    
class Empmas(models.Model):
    pf_choice = [
        ('นาย','นาย'),
        ('นาง' ,'นาง'),
        ('นส.' ,'นส.'),
    ]
    sex_choice=[
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('Q', 'LGBTQ'),
        ('O' , 'NOT SPECIFIED'),
    ]
    workstatus_choice = [
        ('0','ปกติ/ทำงานอยู่'),
        ('8', 'พักงาน') ,
        ('9', 'ลาออก')
    ]
    
    id = models.AutoField(primary_key=True)
    emp_cde = models.CharField(unique=True,max_length=50,db_column='emp_Cde')
    emp_pf = models.CharField(max_length=50,db_column='Emp_pf',blank=True,null=True,choices=pf_choice)
    emp_name= models.CharField(max_length=200,db_column='emp_Name')
    emp_surname= models.CharField(max_length=200,db_column='emp_surname')
    emp_name_eng= models.CharField(max_length=200,db_column ="em_name_eng" ,blank=True,null=True)
    emp_birthdate = models.DateTimeField(blank=True,null=True)
    emp_add1 = models.CharField(max_length=150,db_column='Emp_Add1',blank=True,null=True)
    emp_add2 = models.CharField(max_length=150,db_column='Emp_add2',blank=True,null=True)
    emp_tel = models.CharField(max_length=50,db_column='Emp_Tel',blank=True,null=True)
    emp_fax = models.CharField(max_length=50,db_column='Emp_Fax',blank=True,null=True)
    emp_mobile = models.CharField(max_length=50,db_column='Emp_Mobile',blank=True,null=True)
    emp_email = models.CharField(max_length=30,db_column='Emp_Email',blank=True,null=True)
    emp_taxid = models.CharField(max_length=30,db_column='Emp_TaxId',blank=True,null=True)
    emp_socialid = models.CharField(max_length=30,db_column='Emp_SocialId',blank=True,null=True)
    emp_cardid = models.CharField(max_length=30,db_column='Emp_CardId')
    emp_position = models.ForeignKey(EmpPosition,to_field="cde",db_column='Emp_position',blank=True,null=True,on_delete=models.CASCADE)
    shift = models.ForeignKey(TblShift,to_field="shift",db_column="shiftcode",blank=True,null=True,on_delete=models.CASCADE)
    emp_income = models.FloatField(blank=True , null=True )
    emp_income_d = models.FloatField(blank=True , null=True)
    emp_income_h = models.FloatField(blank=True , null=True)
    emp_cum_income = models.FloatField(blank=True,null=True)
  #  emp_soc = models.FloatField(blank=True,null=True)
    emp_cum_soc = models.FloatField(blank=True,null=True)
   # emp_tax = models.FloatField(blank=True,null=True)
    emp_cum_tax = models.FloatField(blank=True,null=True)
    emp_type = models.ForeignKey(EmployeeType,to_field="cde",db_column="emp_type",max_length=20 ,blank=True,null=True,on_delete=models.CASCADE)
    emp_bank_account = models.CharField(max_length=20 ,db_column="Emp_BankAccount",blank=True,null=True)
    emp_dep = models.ForeignKey(TblDepartment,to_field="dep_code",db_column="Emp_dep",on_delete=models.CASCADE)
    
    workstatus = models.CharField(max_length=10, choices=workstatus_choice )
    
    em_bf_inc = models.FloatField(blank=True , null=True)
    em_bf_soc = models.FloatField(blank=True,null=True)
    em_bf_tax = models.FloatField(blank=True,null=True)
    emp_startworkdate = models.DateTimeField(db_column="emp_StartworkDate" ,blank=True,null=True)
    emp_prodate = models.DateTimeField(db_column="emp_ProDate",blank=True,null=True)
    emp_hiredate = models.DateTimeField(db_column="emp_hireDate",blank=True,null=True)    
    emp_sex = models.CharField(max_length=10,blank=True,null=True ,choices = sex_choice)
    emp_imageurl = models.ImageField(upload_to= "images/profile/" ,blank=True,null=True,
                                     default='images/profile/emp.png')
    
    class Meta:     
        managed= False 
        db_table = 'empmas'
    def __str__(self):
        return '{}-{} {}'.format(self.emp_cde,self.emp_name,self.emp_surname) 

#class for store employee income   ** ไ่ม่ได้ใช้แล้ว
class EmpmasIncome(models.Model):
    id=models.AutoField(primary_key=True)
    empmas = models.ForeignKey(Empmas,to_field='id',db_column='empmas_id',blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.CharField(max_length=50,blank=True,null=True)
    emp_income = models.FloatField(blank=True , null=True)
    emp_cum_income = models.FloatField(blank=True,null=True)
    emp_soc = models.FloatField(blank=True,null=True)
    emp_cum_soc = models.FloatField(blank=True,null=True)
    emp_tax = models.FloatField(blank=True,null=True)
    emp_cum_tax = models.FloatField(blank=True,null=True)        
    em_bf_inc = models.FloatField(blank=True , null=    True)
    em_bf_soc = models.FloatField(blank=True,null=True)
    em_bf_tax = models.FloatField(blank=True,null=True)
    class Meta:
        db_table='empmas_income'
        managed=False
        
    def __str__(self):
        return '{}'.format(self.empmas)

# ตารางสำหรับเก็บข้อมูลบันทึกการลาประจำวัน
class EmpTranLeave(models.Model):
    LeaveType = [
        ('D','ลาเป็นวัน'),
        ('H' ,'ลาเป็นชม.'),
        
    ]
    
    pay = [
        ('Y' , 'YES') ,
        ('N' , 'NO')
    ]
    
    id = models.AutoField(primary_key=True)
    emp_cde= models.ForeignKey(Empmas, to_field="emp_cde",db_column="emp_cde",blank=True,null=True, on_delete=models.CASCADE)
    #emp_cde = models.CharField(max_length=50,blank=True,null=True)
    #empmas = models.ForeignKey(Empmas,unique=True,to_field='id',db_column='empmas_id',blank=True,null=True,on_delete=models.CASCADE)
    leavedate = models.CharField(max_length = 50,blank=True,null=True)
    #leavecode = models.CharField(max_length = 10,blank=True,null=True)
    leavecode = models.ForeignKey(TblLeave ,to_field="leavecode",db_column="leavecode" ,blank=True,null=True ,on_delete=models.SET_NULL )
    starttime = models.CharField(max_length = 20,blank=True,null=True)
    endtime = models.CharField(max_length=20,blank=True,null=True)
    reason = models.CharField(max_length = 200,blank=True,null=True)
    pay = models.CharField(max_length = 1,blank=True,null=True,choices=pay)
    
    leave_type = models.CharField(max_length=30,blank=True,null=True,choices=LeaveType)
    
    approved_by=models.CharField(max_length = 100,blank=True,null=True)
    
    authorized_by = models.CharField(max_length = 100,blank=True,null=True)
    
    class Meta:
        managed = False
        db_table= "emp_tranleave"
    def __str__(self):
        return '{}'.format (self.id)
       
# ตารางสำหรับเก็บข้อมูลการลาออก
class EmpmasResign(models.Model):
    id = models.AutoField(primary_key=True)
    #empmas = models.ForeignKey(Empmas,to_field='id',db_column='empmas_id',blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.ForeignKey(Empmas, to_field="emp_cde",db_column="emp_cde",blank=True,null=True, on_delete=models.CASCADE)
    require_date = models.DateField(db_column = 'resign_require_date' , blank=True,null=True)
    effective_date = models.DateField(db_column = 'resign_effective_date' , blank=True,null=True)
    reason = models.CharField(max_length = 200,db_column = 'resign_reason', blank=True,null=True)
    status = models.CharField(max_length=5,blank=True,null=True)
    approved_by = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        managed = False
        db_table= "empmas_resign"
    def __str__(self):
        return '{}'.format (self.id)
               
#ตารางสำหรับการกำหนดการทำงานเฉพาะ เวลา เช่น การทำ OT    
class EmpWorkTable(models.Model):
    id = models.AutoField(primary_key=True)
    emptype = models.CharField(max_length=20,blank=True,null=True)
    period = models.ForeignKey(EmpPeriod,to_field='cde',blank=True,null=True,db_column="emp_period_cde",on_delete=models.CASCADE)
    #cde = models.CharField(max_length=20,blank=True,null=True,db_column="inc_exp_cde")
    cde = models.ForeignKey(EmpCtlDb,to_field='cde',db_column="inc_exp_cde",blank=True,null=True,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100,blank=True,null=True)
    holiday = models.BooleanField(blank=True,null=True,default=False)
    makepayment = models.BooleanField(blank=True,null=True,default=True)
    workdate= models.CharField(max_length = 30,blank=True,null=True)
    starttime = models.CharField(max_length = 20,blank=True,null=True)
    endtime = models.CharField(max_length = 20,blank=True,null=True)
    shift = models.ForeignKey(TblShift,to_field="shift",db_column="shiftcode",blank=True,null=True,on_delete=models.CASCADE)   
    
    class Meta:
        managed = False
        db_table = 'emp_work_table'
    def __str__(self):
        return '{} {}'.format(self.period,self.cde)
#ตารางเวลาเข้า-ออกงาน 
class TimeMast(models.Model):
    
    id = models.AutoField(primary_key=True)
    emptype = models.CharField(max_length=20,db_column="emp_type",blank=True,null=True)
    emp_cde = models.ForeignKey(Empmas, to_field="emp_cde",db_column="emp_cde",blank=True,null=True, on_delete=models.CASCADE)
    datetimescan = models.CharField(max_length=50 , blank=True,null=True )
    workdate = models.CharField(max_length=20,blank=True,null=True)
    worktime = models.CharField(max_length=20,blank=True,null=True)
    ampm = models.CharField(max_length=10,blank=True,null=True)
    machineno = models.CharField(max_length=10 ,blank=True,null=True)
    shift = models.ForeignKey(TblShift,to_field='shift',blank=True,null=True,db_column="shiftcode",on_delete=models.SET_NULL) 
    #models.CharField(max_length=10 ,db_column = "shiftcode" ,blank=True,null=True)
    period = models.CharField(max_length=10 ,blank=True,null=True)    
    remark = models.CharField(max_length=100 ,blank=True , null=True )
    inout = models.CharField(max_length=100 ,blank=True , null=True )
    
    class Meta:
        managed = False
        db_table = 'ta_mast'
    def __str__(self):
        return '{}'.format(self.id)

class EmpTime(models.Model):
    SelectChoices = [
        ('Y' , 'YES') ,
        ('N' , 'NO')
    ]
    
    id = models.AutoField(primary_key=True)
   # emptype = models.CharField(max_length=20,blank=True,null=True)
    period = models.ForeignKey(EmpPeriod,to_field='cde',blank=True,null=True,db_column="period",on_delete=models.SET_NULL)
    #period = models.CharField(max_length=20,blank=True,null=True)
    emp_cde = models.ForeignKey(Empmas, to_field="emp_cde",db_column="emp_cde",blank=True,null=True, on_delete=models.CASCADE)
   # emp_cde = models.CharField(max_length=20 ,blank=True,null=True )
    
    ta_date = models.DateTimeField(blank=True,null=True )
    timein = models.CharField(max_length=20,blank=True,null=True)
    timeout = models.CharField(max_length=20,blank=True,null=True)
    workdate = models.CharField(max_length=20,blank=True,null=True)
    #shift = models.CharField(max_length=20,db_column='shiftcode',blank=True,null=True)
    shift = models.ForeignKey(TblShift,to_field='shift',blank=True,null=True,db_column="shiftcode",on_delete=models.SET_NULL)
    pay = models.CharField(max_length=1,blank=True,null=True,choices=SelectChoices)
    holiday = models.CharField(max_length=1,blank=True,null=True,choices=SelectChoices)
    leavecode = models.CharField(max_length=10,blank=True,null=True)
    numlate = models.IntegerField(db_column="num_late",blank=True,null=True)
    numot = models.IntegerField(blank=True,null=True,db_column="ot_time")
    numoutbf = models.IntegerField(blank=True,null=True,db_column="num_betimeout")
    remarks= models.CharField(max_length = 100,blank=True,null=True)
    remarks_other = models.CharField(max_length = 200,blank=True,null=True)
    ka = models.CharField(max_length = 30,blank=True,null=True)
    ot = models.CharField(max_length = 20,blank=True,null=True,choices=SelectChoices)
   # ot_type = models.CharField(max_length = 20,blank=True,null=True)
    ot_type = models.ForeignKey(TblOT,to_field='cde',blank=True,null=True,db_column="ot_type",on_delete=models.SET_NULL)
    late = models.CharField(max_length=10,blank=True,null=True)
    leave=models.CharField(max_length=10,blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'emptime_mast'
    def __str__(self):
        return '{}'.format(self.id)
    
    
    
    #def duration(self):
   #     if self.workstarttime is not None and self.workendtime is not None:
   #         return self.workendtime - self.workstarttime 
                
 
class timeshift(models.Model):
    id = models.AutoField(primary_key=True)
    emp_cde = models.ForeignKey(Empmas, to_field="emp_cde",db_column="emp_cde",blank=True,null=True, on_delete=models.CASCADE)
    period = models.ForeignKey(EmpPeriod,to_field='cde',blank=True,null=True,db_column="period",on_delete=models.SET_NULL)
    emp_type = models.CharField(max_length=20,blank=True,null=True)
    workdate = models.CharField(max_length=20,blank=True,null=True)
    #workdate = models.DateField(blank= True ,null=True)
    shift = models.ForeignKey(TblShift,to_field="shift",db_column="shiftcode",blank=True,null=True,on_delete=models.CASCADE)   
    
    class Meta:
        managed=False
        db_table ="emp_timeshift"
    
    def __str__(self):
        return '{}-{}'.format(self.emp_cde,self.workdate)
    
class empstatistic(models.Model): # สถิติการมาทำงานประจำวัน
    id = models.AutoField(primary_key=True)
    emp_type = models.ForeignKey(EmployeeType,to_field="cde",db_column="emp_type",max_length=20 ,blank=True,null=True,on_delete=models.CASCADE) 
    workdate = models.CharField(max_length=20,blank=True,null=True)
    n_work = models.IntegerField()
    n_leave = models.IntegerField()
    n_absent = models.IntegerField()
    n_late = models.IntegerField()
    
    dayofweek = models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.id)

class empstatisticbydep(models.Model): # สถิติการมาทำงานประจำวันของแต่ละแผนก
    # index on emp_type , dep, workdate 
    id = models.AutoField(primary_key=True)
    dep = models.ForeignKey(TblDepartment,to_field="id" ,db_column="dep_id", on_delete=models.CASCADE)
    emp_type = models.ForeignKey(EmployeeType,to_field="cde",db_column="emp_type",max_length=20 ,blank=True,null=True,on_delete=models.CASCADE) 
    workdate = models.CharField(max_length=20,blank=True,null=True)
    n_work = models.IntegerField()
    n_leave = models.IntegerField()
    n_absent = models.IntegerField()
    n_late = models.IntegerField()
    
    dayofweek = models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def n_all(self):
        return int(self.n_work) + int(self.n_leave) + int(self.n_absent)
   
# ตารางสำหรับการบันทึกประจำวัน
class dailyTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    emp_cde = models.ForeignKey(Empmas, to_field="emp_cde",db_column="EMP_CDE",blank=True,null=True, on_delete=models.SET_NULL)
    code = models.ForeignKey(EmpCtlDb, to_field="cde",db_column="INC_EXP_CDE",blank=True,null=True, on_delete=models.SET_NULL)
    item = models.CharField(max_length=3,blank=True,null=True)
    #amt = models.FloatField(blank=True,null=True)
    num = models.FloatField(blank=True,null=True,default=1)
   # period = models.ForeignKey(EmpPeriod,to_field="cde",db_column="period",blank=True,null=True,on_delete=models.SET_NULL) 
    period= models.CharField(max_length=20,blank=True,null=True)
    pdate = models.DateField(blank=True,null=True)
    numhour=models.FloatField(blank=True,null=True) #keep in Minute
    numday=models.FloatField(blank=True,null=True)
    payamt = models.FloatField(blank=True,null=True)
    docno = models.CharField(max_length=30,blank=True,null=True)
    docdate = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=20,blank=True,null=True,default='0')
    workdate = models.CharField(max_length=30,db_column="workdate",blank=True,null=True)
    work_starttime = models.CharField(max_length=30,db_column="starttime",blank=True,null=True)
    work_endtime =  models.CharField(max_length=30,db_column="endtime",blank=True,null=True)
    
    workstarttime = models.CharField(max_length=30,db_column="workstarttime",blank=True,null=True)
    workendtime = models.CharField(max_length=30,db_column="workendtime",blank=True,null=True)
    
    class Meta:
        managed=False
        db_table = 'dtransaction'
   # @property
   # def duration(self):
   #     if self.workstarttime is not None and self.workendtime is not None:
   #         return self.workendtime - self.workstarttime 
        
    def __str__(self):
        return '{} {}{}{}'.format(self.id,self.emp_cde,self.code,self.period)

        
# class Emp sumamary transaction use for employee tax-calculation 
class EmpTransaction (models.Model):
    id= models.AutoField(primary_key=True,db_column="ID")
    emp_cde = models.CharField(max_length=30,db_column="EMP_CDE",blank=True,null=True)
    period = models.ForeignKey(EmpPeriod,to_field="cde",db_column="period",blank=True,null=True,on_delete=models.SET_NULL)
    code = models.ForeignKey(EmpCtlDb,to_field='cde' ,db_column="INC_EXP_CDE" ,blank=True,null=True,on_delete=models.SET_NULL)
    num = models.FloatField(db_column="NUM" ,blank=True,null=True)
    numhour = models.FloatField(db_column="numHour",blank=True,null=True)
    numday=models.IntegerField(db_column="NumDay",blank=True,null=True)
    payamt = models.FloatField(db_column="PayAMT",blank=True,null=True)
    
    class Meta:
        managed = False
        db_table = 'emp_transaction'
        
    def __str__(self):
        return '{} {}{}{}'.format(self.id,self.emp_cde,self.code,self.period)
     
class EmpExper(models.Model):
    id = models.AutoField(primary_key=True)
    empmas = models.ForeignKey(Empmas,to_field='id',blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.CharField(max_length=50,blank=True,null=True)
    p_seq = models.CharField(max_length=10) #require
    p_company = models.CharField(max_length=50) #require
    p_startdte = models.DateTimeField(blank=True,null=True)
    p_enddte = models.DateTimeField(blank=True,null=True)
    p_position = models.CharField(max_length=50,blank=True,null=True)
    p_address = models.CharField(max_length=200,blank=True,null=True)
    p_salary = models.FloatField(blank=True,null=True)
    p_duty = models.CharField(max_length=200,blank=True,null=True)
    p_reason = models.CharField(max_length=100,blank=True,null=True)    
    class Meta:
        managed=False
        db_table = 'hm_exper'
    def __str__(self):
        return '{}'.format(self.id)

# models for P-level (วุุฒิการศึกษา)
class grade(models.Model): 
    id=models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=10)
    desc = models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        managed=False
        db_table='tbl_grade'
    def __str__(self):
        return '{}'.format(self.desc)

# models for P-MAJOR (คณะ /สาขาวิชา)
class gradeMajor(models.Model):
    id=models.AutoField(primary_key=True)
    cde = models.CharField(unique=True,max_length=10)
    desc = models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        managed=False
        db_table='tbl_grade_br'
    def __str__(self):
        return '{}'.format(self.desc)

class EmpEducation(models.Model):
    id = models.AutoField(primary_key=True)
    empmas = models.ForeignKey(Empmas,blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.CharField(max_length=50,blank=True,null=True)
    p_seq = models.CharField(max_length=10) #require
    p_institue = models.CharField(max_length=200) #require
    p_level =  models.ForeignKey(grade,to_field="id",db_column="p_level",on_delete=models.CASCADE) 
    p_major = models.ForeignKey(gradeMajor,to_field="cde",db_column="p_major",blank=True,null=True,on_delete=models.CASCADE)
    p_year = models.CharField(max_length=50,blank=True,null=True)
    p_gpa = models.FloatField(blank=True,null=True)
    #p_provid = models.CharField(max_length=100,blank=True,null=True)    
    class Meta:
        managed=False
        db_table = 'hm_educa'
    def __str__(self):
        return '{}'.format(self.id)
    
class EmpHealth(models.Model):
    selectchioce= [
        ('No' , 'No Defected'),
        ('Yes' , 'Defected'),
    ]
    bloodgroup= [
        ('O', 'หมู่เลือด O'),
        ('A' ,'หมู่เลือด A'),
        ('B' ,'หมู่เลือด B'),
        ('AB' ,'หมู่เลือด AB'),
        ('AB+' ,'หมู่เลือด AB+'),
    ]
    
    id = models.AutoField(primary_key=True)
    empmas = models.ForeignKey(Empmas,blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.CharField(max_length=50,blank=True,null=True)
    p_hieght = models.CharField(max_length=100,blank=True,null=True)
    p_weight = models.CharField(max_length=100,blank=True,null=True)
    p_blood = models.CharField(max_length=100,blank=True,null=True,choices=bloodgroup) # Blood Group
    p_x_ray = models.CharField(max_length=100,blank=True,null=True)
    p_hiv = models.CharField(max_length=10,blank=True,null=True,choices=selectchioce,default="No") #ผลตรวจหาเชื้อ HIV
    p_vdrl = models.CharField(max_length=10,blank=True,null=True,choices=selectchioce,default="No") #ผลตรวจหาเชื้อซิฟิลิส
    p_addict = models.CharField(max_length=10,blank=True,null=True,choices=selectchioce,default="No")  #ผลตรวจหาสารเสพติดในร่างกาย
    p_disease = models.CharField(max_length=100,blank=True,null=True) #โรคประจำตัว
    p_drug= models.CharField(max_length=100,blank=True,null=True)
    p_hemo = models.CharField(max_length=100,blank=True,null=True)
    p_cbc = models.CharField(max_length=100,blank=True,null=True)  #ความสมบูรณ์ของเม็ดเลือด
    p_wbc= models.CharField(max_length=100,blank=True,null=True) # จำนวนเม็ดเลือดขาว
    p_ph = models.CharField(max_length=100,blank=True,null=True)  #ความเป็นกรด-ด่าง
    p_bun = models.CharField(max_length=100,blank=True,null=True)  #ตั้งครรภ์
    p_phy_ex = models.CharField(max_length=100,blank=True,null=True) # phy exception การรับประทานยา
    
    class Meta:
        managed=False
        db_table = 'hm_health'
    def __str__(self):
        return '{}'.format(self.id)
    
class EmpReference(models.Model):
    id = models.AutoField(primary_key=True)
    empmas = models.ForeignKey(Empmas,blank=True,null=True,on_delete=models.CASCADE)
    emp_cde = models.CharField(max_length=50,blank=True,null=True)
    p_seq = models.CharField(max_length=10) #require   
    p_name = models.CharField(max_length=100,db_column="P_NAME")#require
    
    p_career = models.CharField(max_length=50,blank=True,null=True)
    p_address = models.CharField(max_length=200,blank=True,null=True)
    p_tel = models.CharField(max_length=20,blank=True,null=True)
   
    class Meta:
        managed=False
        db_table = 'hm_refer'
    def __str__(self):
        return '{}'.format(self.id)
    
#