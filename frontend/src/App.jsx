import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from "recharts"

function StatCard({ title, value, subtitle }){
  return (
    <div style={{
      background: "#1e1e2e", borderRadius: "12px",
      padding: "20px", flex : 1, minWidth: "150px"

    }}>
      <p style={{color: "#888", margin: 0 }}>{title}</p>
      <h2 style={{ color: "#fff", margin: "8px 0"}}>{value}</h2>
      <p style={{color: "#888", margin: 0, fontSize: "12px" }}>{subtitle}</p>
    </div>
  )
}

function App(){
  const [ data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      const {data, error} = await supabase
      .from("daily_outage_summary")
      .select("*")
      .order("date")

      if (error){
        console.error("Error fetching data:", error)
      } else{
        setData(data)
      }
      setLoading(false)
    }
    fetchData()
  }, [])

  if (loading) return( 
  <div style= {{ color: "#fff", textAlign : "center", marginTop: "100px" }}>
    Loading ShedSight data...
  </div>
)

  const avgStress = (data.reduce((sum, d) => sum + d.avg_uclf_oclf, 0) / data.length).toFixed(2)
  const worstDay = data.reduce((max, d) => d.max_uclf_oclf > max.max_uclf_oclf ? d : max, data[0])
  const bestDay = data.reduce((min, d) => d.avg_uclf_oclf < min.avg_uclf_oclf ? d : min, data[0])
  const totalHighStressHours = data.reduce((sum, d) => sum + d.high_stress_hours, 0)

  return (
    <div style={{
      background: "#0f0f1a", minHeight: "100vh",
      color: "#fff", fontFamily: "sans-serif", padding: "32px"
    }}>
      
      <h1 style={{ fontSize: "28px", marginBottom: "4px" }}>⚡ ShedSight</h1>
      <p style={{ color: "#888", marginBottom: "32px" }}>
        South African Grid Stress Analytics — Last 14 Days
      </p>

      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", marginBottom: "32px" }}>
        <StatCard title="Avg Grid Stress" value={`${avgStress}%`} subtitle="UCLF+OCLF average" />
        <StatCard title="Worst Day" value={worstDay.date} subtitle={`${worstDay.max_uclf_oclf}% max stress`} />
        <StatCard title="Best Day" value={bestDay.date} subtitle={`${bestDay.avg_uclf_oclf}% avg stress`} />
        <StatCard title="High Stress Hours" value={totalHighStressHours} subtitle="Hours above 30% loss" />
      </div>

     
      <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px", marginBottom: "24px" }}>
        <h3 style={{ marginTop: 0 }}>Daily Grid Stress Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="date" stroke="#888" tick={{ fontSize: 11 }} />
            <YAxis stroke="#888" />
            <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
            <Line type="monotone" dataKey="avg_uclf_oclf" stroke="#6c63ff" strokeWidth={2} dot={false} name="Avg Stress %" />
            <Line type="monotone" dataKey="max_uclf_oclf" stroke="#ff6584" strokeWidth={2} dot={false} name="Max Stress %" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      
      <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px", marginBottom: "24px" }}>
        <h3 style={{ marginTop: 0 }}>High Stress Hours Per Day</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="date" stroke="#888" tick={{ fontSize: 11 }} />
            <YAxis stroke="#888" />
            <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
            <Bar dataKey="high_stress_hours" fill="#6c63ff" name="High Stress Hours" />
          </BarChart>
        </ResponsiveContainer>
      </div>

  
      <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px" }}>
        <h3 style={{ marginTop: 0 }}>Raw Data Table</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #333" }}>
              <th style={{ textAlign: "left", padding: "8px", color: "#888" }}>Date</th>
              <th style={{ textAlign: "left", padding: "8px", color: "#888" }}>Avg Stress %</th>
              <th style={{ textAlign: "left", padding: "8px", color: "#888" }}>Max Stress %</th>
              <th style={{ textAlign: "left", padding: "8px", color: "#888" }}>High Stress Hours</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.id} style={{ borderBottom: "1px solid #222" }}>
                <td style={{ padding: "8px" }}>{row.date}</td>
                <td style={{ padding: "8px" }}>{row.avg_uclf_oclf}%</td>
                <td style={{ padding: "8px" }}>{row.max_uclf_oclf}%</td>
                <td style={{ padding: "8px" }}>{row.high_stress_hours}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
export default App