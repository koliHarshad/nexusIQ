import Sidebar from './components/sidebar.jsx'
import Dashboard from './components/dashboard.jsx'
import { useState } from 'react';
// import Dashboard from './ref.jsx'

function App() {

  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  }

  return (
  <div className={`app-container ${isSidebarCollapsed ? 'collapsed' : ''}`}>
      <Sidebar isCollapsed={isSidebarCollapsed} toggleSidebar={toggleSidebar} />
      <Dashboard />
    </div>
  )
}

export default App
