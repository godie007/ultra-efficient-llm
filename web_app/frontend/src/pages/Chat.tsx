import { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { chat } from '../services/api';
import { ChatMessage } from '../types';
import { DEFAULT_TOP_K } from '../config';
import MessageBubble from '../components/MessageBubble';

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const send = async () => {
    const message = input.trim();
    if (!message || loading) return;

    setMessages((prev) => [...prev, { role: 'user', content: message }]);
    setInput('');
    setLoading(true);

    try {
      const response = await chat(message, DEFAULT_TOP_K);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.answer, sources: response.sources },
      ]);
    } catch {
      toast.error('Error al consultar el asistente. ¿Está corriendo el backend?');
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '⚠️ No pude generar una respuesta.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto flex flex-col h-[calc(100vh-7rem)]">
      <h1 className="text-2xl font-bold text-gradient mb-4">Chat</h1>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.length === 0 && (
          <div className="card-neutral text-center text-slate-300">
            <Bot className="h-10 w-10 mx-auto mb-3 text-blue-400" />
            Pregunta algo sobre tus fuentes de conocimiento. El asistente recupera los documentos
            relevantes y responde a partir de ellos.
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800/80 border border-slate-600/40 rounded-2xl p-4 flex items-center gap-2 text-slate-300">
              <Loader2 className="h-4 w-4 animate-spin text-blue-400" /> Pensando...
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <div className="mt-4 flex gap-2 items-end">
        <textarea
          className="input-field resize-none"
          rows={2}
          placeholder="Escribe tu pregunta... (Enter para enviar, Shift+Enter para nueva línea)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button className="btn-primary" onClick={send} disabled={loading || !input.trim()}>
          <Send className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default Chat;
