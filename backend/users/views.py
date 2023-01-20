from rest_framework import permissions, generics, views, status, parsers
from rest_framework.response import Response
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

class UserUsernameChangeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, format=None):
        new_username = request.data.get('username')
        if not new_username:
            return Response({'detail': 'username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.username = new_username
        request.user.save()

        user_serializer = UserSerializer(instance=request.user)

        return Response(user_serializer.data, status=status.HTTP_200_OK)

class UserAvatarChangeView(views.APIView):

    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [parsers.MultiPartParser]

    def patch(self, request, format=None):
        avatar = request.data.get('avatar')

        request.user.avatar.save(f'{request.user.id}_{avatar.name}', avatar)
        request.user.save()

        user_serializer = UserSerializer(instance=request.user)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        request.user.avatar = None
        request.user.save()

        user_serializer = UserSerializer(instance=request.user)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)