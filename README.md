# Chatbot Docker Project

## 1. Giới thiệu

Tài liệu này hướng dẫn cách thiết lập, chạy và cập nhật project chatbot sử dụng Docker.

---

## 2. Yêu cầu

- Đã cài đặt Docker
- Đã cài đặt Docker Compose

---

## 3. Setup Docker

Nếu chưa cài Docker, hãy cài đặt trước khi thực hiện các bước bên dưới.

---

## 4. Load Docker Image từ file `.tar`

Sử dụng lệnh sau để load image đã được đóng gói:

```bash
docker load -i chatbot_offline_project.tar
```

---

## 5. Khởi chạy hệ thống

Sau khi load image, chạy lệnh sau để khởi động toàn bộ services:

```bash
docker-compose up -d --build
```

### Giải thích:

- `-d`: chạy container ở chế độ nền (detached)
- `--build`: build lại image nếu có thay đổi

---

## 6. Cập nhật dữ liệu từ file `.dump`

Đảm bảo file dump (ví dụ: `dump.cypher`) nằm trong thư mục `import` của Neo4j.

Chạy lệnh sau để import dữ liệu:

```bash
cypher-shell -u neo4j -p 123456789 -f /var/lib/neo4j/import/dump.cypher
```

---

## 7. Xóa container và volume (khi update source code)

Khi cần cập nhật lại source code hoặc reset database, sử dụng lệnh:

```bash
docker-compose down -v
```

### Lưu ý:

- Lệnh này sẽ xóa toàn bộ dữ liệu trong database (volume)

---

## 8. Đóng gói Docker Image

Để export toàn bộ image thành file `.tar`, sử dụng lệnh:

```bash
docker save -o chatbot_project.tar \
neo4j:latest \
rasachatbot-frontend:latest \
rasachatbot-rasa:latest \
rasachatbot-action_server:latest \
rasachatbot-backend:latest \
rasachatbot-frontend_client:latest
```

---

## 9. Ghi chú

- Đảm bảo các container chạy ổn định trước khi export
- Kiểm tra dung lượng file `.tar` vì có thể rất lớn
- Khi sử dụng dữ liệu di động, nên hạn chế build lại image để tiết kiệm băng thông

---

## 10. Troubleshooting

### Container không chạy:

```bash
docker ps -a
```

### Xem log container:

```bash
docker logs <container_name>
```

### Restart container:

```bash
docker-compose restart
```
