from django.urls import path
from .views import CreateUserView, VerifyApiView, GetNewVerifyApiView, ChangeUser


urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('resend/', GetNewVerifyApiView.as_view()),
    path('change/', ChangeUser.as_view()),
]


