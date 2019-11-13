import requests
from cachetools import cached, TTLCache


class OpenExchange:
    BASE_URL = "https://openexchangerates.org/api"
    latest = f"{BASE_URL}/latest.json?app_id="
    usage = f"{BASE_URL}/usage.json?app_id="
    currencies = f"{BASE_URL}/currencies.json"

    def __init__(self, app_id):
        self.app_id = app_id

    @property
    @cached(cache=TTLCache(maxsize=2, ttl=900))
    def get_data(self):
        data = requests.get(f"{self.latest}{self.app_id}").json()
        return data

    def convert(self, amount, input_currency, output_currency):
        data = self.get_data['rates']
        input_rate = data[input_currency]
        output_rate = data[output_currency]

        if input_currency == 'USD':
            output_amount = amount*output_rate
        else:
            convert_to_USD = amount / input_rate
            output_amount = convert_to_USD * output_rate

        final_output = str(round(output_amount,2))
        return final_output

    def get_usage(self):
        data = requests.get(f"{self.usage}{self.app_id}").json()
        stats = data["data"]["usage"]

        completed_request = stats["requests"]
        remaining_request = stats["requests_remaining"]
        days_elapsed = stats["days_elapsed"]
        daily_average = stats["daily_average"]

        return completed_request, remaining_request, days_elapsed, daily_average

    def get_all_currencies(self):
        data = requests.get(f"{self.currencies}").json()
        currencies = [f"{key} ({data[key]})" for key in data]

        return currencies
