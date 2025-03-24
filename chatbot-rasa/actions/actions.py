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
        src_currency = tracker.get_slot("src_currency")
        des_currency = tracker.get_slot("des_currency")
        amount = tracker.get_slot("amount")

        api_key = "e61686068c8b2aff51c8519f"
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{src_currency}")
        data = response.json()
        conversion_rate = data["conversion_rates"][des_currency]

        converted_amount = amount * conversion_rate
        dispatcher.utter_message(
            f"The conversion rate from {src_currency} to {des_currency} is {conversion_rate}. {amount} {src_currency} equals {converted_amount} {des_currency}."
        )
        # return [SlotSet("conversion_rate", conversion_rate), SlotSet("converted_amount", converted_amount)]
        return []
