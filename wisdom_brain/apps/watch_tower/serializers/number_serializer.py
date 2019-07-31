from django.conf import settings
from rest_framework import serializers

from wisdom_brain.apps.watch_tower.models import StatisticData


class NumberSerializer(serializers.ModelSerializer):
    number_change = serializers.SerializerMethodField()
    number_details = serializers.SerializerMethodField()
    upscale_number = serializers.SerializerMethodField()
    increase_number = serializers.SerializerMethodField()

    class Meta:
        model = StatisticData
        fields = ('number_change', 'number_details',
                  'upscale_number', 'increase_number')

    @classmethod
    def get_number_change(cls, data):
        # todo:全工业还得考虑一下
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        details = dict()
        all_enterprise = dict()
        industry = dict()
        all_enterprise_year1 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR - 2).values('company_number')
        all_enterprise_year2 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR - 1).values('company_number')
        all_enterprise_year3 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR).values('company_number')
        all_enterprise['%s' % (settings.YEAR - 2)] = all_enterprise_year1
        all_enterprise['%s' % (settings.YEAR - 1)] = all_enterprise_year2
        all_enterprise['%s' % settings.YEAR] = all_enterprise_year3
        industry_year1 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR - 2, ).values('company_number')
        industry_year2 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR - 1, ).values('company_number')
        industry_year3 = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR, ).values('company_number')
        industry['%s' % (settings.YEAR - 2)] = industry_year1
        industry['%s' % (settings.YEAR - 1)] = industry_year2
        industry['%s' % settings.YEAR] = industry_year3
        details['all_enterprise'] = all_enterprise
        details['industry'] = industry
        return details

    @classmethod
    def get_number_details(cls, data):
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        details = StatisticData.objects.filter()
