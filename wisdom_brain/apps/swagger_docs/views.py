#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openapi_codec import encode

from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

from rest_framework_swagger.views import renderers


def _get_custom_responses(link):
    """
    Returns minimally acceptable responses object based
    on action / method type.
    """
    if hasattr(link, '_response_docs'):
        return link._response_docs
    template = {'description': ''}
    if link.action.lower() == 'post':
        return {'201': template}
    if link.action.lower() == 'delete':
        return {'204': template}
    return {'200': template}


# monkey patch
encode._get_responses = _get_custom_responses


def get_custom_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()
