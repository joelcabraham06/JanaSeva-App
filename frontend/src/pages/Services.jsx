import React, { useEffect, useState } from 'react';
import { fetchServices, createService, updateService, deleteService } from '../services/api';
import ServiceCard from '../components/ServiceCard';
import ServiceFormModal from '../components/ServiceFormModal';
import { Plus, Search } from 'lucide-react';

export default function Services({ token }) {
  const [services, setServices] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingService, setEditingService] = useState(null);

  const loadServices = async () => {
    setLoading(true);
    try {
      const data = await fetchServices(token);
      setServices(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadServices();
  }, [token]);

  const handleSave = async (formData) => {
    try {
      if (editingService) {
        await updateService(token, editingService.id, formData);
      } else {
        await createService(token, formData);
      }
      setIsModalOpen(false);
      setEditingService(null);
      loadServices();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Deactivate this government service?')) {
      await deleteService(token, id);
      loadServices();
    }
  };

  const filtered = services.filter(
    (s) =>
      s.name_en.toLowerCase().includes(search.toLowerCase()) ||
      s.name_ml.includes(search) ||
      s.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', width: '320px' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-muted)' }} />
          <input
            className="input-field"
            style={{ paddingLeft: '2.25rem' }}
            placeholder="Search services or categories..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <button
          className="btn btn-primary"
          onClick={() => {
            setEditingService(null);
            setIsModalOpen(true);
          }}
        >
          <Plus size={16} /> Add Government Service
        </button>
      </div>

      {loading ? (
        <div>Loading government services...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.25rem' }}>
          {filtered.map((service) => (
            <ServiceCard
              key={service.id}
              service={service}
              onEdit={(s) => {
                setEditingService(s);
                setIsModalOpen(true);
              }}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      <ServiceFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingService(null);
        }}
        onSave={handleSave}
        initialData={editingService}
      />
    </div>
  );
}
