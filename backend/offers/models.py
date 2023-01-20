from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from users.models import User

class Offer(models.Model):
    class OfferType(models.IntegerChoices):
        RENT = 0
        PURCHASE = 1
    class EstateType(models.IntegerChoices):
        HOUSE = 0
        PLOT = 1
        APARTMENT = 2
        ROOM = 3
        GARAGE_OR_PARKING = 4
        BUSINESS_PREMISES = 5
        WAREHOUSE = 6
        OTHER = 7
    class OfferStatus(models.IntegerChoices):
        ACTIVE = 0
        INACTIVE = 1
    
    title = models.CharField(
        max_length=50
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    status = models.SmallIntegerField(
        choices=OfferStatus.choices,
        default=0
    )
    category = models.SmallIntegerField(
        choices=EstateType.choices
    )
    type = models.SmallIntegerField(
        choices=OfferType.choices
    )
    square_meters = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        null=True
    )
    price = models.IntegerField(
        blank=True,
        null=True,
        validators=[]
    )
    location_lat = models.DecimalField(
        decimal_places=5,
        max_digits=7
    )
    location_lng = models.DecimalField(
        decimal_places=5,
        max_digits=7
    )
    location_city_name = models.CharField(
        max_length=30
    )
    location_street_name = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    location_house_number = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )
    location_apt_number = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    active_until = models.DateTimeField(
        default=now()+timedelta(days=3)
    )
    created_at = models.DateTimeField(
        default=now
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='no_apt_number_if_no_house_number',
                check=models.Q(location_house_number__isnull=True, location_apt_number__isnull=True) | 
                models.Q(location_house_number__isnull=False)
            ),
            models.CheckConstraint(
                name='active_until_greater_than_created_at',
                check=models.Q(active_until__gt=models.F('created_at'))
            )
        ]
    
    def __str__(self):
        return self.title

class OfferPhoto(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(upload_to='offer_photos')

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.photo}" width="100" height="100">')

    def __str__(self):
        return f'Offer Photo {self.id}'