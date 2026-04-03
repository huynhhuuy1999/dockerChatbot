import os
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from dotenv import load_dotenv
from actions.db import get_driver
from actions.utils import format_answer

load_dotenv()


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GPT4ALL_API = "http://127.0.0.1:8000/chat"
MESSAGE_FAILURE_RESPONSE = "Xin lỗi tôi không thể trả lời câu hỏi của bạn"
OLLAMA_URL = "http://localhost:11434/api/generate"


# class HoiVeNhiemVuChucDanhGiangDay(Action):

#     def name(self) -> str:
#         return "hoiVeNhiemVuChucDanhGiangDayAction"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
#     ):
#         drv = get_driver()
#         with drv.session() as session:
#             session = drv.session(database=NEO4J_DATABASE)
#             chucDanh = tracker.get_slot("chucDanh")
#             print("action", chucDanh)
#             entityAction = session.run(
#                 f"MATCH (e:Entity)<-[:HAS_ENTITY]-(i:Intent {{name:'HoiVeNhiemVuChucDanhGiangDay'}})"
#                 f" WITH e,i, apoc.text.levenshteinSimilarity(e.text, '{chucDanh}') AS similarity"
#                 f" ORDER BY similarity DESC LIMIT 1 RETURN e"
#             ).data()
#             print("entityAction", entityAction)
#             if entityAction and len(entityAction) > 0:
#                 result = session.run(
#                     f"MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent)<-[:HAS_INTENT]-(do:DOCUMENT)"
#                     f' WHERE a.entity CONTAINS "{entityAction[0]["e"]["name"]}" AND i.name="HoiVeNhiemVuChucDanhGiangDay"'
#                     f" RETURN a,do,di LIMIT 1;"
#                 ).data()
#                 if result:
#                     answers = [record["a"]["answer"] for record in result]
#                     law = [
#                         {
#                             "name": record["di"]["name"],
#                             "content": record["di"]["content"],
#                         }
#                         for record in result
#                     ]
#                     documents = [record["do"]["text"] for record in result]

#                     if answers:
#                         dispatcher.utter_message(
#                             text=format_answer(
#                                 law,
#                                 answers,
#                                 documents,
#                                 (
#                                     result[0]["a"]["khoan"]
#                                     if result[0]["a"].get("khoan")
#                                     else None
#                                 ),
#                             )
#                         )
#                     else:
#                         dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
#                     drv.close()
#                 else:
#                     dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
#             else:
#                 dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
#         return [SlotSet("chucDanh", None)]
