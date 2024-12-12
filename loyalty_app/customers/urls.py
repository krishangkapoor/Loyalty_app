from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomerProfileView, CustomerRegistrationView

urlpatterns = [
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomerRegistrationView.as_view(), name='customer-register'),
]
