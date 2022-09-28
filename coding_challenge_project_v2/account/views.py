from rest_framework.views import APIView
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SignUpSerializer, UserSerializer

User = get_user_model()


@permission_classes((AllowAny,))
@throttle_classes([AnonRateThrottle])
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=UserSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
        )


@permission_classes((IsAuthenticated,))
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    ordering_fields = (
        'group__name',
    )
    filterset_fields = (
        'username',
        'role',
    )
