from django.urls import path

from . import views

urlpatterns = [
    path(r'watch_tower/area_trade/', views.AreaTradeLView.as_view()),
    path(r'watch_tower/statistics/', views.StatisticsLView.as_view()),
]
