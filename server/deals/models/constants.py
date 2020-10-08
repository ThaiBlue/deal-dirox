from django.http import HttpResponse
from json import dumps

# HTTP response
HTTP_200 = HttpResponse(content=dumps({'status': 'OK', 'description': 'Success'}), status=200, content_type='application/json')
HTTP_405 = HttpResponse(content=dumps({'status': 'Fail', 'description': 'Method Not Allowed'}), status=405, content_type='application/json')
HTTP_404 = HttpResponse(content=dumps({'status': 'Fail', 'description': 'Not Found'}) , status=404, content_type='application/json')
HTTP_408 = HttpResponse(content=dumps({'status': 'Fail', 'description': 'Request Timeout'}), status=408, content_type='application/json')
HTTP_400_LOGIN_REQUIRE = HttpResponse(content=dumps({'error': 'not_authorized', 'description': 'login require'}), status=400, content_type='application/json')
HTTP_400_USER_NOT_FOUND = HttpResponse(content=dumps({'error': 'user_not_found', 'description': 'No such user found from database'}), status=400, content_type='application/json')
HTTP_400_WRONG_PASSWORD = HttpResponse(content=dumps({'error': 'wrong_password', 'description': 'The provided password did not match user\'s credential'}), status=400, content_type='application/json')
HTTP_400_INVALID_QUERY = HttpResponse(content=dumps({'error': 'invalid_query', 'description': 'Not contain the appropriate query params'}), status=400, content_type='application/json')
HTTP_400_NO_SERVICE_AVAILABLE = HttpResponse(content=dumps({'error': 'no_service', 'description': 'User not authorize/connect service account to this account yet'}), status=400, content_type='application/json')
HTTP_400_INVALID_SERVICE = HttpResponse(content=dumps({'error': 'invalid_service', 'description': 'Service is registered in another account'}), status=400, content_type='application/json')
HTTP_400_CACHE_REQUEST_FAIL = HttpResponse(content=dumps({'error': 'missing_argument', 'description': 'Must contain deal_id, folder_id and status'}), status=400, content_type='application/json')
HTTP_403_USER_FORBIDDEN = HttpResponse(content=dumps({'error': 'forbidden', 'description': 'User does not have the right to access this service'}), status=403, content_type='application/json')


# Database relate constants
FETCHING_TIME = 10

# Deals stage
MAKE_OFFER = '2186805'

# LDAP configuration
LDAP_PWD = 'thay-the-root'
LDAP_HOST = '10.84.254.37'
ALLOWED_ACCESS_TITLE = ['Trainee']