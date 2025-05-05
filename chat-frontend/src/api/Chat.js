const API_URL = "http://localhost:8002/chat/api/v1";

export const get_chat_messages = async (chatId, token) => {
    const response = await fetch(`${API_URL}/${chatId}/messages?token=${token}`);
    if (!response.ok) {
      throw new Error('Failed to fetch messages');
    }
    return await response.json();
  };
  

  export const get_chat_by_participants = async (participants, token) => {
    const response = await fetch(`${API_URL}/?participants=${encodeURIComponent(participants[0])}&token=${token}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch chat');
    }
    return await response.json();
  };


  export const create_chat = async (participants, token) => {
    const response = await fetch(`${API_URL}/?token=${token}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ participants: participants }),
    });
    if (!response.ok) {
      throw new Error('Failed to create chat');
    }
    return await response.json();
  };