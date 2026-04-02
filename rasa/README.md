# Chatbot K4 - README

## 0. Cài version python với venv

```bash
uv venv --python 3.10.18
```

## 1. Cài đặt các thư viện cần thiết

Cài đặt toàn bộ thư viện của dự án:

```bash
pip install -r requirements.txt
```

---

## 2. Nạp key Rasa

Trước khi chạy chatbot cần nạp key bản quyền:

```bash
export RASA_LICENSE=YOUR_KEY
```

---

## 3. Chạy PhoGPT (Ollama)

Khởi động dịch vụ mô hình:

```bash
ollama serve
```

---

## 4. Chạy các dịch vụ của Chatbot

### 4.1 Chạy Action Server

```bash
rasa run actions
```

### 4.2 Chạy Rasa Server

```bash
rasa run --enable-api --cors "*" --debug
```

### 4.3 Test chatbot bằng terminal

```bash
rasa shell
```

---

## 5. Chạy ứng dụng Web (Python + HTML)

Khởi động server web:

```bash
python app.py
```

---

## 6. Quy trình chạy hệ thống (khuyến nghị)

Chạy lần lượt các bước sau:

1.  Khởi động PhoGPT

```bash
ollama serve
```

2.  Chạy Action Server

```bash
rasa run actions
```

3.  Chạy Rasa Server

```bash
rasa run --enable-api --cors "*" --debug
```

4.  Chạy Web App

```bash
python app.py
```

---

## 7. Mục đích hệ thống

Chatbot được xây dựng nhằm:

- Hỗ trợ tra cứu thông tin văn bản khoa K4
- Tự động trả lời các câu hỏi thường gặp
- Giảm thời gian tìm kiếm thông tin cho người dùng
