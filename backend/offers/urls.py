from django.urls import path
from .views import OfferList, OfferDetail, RandomOffers, OfferStatus

urlpatterns = [
    path('suggested', RandomOffers.as_view()),
    path('<int:pk>', OfferDetail.as_view()),
    path('<int:pk>/status', OfferStatus.as_view()),
    path('', OfferList.as_view())
]