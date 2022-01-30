from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer

User = get_user_model()


class UserList(ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
