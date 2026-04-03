import os
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from dotenv import load_dotenv
import requests

from actions.db import get_driver

# from actions.actionsBase import customActionBase
# from actions.actionsBase import actionBaseWithEntityForm
from actions.utils import format_answer, MESSAGE_FAILURE_RESPONSE
from rasa_sdk.events import SlotSet


load_dotenv()


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GPT4ALL_API = "http://backend:8000/chat"
OLLAMA_URL = "http://localhost:11434/api/generate"


class trachNhiemVaQuyenHanAction(Action):

    def name(self) -> str:
        return "trachNhiemVaQuyenHanAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            doi_tuong = tracker.get_slot("doi_tuong")
            print("doi_tuong", doi_tuong)

            giangVien = next(
                (e["value"] for e in entities if e["entity"] == "GiangVien"), None
            )
            CBCS = next((e["value"] for e in entities if e["entity"] == "CBCS"), None)
            giangVienThinhGiang = next(
                (e["value"] for e in entities if e["entity"] == "GiangVienThinhGiang"),
                None,
            )
            answers = None
            entity = ""

            if giangVien:
                entity = "GiangVien"
            elif CBCS:
                entity = "CBCS"
            elif giangVienThinhGiang:
                entity = "GiangVienThinhGiang"
            if entity:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entity}"}})-[:BELONG_TO]->(i:Intent {{name:"TrachNhiemVaQuyenHan"}})<-[:HAS_INTENT]-(do:DOCUMENT)'
                    f" return a,do,di LIMIT 1;"
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
            if answers:
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            # drv.close()
        return [SlotSet("doi_tuong", None)]


class TrachNhiemTiepCBCSAction(Action):

    def name(self) -> str:
        return "trachNhiemTiepCBCSAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            doi_tuong = tracker.get_slot("doi_tuong_tiep_CSCS")
            print("doi_tuong_tiep_CSCS", doi_tuong)
            hieuTruong = next(
                (e["entity"] for e in entities if e["entity"] == "HieuTruong"), None
            )
            thuTruong = next(
                (e["entity"] for e in entities if e["entity"] == "ThuTruong"), None
            )

            if hieuTruong or thuTruong:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{hieuTruong or thuTruong}"}})-[:BELONG_TO]->(i:Intent {{name:"TrachNhiemTiepCBCS"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
                ).data()

                if result:
                    answers = [record["a"]["answer"] for record in result]
                    documents = [record["do"]["text"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    dispatcher.utter_message(
                        text=format_answer(law, answers, documents)
                    )
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
        # drv.close()
        return [SlotSet("doi_tuong_tiep_CSCS", None)]


class PhamViGiaiQuyetCongViecAction(Action):

    def name(self) -> str:
        return "phamViGiaiQuyetCongViecAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            doi_tuong = tracker.get_slot("doi_tuong")
            print("doi_tuong", doi_tuong)
            thuTruong = next(
                (e["value"] for e in entities if e["entity"] == "ThuTruong"), None
            )
            phoThuTruong = next(
                (e["value"] for e in entities if e["entity"] == "PhoThuTruong"), None
            )
            answers = None
            entity = ""

            if thuTruong:
                entity = "ThuTruong"
            elif phoThuTruong:
                entity = "PhoThuTruong"
            if entity:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entity}"}})-[:BELONG_TO]->(i:Intent {{name:"PhamViGiaiQuyetCongViec"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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
            if answers:
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            # drv.close()
        return [SlotSet("doi_tuong", None)]


class QuyTrinhXayDungChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "quyTrinhXayDungChuongTrinhCongTacAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            # entities = tracker.latest_message["entities"]
            time = tracker.get_slot("time")
            print("time", time)
            entityTime = session.run(
                f"MATCH (e:Entity)"
                f" WITH e, apoc.text.levenshteinSimilarity(e.text, '{time}') AS similarity"
                f" ORDER BY similarity DESC LIMIT 1 RETURN e"
            ).data()
            print("result", entityTime)
            if entityTime and len(entityTime) > 0:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entityTime[0]["e"]["name"]}"}})-[:BELONG_TO]->(i:Intent {{name:"QuyTrinhXayDungChuongTrinhCongTac"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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
                    khoan = [
                        record["a"]["khoan"] if record["a"]["khoan"] else None
                        for record in result
                    ]
                    if answers:
                        dispatcher.utter_message(
                            text=format_answer(law, answers, documents, khoan)
                        )
                    else:
                        dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
                    # drv.close()
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
        return [SlotSet("time", None)]


