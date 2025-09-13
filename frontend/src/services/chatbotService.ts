import { api } from './api';

export const chatbotService = {
  sendMessage: async (message: string) => {
    const response = await api.post('/chatbot/message', { message });
    return response.data.response;
  },

  getChatHistory: async () => {
    const response = await api.get('/chatbot/history');
    return response.data;
  },
};