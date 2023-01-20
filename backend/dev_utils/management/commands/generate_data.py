import random
import string
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandParser
from django.utils.timezone import now
from users.models import User
from offers.models import Offer, OfferPhoto
import shutil
import os


class Command(BaseCommand):
    help = 'Generates fake data'

    OFFER_CITIES = ['Kraków', 'Krzeszowice', 'Warszawa', 'Gdańsk', 'Grudziądz', 'Bełchatów', 'Katowice', 'Wrocław', 'Cieszyn',
    'Nowy Sącz', 'Jelenia Góra', 'Radom', 'Częstochowa', 'Budapeszt', 'Gdynia', 'Szczecin', 'Wieliczka', 'Lublin', 'Świnoujście']

    OFFER_STREETS = ['Polna', 'Leśna', 'Słoneczna', 'Krótka', 'Szkolna', 'Ogrodowa', 'Lipowa', 'Łąkowa', 'Brzozowa', 'Kwiatowa',
    'Kościelna', 'Sosnowa', 'Zielona', 'Parkowa', 'Akacjowa', 'Kolejowa', 'Kluczwody', 'Południowa', 'Poziomkowa', 'Zachodnia']

    USER_EMAIL_PROVIDERS = ['google.com', 'uek.krakow.pl', 'microsoft.com', 'onet.pl', 'outlook.com', 'mailinator.com', 'yahoo.com']

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
        mock_user_avatars = list(map(lambda filename: os.path.join('user_avatars', filename), os.listdir('media/user_avatars')))

        self.stdout.write('Generating users...')
        generated_users = []
        user_amount = random.randint(200, 300)
        for i in range(user_amount):
            password = self._randString()
            username = f'test user{i} {password}'
            user = User.objects.create_user(
                username=username,
                password=password,
                email=f'{password}@{random.choice(self.USER_EMAIL_PROVIDERS)}.invalid'
            )
            if self._randChance(0.8):
                user.avatar=random.choice(mock_user_avatars)
            if self._randChance(0.7):
                user.phone_number=self._randPhoneNumber()
                user.save()
            generated_users.append(user)

        self.stdout.write('Generating offers...')
        offer_amount = random.randint(1000, 1500)
        photo_amount_total = 0
        offer_name_prefix = self._randString()
        for i in range(offer_amount):
            house_number = random.randint(1, 50) if self._randChance(0.8) else None
            author = random.choice(generated_users)
            offer = Offer.objects.create(
                title=f'Offer {offer_name_prefix}_{i}',
                description=self._randString()*random.randint(5, 80) if self._randChance(0.9) else None,
                status=Offer.OfferStatus.ACTIVE if self._randChance(0.9) else Offer.OfferStatus.INACTIVE,
                category=random.choice(Offer.EstateType.choices)[0],
                type=random.choice(Offer.OfferType.choices)[0],
                square_meters=random.uniform(20.0, 1200.0) if self._randChance(0.5) else None,
                price=random.randint(40, 1100)*10 if self._randChance(0.9) else None,
                location_lat=random.uniform(49.3, 50.8),
                location_lng=random.uniform(19.1, 20.9),
                location_city_name=random.choice(self.OFFER_CITIES),
                location_street_name=random.choice(self.OFFER_STREETS) if self._randChance(0.9) else None,
                location_house_number=house_number,
                location_apt_number=random.choice(string.ascii_uppercase) if house_number is not None and self._randChance(0.2) else None,
                author=author,
                active_until=now()+timedelta(hours=random.randint(1, 72))
            )

            photo_amount = random.randint(0, 5)
            photo_amount_total += photo_amount
            for i in range(photo_amount):
                OfferPhoto.objects.create(
                    offer=offer,
                    photo=random.choice(mock_offer_photos)
                )

        self.stdout.write(f'Generated {user_amount} users and {offer_amount} offers with {photo_amount_total} photos')