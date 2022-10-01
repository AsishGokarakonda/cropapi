from django.urls import path
from .views import CropListView, CropView, RegisterView,LoginView,UserProfileView,LogoutView
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user/',UserProfileView.as_view(),name='profile'),
    path('addcrop/',CropView.as_view(),name='addcrop'),
    path('getcrop/',CropListView.as_view(),name='getcrop'),
]
