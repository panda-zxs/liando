from rest_framework import serializers

from django.conf import settings
from django.db.models import CharField, Sum, Count, Case, When, Value, Q, F

from .models import Area, Company, Industry, Relation
from .utils import get_area_industry


class StatisticsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField(help_text='数量统计')
    number = serializers.SerializerMethodField(help_text='地图旁的分布统计')
    top5 = serializers.SerializerMethodField(help_text='几个top5的统计')
    revenue_data = serializers.SerializerMethodField(help_text='营收数据统计')
    tax_revenue_data = serializers.SerializerMethodField(help_text='税收数据统计')

    class Meta:
        model = Area
        fields = ('data', 'number', 'top5',
                  'tax_revenue_data', 'revenue_data',)

    @classmethod
    def get_data(cls, data):
        return DataSerializer(data).data

    @classmethod
    def get_number(cls, data):
        return NumberSerializer(data).data

    @classmethod
    def get_top5(cls, data):
        return Top5Serializer(data).data

    @classmethod
    def get_revenue_data(cls, data):
        return RevenueDataSerializer(data).data

    @classmethod
    def get_tax_revenue_data(cls, data):
        return TaxRevenueDataSerializer(data).data

class DataSerializer(serializers.ModelSerializer):
    all_enterprise = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()
    tax_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('all_enterprise', 'industry', 'revenue',
                  'tax_revenue', 'profit')

    @classmethod
    def get_all_enterprise(cls, data):
        '''
        全行业企业数量
        :param area:
        :param industry:
        :return:
        '''
        area_id, industry_id = get_area_industry(data)
        # 企业数量
        companys_number = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR)
        # 新增企业数量=当前年份（显示的年份）新创建的企业的数量
        companys_increase = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id,
            company__established_time__year=settings.YEAR)
        ret = dict()
        ret['number'] = len(companys_number)
        ret['increase'] = len(companys_increase)
        ret['increase_rate'] = ret['increase'] / ret['number']
        return ret

    @classmethod
    def get_industry(cls, data):
        # 获取选定地区、行业的所有子地区、子行业
        area_id, industry_id = get_area_industry(data)
        # 工业企业数量
        companys_number = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR,
            industry__grade=1)
        # 新增工业企业数量=当前年份（显示的年份）创建的工业企业数量
        companys_increase = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id,
            company__established_time__year=settings.YEAR,
            industry__grade=1)
        ret = dict()
        ret['number'] = len(companys_number)
        ret['increase'] = len(companys_increase)
        ret['increase_rate'] = ret['increase'] / ret['number']
        return ret

    @classmethod
    def get_revenue(cls, data):
        # 获取选中地区、行业的所有下辖地区、子行业
        area_id, industry_id = get_area_industry(data)
        # 获取该地区、行业下的所有企业
        company = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id).values_list('company', flat=True)
        revenue = Company.objects.filter(
            id__in=company,
            established_time__year__lte=settings.YEAR).aggregate(Sum('revenue'))
        increase = Company.objects.filter(
            id__in=company,
            established_time__year=settings.YEAR).aggregate(Sum('revenue'))
        ret = dict()
        ret['number'] = revenue.get('revenue__sum', 0)
        ret['increase'] = increase.get('revenue__sum', 0)
        ret['increase_rate'] = ret['increase'] / ret['number']
        return ret

    @classmethod
    def get_tax_revenue(cls, data):
        # 获取选中地区、行业的所有下辖地区、子行业
        area_id, industry_id = get_area_industry(data)
        # 获取该地区、行业下的所有企业
        company = Relation.objects.filter(
            area_id__in=area_id,
            industry_id__in=industry_id).values_list('company', flat=True)
        tax = Company.objects.filter(
            id__in=company,
            established_time__year__lte=settings.YEAR).aggregate(Sum('tax'))
        increase = Company.objects.filter(
            id__in=company,
            established_time__year=settings.YEAR).aggregate(Sum('tax'))
        ret = dict()
        ret['number'] = tax.get('tax__sum', 0)
        ret['increase'] = increase.get('tax__sum', 0)
        ret['increase_rate'] = ret['increase'] / ret['number']
        return ret


