from django.core.management.base import BaseCommand
from vendor.models import Category


class Command(BaseCommand):
    help = 'Seed database with product categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Electronics',
                'description': 'Mobile phones, laptops, cameras, and other electronic devices',
                'icon': 'fas fa-laptop'
            },
            {
                'name': 'Clothing & Fashion',
                'description': 'Men, women, and kids clothing, shoes, and accessories',
                'icon': 'fas fa-shirt'
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Kitchen appliances, home decor, and furniture',
                'icon': 'fas fa-home'
            },
            {
                'name': 'Beauty & Personal Care',
                'description': 'Cosmetics, skincare, haircare, and grooming products',
                'icon': 'fas fa-spa'
            },
            {
                'name': 'Books & Media',
                'description': 'Books, ebooks, audiobooks, and educational materials',
                'icon': 'fas fa-book'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment, workout gear, and outdoor activities',
                'icon': 'fas fa-dumbbell'
            },
            {
                'name': 'Toys & Games',
                'description': 'Toys, board games, and games for all ages',
                'icon': 'fas fa-gamepad'
            },
            {
                'name': 'Health & Wellness',
                'description': 'Supplements, fitness trackers, and health products',
                'icon': 'fas fa-heartbeat'
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, tools, and automotive products',
                'icon': 'fas fa-car'
            },
            {
                'name': 'Groceries & Food',
                'description': 'Fresh produce, packaged food, and beverages',
                'icon': 'fas fa-shopping-basket'
            },
            {
                'name': 'Pet Supplies',
                'description': 'Pet food, toys, and pet care products',
                'icon': 'fas fa-paw'
            },
            {
                'name': 'Office Supplies',
                'description': 'Stationery, office equipment, and work materials',
                'icon': 'fas fa-pen'
            },
        ]

        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'~ Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Seeding complete! {created_count} new categories created.')
        )
