import React, { useEffect, useState, useRef } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const token = useSelector((state: RootState) => state.auth.token) || localStorage.getItem('token');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }

    const fetchChatHistory = async () => {
      try {
        const response = await axios.get('http://localhost:8080/chat/chat-history', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessages(response.data.messages);
      } catch (err) {
        console.error('Error fetching chat history', err);
      }
    };

    fetchChatHistory();
  }, [token, navigate]);

  useEffect(() => {
    let socket: WebSocket | null = null;

    const connectWebSocket = () => {
      socket = new WebSocket('wss://echo.websocket.org/');

      socket.onopen = () => {
        console.log('WebSocket connection opened');
      };

      socket.onmessage = (event) => {
        setMessages((prevMessages) => [
          ...prevMessages, 
          { message: event.data, from_user: 'Server', timestamp: new Date() }
        ]);
      };

      socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event.reason);
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      socketRef.current = socket;
    };

    connectWebSocket();

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);

  const sendMessage = async () => {
    if (socketRef.current && message.trim() !== '') {
      socketRef.current.send(message);

      try {
        await axios.post(
          'http://localhost:8080/chat/save-message', 
          { message },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setMessage('');
      } catch (error) {
        console.error('Error saving message:', error);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-4xl h-[80vh] relative">
        <h2 className="text-2xl font-bold mb-4">WebSocket Chat</h2>
        
        <button
          onClick={handleLogout}
          className="absolute top-4 right-4 bg-red-500 text-white p-2 rounded hover:bg-red-600"
        >
          Logout
        </button>

        <div className="mb-4 max-h-[60vh] overflow-y-auto border border-gray-300 rounded p-2">
          {messages.map((msg, index) => (
            <div key={index} className="mb-2">
              <strong>{msg.from_user}: </strong>
              <span>{msg.message}</span>
              <br />
              <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>  {/* Format the timestamp */}
            </div>
          ))}
        </div>

        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="Type a message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 p-2 border border-gray-300 rounded"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            disabled={!message.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
