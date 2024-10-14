from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

urlpatterns = [
    path('register/', views.RegisterApiView.as_view()),
    path('register/verify/', views.VerifyApiView.as_view()),
    path('register/resend-code/', views.ResendVerificationCodeApiView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]