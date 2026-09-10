import React from 'react';
import { Edit2, Trash2, Globe, Clock, FileText, CheckCircle } from 'lucide-react';

export default function ServiceCard({ service, onEdit, onDelete }) {
  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-secondary)', fontWeight: 600 }}>
            {service.category}
          </span>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginTop: '0.2rem' }}>
            {service.name_en}
          </h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontFamily: 'Noto Sans Malayalam' }}>
            {service.name_ml}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            className="btn btn-secondary"
            style={{ padding: '0.4rem 0.6rem' }}
            onClick={() => onEdit(service)}
          >
            <Edit2 size={14} />
          </button>
          <button
            className="btn btn-secondary"
            style={{ padding: '0.4rem 0.6rem', color: 'var(--accent-rose)' }}
            onClick={() => onDelete(service.id)}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
        {service.description_en}
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <Clock size={14} color="var(--accent-amber)" />
          <span>{service.processing_time_days} Days</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <FileText size={14} color="var(--accent-emerald)" />
          <span>Fee: {service.application_fee}</span>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.5rem', borderTop: '1px solid var(--border-color)', fontSize: '0.75rem' }}>
        <a
          href={service.official_website}
          target="_blank"
          rel="noreferrer"
          style={{ color: 'var(--accent-primary)', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
        >
          <Globe size={12} /> {service.official_website.replace('https://', '')}
        </a>
        <span style={{ color: service.is_active ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: 600 }}>
          {service.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>
    </div>
  );
}
