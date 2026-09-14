import React, { useEffect, useState } from 'react';
import { fetchAuditLogs } from '../services/api';
import { ShieldCheck, Clock } from 'lucide-react';

export default function AuditLogs({ token }) {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAuditLogs(token)
      .then((res) => setLogs(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <ShieldCheck color="var(--accent-primary)" size={24} />
        <h3>Administrative Security Audit Logs</h3>
      </div>

      {loading ? (
        <div>Loading audit history...</div>
      ) : (
        <table className="custom-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Admin User</th>
              <th>Action</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <Clock size={12} /> {new Date(log.timestamp).toLocaleString()}
                  </div>
                </td>
                <td style={{ fontWeight: 600 }}>{log.admin_username}</td>
                <td>
                  <span className="brand-badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818CF8' }}>
                    {log.action}
                  </span>
                </td>
                <td style={{ color: 'var(--text-secondary)' }}>{log.details}</td>
              </tr>
            ))}
            {logs.length === 0 && (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No audit events recorded yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
