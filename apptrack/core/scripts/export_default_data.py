
import pandas as pd

from core.choices import (
    get_currency_choices,
    get_country_choices,
    JobFunctionChoices,
    PayRateChoices,
    SourceChoices,
    StatusChoices
)


def export_country_data():
    print("Exporting country data...")

    data = []
    for alpha_2, name in get_country_choices():
        data.append({'alpha_2': alpha_2, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/countries.csv", index=False)


def export_currency_data():
    print("Exporting currency data...")

    data = []
    for alpha_3, name in get_currency_choices():
        data.append({'alpha_3': alpha_3, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/currencies.csv", index=False)


def export_job_function_data():
    print("Exporting job function data...")

    data = []
    for code, name in JobFunctionChoices.choices():
        data.append({'code': code, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/job_functions.csv", index=False)


def export_pay_rate_data():
    print("Exporting pay rate data...")

    data = []
    for code, name in PayRateChoices.choices():
        data.append({'code': code, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/pay_rates.csv", index=False)


def export_source_data():
    print("Exporting source data...")

    data = []
    for code, name in SourceChoices.choices():
        data.append({'code': code, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/sources.csv", index=False)


def export_status_data():
    print("Exporting status data...")

    data = []
    for code, name in StatusChoices.choices():
        data.append({'code': code, 'name': name})

    df = pd.DataFrame(data)
    df.to_csv("core/default_data/statuses.csv", index=False)


def run():
    print("Exporting default data...")
    export_country_data()
    export_currency_data()
    export_job_function_data()
    export_pay_rate_data()
    export_source_data()
    export_status_data()
    print("Default data exported.")
