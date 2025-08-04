import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';

function CustomerTable({ customers }) {
  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Email</TableCell>
            <TableCell>Order Count</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {customers.map((c) => (
            <TableRow key={c.id}>
              <TableCell>{c.first_name} {c.last_name}</TableCell>
              <TableCell>{c.email}</TableCell>
              <TableCell>{c.order_count}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {customers.length === 0 && (
        <Typography sx={{ p: 2 }} align="center">No customers found.</Typography>
      )}
    </TableContainer>
  );
}

export default CustomerTable;
