import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2 } from 'lucide-react';

export default function ServiceFormModal({ isOpen, onClose, onSave, initialData }) {
  const [formData, setFormData] = useState({
    slug: '',
    category: '',
    name_en: '',
    name_ml: '',
    description_en: '',
    description_ml: '',
    eligibility_en: '',
    eligibility_ml: '',
    application_fee: '₹100',
    processing_time_days: 7,
    official_website: 'https://',
    office_type: 'Akshaya / RTO',
    aliases_manglish: '',
    documents: [{ doc_name_en: '', doc_name_ml: '', is_mandatory: true }],
    guides: [{ step_number: 1, title_en: '', title_ml: '', description_en: '', description_ml: '' }],
    faqs: [{ question_en: '', question_ml: '', answer_en: '', answer_ml: '' }]
  });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({
        slug: '',
        category: 'Transport',
        name_en: '',
        name_ml: '',
        description_en: '',
        description_ml: '',
        eligibility_en: '',
        eligibility_ml: '',
        application_fee: '₹100',
        processing_time_days: 7,
        official_website: 'https://',
        office_type: 'Akshaya / RTO',
        aliases_manglish: '',
        documents: [{ doc_name_en: '', doc_name_ml: '', is_mandatory: true }],
        guides: [{ step_number: 1, title_en: '', title_ml: '', description_en: '', description_ml: '' }],
        faqs: [{ question_en: '', question_ml: '', answer_en: '', answer_ml: '' }]
      });
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const addDoc = () => {
    setFormData({
      ...formData,
      documents: [...formData.documents, { doc_name_en: '', doc_name_ml: '', is_mandatory: true }]
    });
  };

  const removeDoc = (index) => {
    setFormData({
      ...formData,
      documents: formData.documents.filter((_, i) => i !== index)
    });
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '750px',
        maxHeight: '90vh',
        overflowY: 'auto',
        position: 'relative'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>{initialData ? 'Edit Service' : 'Add New Government Service'}</h2>
          <button className="btn btn-secondary" onClick={onClose} style={{ padding: '0.4rem' }}>
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Service Slug</label>
              <input
                className="input-field"
                value={formData.slug}
                onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                required
                placeholder="e.g. driving-licence-renewal"
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Category</label>
              <input
                className="input-field"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                required
                placeholder="e.g. Transport"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Name (English)</label>
              <input
                className="input-field"
                value={formData.name_en}
                onChange={(e) => setFormData({ ...formData, name_en: e.target.value })}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Name (Malayalam)</label>
              <input
                className="input-field"
                value={formData.name_ml}
                onChange={(e) => setFormData({ ...formData, name_ml: e.target.value })}
                required
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Description (English)</label>
            <textarea
              className="input-field"
              rows={2}
              value={formData.description_en}
              onChange={(e) => setFormData({ ...formData, description_en: e.target.value })}
              required
            />
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Description (Malayalam)</label>
            <textarea
              className="input-field"
              rows={2}
              value={formData.description_ml}
              onChange={(e) => setFormData({ ...formData, description_ml: e.target.value })}
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Application Fee</label>
              <input
                className="input-field"
                value={formData.application_fee}
                onChange={(e) => setFormData({ ...formData, application_fee: e.target.value })}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Processing Time (Days)</label>
              <input
                type="number"
                className="input-field"
                value={formData.processing_time_days}
                onChange={(e) => setFormData({ ...formData, processing_time_days: parseInt(e.target.value) || 7 })}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Office Type</label>
              <input
                className="input-field"
                value={formData.office_type}
                onChange={(e) => setFormData({ ...formData, office_type: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Official Website URL</label>
            <input
              className="input-field"
              value={formData.official_website}
              onChange={(e) => setFormData({ ...formData, official_website: e.target.value })}
              required
            />
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Manglish Search Keywords (Comma separated)</label>
            <input
              className="input-field"
              value={formData.aliases_manglish || ''}
              onChange={(e) => setFormData({ ...formData, aliases_manglish: e.target.value })}
              placeholder="e.g. license puthukkanam, dl renewal"
            />
          </div>

          {/* Required Documents Section */}
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h4 style={{ fontSize: '0.95rem' }}>Required Documents</h4>
              <button type="button" className="btn btn-secondary" style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }} onClick={addDoc}>
                <Plus size={14} /> Add Document
              </button>
            </div>

            {formData.documents.map((doc, idx) => (
              <div key={idx} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <input
                  className="input-field"
                  placeholder="Doc Name (EN)"
                  value={doc.doc_name_en}
                  onChange={(e) => {
                    const newDocs = [...formData.documents];
                    newDocs[idx].doc_name_en = e.target.value;
                    setFormData({ ...formData, documents: newDocs });
                  }}
                />
                <input
                  className="input-field"
                  placeholder="Doc Name (ML)"
                  value={doc.doc_name_ml}
                  onChange={(e) => {
                    const newDocs = [...formData.documents];
                    newDocs[idx].doc_name_ml = e.target.value;
                    setFormData({ ...formData, documents: newDocs });
                  }}
                />
                <button type="button" className="btn btn-secondary" onClick={() => removeDoc(idx)} style={{ padding: '0.4rem' }}>
                  <Trash2 size={14} color="var(--accent-rose)" />
                </button>
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Service</button>
          </div>
        </form>
      </div>
    </div>
  );
}
