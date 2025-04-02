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
            "BA (Hons) Photography",
            "BA (Hons) Comic and Concept Art",
            "BA (Hons) Game Design",
            "BSc in Psychology - Psychosocial Disciplines (UNINETTUNO)",
            "BSc (Hons) International Business and Management",
            "BA in Economics and Business Administration (UNINETTUNO)",
            "BA (Hons) Tourism and Hospitality Management",
            "BA (Hons) Animation",
            "BA (Hons) Graphic Design (UCA)",
            "BSc (Hons) Computer Science and Digitisation (UCA)",
        ]

        msc_programs = [
            "MA in Fashion and Luxury Brand Management",
            "MBA in Maritime and Shipping Management",
            "MSc Global Logistics and Supply Chain Management",
            "MSc Global Human Resources Management",
            "MSc Project Management",
            "MA User Experience Design",
            "MA Photography",
            "MA Game Design",
            "MSc in Sports Management (UCA)",
            "MSc Artificial Intelligence (UCA)",
            "MSc in Real Estate and Asset Management (UCA)",
            "Global MBA (UNINETTUNO)",
            "MSc in International Health Management (UNINETTUNO)",
            "MA in Finance and Investments (UNINETTUNO)",
            "MBA (CUC)",
            "MSc Digital Marketing",
            "MA in International Tourism, Hospitality and Event Management (UNINETTUNO)",
            "MA in Energy Management (UNINETTUNO)",
            "MA in Innovation and Entrepreneurship (CUC)",
            "MA Tourism, Hospitality and Event Management",
            "Global MBA",
            "MA in Strategic Marketing (UNINETTUNO)",
            "MSc Finance & Investment",
            "MA Visual Communication (UCA)",
            "MSc in Engineering Management (UNINETTUNO)",
            "MA in Logistics (UNINETTUNO)",
            "MSc Information Technology Management",
            "MSc Data Analytics (UCA)",
            "Master in Psychological Science (UNINETTUNO)",
        ]

        if program_type:
            if "bsc" in program_type.lower() or "bachelor" in program_type.lower() or "undergraduate" in program_type.lower():
                message = f"Here are some Bachelor's programs (BSc):\n- " + "\n- ".join(bsc_programs)
            elif "msc" in program_type.lower() or "master" in program_type.lower() or "postgraduate" in program_type.lower():
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

class ActionProvideFeesBasedOnType(Action):
    def name(self) -> Text:
        return "action_provide_fees_based_on_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        payment_type = tracker.get_slot("payment_type")

        if payment_type:
            if "full" in payment_type.lower():
                message = "You can benefit from %25 discount!"
            elif "instal" in payment_type.lower():
                message = "You can pay the tution fees in 12 instalments."
            else:
                message = "I couldn't recognize the payment type. Please specify full or instalments."
        else:
            message = "Would you like to see Full Payment or Instalment condition?"

        dispatcher.utter_message(message)
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

class ActionProvideBranches(Action):
    def name(self) -> Text:
        return "action_provide_branches"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "\n".join(["Berlin School of Business and Innovation is based in Berlin, but have several branches in different cities:",
            "Berlin",
            "Hamburg",
            "Barcelona",
            "Paris"])
        )
        return []
