// UserMessage.js
import React from 'react';

const UserMessage = ({ message }) => (
  <div className="chat-message user">
    <div className="avatar">
      <img src="" alt="User Avatar" />
    </div>
    <div className="message">{message}</div>
  </div>
);

export default UserMessage;
