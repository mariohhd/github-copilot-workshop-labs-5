import React from 'react';
import EmployeeList from './components/EmployeeList';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Employee Management System</h1>
      </header>
      <main>
        <EmployeeList />
      </main>
    </div>
  );
}

export default App;
