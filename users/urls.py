from django.urls import path
from .views import CreateUserView, VerifyApiView, GetNewVerifyApiView, ChangeUserView, ChangeUserInformationView, ChangeUserPhotoView, LoginView, LoginRefreshView, LogoutView, ForgotPasswordView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('resend/', GetNewVerifyApiView.as_view()),
    path('change/', ChangeUserInformationView.as_view()),
    path('change-photo/', ChangeUserPhotoView.as_view()),
]


