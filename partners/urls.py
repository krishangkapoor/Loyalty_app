from django.urls import path
from .views import PartnerRegisterView, PartnerLoginView, PartnerProfileView, AddProductView, ListProductsView

urlpatterns = [
    path('register/', PartnerRegisterView.as_view(), name='partner-register'),
    path('login/', PartnerLoginView.as_view(), name='partner-login'),
    path('profile/', PartnerProfileView.as_view(), name='partner-profile'),
    path('products/add/', AddProductView.as_view(), name='add-product'),
    path('products/', ListProductsView.as_view(), name='list-products'),

]
