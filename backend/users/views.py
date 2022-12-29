from rest_framework import permissions, generics
from .serializers import UserSerializer
from .models import User

class UserSelfView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = UserSerializer

    queryset = User.objects.all()
