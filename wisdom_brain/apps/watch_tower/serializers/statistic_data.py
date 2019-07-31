from rest_framework import serializers

from wisdom_brain.apps.watch_tower.models import StatisticData
from .data_serializer import DataSerializer
from .number_serializer import NumberSerializer


class StatisticsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField(help_text='数量统计')
    number = serializers.SerializerMethodField(help_text='地图旁的分布统计')
    top5 = serializers.SerializerMethodField(help_text='几个top5的统计')
    revenue_data = serializers.SerializerMethodField(help_text='营收数据统计')
    tax_revenue_data = serializers.SerializerMethodField(help_text='税收数据统计')

    class Meta:
        model = StatisticData
        fields = ('data', 'number', 'top5',
                  'tax_revenue_data', 'revenue_data',)

    @classmethod
    def get_data(cls, data):
        return DataSerializer(data).data

    @classmethod
    def get_number(cls, data):
        return NumberSerializer(data).data
