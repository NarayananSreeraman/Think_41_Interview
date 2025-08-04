const API_BASE = 'http://127.0.0.1:5000';

export async function fetchCustomers(page = 1, limit = 20) {
  const res = await fetch(`${API_BASE}/customers?page=${page}&limit=${limit}`);
  if (!res.ok) throw new Error('Failed to fetch customers');
  return await res.json();
}

export async function fetchCustomerById(id) {
  const res = await fetch(`${API_BASE}/customers/${id}`);
  if (!res.ok) throw new Error('Failed to fetch customer');
  return await res.json();
}
