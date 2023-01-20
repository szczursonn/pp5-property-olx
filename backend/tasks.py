from django.utils.timezone import now
from offers.models import Offer

def deactivate_expired_offers():
    expired_offers = Offer.objects.all().filter(status=Offer.OfferStatus.ACTIVE).filter(active_until__lte=now())
    affected = expired_offers.update(status=Offer.OfferStatus.INACTIVE)
    return affected