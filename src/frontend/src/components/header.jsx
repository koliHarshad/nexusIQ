import { Bell, HelpCircle, Menu, LayoutTemplate, AlignCenter } from 'lucide-react';

const Header = () => {
    return (
        <div className="top-header">

            <div className="header-brand">
                <div className="logo-square">
                    <LayoutTemplate size={25} color="black" />
                </div>
                <h2>NexusIQ</h2>
                
                <nav className="header-nav">
                    <a href="/" className="nav-link active">Home</a>
                    <a href="/audit-logs" className="nav-link">Audit Logs</a>
                </nav>
            </div>


                {/* RIGHT: Icons */}
                <div className="header-actions">
                    <div className="icon-btn">
                    <Bell size={20} />
                    {/* Notification Dot */}
                    <span className="notification-dot"></span>
                    </div>
                    <div className="icon-btn">
                    <HelpCircle size={20} />
                    </div>
                    <div className="icon-btn menu-btn">
                    <Menu size={20} />
                    </div>
                </div>
      
        </div>
    );
};

export default Header;