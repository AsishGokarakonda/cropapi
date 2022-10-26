from django.urls import path
from .views import CropListView, CropView, RegisterView,LoginView,UserProfileView,LogoutView,RegisterSuperUserView,LoginSuperUserView, UserListView,UserLocationView
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user/',UserProfileView.as_view(),name='profile'),
    path('addcrop/',CropView.as_view(),name='addcrop'),
    path('getcrop/',CropListView.as_view(),name='getcrop'),
    path('registersuperuser/',RegisterSuperUserView.as_view(),name='registersuperuser'),
    path('loginsuperuser/',LoginSuperUserView.as_view(),name='loginsuperuser'),
    path('getusers/',UserListView.as_view(),name='getusers'),
    path('getuserlocation/',UserLocationView.as_view(),name='getuserlocation'),
]
