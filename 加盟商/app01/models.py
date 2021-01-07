from django.db import models

# Create your models here.
class Dim_franchisee_account_employee(models.Model):
    #加盟商员工账号管理
    id = models.AutoField(primary_key=True,verbose_name="主键")
    franchisee_id = models.OneToOneField(to="Dim_franchisee_basic_info",
                                         verbose_name="加盟商id",on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="数据创建时间",db_index=True)
    updated_at = models.DateTimeField(verbose_name="数据更新时间",auto_now=True)
    deleted_at = models.DateTimeField(verbose_name="数据删除时间")
    desc = models.CharField(max_length=256)
    remark = models.CharField(max_length=128)
    status_id = models.SmallIntegerField()
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=13)
    email = models.EmailField()
    role_choice = ((1,"管理员"),(2,"普通用户")) #用户身份标志
    role = models.SmallIntegerField(choices=role_choice,default=1)

class Dim_franchisee_basic_info(models.Model):
    #加盟商基础信息
    id = models.AutoField(primary_key=True, verbose_name="主键")
    created_at = models.DateTimeField(verbose_name="数据创建时间")
    updated_at = models.DateTimeField(verbose_name="数据更新时间")
    deleted_at = models.DateTimeField(verbose_name="数据删除时间")
    desc = models.CharField(max_length=256)
    remark = models.CharField(max_length=128)
    status_id = models.SmallIntegerField()
    guid = models.CharField(max_length=64)
    title = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    type = models.SmallIntegerField()
    zip = models.CharField(max_length=6)
    province_code = models.CharField(max_length=5)
    province_name = models.CharField(max_length=45)
    city_code = models.CharField(max_length=6)
    city_name = models.CharField(max_length=45)
    district_code = models.CharField(max_length=6)
    district_name = models.CharField(max_length=45)
    street_code = models.CharField(max_length=6)
    street_name = models.CharField(max_length=45)
    address = models.CharField(max_length=256)
    longitude = models.CharField(max_length=45)
    latitude = models.CharField(max_length=45)
    is_audited = models.DateTimeField()

