from django.db.models import Q

from .models import Area, Industry


def get_area_industry(data):
    '''
    获取地区和行业
    :param area:
    :param industry:
    :return:
    '''
    area, industry = data.get('area', ''), data.get('industry', 0)
    if area:
        # 获取该地区下面的所有下级地区
        area_id = Area.objects.filter(
            Q(first_id=area) | Q(second_id=area)).values_list('id', flat=True)
        area_id.append(area)
        # 全国
    else:
        area_id = Area.objects.all().values_list('id', flat=True)
    if industry:
        # 获取该行业下面的所有子行业
        industry_id = Industry.objects.filter(
            first_id=industry).values_list('id', flat=True)
        industry_id.append(industry)
        # 全行业
    else:
        industry_id = Industry.objects.all().values_list('id', flat=True)
    return area_id, industry_id
