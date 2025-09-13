import React from 'react';
import { useAuth } from '../context/AuthContext';
import Chatbot from '../components/Chatbot';
import './ChatbotPage.css';

const ChatbotPage: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return <div>Please log in to use the AI assistant.</div>;
  }

  return (
    <div className="chatbot-page">
      <div className="chatbot-header">
        <h1>AI Phishing Awareness Assistant</h1>
        <p>
          Get personalized help and answers to your phishing-related questions. 
          The assistant is aware of your current learning level and progress.
        </p>
      </div>

      <div className="chatbot-container-wrapper">
        <Chatbot />
      </div>

      <div className="chatbot-tips">
        <h2>Tips for using the AI Assistant</h2>
        <div className="tips-grid">
          <div className="tip-card">
            <div className="tip-icon">💡</div>
            <h3>Ask specific questions</h3>
            <p>Example: "What are the signs of a phishing email?"</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">🔍</div>
            <h3>Request examples</h3>
            <p>Example: "Show me examples of phishing URLs"</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">🛡️</div>
            <h3>Get protection advice</h3>
            <p>Example: "How can I protect myself from spear phishing?"</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">📚</div>
            <h3>Course-related help</h3>
            <p>Example: "Explain module 3 from the beginner course"</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;