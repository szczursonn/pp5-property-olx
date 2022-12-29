from django.contrib import admin
from .models import Offer, OfferPhoto

class OfferAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'category', 'type', 'location_city_name', 'author']

class OfferPhotoAdmin(admin.ModelAdmin):
    list_display=['id', 'image_tag', 'offer', 'photo']

admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferPhoto, OfferPhotoAdmin)