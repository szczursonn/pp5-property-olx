from django.urls import path
from .views import UserView, UserSelfView

urlpatterns = [
    path('me/', UserSelfView.as_view()),
    path('<int:pk>', UserView.as_view())
]