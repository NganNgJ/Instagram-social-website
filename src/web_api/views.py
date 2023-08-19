from rest_framework.response import Response 
from rest_framework.decorators import api_view
from web_api.error_codes import ERROR_CODES
from rest_framework.exceptions import ParseError

from web_api.enum import (
    Status
)

#Currency
@api_view(['GET'])
def get_test(request):
    return Response('ACTIVE')

# raise ParseError(ERROR_CODES[400001], 400001)
# Status.ACTIVE.name .value
