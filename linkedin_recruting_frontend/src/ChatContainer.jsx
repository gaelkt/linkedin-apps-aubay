import React from 'react';
import './ChatContainer.css';

const ChatContainer = ({ query, response }) => {
  return (
    <div className="chat-message-container">
      {/* Message de l'utilisateur */}
      <div className="user-message">
        <p>{query}</p>
      </div>
      
      {/* Réponse de l'API */}
      <div className="api-response">
        <p>{response}</p>
      </div>
    </div>
  );
};

export default ChatContainer;
