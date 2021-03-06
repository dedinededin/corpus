from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import FileSerializer
from nlp.bapCleanAndTokenize import clean_and_tokenize, clean_and_tokenize_v2
from .models import File
import json


class UploadFile(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():

            file_serializer.save()
            data = clean_and_tokenize(request.data['file'])
            # return Response(file_serializer.data, status=status.HTTP_201_CREATED)

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleanWithParameters(APIView):

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        document = File.objects.get(uuid=request.data['uuid'])
        parameters = request.data['checkboxes']
        most_common = int(request.data['mostCommon'])

        data = clean_and_tokenize_v2(document.file, parameters, most_common)

        return Response(data, status=status.HTTP_200_OK)


class Query(APIView):

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        query = request.data['query']
        query_set = File.objects.filter(file__contains=query)
        dictionaries = [obj.as_dict() for obj in query_set]
        data = json.dumps({"data": dictionaries})
        return Response(data, status=status.HTTP_200_OK)


class Test(APIView):
    permission_classes = (AllowAny,)

    # https://www.django-rest-framework.org/api-guide/permissions/

    def get(self, request, format=None):
        return Response("asfasd", status=status.HTTP_200_OK)
