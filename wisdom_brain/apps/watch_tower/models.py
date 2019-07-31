from django.db import models

from common.utils.models import BaseModel


class Area(BaseModel):
    # 主键id，用国家统一规定的行政编码
    id = models.CharField(max_length=20, primary_key=True)
    # 地区名称
    name = models.CharField(max_length=20)
    # 一级辖区id，省、直辖市级
    first_id = models.CharField(max_length=20, null=True)
    # 二级辖区id，地级市级
    second_id = models.CharField(max_length=20, null=True)
    # 地区类型，省、市、县
    grade = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = 'area'


class Industry(BaseModel):
    # 行业名称
    name = models.CharField(max_length=50)
    # 一级行业id
    first_id = models.IntegerField(null=True)
    # 是否是工业类型：1-是，0-否
    grade = models.SmallIntegerField(null=True)

    class Meta:
        db_table = 'industry'


class Company(BaseModel):
    # 企业名称
    name = models.CharField(max_length=50)
    # 税收
    tax = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    # 营收
    revenue = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    # 员工数量
    staff_num = models.IntegerField(null=True)
    # 利润
    profit = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    # 数据统计时间
    statistic_time = models.DateField(null=True)
    # 公司成立时间
    established_time = models.DateField(null=True)
    # 父级公司id
    parent = models.IntegerField(null=True)

    class Meta:
        db_table = 'company'


class Relation(BaseModel):
    area = models.ForeignKey(to='Area', on_delete=models.SET_NULL,
                             null=True, related_name='area_relate')
    industry = models.ForeignKey(to='Industry', on_delete=models.SET_NULL,
                                 null=True, related_name='industry_relate')
    company = models.ForeignKey(to='Company', on_delete=models.SET_NULL,
                                null=True, related_name='company_relate')

    class Meta:
        db_table = 'relation'


class StatisticData(BaseModel):
    company_number = models.IntegerField(help_text='企业数量')
    company_increase = models.IntegerField(help_text='相较于去年，企业新增数量')
    date = models.CharField(max_length=10, help_text='统计年份')
    area = models.ForeignKey(to='Area', on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey(
        to='Industry', on_delete=models.SET_NULL, null=True)
    revenue = models.DecimalField(
        max_digits=20, decimal_places=4, help_text='营收')
    revenue_increase = models.DecimalField(max_digits=20, decimal_places=4,
                                           help_text='相较于去年，营收新增额')
    tax = models.DecimalField(max_digits=20, decimal_places=4, help_text='税收')
    tax_increase = models.DecimalField(max_digits=20, decimal_places=4,
                                       help_text='相较于去年，税收新增')

    class Meta:
        db_table = 'statistic_data'
