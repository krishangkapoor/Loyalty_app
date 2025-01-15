from django.urls import path
from .views import ScanBarcodeView, BarcodeScanHistoryView

urlpatterns = [
    path('scan-barcode/', ScanBarcodeView.as_view(), name='scan-barcode'),
    path('barcode-history/', BarcodeScanHistoryView.as_view(), name='barcode-history'),
]
