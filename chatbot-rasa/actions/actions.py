from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionConvertCurrency(Action):
    def name(self) -> Text:
        return "action_convert_currency"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        src_currency = str(tracker.get_slot("src_currency")).upper()
        des_currency = str(tracker.get_slot("des_currency")).upper()
        amount = tracker.get_slot("amount")

        conversion_found = False
        src_crypto = False
        # First check if the result is available in the currency convertion (In case both are currencies not cryptos)
        api_key = "e61686068c8b2aff51c8519f"
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{src_currency}")
        data = response.json()
        if "conversion_rates" in data:
            if des_currency in data["conversion_rates"]:
                conversion_rate = data["conversion_rates"][des_currency]
                conversion_found = True
            else:
                src_crypto = False
        else:
            src_crypto = True

        # This means that on of the src or des is a crpto not a ordinary cusrrency
        if not conversion_found:
            api_key = "72c440762a98d30f084591df24b14332"
            response = requests.get("http://api.coinlayer.com/api/live", params={
                "access_key" : api_key,
            })
            data = response.json()
            if src_crypto:
                crypto_currency = src_currency
                des_currency = "USD"
            else:
                crypto_currency = des_currency
                src_currency = "USD"
            conversion_rate = data["rates"][crypto_currency]

        converted_amount = amount * conversion_rate
        dispatcher.utter_message(
            f"The conversion rate from {src_currency} to {des_currency} is {conversion_rate}. {amount} {src_currency} equals {converted_amount} {des_currency}."
        )
        return []
    



