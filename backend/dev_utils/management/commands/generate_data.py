import random
import string
from django.core.management.base import BaseCommand, CommandParser
from users.models import User
from offers.models import Offer, OfferPhoto
import shutil
import os

offer_cities = ['Kraków', 'Krzeszowice', 'Warszawa', 'Gdańsk', 'Grudziądz', 'Bełchatów', 'Katowice', 'Wrocław', 'Cieszyn']
user_email_providers = ['google.com', 'uek.krakow.pl', 'microsoft.com', 'onet.pl']

class Command(BaseCommand):
    help = 'Generates fake data'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--seed',
            type=str,
            help='Randomness seed'
        )
    
    def _randChance(self, chance: float) -> bool:
        return random.uniform(0.0, 1.0)>1-chance
    
    def _randString(self) -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(random.randint(8,12)))
    
    def _randPhoneNumber(self) -> str:
        n=''
        for i in range(9):
            n+=str(random.randint(1, 9))
        return n

    def handle(self, *args, **kwargs):
        seed = kwargs['seed']
        if seed:
            random.seed(seed)

        shutil.copytree('dev_utils/mock_media', 'media')

        mock_offer_photos = list(map(lambda filename: os.path.join('offer_photos', filename), os.listdir('media/offer_photos')))

        generated_users = []
        user_amount = random.randint(10, 40)
        for i in range(user_amount):
            password = self._randString()
            username = f'user{i}_{password}'
            user = User.objects.create_user(
                username=username,
                password=password,
                email=f'{username}@{random.choice(user_email_providers)}'
            )
            if self._randChance(0.7):
                user.phone_number=self._randPhoneNumber()
                user.save()
            generated_users.append(user)

        offer_amount = random.randint(250, 1000)
        photo_amount_total = 0
        offer_name_prefix = self._randString()
        for i in range(offer_amount):
            author = random.choice(generated_users)
            offer = Offer.objects.create(
                title=f'Offer {offer_name_prefix}_{i}',
                description=self._randString()*random.randint(5, 80) if self._randChance(0.9) else None,
                status=Offer.OfferStatus.ACTIVE,
                category=random.choice(Offer.EstateType.choices)[0],
                type=random.choice(Offer.OfferType.choices)[0],
                square_meters=random.uniform(20.0, 1200.0) if self._randChance(0.5) else None,
                price=random.randint(40, 1100)*10 if self._randChance(0.9) else None,
                location_lat=random.uniform(49.3, 50.8),
                location_lng=random.uniform(19.1, 20.9),
                location_city_name=random.choice(offer_cities),
                location_street_name=f'street_{self._randString()}' if self._randChance(0.8) else None,
                location_house_number=random.randint(1, 50) if self._randChance(0.8) else None,
                author=author
            )

            photo_amount = random.randint(0, 3)
            photo_amount_total += photo_amount
            for i in range(photo_amount):
                offer_photo = OfferPhoto.objects.create(
                    offer=offer,
                    photo=random.choice(mock_offer_photos)
                )

        self.stdout.write(f'Generated {user_amount} users and {offer_amount} offers with {photo_amount_total} photos')