from django.urls import path
from .views import PartnerProfileView

urlpatterns = [
    path('profile/', PartnerProfileView.as_view(), name='partner-profile'),
]
