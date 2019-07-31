import copy

from wisdom_brain.apps.swagger_docs.schemas import API_LIST_SCHEMA_BASE


BASE_SCHEMA = []

RESP_SCHEMA = copy.deepcopy(API_LIST_SCHEMA_BASE)
RESP_SCHEMA['results'] = BASE_SCHEMA

STRUCTURE = {
    'get': {
        '200': {
            'description': 'Return the list of the Test objects.',
            'schema': {
                'type': 'object',
                'properties': BASE_SCHEMA,
                'example': {
                    "count": 1,
                    "next": '',
                    "previous": '',
                    "results": []
                }
            }
        },
        '404': {
            'description': 'Not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                },
                'example': ''
            }
        }
    },
    'post': {
        '201': {
            'description': 'Create succeed',
            'schema': {
                'type': 'object',
                'properties': BASE_SCHEMA,
                'example': None
            }
        }
    }
}


def doc_exp(get=False, post=False, get_200_exp=None,
            post_201_exp=None, get_404_exp='',
            post_404_exp=''):
    response = copy.deepcopy(STRUCTURE)
    if get:
        response['get']['200']['schema']['example']['results'] = get_200_exp
        response['get']['404']['schema']['example'] = get_404_exp
    else:
        response.pop('get')
    if post:
        response['psot']['201']['schema']['example']['results'] = post_201_exp
        response['psot']['404']['schema']['example'] = post_404_exp
    else:
        response.pop('post')
    return response

AccountLCView_FAKER = {
    "email": "fake-email@email.com",
    "phone": "10012345678",
    "nickname": "",
    "sex": "male",
    "job_num": "",
    "wechat": "",
    "user": {
        "username": "usr-eaqvhubx",
        "user_id": 1,
        "groups": [],
        "permissions": []
    },
    "account_id": 1
}
