import Sidebar from './components/sidebar.jsx'
import Dashboard from './components/dashboard.jsx'
import AuditLogs from './components/audit_logs.jsx';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Dashboard from './ref.jsx'

function App() {

  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  }

  return (
  <Router>
    <div className={`app-container ${isSidebarCollapsed ? 'collapsed' : ''}`}>
        <Sidebar isCollapsed={isSidebarCollapsed} toggleSidebar={toggleSidebar} />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/audit-logs" element={<AuditLogs />} />
        </Routes>
      </div>
  </Router>
  )
}

export default App
