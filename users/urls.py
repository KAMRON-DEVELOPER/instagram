from django.urls import path
from .views import CreateUserView, VerifyApiView, GetNewVerifyApiView, ChangeUserView, ChangeUserInformationView, ChangeUserPhotoView, LoginView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('resend/', GetNewVerifyApiView.as_view()),
    path('change/', ChangeUserInformationView.as_view()),
    path('change-photo/', ChangeUserPhotoView.as_view()),
]


