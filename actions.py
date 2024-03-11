# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType, Form, SlotSet
from rasa_sdk.types import DomainDict


class ActionShowCategoryMenu(Action):
    def name(self) -> Text:
        return "action_show_category_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use the pizza_Category slot value directly
        category = tracker.get_slot("pizza_Category")

        if category:
            category = category.lower()
            if category in ['vegetarian', 'veg']:
                dispatcher.utter_message(template="utter_vegetarian_menu")
            elif category in ['non-vegetarian', 'non vegetarian', 'nonveg', 'non veg', 'non-veg', 'nonvegetarian']:
                dispatcher.utter_message(template="utter_non_vegetarian_menu")
            else:
                dispatcher.utter_message("Sorry, I didn't get that. Please choose either vegetarian or non-vegetarian.")
        else:
            dispatcher.utter_message(
                "Sorry, I couldn't detect the pizza category. Could you please specify if you want vegetarian or non-vegetarian pizza?")

        return []


# class PizzaOrderForm(FormValidationAction):
#     def name(self) -> Text:
#         return "pizza_order_form"
#
#     def required_slots(self, domain: DomainDict) -> List[Text]:
#         return ["pizza_Category", "pizza_type", "toppings", "quantity", "size"]
#
#     async def submit(
#             self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
#     ) -> List[EventType]:
#         # Summarize the order
#         dispatcher.utter_message(template="utter_summarize_order",
#                                  pizza_Category=tracker.get_slot("pizza_Category"),
#                                  pizza_type=tracker.get_slot("pizza_type"),
#                                  toppings=tracker.get_slot("toppings"),
#                                  quantity=tracker.get_slot("quantity"),
#                                  size=tracker.get_slot("size"))
#
#         # Ask for order confirmation
#         dispatcher.utter_message(template="utter_confirm_order")
#         return []


class PizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "action_pizza_order_form"

    async def required_slots(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
        #self, domain: Dict[Text, Any], tracker: Tracker, **kwargs) -> List[Text]:
    # async def required_slots(self, tracker: Tracker, domain: DomainDict) -> List[Text]:
        return ["pizza_type", "size","toppings", "quantity"]

        """Dynamically request slots based on the pizza type."""
        slots = ["pizza_type","toppings" "size", "quantity"]

        # pizza_type = tracker.get_slot("pizza_type")
        # if pizza_type:
        #     # Add 'toppings' slot after 'pizza_type' has been filled
        #     slots.append("toppings")
        # return slots

    async def validate_pizza_type(
            self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,
    ) -> Dict[Text, Any]:
        slot_value = slot_value.lower()
        valid_types = ["margherita", "pepperoni", "vegetarian supreme", "pesto and sun-dried tomato", "bbq chicken",
                       "seafood"]
        if slot_value not in valid_types:
            dispatcher.utter_message(text=f"Sorry, we don't offer {slot_value}. Please choose from our menu.", template="utter_menu")
            return {"pizza_type": None}
        else:
            # Provide default toppings for the chosen pizza type and ask for customization
            default_toppings = self.default_toppings(pizza_type=slot_value)
            dispatcher.utter_message(
                text=f"Your {slot_value} pizza comes with {', '.join(default_toppings)}. Would you like to add or remove any toppings?")
        return {"pizza_type": slot_value}

    async def extract_toppings(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[str, List[str]]: #self, slot_value: Any,
        add_toppings = []
        remove_toppings = []
        error = False  # Flag to indicate if an error occurred during extraction

        for event in reversed(tracker.events):
            if event.get("event") == "user":
                intent_name = event.get("parse_data", {}).get("intent", {}).get("name")
                topping_entities = [e.get("value") for e in event.get("parse_data", {}).get("entities", []) if
                                    e.get("entity") == "topping"]

                if intent_name == "add_topping" and topping_entities:
                    add_toppings.extend(topping_entities)
                elif intent_name == "remove_topping" and topping_entities:
                    remove_toppings.extend(topping_entities)
                elif intent_name not in ["add_topping", "remove_topping"]:
                    # Handle unexpected intents gracefully
                    error = True
                    break  # Optionally break if you want to stop processing after the first error

        if error:
            dispatcher.utter_message(
                text="I noticed an unexpected response. Let's try adding or removing toppings again.")
            return {"add_toppings": [], "remove_toppings": [], "error": True}

        return {"add_toppings": add_toppings, "remove_toppings": remove_toppings, "error": False}

    def default_toppings(self, pizza_type: str) -> List[str]:
        """Returns a list of default toppings for a given pizza type."""
        toppings = {
            "margherita": ["tomato sauce", "mozzarella", "basil"],
            "pepperoni": ["tomato sauce", "mozzarella", "pepperoni"],
            "vegetarian supreme": ["tomato sauce", "mozzarella", "olives", "bell peppers", "mushrooms"],
            "pesto and sun-dried tomato": ["pesto sauce", "mozzarella", "sun-dried tomatoes", "pine nuts"],
            "bbq chicken": ["bbq sauce", "mozzarella", "chicken", "red onions"],
            "seafood": ["tomato sauce", "mozzarella", "shrimp", "calamari"],
        }
        return toppings.get(pizza_type, [])

    async def validate_toppings(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,domain: DomainDict) -> Dict[Text, Any]:
        pizza_type = tracker.get_slot("pizza_type").lower()
        default_toppings = self.default_toppings(pizza_type=pizza_type)
        toppings_modifications = await self.extract_toppings(dispatcher, tracker, domain)

        if toppings_modifications["error"]:
            # If an error was detected during extraction, prompt the user again without changing the slot value
            return {"toppings": None}

        # Apply modifications to default toppings based on user input
        final_toppings = default_toppings[:]
        for topping in toppings_modifications["add_toppings"]:
            if topping not in final_toppings:
                final_toppings.append(topping)
        for topping in toppings_modifications["remove_toppings"]:
            if topping in final_toppings:
                final_toppings.remove(topping)

        return {"toppings": final_toppings}

        # Validate pizza size

    async def validate_size(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
        slot_value = slot_value.lower()
        if slot_value not in ["small", "medium", "large"]:
            dispatcher.utter_message(
                text="Sorry, we don't offer that size. Please choose from small, medium, or large.")
            return {"size": None}
        return {"size": slot_value}

        # Validate pizza quantity

    async def validate_quantity(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
        try:
            slot_value = int(slot_value) if slot_value.isdigit() else slot_value.lower()
            slot_value = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                          "nine": 9, "ten": 10}.get(slot_value, slot_value)
            if 1 <= slot_value <= 10:
                return {"quantity": str(slot_value)}
            else:
                raise ValueError
        except ValueError:
            dispatcher.utter_message(text="Please choose a quantity from 1 to 10.")
            return {"quantity": None}

        # Validate toppings



    # async def validate_toppings(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
    #     # Assuming slot_value is a list of toppings from user input
    #     if not isinstance(slot_value, list):
    #         slot_value = [slot_value.lower()]
    #
    #     valid_toppings = ["olives", "mushrooms", "pepperoni", "pineapple", "cheese", "onions", "peppers", "mozzarella",
    #                       "basil", "arugula", "pesto", "sun-dried tomatoes", "feta", "bbq sauce", "chicken",
    #                       "red onions", "shrimp", "calamari", "clams", "garlic"]
    #     invalid_toppings = [topping for topping in slot_value if topping not in valid_toppings]
    #
    #     if invalid_toppings:
    #         dispatcher.utter_message(
    #             text=f"We don't offer {', '.join(invalid_toppings)}. Please choose from our available toppings: {', '.join(valid_toppings)}.")
    #         return {"toppings": None}
    #     return {"toppings": slot_value}

    async def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> List[EventType]:
        pizza_type = tracker.get_slot("pizza_type")
        toppings = tracker.get_slot("toppings")
        size = tracker.get_slot("size")
        quantity = tracker.get_slot("quantity")

        order_summary = f"Order Summary:\nPizza Type: {pizza_type.title()}\nToppings: {', '.join(toppings).title() if toppings else 'Standard'}\nSize: {size.title()}\nQuantity: {quantity}"
        # Ask for order confirmation
        dispatcher.utter_message(text=order_summary)
        dispatcher.utter_message(
            text="Does everything look correct? Please confirm your order or let us know if there are any changes.")

        dispatcher.utter_message(template="summarize_order")
        return []


class ActionHandleUserRequest(Action):
    def name(self) -> Text:
        return "action_handle_user_request"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")

        if intent == "add_more_pizza":
            dispatcher.utter_message(template="utter_add_more_pizza")
            pizza_size = tracker.get_slot("size")
            pizza_type = tracker.get_slot("pizza_type")
            pizza_amount = tracker.get_slot("quantity")
            if pizza_size is None:
                pizza_size = "medium"
            order_details = str(pizza_amount + " " + pizza_type + " is of " + pizza_size)
            old_order = tracker.get_slot("total_order")
            return [SlotSet("total_order", [order_details]) if old_order is None else SlotSet("total_order", [
                old_order[0] + ' and ' + order_details])]

        elif intent == "remove_pizza":
            # Logic to remove a pizza from the order
            # Example logic: Remove the last pizza added to the order
            last_pizza_index = tracker.get_slot("last_pizza_index")
            if last_pizza_index is not None:
                dispatcher.utter_message(template="utter_remove_pizza_success")
                return [SlotSet("last_pizza_index", None)]
            else:
                dispatcher.utter_message(template="utter_remove_pizza_failure")
        elif intent == "confirm_order":
            dispatcher.utter_message(template="utter_confirm_order")
        elif intent == "deny_order":
            dispatcher.utter_message(template="utter_deny_order")
            return [AllSlotsReset()]

        return []

class ActionProvideToppings(Action):
    def name(self) -> Text:
        return "action_provide_toppings"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pizza = tracker.get_slot('pizza_type')  # Assuming 'pizza_type' is the slot for the type of pizza

        toppings_response = {
            "margherita": "Margherita Pizza has tomato sauce, fresh mozzarella cheese, fresh basil leaves, and a drizzle of olive oil.\n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?",
            "vegetarian_supreme":"Vegetarian Supreme Pizza comes with tomato sauce, mozzarella cheese, bell peppers, red onions, black olives, mushrooms, and spinach.\n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?",
            "pesto_and_sun_dried_tomato": "Pesto and Sun-Dried Tomato Pizza has pesto sauce, mozzarella cheese, sun-dried tomatoes, feta cheese, pine nuts, and fresh arugula.\n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?",
            "pepperoni": "Pepperoni Pizza has tomato sauce, mozzarella cheese, and pepperoni.\n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?",
            "bbq_chicken":"BBQ Chicken Pizza has BBQ sauce, mozzarella cheese, chicken, red onions, and cilantro.\n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?",
            "seafood": "Seafood Pizza has tomato sauce, mozzarella cheese, shrimp, calamari, clams, and garlic. \n Would you like to go with the same toppings or would you like to customize the toppings on your pizza?"
            # Add other pizza types and their toppings description here
        }

        response = toppings_response.get(pizza.lower(), "I'm not sure about the Pizza/toppings for that pizza. please check spellings/menu list and try again.")
        dispatcher.utter_message(text=response)

        return []
class ActionCustomizeToppings(Action):
    def name(self) -> Text:
        return "action_customize_toppings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve the current toppings and pizza type from the tracker
        current_toppings = tracker.get_slot('toppings') or []
        pizza_type = tracker.get_slot('pizza_type') or 'unknown'

        # Default toppings for each pizza type (assuming these are predefined)
        default_toppings = {
            'margherita': ['tomato sauce', 'mozzarella cheese', 'fresh basil leaves', 'olive oil'],
            'vegetarian_supreme': ['tomato sauce', 'mozzarella cheese', 'bell peppers', 'red onions', 'black olives', 'mushrooms', 'spinach'],
            'pesto_and_sun_dried_tomato': ['pesto sauce', 'mozzarella cheese', 'sun-dried tomatoes', 'feta cheese', 'pine nuts', 'arugula'],
            'pepperoni': ['tomato sauce', 'mozzarella cheese', 'pepperoni'],
            'bbq_chicken': ['bbq sauce', 'mozzarella cheese', 'chicken', 'red onions', 'cilantro'],
            'seafood': ['tomato sauce', 'mozzarella cheese', 'shrimp', 'calamari', 'clams', 'garlic']

        }

        # If no current toppings, set to default for the chosen pizza type
        if not current_toppings:
            current_toppings = default_toppings.get(pizza_type, [])

        # Extract toppings information from the user's message
        toppings_to_add = tracker.get_slot("add_topping") or []
        toppings_to_remove = tracker.get_slot("remove_topping") or []

        # Add all available toppings here
        AVAILABLE_TOPPINGS = ["olives", "mushrooms", "pepperoni", "pineapple", "cheese", "onions", "peppers",
                              "mozzarella cheese", "fresh basil leaves",
                              "fresh arugula", "pesto sauce", "sun-dried tomatoes", "feta cheese", "bbq sauce",
                              "chicken", "red onions"]

        unavailable_toppings = []
        # Add toppings if they're available and not already present
        for topping in toppings_to_add:
            if topping in AVAILABLE_TOPPINGS and topping not in current_toppings:
                current_toppings.append(topping)
            elif topping not in AVAILABLE_TOPPINGS:
                unavailable_toppings.append(topping)

        if unavailable_toppings:
            unavailable_toppings_str = ", ".join(unavailable_toppings)
            available_toppings_str = ", ".join(AVAILABLE_TOPPINGS)
            dispatcher.utter_message(text=f"Sorry, we don't have {unavailable_toppings_str}. "
                                          f"Available toppings are: {available_toppings_str}.")

        # Remove toppings if they exist
        current_toppings = [topping for topping in current_toppings if topping not in toppings_to_remove]

        # Update the tracker with the new list of toppings
        dispatcher.utter_message(text=f"Your {pizza_type} pizza now has the following toppings: {', '.join(current_toppings)}.")

        # Set the updated toppings in the tracker
        return [SlotSet("toppings", current_toppings)]


# class ActionChooseTopping(Action):
#     def name(self) -> Text:
#         return "action_choose_topping"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         pizza_type = tracker.get_slot("pizza_type")
#
#         if pizza_type == "Margherita":
#             toppings = [
#                 "Tomato sauce",
#                 "Fresh mozzarella cheese",
#                 "Fresh basil leaves",
#                 "Drizzle of olive oil"
#             ]
#         elif pizza_type == "Vegetarian Supreme":
#             toppings = [
#                 "Tomato sauce",
#                 "Mozzarella cheese",
#                 "Bell peppers (red, green, and yellow)",
#                 "Red onions",
#                 "Black olives",
#                 "Mushrooms",
#                 "Spinach"
#             ]
#         elif pizza_type == "Pesto and Sun-Dried Tomato":
#             toppings = [
#                 "Pesto sauce",
#                 "Mozzarella cheese",
#                 "Sun-dried tomatoes",
#                 "Feta cheese",
#                 "Pine nuts",
#                 "Fresh arugula"
#             ]
#         # Add similar logic for other pizza types
#
#         topping_options = ", ".join(toppings)
#         dispatcher.utter_message(text=f"Toppings available for {pizza_type}:\n{topping_options}")
#
#         return []
#




# class ActionChangeOrder(Action):
# 	def name(self):
# 		return 'action_change_order'
#
# 	def run(self, dispatcher, tracker, domain):
# 		pizza_size = tracker.get_slot("pizza_size")
# 		pizza_type = tracker.get_slot("pizza_type")
# 		pizza_amount = tracker.get_slot("pizza_amount")
# 		SlotSet("pizza_type", pizza_type)
# 		SlotSet("pizza_size", pizza_size)
# 		SlotSet("pizza_amount", pizza_amount)
# 		return[]
#
# class ActionPizzaOrderAdd(Action):
# 	def name(self):
# 		return 'action_pizza_order_add'
#
# 	def run(self, dispatcher, tracker, domain):
# 		pizza_size = tracker.get_slot("pizza_size")
# 		pizza_type = tracker.get_slot("pizza_type")
# 		pizza_amount = tracker.get_slot("pizza_amount")
# 		if pizza_size is None:
# 			pizza_size = "standard"
# 		order_details =  str(pizza_amount + " "+pizza_type + " is of "+pizza_size )
# 		old_order = tracker.get_slot("total_order")
# 		return[SlotSet("total_order", [order_details]) if old_order is None else SlotSet("total_order", [old_order[0]+' and '+order_details])]
#
# class ActionResetPizzaForm(Action):
# 	def name(self):
# 		return 'action_reset_pizza_form'
#
# 	def run(self, dispatcher, tracker, domain):
#
# 		return[SlotSet("pizza_type", None),SlotSet("pizza_size", None),SlotSet("pizza_amount", None)]
#
# class ActionOrderNumber(Action):
# 	def name(self):
# 		return 'action_order_number'
#
# 	def run(self, dispatcher, tracker, domain):
# 		name_person = tracker.get_slot("client_name")
# 		number_person = tracker.get_slot("phone_number")
# 		order_number =  str(name_person + "_"+number_person)
# 		print(order_number)
# 		return[SlotSet("order_number", order_number)]
#
#
# class ActionPizzaQuestions(Action):
# 	def name(self):
# 		return 'action_pizza_questions'
#
# 	def run(self, dispatcher, tracker, domain):
# 		return[]