from rest_framework import status, permissions, generics, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
import geocoder
from .models import Offer, OfferPhoto
from .serializer import OfferSerializer

class OfferList(APIView):
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly, )
    parser_classes = [parsers.MultiPartParser]

    def get(self, request, format=None):

        p=request.query_params

        q = Offer.objects.filter(status=Offer.OfferStatus.ACTIVE)
        if 'category' in p:
            q=q.filter(category=int(p['category']))
        if 'type' in p:
            q=q.filter(type=int(p['type']))
        if 'city' in p:
            city=p['city']
            prox = int(p['proximity']) if 'proximity' in p else 0

            # if prox=0, query by city name, else query by distance
            if prox==0:
                q=q.filter(location_city_name__contains=city)
            else:
                location=geocoder.osm(city)
                if not location.ok:
                    return Response({'detail': 'Unable to locate'}, status=status.HTTP_400_BAD_REQUEST)
                lat, lng = location.json['lat'], location.json['lng']
                prox_deg = (prox/40000)*360
                # TODO: proper query by proximity
                q=q.filter(
                    location_lat__lte=lat+prox_deg,
                    location_lng__lte=lng+prox_deg,
                    location_lat__gte=lat-prox_deg,
                    location_lng__gte=lng-prox_deg
                )
        if 'price_min' in p:
            q=q.filter(price__gte=int(p['price_min']))
        if 'price_max' in p:
            q=q.filter(price__lte=int(p['price_max']))
        if 'area_min' in p:
            q=q.filter(square_meters__gte=float(p['area_min']))
        if 'area_max' in p:
            q=q.filter(square_meters__lte=float(p['area_max']))
        
        q.prefetch_related('offerphoto_set')

        offer_serializer = OfferSerializer(instance=list(q), many=True)

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

class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class RandomOffers(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        q=Offer.objects.order_by('?')[:6]
        offer_serializer = OfferSerializer(instance=list(q), many=True)
        return Response(offer_serializer.data, status=status.HTTP_200_OK)