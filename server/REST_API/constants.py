from django.http import HttpResponse
from json import dumps

# HTTP response
HTTP_405 = HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, content_type='application/json')
HTTP_404 = HttpResponse(content="<h1>Not Found<h1/>" , status=404, content_type='application/json')
HTTP_200 = HttpResponse(content='<h1>Success<h1/>', status=200, content_type='application/json')
HTTP_408 = HttpResponse(content='<h1>Request Timeout<h1/>', status=408, content_type='application/json')
HTTP_400_AUTHENTICATION_FAIL = HttpResponse(content=dumps({'error':'invalid_credential', 'description':'wrong user_id or password'}), status=400, content_type='application/json')
HTTP_400_NO_SERVICE_AVAILABLE = HttpResponse(content=dumps({'error':'no_service', 'description': 'User not authorize/connect service account to this account yet'}), status=400, content_type='application/json')

# Database relate constants
FETCHING_TIME = 10

#Deals stage
MAKE_OFFER = '2186805'