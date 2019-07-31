from django.conf import settings
from rest_framework import serializers

from wisdom_brain.apps.watch_tower.models import StatisticData


class DataSerializer(serializers.ModelSerializer):
    all_enterprise = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()
    tax_revenue = serializers.SerializerMethodField()

    class Meta:
        model = StatisticData
        fields = ('all_enterprise', 'industry', 'revenue', 'tax_revenue')

    @classmethod
    def get_all_enterprise(cls, data):
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        company_number = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR).values('company_number', 'company_increase')
        return company_number

    @classmethod
    def get_industry(cls, data):
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        company_number = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id, industry__grade=1,
            date=settings.YEAR).values('company_number', 'company_increase')
        return company_number

    @classmethod
    def get_revenue(cls, data):
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        revenue_data = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR).values('revenue', 'revenue_increase')
        return revenue_data

    @classmethod
    def get_tax_revenue(cls, data):
        area_id = data.get('area_id', '0')
        industry_id = data.get('industry_id', '0')
        tax_data = StatisticData.objects.filter(
            area_id=area_id, industry_id=industry_id,
            date=settings.YEAR).values('tax', 'tax_increase')
        return tax_data
