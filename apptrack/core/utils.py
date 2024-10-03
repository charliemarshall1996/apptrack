import unicodedata
import pycountry

def normalize_country_name(name):
        return ''.join(
            c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn'
        ).strip()

def get_country_choices():
        country_choices = []
        countries = list(pycountry.countries)

        country_choices = [(country.alpha_2, normalize_country_name(country.name)) for country in countries]
        
        return sorted(country_choices, key=lambda x: x[1])

def get_currency_choices():
        currency_choices = []
        currencies = list(pycountry.currencies)

        currency_choices = [(currency.alpha_3, currency.name) for currency in currencies]
        
        return sorted(currency_choices, key=lambda x: x[1])