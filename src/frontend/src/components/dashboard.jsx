import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, Activity, DollarSign, Users, FileText, CheckCircle } from 'lucide-react';
import Header from './header.jsx';



// Dummy Data
const data = [
  { time: '10:00', errors: 12, sentiment: 80 },
  { time: '11:00', errors: 15, sentiment: 75 },
  { time: '12:00', errors: 40, sentiment: 60 },
  { time: '13:00', errors: 150, sentiment: 40 },
  { time: '14:00', errors: 300, sentiment: 20 },
  { time: '15:00', errors: 180, sentiment: 35 },
  { time: '16:00', errors: 80, sentiment: 55 },
];

const Dashboard = () => {
  return (
    <div className="main-content">
      <Header />
      <h1 style={{padding: "15px", marginLeft: "40px"}}>Sales Activity Report</h1>

      <div className="dashboard-grid">
        
        <div className="summary-column full-height" style={{marginLeft: '60px'}}> 
          <div style={{ borderBottom: '1px solid #eee', paddingBottom: '15px', marginBottom: '15px' }}>
               <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>Summary Report </h3>
            </div>

        </div>
      </div>
    </div>
  )
}

export default Dashboard;