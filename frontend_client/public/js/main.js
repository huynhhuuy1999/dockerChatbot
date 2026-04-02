
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotContainer = document.getElementById('chatbotContainer');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInputForm = document.getElementById('chatbotInputForm');
    const chatbotInput = document.getElementById('chatbotInput');
  
    // Hiển thị/ẩn chatbot
    chatbotToggle.addEventListener('click', () => {
      chatbotContainer.style.display = 'flex';
      chatbotInput.focus();
      loadChatHistory();
    });
    chatbotClose.addEventListener('click', () => {
      chatbotContainer.style.display = 'none';
    });
  
    // Lưu và tải lịch sử chat trong sessionStorage
    function saveChatHistory() {
      const messages = [];
      chatbotMessages.querySelectorAll('.chatbot-message').forEach(msg => {
        messages.push({
          text: msg.textContent,
          sender: msg.classList.contains('user') ? 'user' : 'bot'
        });
      });
      sessionStorage.setItem('chatbotHistory', JSON.stringify(messages));
    }
  
    function loadChatHistory() {
      chatbotMessages.innerHTML = '';
      const history = sessionStorage.getItem('chatbotHistory');
      if (history) {
        const messages = JSON.parse(history);
        messages.forEach(msg => addMessage(msg.text, msg.sender, false));
        scrollToBottom();
      } else {
        // Tin nhắn chào mừng
        addMessage('Xin chào! Tôi là trợ lý ảo của Cổng Thông Tin Đảng Bộ. Bạn cần hỗ trợ gì?', 'bot', false);
      }
    }
  
    // Thêm tin nhắn vào khung chat
    function addMessage(text, sender, save = true) {
      const msgDiv = document.createElement('div');
      msgDiv.classList.add('chatbot-message', sender);
      msgDiv.textContent = text;
      chatbotMessages.appendChild(msgDiv);
      scrollToBottom();
      if (save) saveChatHistory();
    }
  
    // Cuộn xuống dưới cùng
    function scrollToBottom() {
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
  
    // Tự động điều chỉnh chiều cao textarea
    chatbotInput.addEventListener('input', () => {
      chatbotInput.style.height = 'auto';
      chatbotInput.style.height = chatbotInput.scrollHeight + 'px';
    });
  
    // Xử lý gửi tin nhắn
    chatbotInputForm.addEventListener('submit', e => {
      e.preventDefault();
      const userText = chatbotInput.value.trim();
      if (!userText) return;
      addMessage(userText, 'user');
      chatbotInput.value = '';
      chatbotInput.style.height = 'auto';
      botReply(userText);
    });
  
    // Xử lý gửi tin nhắn bằng Enter (không xuống dòng)
    chatbotInput.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatbotInputForm.requestSubmit();
      }
    });
  
    // Hàm trả lời chatbot nâng cao
    function botReply(userText) {
      const text = userText.toLowerCase();
  
      // Các câu trả lời mẫu
      const responses = [
        {
          keywords: ['xin chào', 'chào bạn', 'hello', 'hi'],
          reply: 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?'
        },
        {
          keywords: ['giờ làm việc', 'làm việc', 'thời gian làm việc'],
          reply: 'Giờ làm việc của Đảng bộ là từ 8h sáng đến 5h chiều, từ thứ 2 đến thứ 6.'
        },
        {
          keywords: ['liên hệ', 'địa chỉ', 'số điện thoại', 'email'],
          reply: 'Bạn có thể liên hệ với chúng tôi qua email: support@dangbo.vn hoặc số điện thoại: 0123 456 789.'
        },
        {
          keywords: ['văn bản', 'tài liệu', 'quy định'],
          reply: 'Bạn có thể truy cập mục "Văn bản" trên trang để xem các tài liệu và quy định mới nhất.'
        },
        {
          keywords: ['hoạt động', 'sự kiện', 'chương trình'],
          reply: 'Các hoạt động và sự kiện của Đảng bộ được cập nhật thường xuyên tại mục "Hoạt động".'
        },
        {
          keywords: ['bầu cử', 'đại biểu', 'quốc hội'],
          reply: 'Thông tin về bầu cử đại biểu Quốc hội được đăng tải chi tiết trong mục Tin tức.'
        }
      ];
  
      // Tìm câu trả lời phù hợp
      let matched = false;
      for (const item of responses) {
        if (item.keywords.some(k => text.includes(k))) {
          matched = true;
          setTimeout(() => addMessage(item.reply, 'bot'), 800);
          break;
        }
      }
  
      // Nếu không hiểu, gợi ý câu hỏi mẫu
      if (!matched) {
        setTimeout(() => {
          addMessage(
            'Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi về: "giờ làm việc", "liên hệ", "văn bản", "hoạt động", "bầu cử"...',
            'bot'
          );
        }, 800);
      }
    }
