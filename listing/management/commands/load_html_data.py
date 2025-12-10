from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from listing.models import Category, Amenities


class Command(BaseCommand):
	help = 'Load prefilled data (categories, subcategories, amenities) into the database'

	def add_arguments(self, parser):
		parser.add_argument(
			'--dry-run',
			action='store_true',
			help='Preview changes without saving to database',
		)
		parser.add_argument(
			'--verbose',
			action='store_true',
			help='Show detailed output',
		)
		parser.add_argument(
			'--skip-existing',
			action='store_true',
			default=True,
			help='Skip existing records (default: True)',
		)

	def handle(self, *args, **options):
		self.dry_run = options['dry_run']
		self.verbose = options['verbose']
		self.skip_existing = options['skip_existing']

		self.stdout.write(self.style.SUCCESS('Starting data loading...'))

		# Define categories data extracted from HTML files
		categories_data = self.get_categories_data()

		# Define amenities data extracted from HTML files
		amenities_data = self.get_amenities_data()

		if self.dry_run:
			self.stdout.write(self.style.WARNING('\n=== DRY RUN MODE - No changes will be saved ===\n'))

		# Load categories
		category_stats = self.load_categories(categories_data)

		# Load amenities
		amenity_stats = self.load_amenities(amenities_data)

		# Print summary
		self.print_summary(category_stats, amenity_stats)

	def get_categories_data(self):
		"""Return categories data extracted from HTML template files"""
		return {
			'main': {
				'homes': 'HOMES',
				'plots': 'LAND/PLOTS',
				'commercial': 'COMMERCIAL',
				'room': 'ROOM',
				'other': 'OTHER',
			},
			'subcategories': {
				'homes': [
					'House',
					'Upper Portion',
					'Lower Portion',
					'Penthouse',
					'Flat/Appartment',
				],
				'plots': [
					'Residential Plot',
					'Agricultural Plot',
					'Commercial Plot',
					'Industrial Land',
					'Plot File',
					'Plot Form',
				],
				'commercial': [
					'Office',
					'Shop',
					'Warehouse',
					'Factory',
					'Building',
				],
			}
		}

	def get_amenities_data(self):
		"""Return amenities data extracted from HTML template files"""
		return [
			# Home amenities
			'Servant Quarter',
			'Drawing Room',
			'Dining Room',
			'Kitchen',
			'Study Room',
			'Prayer Room',
			'Powder Room',
			'Gym',
			'Store Room',
			'Steam Room',
			'Lounge or Sitting Room',
			'Garage',
			'Laundry Room',
			# Plot amenities
			'Corner Plot',
			'Park Facing',
			'Disputed',
			'Sewerage',
			'Electricity',
			'Water Supply',
			'Gas Supply',
			'Boundary Wall',
			# Commercial amenities
			'Parking Spaces Available',
			'Lobby in Building',
			'Double Gazed Windows',
			'Central Air Conditioning',
			'Central Heating',
			'Electricity Backup',
			'Waste Disposal',
			'Elevators',
		]

	@transaction.atomic
	def load_categories(self, categories_data):
		"""Load categories and subcategories into database"""
		stats = {
			'created': 0,
			'skipped': 0,
			'errors': 0
		}

		# Create main categories
		main_categories = {}
		for slug, name in categories_data['main'].items():
			try:
				if self.skip_existing and Category.objects.filter(slug=slug).exists():
					if self.verbose:
						self.stdout.write(self.style.WARNING(f'Skipping existing category: {name} ({slug})'))
					stats['skipped'] += 1
					main_categories[slug] = Category.objects.get(slug=slug)
				else:
					if not self.dry_run:
						# Ensure slug is set (Category.save() has a bug referencing self.title)
						category = Category(name=name, slug=slug, parent=None)
						category.save()
						main_categories[slug] = category
						stats['created'] += 1
						if self.verbose:
							self.stdout.write(self.style.SUCCESS(f'Created main category: {name} ({slug})'))
					else:
						stats['created'] += 1
						if self.verbose:
							self.stdout.write(self.style.SUCCESS(f'[DRY RUN] Would create main category: {name} ({slug})'))
			except Exception as e:
				stats['errors'] += 1
				self.stdout.write(self.style.ERROR(f'Error creating category {name}: {str(e)}'))

		# Create subcategories
		for parent_slug, subcategory_names in categories_data['subcategories'].items():
			if parent_slug not in main_categories:
				if self.verbose:
					self.stdout.write(self.style.WARNING(f'Parent category {parent_slug} not found, skipping subcategories'))
				continue

			parent_category = main_categories[parent_slug]
			for sub_name in subcategory_names:
				try:
					sub_slug = slugify(sub_name)
					if self.skip_existing and Category.objects.filter(slug=sub_slug).exists():
						if self.verbose:
							self.stdout.write(self.style.WARNING(f'Skipping existing subcategory: {sub_name} ({sub_slug})'))
						stats['skipped'] += 1
					else:
						if not self.dry_run:
							# Ensure slug is set (Category.save() has a bug referencing self.title)
							subcategory = Category(name=sub_name, slug=sub_slug, parent=parent_category)
							subcategory.save()
							stats['created'] += 1
							if self.verbose:
								self.stdout.write(self.style.SUCCESS(f'Created subcategory: {sub_name} ({sub_slug}) under {parent_category.name}'))
						else:
							stats['created'] += 1
							if self.verbose:
								self.stdout.write(self.style.SUCCESS(f'[DRY RUN] Would create subcategory: {sub_name} ({sub_slug}) under {parent_category.name}'))
				except Exception as e:
					stats['errors'] += 1
					self.stdout.write(self.style.ERROR(f'Error creating subcategory {sub_name}: {str(e)}'))

		return stats

	@transaction.atomic
	def load_amenities(self, amenities_data):
		"""Load amenities into database"""
		stats = {
			'created': 0,
			'skipped': 0,
			'errors': 0
		}

		for amenity_name in amenities_data:
			try:
				if self.skip_existing and Amenities.objects.filter(feature=amenity_name).exists():
					if self.verbose:
						self.stdout.write(self.style.WARNING(f'Skipping existing amenity: {amenity_name}'))
					stats['skipped'] += 1
				else:
					if not self.dry_run:
						Amenities.objects.create(feature=amenity_name)
						stats['created'] += 1
						if self.verbose:
							self.stdout.write(self.style.SUCCESS(f'Created amenity: {amenity_name}'))
					else:
						stats['created'] += 1
						if self.verbose:
							self.stdout.write(self.style.SUCCESS(f'[DRY RUN] Would create amenity: {amenity_name}'))
			except Exception as e:
				stats['errors'] += 1
				self.stdout.write(self.style.ERROR(f'Error creating amenity {amenity_name}: {str(e)}'))

		return stats

	def print_summary(self, category_stats, amenity_stats):
		"""Print summary of operations"""
		self.stdout.write(self.style.SUCCESS('\n=== SUMMARY ==='))
		self.stdout.write(f'\nCategories:')
		self.stdout.write(f'  Created: {category_stats["created"]}')
		self.stdout.write(f'  Skipped: {category_stats["skipped"]}')
		self.stdout.write(f'  Errors: {category_stats["errors"]}')

		self.stdout.write(f'\nAmenities:')
		self.stdout.write(f'  Created: {amenity_stats["created"]}')
		self.stdout.write(f'  Skipped: {amenity_stats["skipped"]}')
		self.stdout.write(f'  Errors: {amenity_stats["errors"]}')

		total_created = category_stats['created'] + amenity_stats['created']
		total_skipped = category_stats['skipped'] + amenity_stats['skipped']
		total_errors = category_stats['errors'] + amenity_stats['errors']

		self.stdout.write(f'\nTotal:')
		self.stdout.write(f'  Created: {total_created}')
		self.stdout.write(f'  Skipped: {total_skipped}')
		self.stdout.write(f'  Errors: {total_errors}')

		if self.dry_run:
			self.stdout.write(self.style.WARNING('\nThis was a DRY RUN - no changes were saved to the database.'))
