import requests

class OpenExchangeClient:
    BASE_URL = "https://openexchangerates.org/api/"

    def __init__(self, app_id):
        self.app_id = app_id

    @property
    def latest(self):
        return requests.get(f"{self.BASE_URL}/latest.json?app_id={self.app_id}").json()

    def convert(self, from_amount, from_currency, to_currency):
        rates = self.latest['rates']
        to_rate = rates[to_currency]

        if from_currency == 'USD':
            return from_amount * to_rate
        else:
            from_in_usd = from_amount / rates[from_currency]
            return from_in_usd * to_rate

APP_ID = "8812fb8e3ec9476e8a164b511b20236c"

test = OpenExchangeClient(APP_ID)

print(test.convert(100, "USD", "GBP"))
print(test.convert(100,"GBP", "MYR"))