from django.urls import path
from .views import CreateUserView, VerifyApiView, GetNewVerifyApiView


urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('new-verify/', GetNewVerifyApiView.as_view()),
]


