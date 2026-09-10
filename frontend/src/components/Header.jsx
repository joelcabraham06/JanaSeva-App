import React from 'react';

export default function Header({ title, subtitle, adminName = "Admin" }) {
  return (
    <header className="top-header">
      <div>
        <h1 className="page-title">{title}</h1>
        <p className="page-subtitle">{subtitle}</p>
      </div>

      <div className="user-profile">
        <div className="user-avatar">{adminName.charAt(0).toUpperCase()}</div>
        <div>
          <div style={{ fontSize: '0.875rem', fontWeight: 600 }}>{adminName}</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Super Admin</div>
        </div>
      </div>
    </header>
  );
}
