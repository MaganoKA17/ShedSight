import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponseConatiner
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

  return(
    <div>
      <h1>ShedSight</h1>
      <p>Rows fetched: {data.length}</p>
      <pre>{JSON.stringify(data[0], null, 2)}</pre>
    </div>
  )
}
export default App