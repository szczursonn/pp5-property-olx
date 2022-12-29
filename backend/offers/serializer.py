from .models import Offer, OfferPhoto
from rest_framework import serializers

class OfferPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferPhoto
        fields = [
            'id',
            'photo'
        ]

class OfferSerializer(serializers.ModelSerializer):

    photos = OfferPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'description',
            'status',
            'category',
            'type',
            'square_meters',
            'price',
            'location_lat',
            'location_lng',
            'location_city_name',
            'location_street_name',
            'location_house_number',
            'location_apt_number',
            'author_id',
            'created_at',
            'photos'
        ]
