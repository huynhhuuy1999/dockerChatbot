MESSAGE_FAILURE_RESPONSE = "Xin lỗi tôi không thể trả lời câu hỏi của bạn"


def format_answer(law, answers, document, khoan=None):
    try:
        # check answers hợp lệ
        if not answers or not isinstance(answers, (list, tuple)) or not document:
            raise ValueError
        if len(answers) > 1:
            answer_text = "\n".join(
                f"- {a}" for a in answers if isinstance(a, str) and a.strip()
            )
        else:
            answer_text = answers[0]
        # nếu có law thì thêm "Căn cứ ..."
        if law and isinstance(law, (list, tuple)) and len(law) > 0:
            if khoan and isinstance(khoan, (list, tuple)) and len(khoan) > 0:
                return f"Căn cứ {law[0]['name'].lower()}, khoản {khoan[0]} trong {document[0]}:\n{answer_text}"
            return f"Căn cứ {law[0]['name'].lower()} {law[0]['content']} trong {document[0]}:\n{answer_text}"
        # không có law → chỉ trả về answer
        return answer_text
    except Exception:
        return "Xin lỗi tôi không thể trả lời câu hỏi của bạn"
