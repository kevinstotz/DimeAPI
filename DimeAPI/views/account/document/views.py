from DimeAPI.settings.base import DOCUMENT_STATUS
from DimeAPI.models import Document, FileType, DocumentType, DocumentStatus
from DimeAPI.serializer import DocumentTypeSerializer, DocumentSerializer
from DimeAPI.classes import ReturnResponse
from DimeAPI.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import views
import json
import logging
from rest_framework import mixins

logger = logging.getLogger(__name__)


class UserDocuments(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    model = Document
    serializer_class = DocumentSerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = Document.objects.all()

    def get(self, request, *args, **kwargs):
        document_serializer = DocumentSerializer(instance=Document.objects.filter(user=self.request.user.user_profile), many=True)
        return Response(json.loads(json.dumps(document_serializer.data)), content_type="application/json")

    def delete(self, request, pk, format=None):
        document = self.get_object()
        if document.user == self.request.user.user_profile:
            document.delete()
            logger.info("Document deleted: " + document.name + ":by user_profile:" + str(self.request.user.user_profile.pk))
        else:
            logger.info(
                "Document tried to be deleted: " + document.name + ":by user_profile:" + str(self.request.user.user_profile.pk))
        return Response(ReturnResponse.Response(0, __name__, "deleted", 0).return_json(),
                        status=status.HTTP_204_NO_CONTENT)


class DocumentTypes(generics.ListAPIView):
    model = DocumentType
    serializer_class = DocumentTypeSerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = DocumentType.objects.all().filter(active=0)


class DocumentUpload(views.APIView):
    model = Document
    parser_classes = (FileUploadParser, )
    permission_classes = (IsAuthenticated,)

    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        document = Document()
        document.document = file_obj
        document.name = file_obj.name
        document.file_type = FileType.objects.get(pk=1)
        document.status = DocumentStatus.objects.get(pk=DOCUMENT_STATUS['READY_TO_VERIFY'])
        document.type = DocumentType.objects.get(pk=file_obj.name[:file_obj.name.index('_')])
        document.user = self.request.user.user_profile
        document.save()
        logger.info("document uploaded " + document.name)
        return Response(ReturnResponse.Response(1, __name__, 'success', "u").return_json(),
                        status=status.HTTP_201_CREATED)

