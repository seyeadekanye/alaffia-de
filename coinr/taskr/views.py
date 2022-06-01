import csv
import logging

from django.http import HttpRequest
from django.http.multipartparser import MultiPartParser
from rest_framework.parsers import JSONParser, FileUploadParser, BaseParser
from rest_framework.response import Response
from rest_framework.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_csv import renderers as r

from .service import handle_json, handle_csv

logger = logging.getLogger(__name__)

class CSVTextParser(BaseParser):
    """
    A CSV parser for DRF APIViews.
    Based on the RFC 4180 text/csv MIME type, but extended with
    a dialect.
    https://tools.ietf.org/html/rfc4180
    """
    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Return a list representing the rows of a CSV file.
        The first element is the header
        """
        media_type_params = dict([param.strip().split('=') for param in media_type.split(';')[1:]])
        charset = media_type_params.get('charset', 'utf-8')
        txt = stream.read().decode(charset)
        return txt.splitlines()


class CoinTaskViewSet(APIView):
    """
    Accepts coin tasks
    """
    parser_classes = [JSONParser, CSVTextParser]

    def post(self, request: HttpRequest):
        logger.info(f"Handling new request with content-type: {request.content_type}")
        logger.info(f"This is csv {request.content_type == 'text/csv'}")
        if request.content_type == 'application/json':
            handle_json(request.data)
            return Response(status=HTTP_200_OK)
        elif request.content_type == 'text/csv':
            handle_csv(request.data)
            return Response(status=HTTP_200_OK)
