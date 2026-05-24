import { User, Bot, BookOpen } from 'lucide-react';
import { ChatMessage } from '../types';

interface Props {
  message: ChatMessage;
}

const MessageBubble: React.FC<Props> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] rounded-2xl p-4 ${
        isUser
          ? 'bg-blue-600/30 border border-blue-500/40'
          : 'bg-slate-800/80 border border-slate-600/40'
      }`}>
        <div className="flex items-center gap-2 mb-2 text-xs font-bold text-slate-400">
          {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4 text-blue-400" />}
          {isUser ? 'Tú' : 'Asistente'}
        </div>
        <p className="text-slate-100 whitespace-pre-wrap">{message.content}</p>

        {message.sources && message.sources.length > 0 && (
          <details className="mt-3">
            <summary className="cursor-pointer text-xs font-bold text-slate-400 flex items-center gap-1">
              <BookOpen className="h-3 w-3" /> Fuentes usadas ({message.sources.length})
            </summary>
            <ul className="mt-2 space-y-2">
              {message.sources.map((source, i) => (
                <li key={i} className="text-xs text-slate-300 bg-slate-900/60 rounded-lg p-2 border border-slate-700/50">
                  <span className="badge badge-primary mr-2">{source.score.toFixed(2)}</span>
                  {source.text}
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
