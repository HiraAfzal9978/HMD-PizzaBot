from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

PIZZA_TYPES = ["margherita", "supreme", "pesto and sun-dried tomato", "pepperoni", "seafood", "bbq chicken"]
PIZZA_SIZES = ["small", "medium", "large"]
PIZZA_QUANTITY = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
PIZZA_TOPPINGS_STD = {
    "margherita": ["Mozzarella Cheese", "Classic Tomato Sauce ", "Fresh Basil Leaves"],
    "supreme": ["Loaded with Mushrooms", "Bell Peppers", "Onions", "Olives", "Tomatoes"],
    "pesto and sun-dried tomato": ["Pesto Sauce", "Sun-dried Tomatoes", "Feta Cheese", "Spinach"],
    "pepperoni": ["Pepperoni Slices", "Mozzarella Cheese", "Classic Tomato Sauce"],
    "bbq chicken": ["BBQ Sauce", "Grilled Chicken", "Red Onions", "Cilantro", "Mozzarella Cheese"],
    "seafood": ["Shrimp", "Mussels", "Clams", "Tomato Sauce", "Mozzarella Cheese"]
}
PIZZA_PRICES = {
    "margherita": {"small": 9.99, "medium": 12.99, "large": 15.99},
    "supreme": {"small": 11.99, "medium": 14.99, "large": 17.99},
    "pesto and sun-dried tomato": {"small": 10.99, "medium": 13.99, "large": 16.99},
    "pepperoni": {"small": 10.99, "medium": 13.99, "large": 16.99},
    "bbq chicken": {"small": 12.99, "medium": 15.99, "large": 18.99},
    "seafood": {"small": 13.99, "medium": 16.99, "large": 19.99}
}


class ActionGreet(Action):
    def name(self) -> Text:
        return "utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_greet")
        return []


class ActionEndGreet(Action):
    def name(self) -> Text:
        return "utter_end_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_end_greet")
        return []


class ActionOutOfScope(Action):
    def name(self) -> Text:
        return "utter_out_of_scope"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_out_of_scope")
        return []


class ActionBotChallenge(Action):
    def name(self) -> Text:
        return "utter_bot_challenge"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_bot_challenge")
        return []


class ActionAffirm(Action):
    def name(self) -> Text:
        return "utter_affirm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_affirm")
        return []


class ActionDeny(Action):
    def name(self) -> Text:
        return "utter_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_deny")
        return []


class ActionInitiateGeneralConversation(Action):
    def name(self) -> Text:
        return "utter_initiate_general_conversation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_initiate_general_conversation")
        return []


class ActionInformMenu(Action):
    def name(self) -> Text:
        return "utter_inform_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_inform_menu")
        return []


class ActionInformVegetarianMenu(Action):
    def name(self) -> Text:
        return "utter_inform_vegetarian_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_inform_vegetarian_menu")
        return []


class ActionInformNonVegetarianMenu(Action):
    def name(self) -> Text:
        return "utter_inform_non_vegetarian_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_inform_non_vegetarian_menu")
        return []


class ActionRecommendPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_recommend_pizza")
        return []


class ActionRecommendVegetarianPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_vegetarian_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_recommend_vegetarian_pizza")
        return []


class ActionRecommendNonVegetarianPizza(Action):
    def name(self) -> Text:
        return "utter_recommend_non_vegetarian_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_recommend_non_vegetarian_pizza")
        return []


class ActionAskPizzaType(Action):
    def name(self) -> Text:
        return "action_ask_pizza_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_pizza_type")
        return []


class ActionAskPizzaTopping(Action):
    def name(self) -> Text:
        return "action_ask_pizza_topping"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza_type = tracker.get_slot("pizza_type").lower()

        if pizza_type:
            dispatcher.utter_message(
                text="The standard toppings for {} are: {}.".format(pizza_type, PIZZA_TOPPINGS_STD[pizza_type]),
                response="utter_ask_topping_confirmation"
            )

            # extract user's intent
            intent = tracker.latest_message['intent'].get('name')
            print("Intent: ", intent)
            if intent == "pizza_standard_topping_confirm":
                # if the user confirms the standard toppings, then proceed with the standard toppings
                return [SlotSet("pizza_topping", PIZZA_TOPPINGS_STD[pizza_type])]
            elif intent == "pizza_custom_topping_confirm":
                # if the user wants custom toppings, then ask for the custom toppings
                # todo: implement the custom toppings
                pass
            else:
                dispatcher.utter_message(response="utter_ask_topping_confirmation")
                return []
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please choose a pizza type from the available menu.", response="utter_inform_menu")
            return []


class ActionAskToppingConfirmation(Action):
    def name(self) -> Text:
        return "action_ask_topping_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_topping_confirmation")
        return []


class ActionAskPizzaSize(Action):
    def name(self) -> Text:
        return "action_ask_pizza_size"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_pizza_size")
        return []


class ActionAskPizzaQuantity(Action):
    def name(self) -> Text:
        return "action_ask_pizza_quantity"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_pizza_quantity")
        return []


# create a FormAction class
class PizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "pizza_order_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
        return ["pizza_type", "pizza_topping", "pizza_size", "pizza_quantity"]
    
    async def validate_pizza_type(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_type value."""
        if slot_value.lower() in PIZZA_TYPES:
            return {"pizza_type": slot_value}
        else:
            dispatcher.utter_message(text="Sorry, we don't have that pizza: {}. Please choose from the available menu.".format(slot_value), response="utter_inform_menu")
            return {"pizza_type": None}

    async def validate_pizza_topping(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_topping value."""
        pizza_type = tracker.get_slot("pizza_type").lower()

        print("Events: ", tracker.events)

        # check user latest intent to confirm the standard toppings or custom toppings
        intent = tracker.latest_message['intent'].get('name')
        print("Latest Intent: ", intent)
        if intent == "pizza_standard_topping_confirm":
            return {"pizza_topping": PIZZA_TOPPINGS_STD[pizza_type]}
        elif intent == "pizza_custom_topping_confirm":
            # todo: implement the custom toppings
            pass

    async def validate_pizza_size(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_size value."""
        if slot_value.lower() in PIZZA_SIZES:
            return {"pizza_size": slot_value}
        else:
            dispatcher.utter_message(text="Sorry, we don't have that size: {}. Please choose from the available sizes.".format(slot_value), response="utter_pizza_size")
            return {"pizza_size": None}

    async def validate_pizza_quantity(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_quantity value."""
        if slot_value.lower() in ["a", "A", "an", "An"]:
            slot_value = "one"
        if slot_value.lower() in PIZZA_QUANTITY:
            return {"pizza_quantity": slot_value}
        else:
            dispatcher.utter_message(text="Sorry, if you want to order more than 10 pizzas, then please contact us on +XX-XXX-XXX-XXXX")
            return {"pizza_quantity": None}

    async def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Submit the form."""
        pizza_type = tracker.get_slot("pizza_type").lower()
        pizza_topping = tracker.get_slot("pizza_topping").lower()
        pizza_size = tracker.get_slot("pizza_size").lower()
        pizza_quantity = tracker.get_slot("pizza_quantity").lower()

        # calculate the price
        pizza_price = PIZZA_PRICES[pizza_type][pizza_size] * PIZZA_QUANTITY.index(pizza_quantity) + 1
        dispatcher.utter_message(response="utter_submit", pizza_type=pizza_type, pizza_topping=pizza_topping,
                                 pizza_size=pizza_size, pizza_quantity=pizza_quantity, pizza_price=pizza_price)
        return []