class NumberSerializer(serializers.ModelSerializer):
    number_change = serializers.SerializerMethodField(
        help_text='企业数量变化趋势')
    number_details = serializers.SerializerMethodField(
        help_text='企业数量分布')
    upscale_number = serializers.SerializerMethodField(
        help_text='规上企业数量分布')
    increase_number = serializers.SerializerMethodField(
        help_text='新增企业数量分布')

    class Meta:
        model = Company
        fields = ('number_change', 'number_details',
                  'upscale_number', 'increase_number')

    @classmethod
    def get_number_change(cls, data):
        area_id, industry_id = get_area_industry(data)
        data = dict()
        # 全部企业近三年数量数据
        all_enterprise = dict()
        all_enterprise_year1 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=(settings.YEAR - 2))
        all_enterprise_year2 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=(settings.YEAR - 1))
        all_enterprise_year3 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR)
        all_enterprise['%s' % (settings.YEAR - 2)] = len(all_enterprise_year1)
        all_enterprise['%s' % (settings.YEAR - 1)] = len(all_enterprise_year2)
        all_enterprise['%s' % settings.YEAR] = len(all_enterprise_year3)
        # 工业企业近三年的数据
        industry = dict()
        industry_year1 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=(settings.YEAR - 2),
            industry__grade=1)
        industry_year2 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=(settings.YEAR - 1),
            industry__grade=1)
        industry_year3 = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR,
            industry__grade=1)
        industry['%s' % (settings.YEAR - 2)] = len(industry_year1)
        industry['%s' % (settings.YEAR - 1)] = len(industry_year2)
        industry['%s' % settings.YEAR] = len(industry_year3)
        data['all_enterprise'] = all_enterprise
        data['industry'] = industry
        return data

    @classmethod
    def get_number_details(cls, data):
        '''
        各行业企业数量分布
        :param data:
        :return:
        '''
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR
        ).values('industry').annotate(
            number=Count('company')
        ).values(
            'industry__name', 'industry_id', 'number')
        return details

    @classmethod
    def get_upscale_number(cls, data):
        '''
        规上企业数量分布
        :param data:
        :return:
        '''
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR,
            company__revenue__gte=2000
        ).values('industry').annotate(
            number=Count('company')
        ).values('industry__name', 'industry_id', 'number')
        return details

    @classmethod
    def get_increase_number(cls, data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year=settings.YEAR
        ).values('industry').annotate(
            number=Count('company')
        ).values(
            'industry__name', 'industry_id', 'number')
        return details


class Top5Serializer(serializers.ModelSerializer):
    number_details = serializers.SerializerMethodField()
    upscale_number = serializers.SerializerMethodField()
    increase_number = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('number_details', 'upscale_number', 'increase_number')

    @classmethod
    def get_number_details(cls, data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR
        ).values(
            'industry'
        ).annotate(
            number=Count('company')
        ).values(
            'industry__name', 'industry_id', 'number'
        ).order_by('number')[:5]

        return details

    @classmethod
    def get_upscale_number(cls, data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year__lte=settings.YEAR,
            company__revenue__gte=2000
        ).values('industry').annotate(
            number=Count('company')
        ).values(
            'industry__name', 'industry_id', 'number'
        ).order_by('number')[:5]
        return details

    @classmethod
    def get_increase_number(cls, data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__established_time__year=settings.YEAR
        ).values('industry').annotate(
            number=Count('company')
        ).values(
            'industry__name', 'industry_id', 'number'
        ).order_by('number')[:5]
        return details


