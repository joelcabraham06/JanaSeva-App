import React from 'react';
import { LayoutDashboard, FileText, BarChart3, Smartphone, ShieldCheck, LogOut } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, onLogout }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'services', label: 'Services Catalog', icon: FileText },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'simulator', label: 'WhatsApp Simulator', icon: Smartphone },
    { id: 'audit', label: 'Audit Logs', icon: ShieldCheck }
  ];

  return (
    <div className="sidebar">
      <div className="brand">
        <span>🏛️ Janaseva</span>
        <span className="brand-badge">PRO</span>
      </div>

      <nav className="nav-menu">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </div>
          );
        })}
      </nav>

      <div style={{ marginTop: 'auto' }}>
        <div className="nav-item" onClick={onLogout} style={{ color: '#F43F5E' }}>
          <LogOut size={18} />
          <span>Sign Out</span>
        </div>
      </div>
    </div>
  );
}
