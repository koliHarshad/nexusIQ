import { LayoutDashboard, FileText, Settings, Menu } from 'lucide-react';
import {Link, useLocation} from 'react-router-dom';

const Sidebar = ({ isCollapsed, toggleSidebar }) => {
    const location = useLocation();
    return (
        <div className="sidebar">
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginBottom: '40px' }}>
                {!isCollapsed &&(
                <div style={{ display: 'flex', alignItems: 'center', paddingLeft: '10px' }}>
                    <div style={{ width: '30px', height: '30px', background: '#4cc9f0', borderRadius: '50%', marginRight: '10px' }}></div>
                    <h2 style={{ margin: 0, fontSize: '1.2rem' }}>NexusIQ</h2>
                </div>)}
                <div style={{ alignItems: 'center', cursor: 'pointer' }} onClick={toggleSidebar}>
                    <Menu size={24} />
                </div>
            </div>


            <nav style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>                    
                    <LayoutDashboard size={20} />
                    {!isCollapsed &&<span>Home</span>}
                </Link>

                <Link to="/audit-logs" className={`nav-item ${location.pathname === '/audit-logs' ? 'active' : ''}`}>
                    <FileText size={20} />
                    {!isCollapsed && <span>Audit Logs</span>}
                </Link>

                <div className="nav-item">
                    <Settings size={20} />
                    {!isCollapsed && <span>Settings</span>}
                </div>
            </nav>
        </div>
    );
};

export default Sidebar;
