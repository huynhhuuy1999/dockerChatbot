import os
import time
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from dotenv import load_dotenv
from actions.db import get_driver
from actions.utils import format_answer, MESSAGE_FAILURE_RESPONSE

load_dotenv()


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GPT4ALL_API = "http://127.0.0.1:8000/chat"
MESSAGE_FAILURE_RESPONSE = "Xin lỗi tôi không thể trả lời câu hỏi của bạn"
OLLAMA_URL = "http://localhost:11434/api/generate"


class customActionBase(Action):

    def name(self) -> str:
        return "customActionBase"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        start_time = time.perf_counter()
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            intentName = tracker.latest_message["intent"].get("name")
            print("intentName", intentName)
            result = session.run(
                f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {{name:"{intentName}"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
            ).data()
            if result:
                answers = [record["a"]["answer"] for record in result]
                law = [
                    {"name": record["di"]["name"], "content": record["di"]["content"]}
                    for record in result
                ]
                documents = [record["do"]["text"] for record in result]
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            end_time = time.perf_counter()
            response_time = end_time - start_time
            print(f"Response time: {response_time}")

        # drv.close()
        return []


class actionBaseWithEntityForm(Action):

    def name(self) -> str:
        return "actionBaseWithEntityForm"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            originalIntent = tracker.get_slot("originalIntent")
            if not originalIntent:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
                return []
            action = tracker.get_slot("actionTT17")
            chucDanh = tracker.get_slot("chucDanh")
            capBac = tracker.get_slot("capBac")
            print("originalIntent", originalIntent, action, chucDanh)
            entityVariable = None
            if action:
                entityVariable = action
            if chucDanh:
                entityVariable = chucDanh
            if capBac:
                entityVariable = capBac
            entityAction = session.run(
                f"MATCH (e:Entity)<-[:HAS_ENTITY]-(i:Intent {{name:'{originalIntent}'}})"
                f" WITH e,i, apoc.text.levenshteinSimilarity(e.text, '{entityVariable}') AS similarity"
                f" ORDER BY similarity DESC LIMIT 1 RETURN e"
            ).data()
            print("entityAction", entityAction)
            if entityAction and len(entityAction) > 0:
                result = session.run(
                    f"MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent)<-[:HAS_INTENT]-(do:DOCUMENT)"
                    f' WHERE a.entity CONTAINS "{entityAction[0]["e"]["name"]}" AND i.name="{originalIntent}"'
                    f" RETURN a,do,di LIMIT 1;"
                ).data()
                if result:
                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    documents = [record["do"]["text"] for record in result]
                    # print("re", result[0]["a"]["khoan"])
                    if answers:
                        dispatcher.utter_message(
                            text=format_answer(
                                law,
                                answers,
                                documents,
                                (
                                    [result[0]["a"]["khoan"]]
                                    if result[0]["a"].get("khoan")
                                    else None
                                ),
                            )
                        )
                    else:
                        dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
                    drv.close()
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            # dispatcher.utter_message(text="vao custom action")
        return [
            SlotSet("originalIntent", None),
            SlotSet("actionTT17", None),
            SlotSet("chucDanh", None),
            SlotSet("capBac", None),
        ]
