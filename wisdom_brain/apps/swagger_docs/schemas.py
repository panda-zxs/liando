#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.schemas import AutoSchema

API_LIST_SCHEMA_BASE = {
    "count": {
        "type": "integer",
    },
    "next": {
        "type": "string",
    },
    "previous": {
        "type": "string",
    },
    "results": {
        "type": "array",
        "items": {

        }
    }
}


class CustomAutoSchema(AutoSchema):

    def get_link(self, path, method, base_url):
        link = super(CustomAutoSchema, self).get_link(path, method, base_url)
        if hasattr(self.view, 'response_docs'):
            link._response_docs = self.view.response_docs.get(method.lower())
        return link
