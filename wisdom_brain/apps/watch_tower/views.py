from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import status

from wisdom_brain.apps.watch_tower.serializers.serializers import \
    AreaTradeLSerializer, StatisticsSerializer

from .filters import StatisticFilter
from .models import Company, Relation


class StatisticsLView(ListAPIView):
    serializer_class = StatisticsSerializer
    queryset = Company.objects.filter()
    filter_class = StatisticFilter

    def get(self, request, *args, **kwargs):
        area = request.query_params.get('area_id', '')
        industry = request.query_params.get('industry_id', 0)
        params = {'area_id': area, 'industry_id': industry}
        data = StatisticsSerializer(params).data
        return Response(status=status.HTTP_200_OK, data=data)


class AreaTradeLView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Relation.objects.filter(deleted=False)
    serializer_class = AreaTradeLSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def get(self, request, *args, **kwargs):
        ret = AreaTradeLSerializer(data=request.data)
        ret.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=ret.data)
