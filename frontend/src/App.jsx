import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Services from './pages/Services';
import Analytics from './pages/Analytics';
import WhatsAppSimulator from './components/WhatsAppSimulator';
import AuditLogs from './pages/AuditLogs';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('janaseva_token') || '');
  const [activeTab, setActiveTab] = useState('dashboard');

  const handleLoginSuccess = (newToken) => {
    setToken(newToken);
    localStorage.setItem('janaseva_token', newToken);
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('janaseva_token');
  };

  if (!token) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'services':
        return <Services token={token} />;
      case 'analytics':
        return <Analytics />;
      case 'simulator':
        return <WhatsAppSimulator />;
      case 'audit':
        return <AuditLogs token={token} />;
      default:
        return <Dashboard />;
    }
  };

  const titles = {
    dashboard: { title: 'Executive Overview', subtitle: 'Real-time metrics and citizen engagement analytics' },
    services: { title: 'Government Services Catalog', subtitle: 'Manage, edit, or append government procedures & requirements' },
    analytics: { title: 'Analytics & Insights', subtitle: 'Deep dive into language distribution and search statistics' },
    simulator: { title: 'WhatsApp Live Simulator', subtitle: 'Test user flows, Malayalam/Manglish queries, and document readiness in real-time' },
    audit: { title: 'Security Audit Log', subtitle: 'Trace administrative actions and system modifications' }
  };

  const currentHeader = titles[activeTab] || titles.dashboard;

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
      <main className="main-content">
        <Header title={currentHeader.title} subtitle={currentHeader.subtitle} />
        {renderContent()}
      </main>
    </div>
  );
}
