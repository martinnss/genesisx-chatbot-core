document.getElementById('loadHistoryBtn').addEventListener('click', async () => {
  const userId = document.getElementById('userIdInput').value.trim();
  if (!userId) return;

  const res = await fetch(`http://127.0.0.1:5000/history/${userId}`);
  const data = await res.json();
  const list = document.getElementById('convList');
  list.innerHTML = '';

  if (!res.ok) {
    list.innerHTML = `<div class="text-center text-red-600">${data.error || 'No hay historial'}</div>`;
    return;
  }

  data.forEach(convo => {
    const item = document.createElement('div');
    item.textContent = `Conversación ${convo.conversation_id} - ${new Date(convo.created_at).toLocaleString()}`;
    item.className = 'p-3 border rounded cursor-pointer bg-white hover:bg-gray-100 transition shadow-sm';
    item.dataset.convId = convo.conversation_id;
    item.addEventListener('click', () => loadMessages(convo.conversation_id));
    list.appendChild(item);
  });
});

async function loadMessages(conversationId) {
  const res = await fetch(`http://127.0.0.1:5000/conversation/${conversationId}`);
  const msgs = await res.json();
  const area = document.getElementById('messagesArea');
  area.innerHTML = '';

  if (!res.ok) {
    area.innerHTML = `<div class="text-center text-red-600">${msgs.error || 'Error al cargar mensajes'}</div>`;
    return;
  }

  msgs.forEach(m => {
    const wrapper = document.createElement('div');
    const bubble = document.createElement('div');

    if (m.sender === 'user') {
      wrapper.className = 'flex justify-end';
      bubble.className =
        'inline-block bg-[#805bff] text-white text-sm px-4 py-2 rounded-2xl max-w-[75%] shadow-md';
    } else {
      wrapper.className = 'flex justify-start';
      bubble.className =
        'inline-block bg-white text-gray-800 text-sm px-4 py-2 rounded-2xl border border-gray-200 max-w-[75%] shadow';
    }

    bubble.textContent = `${m.sender === 'user' ? 'Tú' : 'Bot'}: ${m.content}`;
    wrapper.appendChild(bubble);
    area.appendChild(wrapper);
  });

  area.scrollTop = area.scrollHeight;
}
