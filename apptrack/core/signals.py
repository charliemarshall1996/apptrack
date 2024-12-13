
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .apps import CoreConfig
from .models import Country, Currency
from .utils import get_country_choices, get_currency_choices


@receiver(post_migrate, sender=CoreConfig)
def post_migrate(sender, instance, *args, **kwargs):
    for alpha_2, country in get_country_choices():
        Country.objects.get_or_create(alpha_2=alpha_2, name=country)

    for alpha_3, currency in get_currency_choices():
        Currency.objects.get_or_create(alpha_3=alpha_3, name=currency)
