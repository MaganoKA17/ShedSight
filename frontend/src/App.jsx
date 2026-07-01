import { useEffect, useState } from "react"
import { supabase } from "./supabaseClient"
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from "recharts"

const TABS = ["Overview", "Trends", "Stress Hours", "Data Table", "AI Insights"]

const DARK = {
  bg: "#0a0a1a",
  card: "#0d1b2a",
  tabBar: "#0d1b2a",
  tabActive: "#f5c518",
  tabActiveText: "#0a0a1a",
  tabInactive: "#888",
  text: "#ffffff",
  subtext: "#888",
  accent: "#f5c518",
  accent2: "#ff6b00",
  border: "#1a2a3a",
  chartColor: "#f5c518",
  chartColor2: "#ff6b00",
  tooltip: "#0d1b2a",
}

const LIGHT = {
  bg: "#f8f9fa",
  card: "#ffffff",
  tabBar: "#0d1b2a",
  tabActive: "#f5c518",
  tabActiveText: "#0a0a1a",
  tabInactive: "#ccc",
  text: "#0a0a1a",
  subtext: "#888",
  accent: "#ff6b00",
  accent2: "#cc4400",
  border: "#e0e0e0",
  chartColor: "#ff6b00",
  chartColor2: "#cc4400",
  tooltip: "#ffffff",
}

function StatCard({ title, value, subtitle, theme, valueColor }) {
  return (
    <div style={{
      background: theme.card, borderRadius: "12px",
      padding: "20px", flex: 1, minWidth: "150px",
      border: `1px solid ${theme.border}`
    }}>
      <p style={{ color: theme.subtext, margin: 0, fontSize: "13px" }}>{title}</p>
      <h2 style={{ color: valueColor || theme.accent, margin: "8px 0" }}>{value}</h2>
      <p style={{ color: theme.subtext, margin: 0, fontSize: "12px" }}>{subtitle}</p>
    </div>
  )
}

