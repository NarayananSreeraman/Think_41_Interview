import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, CircularProgress, Alert } from '@mui/material';
import CustomerTable from './CustomerTable';
import { fetchCustomers, fetchCustomerById } from './api';

function App() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError('');
      try {
        const data = await fetchCustomers(1, 50);
        // For each customer, fetch order count
        const withOrderCount = await Promise.all(
          data.map(async (c) => {
            try {
              const detail = await fetchCustomerById(c.id);
              return { ...c, order_count: detail.order_count };
            } catch {
              return { ...c, order_count: 0 };
            }
          })
        );
        setCustomers(withOrderCount);
      } catch (e) {
        setError(e.message);
      }
      setLoading(false);
    }
    load();
  }, []);

  const filtered = customers.filter(
    (c) =>
      c.first_name.toLowerCase().includes(search.toLowerCase()) ||
      c.last_name.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Customer List
      </Typography>
      <TextField
        label="Search by name or email"
        variant="outlined"
        fullWidth
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        sx={{ mb: 2 }}
      />
      {loading ? (
        <CircularProgress sx={{ display: 'block', mx: 'auto', my: 4 }} />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <CustomerTable customers={filtered} />
      )}
    </Container>
  );
}

export default App;
