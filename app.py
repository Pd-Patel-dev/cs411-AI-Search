import os
import json
from flask import Flask, render_template, jsonify, request

from uninformed import bfs, dfs, ucs, ids
from informed import greedy, astar, sma_star

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"


def load_map_data():
    """Load graph and location data from map_data.json if available."""
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading map_data.json:", e)
    return {
        "region": "State / Metro Area",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():
    """Renders the main deployment webpage."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Returns map locations and graph connections."""
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    # get the start city, goal city and which algorithm they picked
    payload = request.get_json() or {}
    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = payload.get("algorithm", "")

    data = load_map_data()
    graph = data.get("graph", {})
    locations = data.get("locations", {})

    if start == "" or goal == "":
        return jsonify({
            "status": "error",
            "message": "Please pick a start and destination.",
            "path": [],
            "cost": 0,
            "nodes_expanded": 0
        })

    if start not in graph or goal not in graph:
        return jsonify({
            "status": "error",
            "message": "That city is not in the map data.",
            "path": [],
            "cost": 0,
            "nodes_expanded": 0
        })

    # I just use if/elif to call the right function
    algo = algorithm.lower().strip()
    path = None
    cost = 0
    expanded = 0

    if algo == "bfs":
        path, cost, expanded = bfs(graph, start, goal)
    elif algo == "dfs":
        path, cost, expanded = dfs(graph, start, goal)
    elif algo == "ucs":
        path, cost, expanded = ucs(graph, start, goal)
    elif algo == "ids" or algo == "iddfs":
        path, cost, expanded = ids(graph, start, goal)
    elif algo == "greedy" or algo == "greedy_best_first":
        path, cost, expanded = greedy(graph, start, goal, locations)
    elif algo == "astar" or algo == "a_star" or algo == "a*":
        path, cost, expanded = astar(graph, start, goal, locations)
    elif algo == "memory_bounded" or algo == "sma" or algo == "sma_star":
        # memory limit of 15 nodes, seemed like a decent number for this graph
        path, cost, expanded = sma_star(graph, start, goal, locations, 15)
    else:
        return jsonify({
            "status": "error",
            "message": "I don't know that algorithm: " + str(algorithm),
            "path": [],
            "cost": 0,
            "nodes_expanded": 0
        })

    if path is None:
        return jsonify({
            "status": "error",
            "message": "No path found from " + start + " to " + goal,
            "path": [],
            "cost": 0,
            "nodes_expanded": expanded
        })

    return jsonify({
        "status": "ok",
        "message": "Found a path",
        "path": path,
        "cost": cost,
        "nodes_expanded": expanded
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
