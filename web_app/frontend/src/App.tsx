
import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Training from './pages/Training';

import ModelStatus from './pages/ModelStatus';
import ModelManagement from './pages/ModelManagement';
import ChatbotReasoning from './pages/ChatbotReasoning';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900">
      <Navbar />
      <main className="container mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/training" element={<Training />} />

          <Route path="/status" element={<ModelStatus />} />
          <Route path="/models" element={<ModelManagement />} />
          <Route path="/chatbot" element={<ChatbotReasoning />} />
        </Routes>
      </main>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'rgba(30, 41, 59, 0.95)',
            color: '#f1f5f9',
            border: '1px solid rgba(71, 85, 105, 0.3)',
            backdropFilter: 'blur(10px)',
            borderRadius: '12px',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
          },
        }}
      />
    </div>
  );
}

export default App; 