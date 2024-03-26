from django.urls import path
from .views import CreateUserView, VerifyApiView, GetNewVerifyApiView, ChangeUserView, ChangeUserInformationView


urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('resend/', GetNewVerifyApiView.as_view()),
    path('change/', ChangeUserInformationView.as_view()),
]


