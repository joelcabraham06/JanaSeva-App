import React, { useEffect, useState } from 'react';
import { fetchAnalytics } from '../services/api';
import { Users, MessageSquare, TrendingUp, Star, Award, Zap } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics()
      .then((res) => setData(res))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* KPI Cards */}
      <div className="metrics-grid">
        <div className="glass-card metric-card">
          <div className="metric-header">
            <span>Total Citizens</span>
            <div className="metric-icon"><Users size={20} /></div>
          </div>
          <div className="metric-value">{data?.total_users || 148}</div>
          <span style={{ fontSize: '0.8rem', color: 'var(--accent-emerald)' }}>+18% from last week</span>
        </div>

        <div className="glass-card metric-card">
          <div className="metric-header">
            <span>Daily Requests</span>
            <div className="metric-icon" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-secondary)' }}>
              <MessageSquare size={20} />
            </div>
          </div>
          <div className="metric-value">{data?.daily_requests_today || 42}</div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Active WhatsApp sessions</span>
        </div>

        <div className="glass-card metric-card">
          <div className="metric-header">
            <span>Satisfaction Rate</span>
            <div className="metric-icon" style={{ background: 'rgba(245, 158, 11, 0.15)', color: 'var(--accent-amber)' }}>
              <Star size={20} />
            </div>
          </div>
          <div className="metric-value">{data?.satisfaction_rate_pct || 96}%</div>
          <span style={{ fontSize: '0.8rem', color: 'var(--accent-emerald)' }}>High User Trust</span>
        </div>

        <div className="glass-card metric-card">
          <div className="metric-header">
            <span>Verified Services</span>
            <div className="metric-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: 'var(--accent-emerald)' }}>
              <Award size={20} />
            </div>
          </div>
          <div className="metric-value">17 Core</div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Malayalam & English</span>
        </div>
      </div>

      {/* Popular Services & Language Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem', flexWrap: 'wrap' }}>
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>🔥 Most Requested Government Services</h3>
          <table className="custom-table">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Malayalam Name</th>
                <th>Requests</th>
              </tr>
            </thead>
            <tbody>
              {data?.popular_services.map((item, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600 }}>{item.name_en}</td>
                  <td style={{ fontFamily: 'Noto Sans Malayalam' }}>{item.name_ml}</td>
                  <td>
                    <span className="brand-badge" style={{ background: 'rgba(99, 102, 241, 0.2)', color: '#818CF8' }}>
                      {item.request_count} queries
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>🌐 Preferred Language</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                <span>Malayalam (മലയാളം)</span>
                <span style={{ fontWeight: 700 }}>68%</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.1)', height: '8px', borderRadius: '4px' }}>
                <div style={{ background: 'var(--accent-primary)', width: '68%', height: '100%', borderRadius: '4px' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                <span>Manglish</span>
                <span style={{ fontWeight: 700 }}>22%</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.1)', height: '8px', borderRadius: '4px' }}>
                <div style={{ background: 'var(--accent-secondary)', width: '22%', height: '100%', borderRadius: '4px' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                <span>English</span>
                <span style={{ fontWeight: 700 }}>10%</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.1)', height: '8px', borderRadius: '4px' }}>
                <div style={{ background: 'var(--accent-emerald)', width: '10%', height: '100%', borderRadius: '4px' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
