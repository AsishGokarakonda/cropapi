from django.urls import path
from .views import RegisterView,LoginView,UserProfileView,LogoutView,RegisterSuperUserView,LoginSuperUserView, UserListView,UserLocationView,AddFieldView, checkJwtValidatedView, GetFieldListView, UpdateCurDayView
# CropListView, CropView, 
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user/',UserProfileView.as_view(),name='profile'),
    path('checkjwt/',checkJwtValidatedView.as_view(),name='checkjwt'),
    path('registersuperuser/',RegisterSuperUserView.as_view(),name='registersuperuser'),
    path('loginsuperuser/',LoginSuperUserView.as_view(),name='loginsuperuser'),
    path('getusers/',UserListView.as_view(),name='getusers'),
    path('getuserlocation/',UserLocationView.as_view(),name='getuserlocation'),
    path('addfield/',AddFieldView.as_view(),name='addfield'),
    path('getfields/',GetFieldListView.as_view(),name='getfields'),
    path('updatecurday/',UpdateCurDayView.as_view(),name='updatecurday'),
]
