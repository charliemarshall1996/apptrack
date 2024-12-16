from django.test import TestCase
from django.apps import apps
from core.models import Country, Currency
from core.signals import post_migrate
from core.utils import get_country_choices, get_currency_choices


class PostMigrateSignalTest(TestCase):
    def test_post_migrate_creates_countries_and_currencies(self):
        # Clear existing data to ensure a clean test environment
        Country.objects.all().delete()
        Currency.objects.all().delete()

        # Trigger the signal manually
        sender = apps.get_app_config('core')
        post_migrate(sender=sender, instance=None)

        # Assert that countries were created
        country_choices = get_country_choices()
        self.assertEqual(Country.objects.count(), len(country_choices))
        for alpha_2, country_name in country_choices:
            self.assertTrue(Country.objects.filter(
                alpha_2=alpha_2, name=country_name).exists())

        # Assert that currencies were created
        currency_choices = get_currency_choices()
        self.assertEqual(Currency.objects.count(), len(currency_choices))
        for alpha_3, currency_name in currency_choices:
            self.assertTrue(Currency.objects.filter(
                alpha_3=alpha_3, name=currency_name).exists())
