from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProvidePrograms(Action):
    def name(self) -> Text:
        return "action_provide_programs"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "BSBI offers bachelor's and master's programs, including Business Administration, Digital Marketing, "
            "International Business Management, and Data Analytics."
        )
        return []

class ActionProvideProgramsBasedOnType(Action):
    def name(self) -> Text:
        return "action_provide_programs_based_on_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program_type = tracker.get_slot("program_type")

        bsc_programs = [
            "BSc in Business Administration",
            "BSc in Marketing & Digital Business",
            "BSc in Data Science",
        ]

        msc_programs = [
            "MSc in International Business Management",
            "MSc in Finance & Investment",
            "MSc in Digital Marketing & Analytics",
        ]

        print(f"\n\nPROGRAM_TYPE: {program_type}\n\n")
        if program_type:
            if "bsc" in program_type.lower():
                message = f"Here are some Bachelor's programs (BSc):\n- " + "\n- ".join(bsc_programs)
            elif "msc" in program_type.lower():
                message = f"Here are some Master's programs (MSc):\n- " + "\n- ".join(msc_programs)
            else:
                message = "I couldn't recognize the program type. Please specify BSc or MSc."
        else:
            message = "Would you like to see Bachelor's (BSc) or Master's (MSc) programs?"

        dispatcher.utter_message(text=message)
        return []

class ActionProvideFees(Action):
    def name(self) -> Text:
        return "action_provide_fees"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "The tuition fees vary by program. A bachelor's degree costs around €8,000 - €10,000 per year, "
            "and a master's degree costs around €11,000 - €13,000 per year."
        )
        return []

class ActionProvideAdmissionInfo(Action):
    def name(self) -> Text:
        return "action_provide_admission_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "The admission process includes submitting an application, proof of English proficiency, and academic qualifications. "
            "Some programs may require additional documents or an interview."
        )
        return []
