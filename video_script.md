# Video Presentation Script (about 5 minutes)

**Name:** Pradhuman Patel  
**netID:** Ppate575  
**Live site:** https://cs411-ai-search.onrender.com/

## Before you record

- Turn the camera on so your face is visible the whole time (Zoom / Loom picture-in-picture is fine)
- Open the live site first and make sure it loads
- Optional: keep `map_data.json` open if you want to show Chicago’s neighbors
- Speak a little slower than normal. If you rush, run UCS once extra and say it matches A*

---

## 0:00–0:30 — Intro

Hey, my name is Pradhuman Patel, netID Ppate575. This is my CS 411 project, the Intelligent Search Visualizer.

I built a small web app that finds routes between cities in Illinois using six search algorithms: BFS, DFS, UCS, IDS, Greedy Best-First, and A-star. The map has 22 cities and 35 road connections. I got the coordinates from OpenStreetMap Nominatim and the driving distances from OSRM, then saved that into `map_data.json`.

Let me just show it working first.

---

## 0:30–1:30 — Demo the app

**On screen:** Start = `Chicago, IL`. Destination = `Springfield, IL`. Algorithm = `A*`. Click **Run Search**.

Okay so I picked Chicago as the start and Springfield as the goal, and I’m running A-star. You can see it draws the path on the map: Chicago, then Joliet, Bloomington, and Springfield. Total cost is 205.43 miles, and it only expanded 11 nodes.

On the left it also shows the concept note. For A-star, the main idea is it uses actual cost so far plus a guess of what’s left, so f(n) equals g(n) plus h(n).

**On screen:** Switch algorithm to `DFS`. Click **Run Search**.

If I run DFS on the same two cities, it still finds a path, but it’s way longer. It goes up through Evanston, Waukegan, Rockford, Peoria… and the cost jumps to about 359 miles. So same start and goal, totally different path, because DFS just goes deep first. It doesn’t care about distance.

You can pick any of the six algorithms from the dropdown. Same idea each time: it returns the path, the cost, and how many nodes got expanded.

---

## 1:30–2:00 — State space

So, how this is set up as a search problem.

A **state** in my project is just one city. Like “Chicago, IL” or “Joliet, IL”. I’m not searching street by street. Each city is one node.

There are **22 states** in the graph, because I have 22 cities. The whole search space is those 22 cities plus the roads between them.

---

## 2:00–2:20 — Initial state and goal state

The **initial state** and **goal state** come straight from the two dropdowns. Whatever city the user picks as Start is the start node, and Destination is the goal. In Flask I read those from the POST request and pass them into the search function. So when I picked Chicago and Springfield, that’s start and goal.

---

## 2:20–2:50 — Actions and transition model

The **actions** are “drive to a neighboring city.” I stored that as an adjacency list in `map_data.json`. Each city maps to a dictionary of neighbors and the road distance.

For example, from Chicago you can go to Evanston, Skokie, Des Plaines, Naperville, Joliet, or Orland Park. So from the Chicago state, those are the legal transitions. If I’m in Joliet, I can go to Chicago, Aurora, Bolingbrook, Orland Park, Kankakee, or Bloomington. The algorithm just looks up `graph[current_city]` to see where it can go next.

---

## 2:50–3:20 — Path cost

The **path cost** is driving distance in miles. I didn’t make those numbers up. `data_fetcher.py` calls the OSRM routing API for each road I defined, and it stores that number on the edge. So Chicago to Joliet is about 44.54 miles, Joliet to Bloomington is 95.12, and so on.

When a search finishes, I add up those edge weights along the path. That’s the total cost you see in the UI, like 205.43 for A-star. BFS and DFS still show that real mileage, even though they don’t use it to decide which node to expand.

---

## 3:20–3:50 — Abstraction

For **abstraction**, I kept the stuff that matters for routing: city name, lat/long, which cities are connected, and the driving distance.

I left out a lot of real-world stuff. No actual street geometry, no traffic, no speed limits, no one-way streets, no turn restrictions, no time of day. I also didn’t keep every small town in between. I just picked 22 cities and connected them with the main roads so the graph stays connected but still small enough to search.

---

## 3:50–4:45 — Completeness and optimality

On **completeness and optimality**, since my graph is finite and connected, BFS, UCS, IDS, and A-star are complete. They’ll find a path if one exists. DFS is complete on this graph because there are no infinite loops if I mark cities as visited, but in general DFS isn’t a great guarantee.

For **optimality**: UCS and A-star are optimal for the cheapest path in miles, because they use the real edge costs. My A-star heuristic is straight-line distance, which should never overestimate road distance, so it’s admissible. BFS and IDS are optimal only for fewest hops, not fewest miles. Greedy and DFS are not optimal.

You can see that in the demo. Chicago to Springfield, A-star and UCS both get 205.43 miles. DFS gets 359. Same problem, DFS is not optimal. On another pair I tried, Evanston to Champaign, greedy was 204 miles and A-star was 172 through Kankakee. So greedy can look closer on the map and still miss the cheaper road.

That’s why I think A-star is the best one for this project. Same cost as UCS, but it expands fewer nodes.

---

## 4:45–5:10 — What I learned / close

What I learned is that “shortest path” depends on what you’re measuring. BFS feels like it should be shortest, but on a weighted map it isn’t always. And writing the algorithms next to a real map made it way easier to see why greedy is fast but can be wrong.

That’s my project. The live site is on Render. Thanks for watching.

---

## After you record

1. Export as `.mp4` (keep it under 7 minutes)
2. Upload to YouTube, Google Drive, or Dropbox
3. Make the link public / anyone-with-the-link
4. Paste the link in `report.md` under **Video Presentation Link**
