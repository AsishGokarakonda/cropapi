from django.urls import path
from .views import PredictMarketPrice
# CropListView, CropView, 
urlpatterns = [
    path('predictmarketprice/',PredictMarketPrice.as_view(),name='predictmarketprice'),
]
