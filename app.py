from flask import Flask, jsonify
from flask_cors import CORS
import plotly.express as px

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

@app.route('/api/data')
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/api/plot")
def get_plot():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    graph_json = fig.to_json()  # convert figure to JSON
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
