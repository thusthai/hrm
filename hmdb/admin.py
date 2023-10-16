# Register your models here.
from django.contrib import admin

# Register your models here.
from hmdb.models import grade,gradeMajor,EmpEducation,EmpHealth,EmpReference,EmpCtlDb,TaxRate,EmpPosition,TaxDeduction 

from hmdb.models import PaymentPeriod,EmployeeType,Company,Acyear,EmpPeriod,Acmonth,EmpWorkTable

class gradeAdmin(admin.ModelAdmin):
    list_display = ['id','desc']
class gradeMajorAdmin(admin.ModelAdmin):
    list_display = ['id','cde','desc']
class EmpEducationAdmin(admin.ModelAdmin):
    list_display = ['id','empmas','p_level','p_institue','p_major']

class EmpCtlDbAdmin(admin.ModelAdmin):
    list_display = ['id','cde','desc','defaultvalue']
    
class TaxRateAdmin(admin.ModelAdmin):
    list_display= ['id','cde','desc','taxrate','maxtax']

class TaxDeductionAdmin(admin.ModelAdmin):
    list_display= ['id','cde','desc','defaultvalue']
class EmpPositionAdmin(admin.ModelAdmin):
       list_display= ['id','cde','desc']
class PaymentTypeAdmin(admin.ModelAdmin):
       list_display= ['id','cde','desc']      
class EmpPloyeeTypeAdmin(admin.ModelAdmin):
       list_display= ['id','cde','desc','pnd1']
class CompanyAdmin(admin.ModelAdmin):
    list_display= ['companyid','companyname']
    labels = {
        'companyname': 'ชื่อบริษัทฯ',
    }
class EmpPeriodAdmin(admin.ModelAdmin):
    list_display = ['id','emptype','cde','status','work_start_date','work_end_date']
    
class EmpworktableAdmin(admin.ModelAdmin):
    list_display= ['id','period','cde','makepayment','workdate','starttime','endtime']
           

class AcyearAdmin(admin.ModelAdmin):
    list_display=['id','cde','desc','status']
class AcmonthAdmin (admin.ModelAdmin):
    list_display=['id','cde','desc','acyear','status']
    
admin.site.register(grade,gradeAdmin)
admin.site.register(gradeMajor,gradeMajorAdmin)
#admin.site.register(EmpEducation,EmpEducationAdmin)
# models for Setting 
admin.site.register(EmpCtlDb,EmpCtlDbAdmin)
admin.site.register(TaxRate,TaxRateAdmin)
admin.site.register(TaxDeduction,TaxDeductionAdmin)
admin.site.register(EmpPosition,EmpPositionAdmin)
admin.site.register(PaymentPeriod,PaymentTypeAdmin)
admin.site.register(EmployeeType,EmpPloyeeTypeAdmin)
admin.site.register(Company,CompanyAdmin)
#admin.site.register(Company,CompanyAdmin)
admin.site.register(Acyear,AcyearAdmin)
admin.site.register(Acmonth,AcmonthAdmin)

admin.site.register(EmpPeriod,EmpPeriodAdmin)
admin.site.register(EmpWorkTable,EmpworktableAdmin)

