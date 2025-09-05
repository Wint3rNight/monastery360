"""
Django management command to load demo data for Monastery360.
This command creates comprehensive demo fixtures with authentic Sikkim monastery data.
"""

import json
import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

# from django.contrib.gis.geos import Point  # Disabled for demo
from django.utils import timezone
from django.utils.text import slugify

from archives.models import ArchiveItem
from bookings.models import Booking
from core.models import AudioPOI, Monastery
from events.models import Event
from tours.models import Panorama


class Command(BaseCommand):
    help = 'Load comprehensive demo data for Monastery360 with authentic Sikkim monasteries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading',
        )
        parser.add_argument(
            '--minimal',
            action='store_true',
            help='Load minimal dataset for testing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        if options['minimal']:
            self.stdout.write('Loading minimal demo data...')
            self.load_minimal_data()
        else:
            self.stdout.write('Loading comprehensive demo data...')
            self.load_comprehensive_data()

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded demo data!')
        )

    def clear_data(self):
        """Clear existing data"""
        models_to_clear = [
            Booking, Event, ArchiveItem, Panorama, AudioPOI, Monastery
        ]

        for model in models_to_clear:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f'Cleared {count} {model.__name__} objects')

    def load_minimal_data(self):
        """Load minimal dataset for testing"""
        # Create 3 key monasteries
        monasteries_data = self.get_key_monasteries_data()[:3]

        for monastery_data in monasteries_data:
            self.create_monastery(monastery_data)

    def load_comprehensive_data(self):
        """Load comprehensive demo dataset"""
        # Create all monasteries
        monasteries_data = self.get_key_monasteries_data()
        monasteries = []

        for monastery_data in monasteries_data:
            monastery = self.create_monastery(monastery_data)
            monasteries.append(monastery)

        # Create additional content for each monastery
        for monastery in monasteries:
            self.create_audio_pois(monastery)
            self.create_panoramas(monastery)
            self.create_archive_items(monastery)
            self.create_events(monastery)
            self.create_sample_bookings(monastery)

        self.stdout.write(f'Created {len(monasteries)} monasteries with full content')

    def get_key_monasteries_data(self):
        """Return authentic data for major Sikkim monasteries"""
        return [
            {
                'name': 'Rumtek Monastery',
                'local_name': 'རུམ་ཐེག་དགོན་པ།',
                'description': 'The Rumtek Monastery, also called the Dharmachakra Centre, is a gompa located in the Indian state of Sikkim near the capital Gangtok. It is the largest monastery in Sikkim and is the seat-in-exile of the Gyalwa Karmapa, inaugurated in 1966 by the 16th Karmapa. Built in the 1960s, it is modeled after the Karma Kagyu monastery of Tsurphu in Tibet.',
                'short_description': 'The largest monastery in Sikkim and seat-in-exile of the Gyalwa Karmapa',
                'monastery_type': 'kagyu',
                'established_year': 1966,
                'district': 'East Sikkim',
                'location_description': 'Rumtek, 24 km from Gangtok',
                'latitude': 27.3133,
                'longitude': 88.5478,
                'altitude': 1547,
                'monk_count': 300,
                'is_accessible': True,
                'visiting_hours_start': '06:00',
                'visiting_hours_end': '18:00',
                'entry_fee': Decimal('0.00'),
                'phone_number': '+91-3592-252023',
                'website': 'http://www.rumtek.org',
                'is_featured': True,
                'cultural_significance': 'Home to the Golden Stupa containing relics of the 16th Karmapa. Houses precious artifacts, thangkas, and the crown and robes of the Karmapa.',
                'architectural_style': 'Traditional Tibetan architecture with ornate decorations and golden roof',
                'festivals': 'Kagyu Monlam, Losar, Buddha Jayanti',
                'special_features': 'Golden Stupa, Prayer Wheels, Ancient Manuscripts, Monastic University'
            },
            {
                'name': 'Enchey Monastery',
                'local_name': 'ཨེན་ཅེ་དགོན་པ།',
                'description': 'Enchey Monastery is an important monastery of the Nyingma sect located in Gangtok, the capital city of Sikkim. Built in 1909, it was established by Lama Druptob Karpo, a famous Sikkimese mystic known for his flying powers. The monastery houses images of gods, goddesses, and other religious artifacts.',
                'short_description': 'Historic Nyingma monastery in Gangtok built by the famous flying lama',
                'monastery_type': 'nyingma',
                'established_year': 1909,
                'district': 'East Sikkim',
                'location_description': 'Gangtok, near TV Tower',
                'latitude': 27.3314,
                'longitude': 88.6138,
                'altitude': 1830,
                'monk_count': 90,
                'is_accessible': True,
                'visiting_hours_start': '05:30',
                'visiting_hours_end': '19:00',
                'entry_fee': Decimal('0.00'),
                'phone_number': '+91-3592-202123',
                'is_featured': True,
                'cultural_significance': 'Associated with Lama Druptob Karpo, known for miraculous flying abilities. Important center for Nyingma teachings.',
                'architectural_style': 'Traditional Sikkimese architecture with colorful murals and intricate woodwork',
                'festivals': 'Chaam Dance during Pang Lhabsol, Losar, Drupka Teshi',
                'special_features': 'Flying Lama Legend, Sacred Masks, Traditional Chaam Dance'
            },
            {
                'name': 'Tashiding Monastery',
                'local_name': 'བཀྲ་ཤིས་སྡིང་དགོན་པ།',
                'description': 'Tashiding Monastery is a Buddhist monastery of the Nyingma sect located on top of a hill between the Rathong and Rangeet rivers in Tashiding, Sikkim. Founded in 1641, it is one of the most sacred monasteries in Sikkim. The monastery is famous for its holy water (Bum Chu) ceremony during Losar.',
                'short_description': 'One of the most sacred Nyingma monasteries, famous for the holy water ceremony',
                'monastery_type': 'nyingma',
                'established_year': 1641,
                'district': 'West Sikkim',
                'location_description': 'Tashiding, between Rathong and Rangeet rivers',
                'latitude': 27.3472,
                'longitude': 88.2750,
                'altitude': 1465,
                'monk_count': 45,
                'is_accessible': False,
                'visiting_hours_start': '06:00',
                'visiting_hours_end': '17:00',
                'entry_fee': Decimal('10.00'),
                'phone_number': '+91-3595-242015',
                'is_featured': True,
                'cultural_significance': 'Center of the famous Bum Chu ceremony. Believed that a sip of holy water from here can wash away sins.',
                'architectural_style': 'Ancient Nyingma architecture with traditional Sikkimese elements',
                'festivals': 'Bum Chu Festival, Losar, Saga Dawa',
                'special_features': 'Holy Water Ceremony, Sacred Chortens, Ancient Texts'
            },
            {
                'name': 'Pemayangtse Monastery',
                'local_name': 'པད་མ་ཡང་རྩེ་དགོན་པ།',
                'description': 'Pemayangtse Monastery is a Buddhist monastery in Pemayangtse, near Pelling in the northeastern Indian state of Sikkim. Planned, designed and founded by Lama Lhatsun Chempo in 1705, it is one of the oldest and premier monasteries of Sikkim, also holding the distinction of being the head monastery of the Nyingma sect.',
                'short_description': 'Premier Nyingma monastery and one of the oldest in Sikkim',
                'monastery_type': 'nyingma',
                'established_year': 1705,
                'district': 'West Sikkim',
                'location_description': 'Pemayangtse, near Pelling',
                'latitude': 27.2956,
                'longitude': 88.2131,
                'altitude': 2085,
                'monk_count': 108,
                'is_accessible': True,
                'visiting_hours_start': '07:00',
                'visiting_hours_end': '17:00',
                'entry_fee': Decimal('5.00'),
                'phone_number': '+91-3595-250221',
                'is_featured': True,
                'cultural_significance': 'Head monastery of Nyingma sect in Sikkim. Only pure-blood Bhutias can become monks here.',
                'architectural_style': 'Three-storied traditional architecture with exquisite woodcarving',
                'festivals': 'Chaam Dance, Losar, Drupka Teshi',
                'special_features': 'Seven-tiered Wooden Sculpture, Ancient Murals, Monastery Museum'
            },
            {
                'name': 'Dubdi Monastery',
                'local_name': 'འདུབ་སྡེ་དགོན་པ།',
                'description': 'Dubdi Monastery, also known as Yuksom Monastery, is a Buddhist monastery of the Nyingma sect located near Yuksom in Sikkim. Built in 1701, it is the oldest monastery in Sikkim and holds great historical significance as it was here that the first Chogyal was crowned.',
                'short_description': 'The oldest monastery in Sikkim where the first Chogyal was crowned',
                'monastery_type': 'nyingma',
                'established_year': 1701,
                'district': 'West Sikkim',
                'location_description': 'Yuksom, trek from Yuksom village',
                'latitude': 27.3628,
                'longitude': 88.2297,
                'altitude': 2100,
                'monk_count': 25,
                'is_accessible': False,
                'visiting_hours_start': '06:00',
                'visiting_hours_end': '16:00',
                'entry_fee': Decimal('20.00'),
                'is_featured': False,
                'cultural_significance': 'Coronation site of first Chogyal. Oldest monastery in Sikkim with immense historical importance.',
                'architectural_style': 'Ancient Sikkimese architecture in pristine mountain setting',
                'festivals': 'Coronation Day, Losar, Local festivals',
                'special_features': 'Historical Coronation Site, Meditation Caves, Ancient Artifacts'
            },
            {
                'name': 'Ralang Monastery',
                'local_name': 'རབ་གླིང་དགོན་པ།',
                'description': 'Ralang Monastery is a Buddhist monastery of the Kagyu sect in South Sikkim, built in 1730. It is famous for its annual Pang Lhabsol festival and houses several ancient relics and manuscripts. The monastery offers stunning views of Mount Kanchenjunga.',
                'short_description': 'Historic Kagyu monastery famous for Pang Lhabsol festival',
                'monastery_type': 'kagyu',
                'established_year': 1730,
                'district': 'South Sikkim',
                'location_description': 'Ralang, 6 km from Ravangla',
                'latitude': 27.2889,
                'longitude': 88.4167,
                'altitude': 1200,
                'monk_count': 60,
                'is_accessible': True,
                'visiting_hours_start': '06:00',
                'visiting_hours_end': '18:00',
                'entry_fee': Decimal('0.00'),
                'is_featured': False,
                'cultural_significance': 'Center for Pang Lhabsol festival celebrating Mount Kanchenjunga. Houses ancient Kagyu texts.',
                'architectural_style': 'Traditional Kagyu architecture with mountain views',
                'festivals': 'Pang Lhabsol, Kagyu Monlam, Buddha Purnima',
                'special_features': 'Kanchenjunga Views, Ancient Manuscripts, Festival Grounds'
            },
            {
                'name': 'Phensang Monastery',
                'local_name': 'ཕན་བསམ་དགོན་པ།',
                'description': 'Phensang Monastery is a Nyingma monastery located in North Sikkim. Founded in the 17th century, it is known for its remote location and pristine mountain environment. The monastery serves as an important meditation retreat center.',
                'short_description': 'Remote Nyingma monastery serving as a meditation retreat center',
                'monastery_type': 'nyingma',
                'established_year': 1640,
                'district': 'North Sikkim',
                'location_description': 'Lachen Valley, North Sikkim',
                'latitude': 27.6833,
                'longitude': 88.5333,
                'altitude': 2800,
                'monk_count': 35,
                'is_accessible': False,
                'visiting_hours_start': '07:00',
                'visiting_hours_end': '16:00',
                'entry_fee': Decimal('15.00'),
                'is_featured': False,
                'cultural_significance': 'Important meditation center in remote Himalayan setting. Preserves ancient Nyingma traditions.',
                'architectural_style': 'Simple mountain architecture adapted to harsh climate',
                'festivals': 'Local Nyingma festivals, Meditation retreats',
                'special_features': 'Meditation Caves, Alpine Setting, Traditional Retreats'
            },
            {
                'name': 'Sanga Choeling Monastery',
                'local_name': 'གསང་སྔགས་ཆོས་གླིང་དགོན་པ།',
                'description': 'Sanga Choeling Monastery is one of the oldest monasteries in Sikkim, built in 1697. Located on a ridge above Pelling, it offers panoramic views of the Himalayas including Kanchenjunga. The monastery is reached by a moderate trek through beautiful forests.',
                'short_description': 'One of Sikkim\'s oldest monasteries with panoramic Himalayan views',
                'monastery_type': 'nyingma',
                'established_year': 1697,
                'district': 'West Sikkim',
                'location_description': 'Ridge above Pelling, 30-minute trek',
                'latitude': 27.3167,
                'longitude': 88.2167,
                'altitude': 2100,
                'monk_count': 40,
                'is_accessible': False,
                'visiting_hours_start': '06:00',
                'visiting_hours_end': '17:00',
                'entry_fee': Decimal('10.00'),
                'is_featured': False,
                'cultural_significance': 'Among the oldest monasteries. Offers spectacular mountain vistas and spiritual solitude.',
                'architectural_style': 'Traditional ridge-top architecture with panoramic design',
                'festivals': 'Mountain festivals, Seasonal celebrations',
                'special_features': 'Himalayan Panorama, Forest Trek, Meditation Spots'
            }
        ]

    def create_monastery(self, data):
        """Create a monastery with all its data"""
        monastery = Monastery.objects.create(
            name=data['name'],
            slug=slugify(data['name']),
            description=data['description'],
            short_description=data['short_description'],
            established_year=data.get('established_year'),
            district=data['district'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data.get('address', data['district']),
            altitude=data.get('altitude'),
            phone=data.get('phone_number', ''),
            website=data.get('website', ''),
            is_featured=data.get('is_featured', False),
            is_active=True,
        )

        self.stdout.write(f'Created monastery: {monastery.name}')
        return monastery

    def create_audio_pois(self, monastery):
        """Create audio points of interest for a monastery"""
        audio_pois_data = [
            {
                'title': 'Main Entrance',
                'description': 'Welcome to the sacred grounds. Listen to the history and significance of this entrance.',
                'audio_text': f'Welcome to {monastery.name}. This sacred entrance has welcomed pilgrims for centuries...',
                'order': 1,
            },
            {
                'title': 'Prayer Hall',
                'description': 'Experience the main prayer hall where monks gather for daily prayers.',
                'audio_text': 'The main prayer hall is the heart of monastic life. Here, monks gather at dawn and dusk...',
                'order': 2,
            },
            {
                'title': 'Buddha Statue',
                'description': 'Learn about the magnificent Buddha statue and its spiritual significance.',
                'audio_text': 'This ancient Buddha statue represents the enlightened mind. Crafted with devotion...',
                'order': 3,
            },
            {
                'title': 'Prayer Wheels',
                'description': 'Discover the meaning behind the spinning prayer wheels.',
                'audio_text': 'Each turn of these prayer wheels sends mantras into the universe, creating merit...',
                'order': 4,
            },
        ]

        for i, poi_data in enumerate(audio_pois_data, 1):
            # Create location near monastery with slight offset
            lat_offset = random.uniform(-0.001, 0.001)
            lng_offset = random.uniform(-0.001, 0.001)

            AudioPOI.objects.create(
                monastery=monastery,
                title=poi_data['title'],
                description=poi_data['description'],
                latitude=monastery.latitude + lat_offset,
                longitude=monastery.longitude + lng_offset,
                audio_transcript=poi_data['audio_text'],
                audio_duration=random.randint(60, 180),
                order=poi_data['order'],
                is_active=True,
            )

        self.stdout.write(f'Created {len(audio_pois_data)} audio POIs for {monastery.name}')

    def create_panoramas(self, monastery):
        """Create panoramic tours for a monastery"""
        panoramas_data = [
            {
                'title': f'{monastery.name} - Main View',
                'description': 'Panoramic view of the main monastery complex',
                'scene_type': 'main_hall',
            },
            {
                'title': f'{monastery.name} - Courtyard',
                'description': 'Central courtyard where ceremonies take place',
                'scene_type': 'courtyard',
            },
            {
                'title': f'{monastery.name} - Prayer Wheels',
                'description': 'Traditional prayer wheels area',
                'scene_type': 'prayer_area',
            },
        ]

        for i, pano_data in enumerate(panoramas_data, 1):
            # Sample hotspots data
            hotspots_data = [
                {
                    'id': f'hotspot_{i}_1',
                    'pitch': random.randint(-20, 20),
                    'yaw': random.randint(0, 360),
                    'type': 'info',
                    'text': f'Learn about this sacred area of {monastery.name}',
                },
                {
                    'id': f'hotspot_{i}_2',
                    'pitch': random.randint(-20, 20),
                    'yaw': random.randint(0, 360),
                    'type': 'info',
                    'text': 'Historical significance of this location',
                },
            ]

            Panorama.objects.create(
                monastery=monastery,
                title=pano_data['title'],
                description=pano_data['description'],
                location_name=pano_data.get('scene_type', 'Main Area'),
                hotspots_data=hotspots_data,
                order=i,
                is_active=True,
            )

        self.stdout.write(f'Created {len(panoramas_data)} panoramas for {monastery.name}')

    def create_archive_items(self, monastery):
        """Create digital archive items for a monastery"""
        archive_items_data = [
            {
                'title': f'Ancient Manuscript from {monastery.name}',
                'description': 'Buddhist text written in traditional Tibetan script',
                'item_type': 'manuscript',
                'material': 'paper',
                'condition': 'fair',
                'cultural_significance': 'Contains rare Buddhist teachings and historical records',
            },
            {
                'title': f'Ritual Mask from {monastery.name}',
                'description': 'Traditional Cham dance mask used in ceremonies',
                'item_type': 'artifact',
                'material': 'wood',
                'condition': 'good',
                'cultural_significance': 'Used in sacred Cham dances during festivals',
            },
            {
                'title': f'Historical Photograph - {monastery.name} 1950s',
                'description': 'Rare photograph showing the monastery in the 1950s',
                'item_type': 'photograph',
                'material': 'paper',
                'condition': 'excellent',
                'cultural_significance': 'Documents historical changes and preservation efforts',
            },
            {
                'title': f'Prayer Flag from {monastery.name}',
                'description': 'Traditional prayer flag with mantras and symbols',
                'item_type': 'textile',
                'material': 'cloth',
                'condition': 'poor',
                'cultural_significance': 'Carries prayers and blessings in the wind',
            },
        ]

        for i, item_data in enumerate(archive_items_data):
            ArchiveItem.objects.create(
                monastery=monastery,
                title=item_data['title'],
                description=item_data['description'],
                item_type=item_data['item_type'],
                material=item_data['material'],
                condition=item_data['condition'],
                cultural_significance=item_data['cultural_significance'],
                catalog_number=f"{monastery.slug.upper()}-{item_data['item_type'].upper()}-{i+1:03d}",
                acquisition_date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                is_public=True,
            )

        self.stdout.write(f'Created {len(archive_items_data)} archive items for {monastery.name}')

    def create_events(self, monastery):
        """Create events for a monastery"""
        base_date = timezone.now()

        events_data = [
            {
                'title': f'Morning Prayer Session at {monastery.name}',
                'description': 'Join the monks for their daily morning prayers and meditation',
                'event_type': 'prayer',
                'days_offset': 1,
                'duration_hours': 2,
                'max_participants': 50,
                'is_featured': True,
            },
            {
                'title': f'Buddhist Philosophy Talk at {monastery.name}',
                'description': 'Learn about Buddhist teachings from senior monks',
                'event_type': 'education',
                'days_offset': 7,
                'duration_hours': 3,
                'max_participants': 30,
                'is_featured': False,
            },
            {
                'title': f'Meditation Retreat at {monastery.name}',
                'description': 'Weekend meditation retreat for beginners and advanced practitioners',
                'event_type': 'retreat',
                'days_offset': 14,
                'duration_hours': 48,
                'max_participants': 20,
                'is_featured': True,
            },
            {
                'title': f'Cultural Festival at {monastery.name}',
                'description': 'Annual cultural festival with traditional dances and ceremonies',
                'event_type': 'festival',
                'days_offset': 30,
                'duration_hours': 8,
                'max_participants': 200,
                'is_featured': True,
            },
        ]

        for event_data in events_data:
            start_time = base_date + timedelta(days=event_data['days_offset'])
            end_time = start_time + timedelta(hours=event_data['duration_hours'])

            Event.objects.create(
                monastery=monastery,
                title=event_data['title'],
                description=event_data['description'],
                event_type=event_data['event_type'],
                start_time=start_time,
                end_time=end_time,
                max_participants=event_data['max_participants'],
                requires_registration=True,
                is_featured=event_data['is_featured'],
                is_public=True,
            )

        self.stdout.write(f'Created {len(events_data)} events for {monastery.name}')

    def create_sample_bookings(self, monastery):
        """Create sample bookings for testing"""
        # Create some past and future bookings
        base_date = timezone.now()

        bookings_data = [
            {
                'visitor_name': 'John Smith',
                'visitor_email': 'john.smith@email.com',
                'visitor_phone': '+91-9876543210',
                'visit_date': base_date + timedelta(days=3),
                'group_size': 2,
                'purpose': 'tourism',
                'status': 'confirmed',
            },
            {
                'visitor_name': 'Maria Garcia',
                'visitor_email': 'maria.garcia@email.com',
                'visitor_phone': '+91-9876543211',
                'visit_date': base_date + timedelta(days=10),
                'group_size': 4,
                'purpose': 'spiritual',
                'status': 'pending',
            },
            {
                'visitor_name': 'David Chen',
                'visitor_email': 'david.chen@email.com',
                'visitor_phone': '+91-9876543212',
                'visit_date': base_date - timedelta(days=5),
                'group_size': 1,
                'purpose': 'research',
                'status': 'completed',
            },
        ]

        for booking_data in bookings_data:
            Booking.objects.create(
                monastery=monastery,
                name=booking_data['visitor_name'],
                email=booking_data['visitor_email'],
                phone=booking_data['visitor_phone'],
                visit_date=booking_data['visit_date'],
                number_of_visitors=booking_data['group_size'],
                purpose_of_visit=booking_data['purpose'],
                status=booking_data['status'],
            )

        self.stdout.write(f'Created {len(bookings_data)} sample bookings for {monastery.name}')
