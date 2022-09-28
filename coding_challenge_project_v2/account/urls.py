from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUpView, UserView

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
]