class RevenueDataSerializer(serializers.ModelSerializer):
    receivable_interval_count = serializers.SerializerMethodField(
        method_name='get_count')
    annual_revenue_trend = serializers.SerializerMethodField(
        method_name='get_trend')
    area_revenue = serializers.SerializerMethodField(
        method_name='get_area')

    class Meta:
        model = Company
        fields = (
            'receivable_interval_count',
            'annual_revenue_trend',
            'area_revenue',
        )

    @staticmethod
    def get_count(data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year=settings.YEAR
        ).values(
            interval=Case(
                When(Q(company__revenue__lt=10**7), then=Value('0-1')),
                When(Q(company__revenue__gte=10**7) &
                     Q(company__revenue__lt=2*10**7),
                     then=Value('1-2')),
                When(Q(company__revenue__gte=2*10**7) &
                     Q(company__revenue__lt=3*10**7),
                     then=Value('2-3')),
                When(Q(company__revenue__gte=3*10**7) &
                     Q(company__revenue__lt=5*10**7),
                     then=Value('3-5')),
                When(Q(company__revenue__gte=5*10**7) &
                     Q(company__revenue__lt=7*10**7),
                     then=Value('5-7')),
                When(Q(company__revenue__gte=7*10**7) &
                     Q(company__revenue__lt=1*10**8),
                     then=Value('7-10')),
                When(Q(company__revenue__gte=1*10**7) &
                     Q(company__revenue__lt=15*10**7),
                     then=Value('10-15')),
                When(Q(company__revenue__gte=15*10**7) &
                     Q(company__revenue__lt=3*10**8),
                     then=Value('15-30')),
                When(Q(company__revenue__gte=3*10**8),
                     then=Value('30')),
                default=Value(0),
                output_field=CharField(),
            )).annotate(count=Count('id')).values('count', 'interval')
        return details

    @staticmethod
    def get_trend(data):
        area_id, industry_id = get_area_industry(data)
        all_industry_revenue = Relation.objects.filter(
            area_id__in=area_id,
            company__statistic_time__year__lte=settings.YEAR,
            company__statistic_time__year__gte=settings.YEAR-3
        ).values(
            'company__statistic_time__year'
        ).annotate(
            accounts=Sum('company__revenue')
        ).values('accounts', 'company__statistic_time__year')
        industry_revenue = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR,
            company__statistic_time__year__gte=settings.YEAR-3
        ).values(
            'company__statistic_time__year'
        ).annotate(
            accounts=Sum('company__revenue'),
            year=F('company__statistic_time__year')
        ).order_by(
            'company__statistic_time__year'
        ).values('accounts', 'company__statistic_time__year')
        return {'all_industry_revenue':all_industry_revenue,
                'industry_revenue':industry_revenue}

    @staticmethod
    def get_area(data):
        area_id, industry_id = get_area_industry(data)
        area_revenue = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR
        ).values(
            'company__statistic_time__year',
            'area_id'
        ).annotate(
            account=Sum('company__revenue')
        ).order_by('account')[:10].values(
            'area_id', 'area__name', 'account')
        all_area_revenue = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR
        ).values(
            'company__statistic_time__year'
        ).annotate(
            account=Sum('company__revenue')
        ).order_by('account').values(
            'account')[0]
        for i in area_revenue:
            i['rate'] = i.get('account')/all_area_revenue['account']
        return area_revenue


