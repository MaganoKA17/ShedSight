import { useEffect, useState } from "react"
import { supabase } from "./supabaseClient"
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from "recharts"

const TABS = ["Overview", "Trends", "Stress Hours", "Data Table", "AI Insights"]

function StatCard({ title, value, subtitle }) {
  return (
    <div style={{
      background: "#16213e", borderRadius: "12px",
      padding: "24px", flex: 1, minWidth: "150px"
    }}>
      <p style={{ color: "#888", margin: 0 }}>{title}</p>
      <h2 style={{ color: "#fff", margin: "8px 0" }}>{value}</h2>
      <p style={{ color: "#888", margin: 0, fontSize: "12px" }}>{subtitle}</p>
    </div>
  )
}

function TabButton({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: active ? "#6c63ff" : "transparent",
        color: active ? "#fff" : "#888",
        border: "none",
        borderRadius: "8px",
        padding: "10px 20px",
        cursor: "pointer",
        fontSize: "14px",
        fontWeight: active ? "bold" : "normal",
        transition: "all 0.2s"
      }}
    >
      {label}
    </button>
  )
}

function App() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("Overview")
  const [insights, setInsights] = useState("")
  const [insightsLoading, setInsightsLoading] = useState(false)

  useEffect(() => {
    async function fetchData() {
      const { data, error } = await supabase
        .from("daily_outage_summary")
        .select("*")
        .order("date")
      if (error) console.error(error)
      else setData(data)
      setLoading(false)
    }
    fetchData()
  }, [])

  const fetchInsights = async () => {
    setInsightsLoading(true)
    try {
      const response = await fetch("http://127.0.0.1:5000/insights")
      const data = await response.json()
      setInsights(data.insights)
    } catch (error) {
      console.error("Error fetching insights:", error)
    }
    setInsightsLoading(false)
  }

  if (loading) return (
    <div style={{ color: "#fff", textAlign: "center", marginTop: "100px" }}>
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
      <p style={{ color: "#888", marginBottom: "24px" }}>
        South African Grid Stress Analytics — Last 14 Days
      </p>

     
      <div style={{
        display: "flex", gap: "8px", marginBottom: "32px",
        background: "#1e1e2e", borderRadius: "12px", padding: "8px",
        flexWrap: "wrap"
      }}>
        {TABS.map(tab => (
          <TabButton
            key={tab}
            label={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
          />
        ))}
      </div>

      
      {activeTab === "Overview" && (
        <div>
          <h2 style={{ marginBottom: "24px" }}>Overview</h2>
          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
            <StatCard
              title="Avg Grid Stress"
              value={`${avgStress}%`}
              subtitle="UCLF+OCLF average"
            />
            <StatCard
              title="Worst Day"
              value={worstDay.date}
              subtitle={`${worstDay.max_uclf_oclf}% max stress`}
            />
            <StatCard
              title="Best Day"
              value={bestDay.date}
              subtitle={`${bestDay.avg_uclf_oclf}% avg stress`}
            />
            <StatCard
              title="High Stress Hours"
              value={totalHighStressHours}
              subtitle="Hours above threshold"
            />
          </div>
        </div>
      )}

     
      {activeTab === "Trends" && (
        <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px" }}>
          <h2 style={{ marginTop: 0 }}>Daily Grid Stress Trend</h2>
          <ResponsiveContainer width="100%" height={400}>
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
      )}

      
      {activeTab === "Stress Hours" && (
        <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px" }}>
          <h2 style={{ marginTop: 0 }}>High Stress Hours Per Day</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="date" stroke="#888" tick={{ fontSize: 11 }} />
              <YAxis stroke="#888" />
              <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
              <Bar dataKey="high_stress_hours" fill="#6c63ff" name="High Stress Hours" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

    
      {activeTab === "Data Table" && (
        <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px" }}>
          <h2 style={{ marginTop: 0 }}>Data Table</h2>
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
      )}

      
      {activeTab === "AI Insights" && (
        <div style={{ background: "#1e1e2e", borderRadius: "12px", padding: "24px" }}>
          <h2 style={{ marginTop: 0 }}>AI Insights</h2>
          <p style={{ color: "#888", marginBottom: "16px" }}>
            Click the button below to generate AI-powered analysis of the last 14 days of Eskom grid data.
          </p>
          <button
            onClick={fetchInsights}
            style={{
              background: "#6c63ff", color: "#fff",
              border: "none", borderRadius: "8px",
              padding: "12px 24px", cursor: "pointer",
              fontSize: "14px", marginBottom: "24px"
            }}
          >
            {insightsLoading ? "Generating insights..." : "Generate AI Insights"}
          </button>
          {insights && (
            <div style={{
              color: "#ccc", lineHeight: "1.8",
              whiteSpace: "pre-wrap"
            }}>
              {insights}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App