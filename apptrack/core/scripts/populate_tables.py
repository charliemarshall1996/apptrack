import pandas as pd

from core.models import Country, Currency, JobFunction, PayRate


def populate_countries():
    print("Populating countries...")

    df = pd.read_csv("core/default_data/countries.csv")

    for _, row in df.iterrows():
        country, _ = Country.objects.get_or_create(
            alpha_2=row.alpha_2, name=row["name"]
        )
        country.save()


def populate_currencies():
    print("Populating currencies...")

    df = pd.read_csv("core/default_data/currencies.csv")

    for _, row in df.iterrows():
        currency, _ = Currency.objects.get_or_create(
            alpha_3=row.alpha_3, name=row["name"]
        )
        currency.save()


def populate_job_functions():
    print("Populating job functions...")

    df = pd.read_csv("core/default_data/job_functions.csv")

    for _, row in df.iterrows():
        job_function, _ = JobFunction.objects.get_or_create(
            code=row.code, name=row["name"]
        )
        job_function.save()


def populate_pay_rates():
    print("Populating pay rates...")

    df = pd.read_csv("core/default_data/pay_rates.csv")

    for _, row in df.iterrows():
        pay_rate, _ = PayRate.objects.get_or_create(code=row.code, name=row["name"])
        pay_rate.save()


def run():
    print("Populating tables...")
    populate_countries()
    populate_currencies()
    populate_job_functions()
    populate_pay_rates()
    print("Tables populated.")
