from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGreet(Action):
    def name(self) -> Text:
        return "utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_greet")
        return []


class ActionEndGreet(Action):
    def name(self) -> Text:
        return "utter_end_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_end_greet")
        return []


class ActionOutOfScope(Action):
    def name(self) -> Text:
        return "utter_out_of_scope"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_out_of_scope")
        return []


class ActionBotChallenge(Action):
    def name(self) -> Text:
        return "utter_bot_challenge"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_bot_challenge")
        return []


class ActionAffirm(Action):
    def name(self) -> Text:
        return "utter_affirm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_affirm")
        return []


class ActionDeny(Action):
    def name(self) -> Text:
        return "utter_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_deny")
        return []


class ActionInitiateGeneralConversation(Action):
    def name(self) -> Text:
        return "utter_initiate_general_conversation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_initiate_general_conversation")
        return []


class ActionInformMenu(Action):
    def name(self) -> Text:
        return "utter_inform_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_inform_menu")
        return []


class ActionInformVegetarianMenu(Action):
    def name(self) -> Text:
        return "utter_inform_vegetarian_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_inform_vegetarian_menu")
        return []


class ActionInformNonVegetarianMenu(Action):
    def name(self) -> Text:
        return "utter_inform_non_vegetarian_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_inform_non_vegetarian_menu")
        return []


class ActionRecommendPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_recommend_pizza")
        return []


class ActionRecommendVegetarianPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_vegetarian_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_recommend_vegetarian_pizza")
        return []


class ActionRecommendNonVegetarianPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_non_vegetarian_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_recommend_non_vegetarian_pizza")
        return []
