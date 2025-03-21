# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import requests
from rasa_sdk import Action

class ActionGetCoinPrice(Action):
    def name(self):
        return "action_get_coin_price"

    def run(self, dispatcher, tracker, domain):
        coin = next(tracker.get_latest_entity_values("cryptocurrency"), None)

        if not coin:
            dispatcher.utter_message(text="Please specify which cryptocurrency you want the price for.")
            return []

        coin = coin.lower()

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if coin in data:
                price = data[coin]["usd"]
                dispatcher.utter_message(text=f"The current price of {coin.capitalize()} is ${price:.2f} USD.")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the price for {coin}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the price at the moment. Please try again later.")

        return []

class ActionGetCurrencyPrice(Action):
    def name(self):
        return "action_get_currency_price"

    def run(self, dispatcher, tracker, domain):
        base_currency = next(tracker.get_latest_entity_values("fiat_currency"), None)
        target_currency = "USD"  # Default target currency is USD

        if not base_currency:
            dispatcher.utter_message(text="Please specify the currency you want to convert.")
            return []

        base_currency = base_currency.upper()

        # Fetch exchange rate from CurrencyFreaks API
        API_KEY = "822306c265854c0e80b66a26316a4bbd"
        url = f"https://api.currencyfreaks.com/latest?apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})

            if target_currency in rates and base_currency in rates:
                rate = float(rates[target_currency]) / float(rates[base_currency])
                dispatcher.utter_message(text=f"1 {base_currency} is equal to {rate:.2f} {target_currency}.")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the exchange rate for {base_currency}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the exchange rate at the moment. Please try again later.")

        return []
