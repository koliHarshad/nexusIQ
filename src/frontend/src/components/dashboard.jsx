import { LineChart,Bar,PieChart, Cell, Legend, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Pie } from 'recharts';
import { AlertTriangle, Activity, DollarSign, Users, FileText, CheckCircle, BookTemplate } from 'lucide-react';
import Header from './header.jsx';
import { useEffect, usestate } from 'react';


const Dashboard = () => {

  // const [incidentData, setIncidentData] = usestate(null);
  // const [dashboardMetrics, setDashboardMetrics] = usestate(null);
  // const [loading, setLoading] = usestate(true);

  // useEffect(() => {
  //   // Fetch incident data using fastapi
  //   fetch('http://localhost:8000/api/latest-report')
  //     .then(res => res.json())
  //     .then(data => {
  //       setIncidentData(data);
  //       setLoading(false);
  //     })
  //     .catch(err => {
  //       console.error('Error fetching incident data:', err);
  //       setLoading(false);
  //     });

  //   fetch('http://localhost:8000/api/dashboard-metrics')
  //     .then(res => res.json())
  //     .then(data => {
  //       setDashboardMetrics(data);
  //     })
  //     .catch(err => {
  //       console.error('Error fetching dashboard metrics:', err);
  //     });

  // }, []);
    


  // if (loading) return <div style={{padding: '50px', textAlign: 'center', color: '#666'}}>Initializing NexusIQ Analysis...</div>;
  // if (!incidentData || incidentData.error) return <div style={{padding: '50px', textAlign: 'center'}}>No Analysis Found. Run the reporter script first.</div>;

  const sampleData = [
           {
            "id": 14039,
            "timestamp": 2023-10-11,
            "verdictTitle": "Sales Trend Analysis",
            "verdictStatus": "Critical",
            "verdictText": "The incident began on 2023-10-11 at 19:00:00. Logs explicitly show a high volume of 500 errors originating from the /api/v1/checkout endpoint.",
            "timelineText": "No timeline available.",
            "recommendedActions": "Couldn't provide recommended actions.",
            "clusters": "No clusters available."
          }
  ]
  const dashboardSampleMetrics = {
    "sales_trend": [
        { "time": "2023-10-12 10:00:00", "revenue": 15200.50 },
        { "time": "2023-10-12 11:00:00", "revenue": 16100.00 },
        { "time": "2023-10-12 12:00:00", "revenue": 15800.75 },
        { "time": "2023-10-12 13:00:00", "revenue": 14200.20 },
        { "time": "2023-10-12 14:00:00", "revenue": 8500.00 },  // The Drop starts
        { "time": "2023-10-12 15:00:00", "revenue": 4200.00 },  // Deep impact
        { "time": "2023-10-12 16:00:00", "revenue": 3800.50 },  // Deep impact
        { "time": "2023-10-12 17:00:00", "revenue": 9100.00 },  // Recovery starts
        { "time": "2023-10-12 18:00:00", "revenue": 14500.00 }, // Recovered
        { "time": "2023-10-12 19:00:00", "revenue": 16200.00 }
    ],
    "error_trend": [
        { "time": "2023-10-12 10:00:00", "count": 12 },
        { "time": "2023-10-12 11:00:00", "count": 15 },
        { "time": "2023-10-12 12:00:00", "count": 10 },
        { "time": "2023-10-12 13:00:00", "count": 45 },  // Warning signs
        { "time": "2023-10-12 14:00:00", "count": 312 }, // The Spike
        { "time": "2023-10-12 15:00:00", "count": 450 }, // Peak errors
        { "time": "2023-10-12 16:00:00", "count": 410 },
        { "time": "2023-10-12 17:00:00", "count": 120 }, // Subsiding
        { "time": "2023-10-12 18:00:00", "count": 25 },
        { "time": "2023-10-12 19:00:00", "count": 14 }
    ],
    "sentiment": {
        "total": 1250,
        "negative": 850,
        "positive": 400
    }
  };


  return (
    <div className="main-content">
      <Header />
      <h1 style={{padding: "15px", marginLeft: "17px"}}>Sales Activity Report</h1>
      <h3 style={{marginLeft: '50px', marginBottom: '20px'  }}> Incident number: {sampleData[0].id}</h3>

      <div className="dashboard-grid">
        
        <div className="summary-column"> 
          <div className="summary-card" style={{marginLeft: '60px'}}>
            <div style={{ borderBottom: '1px solid #eee', paddingBottom: '15px', marginBottom: '15px' }}>
               <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>Summary Report </h3>
            </div>
         
            <h4 style={{ color: '#555', marginTop: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}> 
              <AlertTriangle size={20} color="#ff4d4f" />
              Verdict: {sampleData[0].verdictStatus}</h4>
            <p style={{ lineHeight: '1.6', color: '#666', fontSize: '0.9rem' }}>
              {sampleData[0].verdictText} </p>
            
            <h4 style={{ color: '#555', marginTop: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}> 
              Timeline Analysis</h4>
            <p style={{ lineHeight: '1.6', color: '#666', fontSize: '0.9rem' }}>
              {sampleData[0].verdictText} </p>

            <h4 style={{ color: '#555', marginTop: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}> 
              Recommended Actions</h4>
            <p style={{ lineHeight: '1.6', color: '#666', fontSize: '0.9rem' }}>
              {sampleData[0].verdictText} </p>

            <div style={{ marginTop: 'auto', paddingTop: '20px' }}>
                <button className="secondary-btn">View Raw Logs</button>
            </div>
          </div>
        </div>

        <div className="charts-column">

          {/* KPI Cards */}
          <div className="kpi-grid">
            <div className="kpi-card">
              <div className="icon-bg red"><Activity size={20} color="#ff4d4f" /></div>
              <div><p className="kpi-label">Events</p><h3>{sampleData[0].clusters.length}</h3></div>
            </div>

            <div className="kpi-card">
              <div className="icon-bg blue"><Users size={20} color="#1890ff" /></div>
              <div><p className="kpi-label">Sentiments</p><h3>-30%</h3></div>
            </div>

            <div className="kpi-card">
              <div className="icon-bg green"><DollarSign size={20} color="#52c41a" /></div>
              <div><p className="kpi-label">Est. Loss</p><h3>$50k</h3></div>
            </div>

          </div>

          {/* sales graph */}
          <div className="chart-container">
            <h3  style={{marginBottom:"25px"}}> Sales Activity </h3>
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={dashboardSampleMetrics.sales_trend}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis 
                    dataKey="time" 
                    tickFormatter={(str) => str.split(" ")[1].substring(0,5)}
                    stroke="#888"
                    fontSize={12}
                    tickMargin={10}
                  />  
                  <YAxis 
                    tickFormatter={(val) => `$${(val / 1000).toFixed(0)}k`} 
                    stroke="#888"
                    fontSize={12} 
                  />
                  <Tooltip 
                    formatter={(value) => [`$${value.toLocaleString()}`, "Revenue"]}
                    labelFormatter={(label) => `Time: ${label}`}
                  />
                  <Line type="monotone" dataKey="revenue" stroke="#3328ffff" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <h3 style={{marginTop:"25px", marginBottom: "0px"}}> Evidence Locker</h3>
            <div style={{display: "flex", gap: "7px", width:"100%"}}>
              <div className='kpi-card' style={{ boxShadow:"0 4px 8px rgba(0,0,0,0.1)",flex: 2, display: "flex", flexDirection: "column" , alignItems:"start", height: "300px", width: "170%"}}>
                <h4>Error Count</h4>

                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={dashboardSampleMetrics.error_trend}>
                    {/* X-Axis: Shows Time (10:00) */}
                    <XAxis 
                      dataKey="time" 
                      tickFormatter={(str) => str.split(' ')[1].substring(0, 5)}
                      stroke="#888"
                      fontSize={12}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      dataKey="count"
                    />
                    <Tooltip 
                      cursor={{fill: 'transparent'}}
                      formatter={(value) => [`${value} Errors`, "Count"]}
                    />
                    {/* The Bars: Blue color with rounded tops */}
                    <Bar 
                      dataKey="count" 
                      fill="#4361ee" 
                      radius={[4, 4, 0, 0]} 
                      barSize={30} 
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className='kpi-card' style={{ flex:1, boxShadow: "0 4px 8px rgba(0,0,0,0.1)", display: "flex", flexDirection: "column", alignItems:"start", height: "300px", width: "30%" }}>
                <h3>Social Sentiments</h3>

                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie 
                      data={[
                        { name: 'Negative', value: dashboardSampleMetrics.sentiment.negative},
                        { name: 'Positive', value: dashboardSampleMetrics.sentiment.positive}
                      ]}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={1}
                      dataKey="value"
                      >
                      <Cell fill="#ff4d4f" />
                      <Cell fill="#4361ee" />
                    </Pie>
                    <Tooltip />
                    <Legend verticalAlign="bottom" height={36} />
                  </PieChart>
                </ResponsiveContainer>

              </div>
          </div>

        </div>

          {/* <div className="chart-container" style={{ marginTop: '7px'}}>

          </div> */}

        </div>
      

      </div>
    </div>
  )
}

export default Dashboard;