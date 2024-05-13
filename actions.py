from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from typing import Dict, Text, Any, List, Union, Optional


PIZZA_TYPES = ["margherita", "supreme", "pesto and sun-dried tomato", "pepperoni", "seafood", "bbq chicken"]
PIZZA_SIZES = ["small", "medium", "large"]
PIZZA_QUANTITY = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
PIZZA_TOPPINGS_STD = {
    "margherita": ["Mozzarella Cheese", "Tomato Sauce", "Basil Leaves"],
    "supreme": ["Mushrooms", "Bell Peppers", "Onions", "Olives", "Tomatoes"],
    "pesto and sun-dried tomato": ["Pesto Sauce", "Sun-dried Tomatoes", "Feta Cheese", "Spinach"],
    "pepperoni": ["Pepperoni Slices", "Mozzarella Cheese", "Tomato Sauce"],
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

AVAILABLE_POSSIBLE_TOPPINGS = [
    "mozzarella cheese",
    "feta cheese",
    "tomato sauce"
    "pesto sauce",
    "bbq sauce",
    "grilled chicken",
    "tomatoes",
    "sun-dried tomatoes",
    "spinach",
    "basil leaves",
    "pepperoni slices",
    "mushrooms",
    "onions",
    "red onions",
    "olives",
    "prosciutto",
    "artichokes",
    "anchovies",
    "bell peppers",
    "cilantro",
    "shrimp",
    "mussels",
    "clams"
]


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
                text="The standard toppings for {} are: {}.".format(pizza_type, PIZZA_TOPPINGS_STD[pizza_type])
            )
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
        dispatcher.utter_message(text="🍕 Would you like to go with the standard toppings or customize your own toppings?")

        # de-activate the pizza_order_form and allow user to choose either standard or custom toppings
        return [FollowupAction("action_listen")]


class ActionAskPizzaCustomToppings(Action):
    def name(self) -> Text:
        return "action_ask_pizza_custom_toppings"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get current selected pizza_topping for the current pizza_type
        pizza_topping = tracker.get_slot("pizza_topping")

        # get the available possible toppings
        available_possible_toppings = AVAILABLE_POSSIBLE_TOPPINGS

        # remove the standard toppings from the available possible toppings
        for topping in pizza_topping:
            if topping.lower() in available_possible_toppings:
                available_possible_toppings.remove(topping.lower())

        # add 'and' before the last topping if there are more than one pizza_topping
        if len(pizza_topping) > 1:
            pizza_topping[-1] = "and " + pizza_topping[-1]

        # add 'and' before the last topping if there are more than one topping
        if len(available_possible_toppings) > 1:
            available_possible_toppings[-1] = "and " + available_possible_toppings[-1]

        message = "🍕 Current Selected Toppings for Your '{}' Pizza are: {}".format(
            tracker.get_slot("pizza_type"), ", ".join(pizza_topping)
        )
        message += "\n🍕 We offer the following topping options: {}.".format(", ".join(available_possible_toppings))
        message += "\n\n👋 Please make your own custom toppings (🍕) selection(s)..."

        dispatcher.utter_message(text=message)

        return []


class ActionAskToppingSatisfaction(Action):
    def name(self) -> Text:
        return "action_ask_topping_satisfaction"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get the latest customized toppings
        # pizza_custom_toppings = tracker.get_slot("pizza_topping")
        # # Show the latest customized toppings with an engaging message to the customer to confirm the toppings
        # dispatcher.utter_message(text="🍕 Your updated toppings are: {}.".format(pizza_custom_toppings))
        dispatcher.utter_message(response="utter_ask_topping_satisfaction")
        return []


class ActionSetCustomToppingsNull(Action):
    def name(self) -> Text:
        return "action_set_custom_toppings_null"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get pizza_type and pizza_topping from the tracker
        pizza_type = tracker.get_slot("pizza_type").lower()
        if pizza_type:
            # set the pizza_topping slot with the standard toppings
            return [SlotSet("pizza_topping", PIZZA_TOPPINGS_STD[pizza_type]), SlotSet("pizza_custom_toppings", None)]


class ActionSetStandardToppingsNull(Action):
    def name(self) -> Text:
        return "action_set_standard_toppings_null"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("pizza_topping", None)]


class ValidatePizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_order_form"

    async def validate_pizza_type(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_type value."""
        if slot_value.lower() in PIZZA_TYPES:
            return {"pizza_type": slot_value}
        else:
            dispatcher.utter_message(text="Sorry, we don't have that pizza: {}. Please choose from the available menu.".format(slot_value), response="utter_inform_menu")
            return {"pizza_type": None}

    async def validate_pizza_topping(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_topping value."""
        # pizza_type = tracker.get_slot("pizza_type").lower()
        # pizza_custom_toppings = tracker.get_slot("pizza_custom_toppings")
        pizza_topping = tracker.get_slot("pizza_topping")

        # if pizza_custom_toppings:
        #     dispatcher.utter_message(text="Your customized toppings are: {}.".format(pizza_topping))
        #     return {"pizza_topping": pizza_topping}
        # elif pizza_topping:
        #     return {"pizza_topping": pizza_topping}

        if pizza_topping:
            return {"pizza_topping": pizza_topping}
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please choose a pizza type from the available menu.", response="utter_inform_menu")
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

    async def extract_order_list(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:
        order_list = tracker.get_slot("order_list") or []
        return {"order_list": order_list}

    # async def validate_order_list(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
    #     """Validate order_list value."""
    #     # order list only contains the items which are dict type (i.e. the selected items) that are added to
    #     # the order_list slot in the action_submit_pizza_order_form. Since the order list mapping is defined as
    #     # from_text, so we need to remove any string type items from the order_list slot.
    #     if slot_value:
    #         return {"order_list": [item for item in slot_value if isinstance(item, dict)]}
    #     else:
    #         return {"order_list": []}


class ActionSubmitPizzaOrderForm(Action):
    def name(self) -> Text:
        return "action_submit_pizza_order_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza_type = tracker.get_slot("pizza_type").lower()
        pizza_size = tracker.get_slot("pizza_size").lower()
        pizza_quantity = tracker.get_slot("pizza_quantity").lower()
        pizza_topping = tracker.get_slot("pizza_topping")

        if pizza_type and pizza_size and pizza_quantity:
            order_list = tracker.get_slot("order_list") or []

            # if order_list is not empty, then remove all the items from the order_list which are not dict type
            order_list = [item for item in order_list if isinstance(item, dict)]

            # calculate the total price of current selected items
            current_item_price = PIZZA_PRICES[pizza_type][pizza_size] * PIZZA_QUANTITY.index(pizza_quantity) + 1

            # if order_list is not empty, then calculate the total price of all items
            if order_list:
                total_price = sum([item["price"] for item in order_list]) + current_item_price
            else:
                total_price = current_item_price

            # add the current selected item to the order_list
            order_list.append({
                "type": pizza_type,
                "size": pizza_size,
                "topping": pizza_topping,
                "quantity": pizza_quantity,
                "price": current_item_price
            })

            # Display Order Summary with the total price in a nice format
            message = "🍕Here's Your Order Summary:\n"
            for i, item in enumerate(order_list):
                message += "{}. {} {} Pizza\n".format(i + 1, item["size"].capitalize(), item["type"].capitalize())
                message += "   - Toppings: {}\n".format(", ".join(item["topping"]))
                message += "   - Quantity: {}\n".format(item["quantity"].capitalize())
                message += "   - Price: ${:.2f}\n".format(item["price"])

            message += "\nTotal Price: ${:.2f}".format(total_price)

            # prompt to ask if the customer wants to add more items to the order
            message += "\n\n🍕 Would you like to add another Pizza to your order? or Proceed to Pickup?"

            dispatcher.utter_message(text=message)

            # set pizza_order_form slots to None so that the form can be filled again for the next order item
            return [
                SlotSet("pizza_type", None),
                SlotSet("pizza_topping", None),
                SlotSet("pizza_size", None),
                SlotSet("pizza_quantity", None),
                SlotSet("order_list", order_list),
                FollowupAction("action_listen")
            ]
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Please provide all the required information.")
            return [FollowupAction("action_restart")]


class ValidatePizzaCustomToppingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_custom_topping_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[List[Text]]:
        if tracker.get_slot("topping_satisfaction"):
            return []
        else:
            return ["pizza_custom_toppings", "topping_satisfaction"]

    async def validate_pizza_custom_toppings(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate pizza_custom_toppings value."""
        pizza_topping = tracker.get_slot("pizza_topping")
        pizza_custom_toppings = tracker.get_slot("pizza_custom_toppings")
        pizza_topping = ", ".join(pizza_topping)
        if pizza_custom_toppings:
            if pizza_custom_toppings.__contains__(","):
                pizza_custom_toppings = pizza_custom_toppings.split(",")
            else:
                pizza_custom_toppings = [pizza_custom_toppings]

            # check the intent of customer
            latest_intent = tracker.latest_message["intent"].get("name")
            if latest_intent == "add_pizza_custom_toppings":
                pizza_custom_toppings = [topping.strip() for topping in pizza_custom_toppings]
            elif latest_intent == "remove_pizza_custom_toppings":
                pizza_custom_toppings = [topping.strip() for topping in pizza_custom_toppings]
                pizza_topping = pizza_topping.split(",")
                pizza_topping = [topping.strip() for topping in pizza_topping]
                for topping in pizza_custom_toppings:
                    if topping in pizza_topping:
                        pizza_topping.remove(topping)
                pizza_topping = ", ".join(pizza_topping)

            # split the toppings into a list
            pizza_topping = pizza_topping.split(",")
            pizza_topping = [topping.strip() for topping in pizza_topping]

            if pizza_custom_toppings:
                # add the custom toppings to the standard toppings list
                if latest_intent == "add_pizza_custom_toppings":
                    pizza_topping.extend(pizza_custom_toppings)
                    dispatcher.utter_message(text="We have added {} to your toppings. You now have: {}.".format(
                        pizza_custom_toppings, pizza_topping)
                    )
                elif latest_intent == "remove_pizza_custom_toppings":
                    dispatcher.utter_message(text="We have removed {} from your toppings. You now have: {}.".format(
                        pizza_custom_toppings, pizza_topping)
                    )

            return {"pizza_topping": pizza_topping, "pizza_custom_toppings": pizza_custom_toppings}
        else:
            return {"pizza_topping": pizza_topping, "pizza_custom_toppings": None}

    async def validate_topping_satisfaction(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        """Validate topping_satisfaction value."""
        latest_intent = tracker.latest_message["intent"].get("name")
        if latest_intent == "pizza_custom_toppings_happy":
            return {"topping_satisfaction": True}
        else:
            return {"topping_satisfaction": None}
        # if slot_value:
        #     return {"topping_satisfaction": slot_value}
        # else:
        #     return {"topping_satisfaction": None}


class ActionSubmitPizzaCustomToppingForm(Action):
    def name(self) -> Text:
        return "action_submit_pizza_custom_topping_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza_topping = tracker.get_slot("pizza_topping")
        pizza_topping = [topping.strip() for topping in pizza_topping]

        return [
            SlotSet("pizza_topping", pizza_topping),  # set the slot value
            FollowupAction("pizza_order_form")  # go back to the pizza_order_form
        ]
