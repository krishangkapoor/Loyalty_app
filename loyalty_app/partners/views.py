from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Partner
from .serializers import PartnerSerializer

class PartnerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        partner = request.user
        serializer = PartnerSerializer(partner)
        return Response(serializer.data)

