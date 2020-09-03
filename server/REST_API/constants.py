from django.http import HttpResponse

# HTTP response
HTTP_405 = HttpResponse(content='<h1>Method Not Allowed<h1/>', status=405, reason='Method Not Allowed')
HTTP_404 = HttpResponse(content="<h1>Page Not Found<h1/>" , status=404, reason="Page Not Found")
HTTP_401 = HttpResponse(content='<h1>Not Authorized<h1/>', status=401, reason='Not Authorized')
HTTP_200 = HttpResponse(content='<h1>Success<h1/>', status=200)
HTTP_408 = HttpResponse(content='<h1>Request Timeout<h1/>', status=408, reason='Request Timeout')

# Database relate constants
FETCHING_TIME = 60

#Deals stage
MAKE_OFFER = '2186805'