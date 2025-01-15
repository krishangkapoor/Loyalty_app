from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import PartnerRegisterSerializer, PartnerLoginSerializer
from .models import Partner
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import PartnerProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView
from .models import Product
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

class PartnerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Partner registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartnerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartnerLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user and isinstance(user, Partner):
                refresh = RefreshToken()
                refresh.payload['user_id'] = user.id
                refresh.payload['username'] = user.username
                refresh.payload['user_type'] = 'partner'

                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials or not a partner"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartnerProfileView(RetrieveUpdateAPIView):
    serializer_class = PartnerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        print("Authenticated User:", user)
        print("User Type:", type(user))
        if isinstance(user, Partner):
            return user
        
        raise PermissionDenied(detail="You are not authorized to access this resource.")
    
class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(partner=request.user)  
            return Response({
                "message": "Product added successfully",
                "product": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(partner=self.request.user)