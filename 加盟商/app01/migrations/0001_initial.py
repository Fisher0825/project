# Generated by Django 2.2.2 on 2021-01-06 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dim_franchisee_basic_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('created_at', models.DateTimeField(verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(verbose_name='数据删除时间')),
                ('desc', models.CharField(max_length=256)),
                ('remark', models.CharField(max_length=128)),
                ('status_id', models.SmallIntegerField()),
                ('guid', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=45)),
                ('name', models.CharField(max_length=45)),
                ('type', models.SmallIntegerField()),
                ('zip', models.CharField(max_length=6)),
                ('province_code', models.CharField(max_length=5)),
                ('province_name', models.CharField(max_length=45)),
                ('city_code', models.CharField(max_length=6)),
                ('city_name', models.CharField(max_length=45)),
                ('district_code', models.CharField(max_length=6)),
                ('district_name', models.CharField(max_length=45)),
                ('street_code', models.CharField(max_length=6)),
                ('street_name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=256)),
                ('longitude', models.CharField(max_length=45)),
                ('latitude', models.CharField(max_length=45)),
                ('is_audited', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Dim_franchisee_account_employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('created_at', models.DateTimeField(db_index=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(verbose_name='数据删除时间')),
                ('desc', models.CharField(max_length=256)),
                ('remark', models.CharField(max_length=128)),
                ('status_id', models.SmallIntegerField()),
                ('username', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=32)),
                ('mobile', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.SmallIntegerField(choices=[(1, '管理员'), (2, '普通用户')], default=1)),
                ('franchisee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Dim_franchisee_basic_info', verbose_name='加盟商id')),
            ],
        ),
    ]
