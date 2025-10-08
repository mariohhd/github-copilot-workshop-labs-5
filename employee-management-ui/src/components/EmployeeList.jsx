import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './EmployeeList.css';

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/employees')
      .then(response => {
        setEmployees(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to fetch employees');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading employees...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="employee-list-container">
      <div className="employee-list-header">
        <button className="add-btn">Add Employee</button>
      </div>
      <table className="employee-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map(emp => (
            <tr key={emp.id}>
              <td>{emp.id}</td>
              <td>{emp.name}</td>
              <td>{emp.role}</td>
              <td>{emp.email}</td>
              <td>
                <button className="view-btn">View</button>
                <button className="edit-btn">Edit</button>
                <button className="delete-btn">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EmployeeList;
