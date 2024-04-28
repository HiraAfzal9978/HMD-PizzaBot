from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from typing import Dict, Text, Any, List, Union, Optional


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
            # dispatcher.utter_message(response="utter_ask_topping_confirmation")
            return [
                SlotSet("pizza_topping", PIZZA_TOPPINGS_STD[pizza_type]),
                FollowupAction("action_ask_topping_confirmation")
            ]
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please choose a pizza type from the available menu.", response="utter_inform_menu")
            return []


class ActionAskToppingConfirmation(Action):
    def name(self) -> Text:
        return "action_ask_topping_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="🍕 Would you like to go with the standard toppings or customize your own toppings?",
            response="utter_ask_custom_toppings"
        )

        return []


class ActionAskPizzaCustomToppings(Action):
    def name(self) -> Text:
        return "action_ask_pizza_custom_toppings"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_custom_toppings")
        return []


class ActionSetStandardToppingsNull(Action):
    def name(self) -> Text:
        return "action_set_standard_toppings_null"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("pizza_topping", None)]


class ActionValidatePizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_pizza_order_form"

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
        pizza_topping = slot_value.split(",")
        pizza_topping = [topping.strip() for topping in pizza_topping]

        if all(topping in PIZZA_TOPPINGS_STD[pizza_type] for topping in pizza_topping):
            return {"pizza_topping": pizza_topping}
        else:
            dispatcher.utter_message(text="Sorry, we don't have that topping: {}. Please choose from the available toppings.".format(slot_value), response="utter_ask_topping_confirmation")
            return {"pizza_topping": None}

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


class ActionSubmitPizzaOrderForm(Action):
    def name(self) -> Text:
        return "action_submit_pizza_order_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza_type = tracker.get_slot("pizza_type").lower()
        pizza_size = tracker.get_slot("pizza_size").lower()
        pizza_quantity = tracker.get_slot("pizza_quantity").lower()
        pizza_topping = tracker.get_slot("pizza_topping")

        if pizza_type and pizza_size and pizza_quantity:
            pizza_price = PIZZA_PRICES[pizza_type][pizza_size]
            pizza_quantity = PIZZA_QUANTITY.index(pizza_quantity) + 1
            total_price = pizza_price * pizza_quantity

            dispatcher.utter_message(
                text="You have ordered {} {} {} pizza(s) with {} topping(s). Your total bill is ${:.2f}.".format(
                    pizza_quantity, pizza_size, pizza_type, len(pizza_topping), total_price
                )
            )
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please provide all the required information.")
            return [FollowupAction("action_restart")]

        return []


class ActionValidatePizzaCustomToppingForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_pizza_custom_topping_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[List[Text]]:
        return ["pizza_custom_toppings"]

    async def validate_pizza_custom_toppings(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_custom_toppings value."""
        pizza_type = tracker.get_slot("pizza_type").lower()
        pizza_topping = tracker.get_slot("pizza_topping")

        print("pizza_type: ", pizza_type)
        print("pizza_topping: ", pizza_topping)

        # set pizza_custom_toppings slot with value from pizza_topping slot
        if pizza_topping:
            return {"pizza_custom_toppings": pizza_topping}
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please provide the custom toppings for your pizza.")
            return {"pizza_custom_toppings": None}


class ActionSubmitPizzaCustomToppingForm(Action):
    def name(self) -> Text:
        return "action_submit_pizza_custom_topping_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza_topping = tracker.get_slot("pizza_topping")
        pizza_topping = pizza_topping.split(",")
        pizza_topping = [topping.strip() for topping in pizza_topping]

        return [
            SlotSet("pizza_topping", pizza_topping),  # set the slot value
            FollowupAction("pizza_order_form")  # go back to the pizza_order_form
        ]
