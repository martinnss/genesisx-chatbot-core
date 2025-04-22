let currentConversationId = null;

document.getElementById('chatForm').addEventListener('submit', async e => {
  e.preventDefault();
  const userId = document.getElementById('userIdInput').value.trim();
  const message = document.getElementById('messageInput').value.trim();
  if (!userId || !message) return;

  appendMessage('Tú', message);
  document.getElementById('messageInput').value = '';

  const payload = { user_id: userId, message, conversation_id: currentConversationId };
  const res = await fetch('http://127.0.0.1:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  if (res.ok) {
    appendMessage('Bot', data.reply);
    if (!currentConversationId) currentConversationId = data.conversation_id;
  } else {
    appendMessage('Error', data.error || 'Falló la petición');
  }
});

function appendMessage(who, text) {
  const area = document.getElementById('chatArea');
  const wrapper = document.createElement('div');
  const bubble = document.createElement('div');

  if (who === 'Tú') {
    wrapper.className = 'flex justify-end mb-3';
    bubble.className =
      'inline-block bg-[#805bff] text-white text-sm px-4 py-2 rounded-2xl max-w-[75%] shadow-md';
  } else if (who === 'Bot') {
    wrapper.className = 'flex justify-start mb-3';
    bubble.className =
      'inline-block bg-white text-gray-800 text-sm px-4 py-2 rounded-2xl border border-gray-200 max-w-[75%] shadow';
  } else {
    wrapper.className = 'flex justify-center mb-3';
    bubble.className =
      'inline-block bg-red-100 text-red-600 text-sm px-4 py-2 rounded-2xl border border-red-200 max-w-[75%] shadow';
  }

  bubble.textContent = text;
  wrapper.appendChild(bubble);
  area.appendChild(wrapper);
  area.scrollTop = area.scrollHeight;
}

