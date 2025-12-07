from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TableQRCode
from .serializers import MenuSerializer

class MenuByCode(APIView):
    def get(self, request, code):
        try:
            qr = TableQRCode.objects.get(code=code)
            serializer = MenuSerializer(qr.menu, context={'request': request})
            return Response(serializer.data)
        except TableQRCode.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