function TabButton({ label, active, onClick, theme }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: active ? theme.tabActive : "transparent",
        color: active ? theme.tabActiveText : theme.tabInactive,
        border: "none", borderRadius: "6px",
        padding: "8px 16px", cursor: "pointer",
        fontSize: "13px", fontWeight: active ? "500" : "400",
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
  const [darkMode, setDarkMode] = useState(true)

  const theme = darkMode ? DARK : LIGHT

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
    <div style={{ color: theme.text, textAlign: "center", marginTop: "100px", background: theme.bg, minHeight: "100vh" }}>
      Loading ShedSight data...
    </div>
  )

  const avgStress = (data.reduce((sum, d) => sum + d.avg_uclf_oclf, 0) / data.length).toFixed(2)
  const worstDay = data.reduce((max, d) => d.max_uclf_oclf > max.max_uclf_oclf ? d : max, data[0])
  const bestDay = data.reduce((min, d) => d.avg_uclf_oclf < min.avg_uclf_oclf ? d : min, data[0])
  const totalHighStressHours = data.reduce((sum, d) => sum + d.high_stress_hours, 0)
  const startDate = data[0]?.date
  const endDate = data[data.length - 1]?.date

  return (
    <div style={{
      background: theme.bg, minHeight: "100vh",
      color: theme.text, fontFamily: "sans-serif", padding: "32px",
      transition: "all 0.3s"
    }}>
    
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
        <h1 style={{ fontSize: "28px", margin: 0, color: theme.accent }}>ShedSight</h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          style={{
            background: theme.card, color: theme.text,
            border: `1px solid ${theme.border}`,
            borderRadius: "8px", padding: "8px 16px",
            cursor: "pointer", fontSize: "13px"
          }}
        >
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>
      <p style={{ color: theme.subtext, marginBottom: "24px" }}>
        South African Grid Stress Analytics — {startDate} to {endDate}
      </p>

      <div style={{
        display: "flex", gap: "6px", marginBottom: "32px",
        background: theme.tabBar, borderRadius: "10px",
        padding: "6px", flexWrap: "wrap"
      }}>
        {TABS.map(tab => (
          <TabButton
            key={tab} label={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
            theme={theme}
          />
        ))}
      </div>

      {activeTab === "Overview" && (
        <div>
          <h2 style={{ marginBottom: "24px", color: theme.text }}>Overview</h2>
          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
            <StatCard title="Avg Grid Stress" value={`${avgStress}%`} subtitle="UCLF+OCLF average" theme={theme} valueColor={theme.accent} />
            <StatCard title="Worst Day" value={worstDay.date} subtitle={`${worstDay.max_uclf_oclf}% max stress`} theme={theme} valueColor={theme.accent2} />
            <StatCard title="Best Day" value={bestDay.date} subtitle={`${bestDay.avg_uclf_oclf}% avg stress`} theme={theme} valueColor={theme.text} />
            <StatCard title="High Stress Hours" value={totalHighStressHours} subtitle="Hours above threshold" theme={theme} valueColor={theme.accent} />
          </div>
        </div>
      )}

      {activeTab === "Trends" && (
        <div style={{ background: theme.card, borderRadius: "12px", padding: "24px", border: `1px solid ${theme.border}` }}>
          <h2 style={{ marginTop: 0, color: theme.text }}>Daily Grid Stress Trend</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
              <XAxis dataKey="date" stroke={theme.subtext} tick={{ fontSize: 11 }} />
              <YAxis stroke={theme.subtext} />
              <Tooltip contentStyle={{ background: theme.tooltip, border: `1px solid ${theme.border}`, color: theme.text }} />
              <Line type="monotone" dataKey="avg_uclf_oclf" stroke={theme.chartColor} strokeWidth={2} dot={false} name="Avg Stress %" />
              <Line type="monotone" dataKey="max_uclf_oclf" stroke={theme.chartColor2} strokeWidth={2} dot={false} name="Max Stress %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {activeTab === "Stress Hours" && (
        <div style={{ background: theme.card, borderRadius: "12px", padding: "24px", border: `1px solid ${theme.border}` }}>
          <h2 style={{ marginTop: 0, color: theme.text }}>High Stress Hours Per Day</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
              <XAxis dataKey="date" stroke={theme.subtext} tick={{ fontSize: 11 }} />
              <YAxis stroke={theme.subtext} />
              <Tooltip contentStyle={{ background: theme.tooltip, border: `1px solid ${theme.border}`, color: theme.text }} />
              <Bar dataKey="high_stress_hours" fill={theme.chartColor} name="High Stress Hours" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {activeTab === "Data Table" && (
        <div style={{ background: theme.card, borderRadius: "12px", padding: "24px", border: `1px solid ${theme.border}` }}>
          <h2 style={{ marginTop: 0, color: theme.text }}>Data Table</h2>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
                <th style={{ textAlign: "left", padding: "8px", color: theme.subtext }}>Date</th>
                <th style={{ textAlign: "left", padding: "8px", color: theme.subtext }}>Avg Stress %</th>
                <th style={{ textAlign: "left", padding: "8px", color: theme.subtext }}>Max Stress %</th>
                <th style={{ textAlign: "left", padding: "8px", color: theme.subtext }}>High Stress Hours</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.id} style={{ borderBottom: `1px solid ${theme.border}` }}>
                  <td style={{ padding: "8px", color: theme.text }}>{row.date}</td>
                  <td style={{ padding: "8px", color: theme.accent }}>{row.avg_uclf_oclf}%</td>
                  <td style={{ padding: "8px", color: theme.accent2 }}>{row.max_uclf_oclf}%</td>
                  <td style={{ padding: "8px", color: theme.text }}>{row.high_stress_hours}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === "AI Insights" && (
        <div style={{ background: theme.card, borderRadius: "12px", padding: "24px", border: `1px solid ${theme.border}` }}>
          <h2 style={{ marginTop: 0, color: theme.text }}>AI Insights</h2>
          <p style={{ color: theme.subtext, marginBottom: "16px" }}>
            Click the button below to generate AI-powered analysis of the last 14 days of Eskom grid data.
          </p>
          <button
            onClick={fetchInsights}
            style={{
              background: theme.accent, color: "#0a0a1a",
              border: "none", borderRadius: "8px",
              padding: "12px 24px", cursor: "pointer",
              fontSize: "14px", fontWeight: "500", marginBottom: "24px"
            }}
          >
            {insightsLoading ? "Generating insights..." : "Generate AI Insights"}
          </button>
          {insights && (
            <div style={{ color: theme.text, lineHeight: "1.8", whiteSpace: "pre-wrap" }}>
              {insights}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App