import React, { useEffect, useState } from 'react';
import Header from './header';

const AuditLogs = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/incident-history')
        .then(res => res.json())
        .then(data => {
            setLogs(data);
            setLoading(false);
        })
        .catch(err => console.error("Failed to load history:", err));
    }, []);

    const generateLogContent = (log) => {
    const { id, timestamp, summary_report, raw_logs } = log;
    
    // Helper to keep formatting consistent
    const createSection = (title, content) => {
        const separator = "=".repeat(50);
        return `${title.toUpperCase()}\n${separator}\n${content || "No data provided."}\n\n`;
    };

    // 1. Build the Header
    let fileContent = createSection("Incident Report", 
        `ID:        ${id}
    Timestamp: ${new Date(timestamp).toLocaleString()}
    Generated: ${new Date().toLocaleString()}`
    );

    // 2. Add Core Sections
    fileContent += createSection("Executive Summary", summary_report?.verdict);
    fileContent += createSection("Timeline", summary_report?.timeline);
    fileContent += createSection("Recommended Actions", summary_report?.actions);

    // 3. Format Technical Evidence (Loop Logic)
    let evidenceText = "No clusters found.";
    if (raw_logs && raw_logs.length > 0) {
        evidenceText = raw_logs.map((cluster, i) => (
    `[Cluster #${i + 1}]
    Time:    ${cluster.anchor?.time || "N/A"}
    Type:    ${cluster.anchor?.type || "Unknown"}
    Details: ${cluster.anchor?.details || "None"}
    `
        )).join("\n"); // Join array items with a newline
    }
    
    fileContent += createSection("Technical Evidence", evidenceText);

    return fileContent;
    };

    const downloadReport = (log) => {

        const content = generateLogContent(log);

        // 1. Create a Blob from the JSON string
        const blob = new Blob([content], { type: "text/plain" });
        
        // 2. Create a download link dynamically
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Incident-Report-${log.id}.txt`;
        
        // 3. Trigger download and cleanup
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };


    return(
        <div className="main-content">
            <Header />
            <header className = "dashboard-header">
                <div style={{padding:"30px", marginLeft:"10px"}}>
                    <h1>Audit Loogs</h1>
                    <p>Historical archive of system anomalies</p>
                </div>
            </header>

        <div className="content-wrapper" style={{marginTop: '20px'}}>
            <div className="kpi-card" style={{ marginLeft:"20px" ,width: '94%', overflowX: 'auto'}}>
            
            {loading ? (
                <p style={{padding: '20px'}}>Loading archives...</p>
            ) : (
                <table style={{width: '100%', borderCollapse: 'collapse', minWidth: '600px'}}>
                <thead>
                    <tr style={{borderBottom: '2px solid #eee', textAlign: 'left'}}>
                    <th style={{padding: '15px'}}>Date & Time</th>
                    <th style={{padding: '15px'}}>Incident ID</th>
                    <th style={{padding: '15px'}}>Status</th>
                    <th style={{padding: '15px', textAlign: 'right'}}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map((log) => (
                    <tr key={log.id} style={{borderBottom: '1px solid #f0f0f0'}}>
                        <td style={{padding: '15px'}}>
                        {new Date(log.timestamp).toLocaleString()}
                        </td>
                        <td style={{padding: '15px', fontFamily: 'monospace', color: '#666'}}>
                        {log.id}
                        </td>
                        <td style={{padding: '15px'}}>
                        <span style={{
                            backgroundColor: '#ffe5e5', color: '#ff4d4f', 
                            padding: '4px 8px', borderRadius: '4px', fontSize: '0.85rem'
                        }}>
                            Critical
                        </span>
                        </td>
                        <td style={{padding: '15px', textAlign: 'right'}}>
                        <button 
                            onClick={() => downloadReport(log)}
                            style={{
                            backgroundColor: '#4361ee', color: 'white', border: 'none',
                            padding: '8px 16px', borderRadius: '6px', cursor: 'pointer'
                            }}
                        >
                            Download Report
                        </button>
                        </td>
                    </tr>
                    ))}
                </tbody>
                </table>
            )}
            
            {!loading && logs.length === 0 && (
                <div style={{padding: '40px', textAlign: 'center', color: '#888'}}>
                No incident history found.
                </div>
            )}

            </div>
            </div>
        </div>
    );
};

export default AuditLogs;