class TaxRevenueDataSerializer(serializers.ModelSerializer):
    receivable_interval_count = serializers.SerializerMethodField(
        method_name='get_count')
    annual_tax_trend = serializers.SerializerMethodField(
        method_name='get_trend')
    area_tax = serializers.SerializerMethodField(
        method_name='get_area')

    class Meta:
        model = Company
        fields = (
            'receivable_interval_count',
            'annual_tax_trend',
            'area_tax',
        )

    @staticmethod
    def get_count(data):
        area_id, industry_id = get_area_industry(data)
        details = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year=settings.YEAR
        ).values(
            interval=Case(
                When(Q(company__tax__lt=3 ** 5),
                     then=Value('0-0.3')),
                When(Q(company__tax__gte=3 ** 5) &
                     Q(company__tax__lt=5 * 10 ** 5),
                     then=Value('0.3-0.5')),
                When(Q(company__tax__gte=5 * 10 ** 5) &
                     Q(company__tax__lt=1 * 10 ** 6),
                     then=Value('0.5-1')),
                When(Q(company__tax__gte=1 * 10 ** 6) &
                     Q(company__tax__lt=15 * 10 ** 5),
                     then=Value('1-1.5')),
                When(Q(company__tax__gte=15 * 10 ** 5) &
                     Q(company__tax__lt=2 * 10 ** 6),
                     then=Value('1.5-2')),
                When(Q(company__tax__gte=2 * 10 ** 6) &
                     Q(company__tax__lt=3 * 10 ** 6),
                     then=Value('2-3')),
                When(Q(company__tax__gte=3 * 10 ** 6) &
                     Q(company__tax__lt=4 * 10 ** 6),
                     then=Value('3-4')),
                When(Q(company__tax__gte=4 * 10 ** 6) &
                     Q(company__tax__lt=1 * 10 ** 7),
                     then=Value('4-10')),
                When(Q(company__tax__gte=1 * 10 ** 7) &
                     Q(company__tax__lt=12 * 10 ** 6),
                     then=Value('10-12')),
                When(Q(company__tax__gte=12 * 10 ** 6) &
                     Q(company__tax__lt=15 * 10 ** 6),
                     then=Value('12-15')),
                When(Q(company__tax__gte=15 * 10 ** 6) &
                     Q(company__tax__lt=2 * 10 ** 7),
                     then=Value('15-20')),
                When(Q(company__tax__gte=2 * 10 ** 7) &
                     Q(company__tax__lt=3 * 10 ** 7),
                     then=Value('20-30')),
                When(Q(company__tax__gte=3 * 10 ** 7),
                     then=Value('30')),
                default=Value(0),
                output_field=CharField(),
            )).annotate(count=Count('id')).values('count', 'interval')
        return details

    @staticmethod
    def get_trend(data):
        area_id, industry_id = get_area_industry(data)
        all_industry_tax = Relation.objects.filter(
            area_id__in=area_id,
            company__statistic_time__year__lte=settings.YEAR,
            company__statistic_time__year__gte=settings.YEAR - 3
        ).values(
            'company__statistic_time__year'
        ).annotate(
            accounts=Sum('company__tax')
        ).values('accounts', 'company__statistic_time__year')
        industry_tax = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR,
            company__statistic_time__year__gte=settings.YEAR - 3
        ).values(
            'company__statistic_time__year'
        ).annotate(
            accounts=Sum('company__tax'),
            year=F('company__statistic_time__year')
        ).order_by(
            'company__statistic_time__year'
        ).values(
            'accounts',
            'company__statistic_time__year')
        return {'all_industry_tax': all_industry_tax,
                'industry_tax': industry_tax}

    @staticmethod
    def get_area(data):
        area_id, industry_id = get_area_industry(data)
        area_tax = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR
        ).values(
            'company__statistic_time__year',
            'area_id'
        ).annotate(
            account=Sum('company__tax')
        ).order_by('account')[:10].values(
            'area_id', 'area__name', 'account')
        all_area_tax = Relation.objects.filter(
            area_id__in=area_id, industry_id__in=industry_id,
            company__statistic_time__year__lte=settings.YEAR
        ).values(
            'company__statistic_time__year'
        ).annotate(
            account=Sum('company__tax')
        ).order_by('account').values(
            'account')[0]
        print(area_tax, all_area_tax)
        for i in area_tax:
            i['rate'] = i.get('account') / all_area_tax['account']
        return area_tax

class AreaTradeLSerializer(serializers.ModelSerializer):
    area_info = serializers.SerializerMethodField(
        method_name='get_area')
    industry_info = serializers.SerializerMethodField(
        method_name='get_industry')

    class Meta:
        model = Company
        fields = ('area_info', 'industry_info')

    @staticmethod
    def get_area(_):
        return Area.objects.filter(
            deleted=False
        ).values(
            'id', 'name', 'first_id',
            'second_id', 'grade',
        )

    @staticmethod
    def get_industry(_):
        return Industry.objects.filter(
            deleted=False
        ).values(
            'id', 'name', 'first_id', 'grade',
        )
