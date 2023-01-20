from rest_framework import status, permissions, generics, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
import datetime
import geocoder

from .models import Offer, OfferPhoto
from .serializers import OfferSerializer

class OfferList(APIView):
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly, )
    parser_classes = [parsers.MultiPartParser]

    def get(self, request, format=None):

        offer_query = OfferQueryParams(request.query_params)
        offers = Offer.objects.all()

        if offer_query.author_id is not None:
            offers=offers.filter(author_id=offer_query.author_id)

        if offer_query.category is not None:
            offers=offers.filter(category=offer_query.category)

        if offer_query.type is not None:
            offers=offers.filter(type=offer_query.type)

        if offer_query.status is not None:
            offers=offers.filter(status=offer_query.status)

        if offer_query.city is not None:
            if offer_query.proximity is None or offer_query.proximity==0:
                offers=offers.filter(location_city_name__contains=offer_query.city)
            else:
                location=geocoder.osm(offer_query.city)
                if not location.ok:
                    return Response(
                        {'detail': 'Unable to locate'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                lat, lng = location.json['lat'], location.json['lng']
                # TODO: proper proximity query instead of a bad rectangle
                proximity_as_deg = (offer_query.proximity/40000)*360
                offers=offers.filter(
                    location_lat__lte=lat+proximity_as_deg,
                    location_lng__lte=lng+proximity_as_deg,
                    location_lat__gte=lat-proximity_as_deg,
                    location_lng__gte=lng-proximity_as_deg
                )

        if offer_query.price_min is not None:
            offers=offers.filter(price__gte=offer_query.price_min)
        if offer_query.price_max is not None:
            offers=offers.filter(price__lte=offer_query.price_max)

        if offer_query.area_min is not None:
            offers=offers.filter(square_meters__gte=offer_query.area_min)
        if offer_query.area_max is not None:
            offers=offers.filter(square_meters__lte=offer_query.area_max)
        
        offers.prefetch_related('offerphoto_set')

        offer_serializer = OfferSerializer(instance=list(offers), many=True)

        return Response(offer_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        if request.user is AnonymousUser:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        d = request.data

        files = d.getlist('photos')
        title = d.get('title')
        description = d.get('description')
        category = d.get('category')
        offer_type = d.get('type')
        city = d.get('city')
        street_name = d.get('street_name')
        house_number = d.get('house_number')
        apt_number = d.get('apartment_number')
        square_meters = d.get('square_meters')
        price = d.get('price')

        # just the city
        geocode_queries=[city]
        # city with no streets
        if house_number is not None:
            geocode_queries.append(f'{city} {house_number}')
        # full address
        if street_name is not None and house_number is not None:
            geocode_queries.append(f'{city} {street_name} {house_number}')
        
        location=None
        while (location is None or not location.ok) and len(geocode_queries)>0:
            query=geocode_queries.pop()
            location=geocoder.osm(query)

        if not location.ok:
            return Response({'detail': 'Unable to locate'}, status=status.HTTP_400_BAD_REQUEST)

        lat, lng = location.json['lat'], location.json['lng']

        offer = Offer.objects.create(
            title=title,
            description=description,
            status=Offer.OfferStatus.ACTIVE,
            category=category,
            type=offer_type,
            square_meters=square_meters,
            price=price,
            location_lat=lat,
            location_lng=lng,
            location_city_name=city,
            location_street_name=street_name,
            location_house_number=house_number,
            location_apt_number=apt_number,
            author = request.user
        )
        for f in files:
            offer_photo = OfferPhoto()
            offer_photo.offer=offer
            offer_photo.photo.save(f'{offer.id}_{f.name}', f)
            offer_photo.save()

        responseData = {'id': offer.id, 'lat': lat, 'lng': lng}
        return Response(responseData, status=status.HTTP_201_CREATED)

class OfferQueryParams:
    category: int|None
    type: int|None
    status: int|None
    author_id: int|None
    city: str|None
    proximity: int|None
    price_min: int|None
    price_max: int|None
    area_min: float|None
    area_max: float|None

    def __init__(self, p):
        self.category = int(p['category']) if 'category' in p else None
        self.type = int(p['type']) if 'type' in p else None
        self.status = int(p['status']) if 'status' in p else None
        self.author_id = int(p['author_id']) if 'author_id' in p else None
        self.city = p.get('city')
        self.proximity = int(p['proximity']) if 'proximity' in p else None
        self.price_min = int(p['price_min']) if 'price_min' in p else None
        self.price_max = int(p['price_max']) if 'price_max' in p else None
        self.area_min = float(p['area_min']) if 'area_min' in p else None
        self.area_max = float(p['area_max']) if 'area_max' in p else None


class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class RandomOffers(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Offer.objects.filter(status=Offer.OfferStatus.ACTIVE).order_by('?')[:6]
    serializer_class = OfferSerializer

class OfferStatus(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk, format=None):

        offer = Offer.objects.get(id=pk)

        if offer.author.pk != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        offer.status = request.data.get('status')
        if offer.status == Offer.OfferStatus.ACTIVE:
            offer.active_until = now() + datetime.timedelta(days=3)
        elif offer.status == Offer.OfferStatus.INACTIVE:
            offer.active_until = now()
        offer.save()

        offer_serializer = OfferSerializer(instance=offer)

        return Response(data=offer_serializer.data, status=status.HTTP_200_OK)