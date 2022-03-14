# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from nrclex import NRCLex  # For emotion recognition
from deep_translator import GoogleTranslator # To tranlste the to the user language
from langdetect import detect, detect_langs, DetectorFactory # To detect the user language

class ActionEmotionRecognition(Action):
   def name(self) -> Text:
       return "action_emotion_recognition"
   
   def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      text = str(tracker.latest_message["text"])
      emotion = NRCLex(text)

      dispatcher.utter_message(text="The Affect dictionary of the emotions detected are {}".format(emotion.affect_dict))
      dispatcher.utter_message(text="The emotion scores detected are {}".format(emotion.raw_emotion_scores))
      dispatcher.utter_message(text="The top emotions detected are {}".format(emotion.top_emotions))
      dispatcher.utter_message(text="The Affect frequencies detected are {}".format(emotion.affect_frequencies))
      return []

class ActionTranslation(Action):
   def name(self) -> Text:
       return "action_translation"
   
   def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      userMsg = str(tracker.latest_message["text"])
      DetectorFactory.seed = 0
      inputLangList = detect_langs(userMsg)
      langName = ""
      langConfidence = 0
      for item in inputLangList:
          if(float(str(item).split(":",1)[1]) >= langConfidence):
              langConfidence = float(str(item).split(":",1)[1])
              langName = str(item).split(":")[0]
      
      translatedText = GoogleTranslator(source='auto', target=langName).translate("I am very happy and joyful.")

      dispatcher.utter_message(text="The language of the user is {}".format(langName))
      dispatcher.utter_message(text="The translated message is {}".format(translatedText))
      
      return[]