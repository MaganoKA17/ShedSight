import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";

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

  if (loading) return <p>Loading ShedSight data...</p>

  return(
    <div>
      <h1>ShedSight</h1>
      <p>Rows fetched: {data.length}</p>
      <pre>{JSON.stringify(data[0], null, 2)}</pre>
    </div>
  )
}
export default App