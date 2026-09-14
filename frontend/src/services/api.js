const API_BASE = '/api/v1';

export async function loginAdmin(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error('Invalid username or password');
  return res.json();
}

export async function fetchServices(token) {
  const res = await fetch(`${API_BASE}/services/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch services');
  return res.json();
}

export async function createService(token, serviceData) {
  const res = await fetch(`${API_BASE}/services/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(serviceData)
  });
  if (!res.ok) throw new Error('Failed to create service');
  return res.json();
}

export async function updateService(token, serviceId, updateData) {
  const res = await fetch(`${API_BASE}/services/${serviceId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(updateData)
  });
  if (!res.ok) throw new Error('Failed to update service');
  return res.json();
}

export async function deleteService(token, serviceId) {
  const res = await fetch(`${API_BASE}/services/${serviceId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to delete service');
  return true;
}

export async function fetchAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/dashboard`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function sendSimulatorMessage(phone, text, msgType = 'text') {
  const res = await fetch(`${API_BASE}/webhook/simulator`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      phone_number: phone,
      message_type: msgType,
      text_body: text
    })
  });
  if (!res.ok) throw new Error('Simulator communication failed');
  return res.json();
}

export async function fetchAuditLogs(token) {
  const res = await fetch(`${API_BASE}/admin/audit-logs`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch audit logs');
  return res.json();
}
