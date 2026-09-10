import React, { useState } from 'react';
import { sendSimulatorMessage } from '../services/api';
import { Send, Mic, RefreshCw } from 'lucide-react';

export default function WhatsAppSimulator() {
  const [phone, setPhone] = useState('919876543210');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: '🙏 *Janaseva - Government Service Assistant*\nജനസേവ സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:\n\nWelcome! Choose your preferred language:',
      buttons: [
        { id: 'lang_ml', title: 'മലയാളം (Malayalam)' },
        { id: 'lang_en', title: 'English' }
      ]
    }
  ]);

  const handleSendMessage = async (customText = null, buttonId = null) => {
    const textToSend = customText !== null ? customText : input;
    if (!textToSend && !buttonId) return;

    const userMsg = { sender: 'user', text: buttonId || textToSend };
    setMessages((prev) => [...prev, userMsg]);
    if (customText === null && !buttonId) setInput('');

    setLoading(true);
    try {
      const res = await sendSimulatorMessage(phone, textToSend || buttonId, buttonId ? 'button_reply' : 'text');
      const botMsg = {
        sender: 'bot',
        text: res.reply_text,
        buttons: res.interactive_buttons || []
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '⚠️ Connection error with Janaseva Backend API.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceNoteMock = async () => {
    const userMsg = { sender: 'user', text: '🎤 [Voice Note: "license puthukkanam"]' };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    try {
      const res = await sendSimulatorMessage(phone, 'license puthukkanam', 'text');
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: res.reply_text, buttons: res.interactive_buttons || [] }
      ]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: 'bot', text: '⚠️ Error processing voice note.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([
      {
        sender: 'bot',
        text: '🙏 *Janaseva - Government Service Assistant*\nജനസേവ സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:\n\nWelcome! Choose your preferred language:',
        buttons: [
          { id: 'lang_ml', title: 'മലയാളം (Malayalam)' },
          { id: 'lang_en', title: 'English' }
        ]
      }
    ]);
  };

  return (
    <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
      <div className="phone-mockup">
        {/* WhatsApp Phone Bar */}
        <div className="phone-header">
          <div className="user-avatar" style={{ background: '#059669' }}>🏛️</div>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>Janaseva Assistant</div>
            <div style={{ fontSize: '0.75rem', color: '#10B981' }}>Official Govt Bot • Online</div>
          </div>
          <button
            onClick={handleReset}
            style={{ background: 'none', border: 'none', color: '#9CA3AF', cursor: 'pointer' }}
            title="Reset Chat"
          >
            <RefreshCw size={16} />
          </button>
        </div>

        {/* Chat Stream */}
        <div className="phone-chat-body">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-bubble ${msg.sender === 'user' ? 'outgoing' : 'incoming'}`}
            >
              <div>{msg.text}</div>
              {msg.buttons && msg.buttons.length > 0 && (
                <div className="chat-buttons">
                  {msg.buttons.map((btn, bIdx) => (
                    <button
                      key={bIdx}
                      className="chat-btn-option"
                      onClick={() => handleSendMessage(btn.title, btn.id)}
                    >
                      {btn.title}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="chat-bubble incoming" style={{ fontStyle: 'italic', opacity: 0.7 }}>
              Janaseva is typing...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div style={{ background: '#1F2937', padding: '0.75rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <input
            className="input-field"
            style={{ borderRadius: '20px', padding: '0.5rem 1rem' }}
            placeholder="Type Malayalam / Manglish / English..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button
            onClick={handleVoiceNoteMock}
            style={{ background: '#374151', border: 'none', color: '#10B981', padding: '0.6rem', borderRadius: '50%', cursor: 'pointer' }}
            title="Send Voice Note"
          >
            <Mic size={18} />
          </button>
          <button
            onClick={() => handleSendMessage()}
            style={{ background: '#059669', border: 'none', color: 'white', padding: '0.6rem', borderRadius: '50%', cursor: 'pointer' }}
          >
            <Send size={18} />
          </button>
        </div>
      </div>

      {/* Quick Test Helper Panel */}
      <div className="glass-card" style={{ flex: 1, minWidth: '300px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <h3>⚡ Quick Test Scenarios</h3>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Click any sample query to test live response resolution:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('license puthukkanam')}>
            🇲🇱 Manglish: "license puthukkanam"
          </button>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('ലൈസൻസ് പുതുക്കണം')}>
            🇱🇰 Malayalam: "ലൈസൻസ് പുതുക്കണം"
          </button>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('renew driving licence')}>
            🇬🇧 English: "renew driving licence"
          </button>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('passport edukkanam')}>
            🇲🇱 Manglish: "passport edukkanam"
          </button>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('ration card maattanum')}>
            🇲🇱 Manglish: "ration card maattanum"
          </button>
          <button className="btn btn-secondary" onClick={() => handleSendMessage('aadhaar update')}>
            🇬🇧 English: "aadhaar update"
          </button>
        </div>
      </div>
    </div>
  );
}
