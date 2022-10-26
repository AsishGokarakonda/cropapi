from django.urls import path
from .views import CropListView, CropView
urlpatterns = [
    path('addcrop/',CropView.as_view(),name='addcrop'),
    path('getcrop/',CropListView.as_view(),name='getcrop')
]
