// BotMessage.js
import React from 'react';

const BotMessage = ({ message }) => (
  <div className="chat-message bot">
    <div className="avatar">
      <img src="" alt="Bot Avatar" />
    </div>
    <div className="message" dangerouslySetInnerHTML={{ __html: message }} />
  </div>
);

export default BotMessage;
