import { Link, useLocation } from 'react-router-dom';
import { Bot, MessageSquare, BookOpen } from 'lucide-react';

const Navbar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Chat', icon: MessageSquare },
    { path: '/sources', label: 'Fuentes de conocimiento', icon: BookOpen },
  ];

  return (
    <nav className="bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50 shadow-2xl sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="p-2 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 rounded-lg backdrop-blur-sm border border-blue-400/30 group-hover:border-blue-400/50 transition-all duration-300">
              <Bot className="h-6 w-6 text-blue-400" />
            </div>
            <span className="text-xl font-bold text-gradient group-hover:text-glow transition-all duration-300">
              Asistente RAG
            </span>
          </Link>

          <div className="flex items-center space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-bold transition-all duration-300 backdrop-blur-sm ${
                    isActive
                      ? 'bg-blue-500/20 text-blue-400 border border-blue-400/30 shadow-lg'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
