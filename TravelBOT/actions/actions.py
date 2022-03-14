# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"



# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"



class FetchStatus(Action):
    def name(self):
        return 'action_fetch_status'
    def run(self, dispatcher, tracker, domain):
        url = "https://some.api.com/user/xxx/status"
        status = requests.get(url).json
        return [SlotSet("status", status)]