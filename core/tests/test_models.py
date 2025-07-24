import pytest
from core.models import Country, Currency


@pytest.mark.django_db
def test_country_model():
    alpha_2 = "uk"
    name = "United Kingdom"
    country = Country.objects.create(alpha_2=alpha_2, name=name)
    assert country.alpha_2 == alpha_2
    assert country.name == name
    assert str(country) == country.name


@pytest.mark.django_db
def test_currency_model():
    alpha_3 = "usd"
    name = "United States Dollar"
    currency = Currency.objects.create(alpha_3=alpha_3, name=name)
    assert currency.alpha_3 == alpha_3
    assert currency.name == name
    assert str(currency) == currency.name
