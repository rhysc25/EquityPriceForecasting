from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_form():
    current_date = datetime.now(pytz.UTC).strftime("%Y-%m-%d")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stock Data Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            form {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-top: 10px;
            }}
            input, button {{
                width: 100%;
                padding: 8px;
                margin-top: 5px;
            }}
            button {{
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                margin-top: 15px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <h2>Stock Data Viewer</h2>
        <form id="stockForm">
            <label for="ticker">Stock Ticker Symbol:</label>
            <input type="text" id="ticker" name="ticker" required>

            <label for="start_date">Start Date:</label>
            <input type="date" id="start_date" name="start_date" required>

            <label for="end_date">End Date:</label>
            <input type="date" id="end_date" name="end_date" value="{current_date}" required>

            <button type="submit">Get Data</button>
        </form>

        <div id="chart"></div>

        <script>
            document.getElementById("stockForm").addEventListener("submit", async function(e) {{
                e.preventDefault();
                const ticker = document.getElementById("ticker").value;
                const start_date = document.getElementById("start_date").value;
                const end_date = document.getElementById("end_date").value;

                const response = await fetch(`/data?ticker=${{ticker}}&start_date=${{start_date}}&end_date=${{end_date}}`);
                const data = await response.json();

                const tracePrice = {{
                    x: data.dates,
                    y: data.prices,
                    mode: 'lines',
                    name: 'Price'
                }};

                const traceMA = {{
                    x: data.dates,
                    y: data.moving_average,
                    mode: 'lines',
                    name: 'Moving Average'
                }};

                const traceRSI = {{
                    x: data.dates,
                    y: data.rsi,
                    mode: 'lines',
                    name: 'RSI',
                    yaxis: 'y2'
                }};

                const layout = {{
                    title: `${{ticker}} Price & Indicators`,
                    xaxis: {{ title: 'Date' }},
                    yaxis: {{ title: 'Price' }},
                    yaxis2: {{
                        title: 'RSI',
                        overlaying: 'y',
                        side: 'right',
                        range: [0, 100]
                    }},
                    hovermode: 'x unified'
                }};

                Plotly.newPlot('chart', [tracePrice, traceMA, traceRSI], layout);
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
