"""wisdom_brain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .base import urlpatterns as base_url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.views import defaults as default_views
from django.views.generic import RedirectView
from django.conf.urls import url

from wisdom_brain.apps.swagger_docs.views import get_custom_swagger_view

version = '%s/api/' % settings.VERSION

urlpatterns = [
    path("",RedirectView.as_view(url="/swagger/"),
         name="home"),
    path('admin/', admin.site.urls),
    path(version, include('wisdom_brain.apps.watch_tower.urls'),
         name='watch_tower'),
    path(r'swagger/', get_custom_swagger_view(),
         name='swaggerdoc'),

    # path('api/watch_tower', include('wisdom_brain.apps.watch_tower.urls'),
    #      name='watch_tower'),
    # path('api/investment', include('wisdom_brain.apps.intelligent_attract_investment.urls'),
    #      name='investment'),
    url(r'docs/(?P<path>.*)$', serve, {'document_root': settings.SPHINX_DOCS_ROOT, 'show_indexes': True}),
    url(r'docs/', serve,
        {'document_root': settings.SPHINX_DOCS_ROOT, 'path': 'index.html', 'show_indexes': True}),
]

urlpatterns += base_url
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/",
                            include(debug_toolbar.urls))] + urlpatterns