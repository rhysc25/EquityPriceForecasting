import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

function App() {
  const [figure, setFigure] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/plot")
      .then((res) => res.json())
      .then((data) => setFigure(JSON.parse(data)));
  }, []);

  return (
    <div>
      <h1>Flask + React + Plotly</h1>
      {figure ? <Plot data={figure.data} layout={figure.layout} /> : <p>Loading...</p>}
    </div>
  );
}

export default App;