class hoiVeDieuAction(Action):

    def name(self) -> str:
        return "hoiVeDieuAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]

            article_number = next(
                (e["value"] for e in entities if e["entity"] == "article_number"), None
            )
            document_name = next(
                (e["value"] for e in entities if e["entity"] == "document_name"), None
            )
            print("ayz", article_number)
            print("agxxx", document_name)

            if article_number and document_name:
                listDoc = session.run(
                    f"MATCH (do:DOCUMENT)"
                    f' WITH do, apoc.text.levenshteinSimilarity(do.name, "{document_name}") AS similarity '
                    f"ORDER BY similarity DESC LIMIT 1 "
                    f"RETURN do.name AS name;"
                ).data()
                print("listDoc", listDoc)
                if len(listDoc) > 0:
                    document_name = listDoc[0]["name"]
                result = session.run(
                    f'MATCH (di:DIEU {{name:"Điều {article_number}"}})-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent)<-[:HAS_INTENT]-(do:DOCUMENT)'
                    f' WHERE do.name="{document_name}" ORDER BY a.khoan ASC '
                    f"RETURN a,di,do;"
                ).data()
                print("result", result)
                if result:
                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    document = [record["do"]["text"] for record in result]
                    dispatcher.utter_message(text=format_answer(law, answers, document))
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)

        return []


class ActionFallbackHandler(Action):
    def name(self) -> Text:
        return "action_fallback_handler"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("name")
        if intent == "nlu_fallback":
            dispatcher.utter_message(
                "Xin lỗi tôi không thể hiểu ý định của bạn! Bạn có thể thử hỏi lại hoặc liên hệ với bộ phận hỗ trợ để được giúp đỡ."
            )
        else:
            dispatcher.utter_message(
                "Xin lỗi, có vẻ như tôi không thể giúp bạn với điều đó."
            )
        return []


class ActionPhoGPTFallback(Action):

    def name(self) -> Text:
        return "action_phogpt_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")

        try:
            response = requests.post(
                GPT4ALL_API, json={"message": user_message}, timeout=20
            )
            response.raise_for_status()
            print("PhoGPT API response:", response.json())
            answer = response.json().get("text", "")
            if not answer:
                answer = "Mình chưa có đủ thông tin để trả lời câu hỏi này."

        except Exception as e:
            print("Error occurred while calling PhoGPT API", e)
            answer = "Hệ thống AI nâng cao đang tạm thời không khả dụng."

        dispatcher.utter_message(text=answer)
        return []


class ActionAskOllamaPhoGPT(Action):

    def name(self) -> Text:
        return "action_fallback_ollama_phogpt"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # 1. Lấy tin nhắn người dùng
        user_message = tracker.latest_message.get("text")

        print("tracker", tracker.latest_message)

        # 2. Cấu hình API endpoint của Ollama
        ollama_url = OLLAMA_URL

        # 3. Tạo payload
        # Lưu ý: stream=False để Rasa đợi lấy toàn bộ câu trả lời rồi mới hiển thị
        payload = {
            "model": "phogpt",
            "prompt": user_message,
            "stream": False,
            "options": {
                "num_predict": 256,  # Giới hạn độ dài câu trả lời để phản hồi nhanh
                "temperature": 0.2,  # Giữ cho câu trả lời ổn định
                "num_ctx": 2048,  # Độ dài ngữ cảnh
            },
        }

        try:
            # 4. Gửi request
            # Timeout thấp để tránh treo chatbot nếu model xử lý quá lâu
            response = requests.post(ollama_url, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "")

                # Xử lý làm sạch câu trả lời nếu cần
                if not bot_response.strip():
                    bot_response = "Xin lỗi, tôi chưa nghĩ ra câu trả lời."

                dispatcher.utter_message(text=bot_response)
            else:
                dispatcher.utter_message(text=f"Lỗi kết nối AI: {response.status_code}")

        except Exception as e:
            print("Da vao nhung bi loi")
            dispatcher.utter_message(
                text=f"Hệ thống đang bận, vui lòng thử lại sau. ({str(e)})"
            )

        return []
