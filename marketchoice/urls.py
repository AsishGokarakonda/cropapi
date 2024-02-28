from django.urls import path
from .views import PredictMarketPrice, GetNearestMarkets, AddNewMarket
# CropListView, CropView, 
urlpatterns = [
    path('predictmarketprice/',PredictMarketPrice.as_view(),name='predictmarketprice'),
    path('getnearestmarkets/',GetNearestMarkets.as_view(),name='getnearestmarkets'),
    path('addnewmarket/',AddNewMarket.as_view(),name='addnewmarket'),
]
