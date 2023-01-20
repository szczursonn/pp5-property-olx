from django.urls import path
from .views import UserView, UserSelfView, UserUsernameChangeView, UserAvatarChangeView

urlpatterns = [
    path('me/avatar/', UserAvatarChangeView.as_view()),
    path('me/username/', UserUsernameChangeView.as_view()),
    path('me/', UserSelfView.as_view()),
    path('<int:pk>', UserView.as_view())
]