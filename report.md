# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Pradhuman Patel
- **UID (netID):** Ppate575
- **UIN:** 660584048

---

## Section 1: Selected City Region
- **Selected Region:** Illinois, USA

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 35
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://cs411-ai-search.onrender.com/
- **Video Presentation Link:** https://drive.google.com/file/d/1h977_8lfQPth8TMayYM1lkLiIz-fyESy/view?usp=sharing

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
    For this project I think A* is the best one. The graph is a road network and the edge weights are real driving distances from OSRM, so we care about the shortest path in miles, not just the path with the fewest cities. BFS and IDS only look at how many hops you take, so they can pick a path that has more miles if it has fewer cities. DFS can go the wrong way for a long time and the path is usually not the shortest. Greedy is fast because it only uses the straight line distance to the goal, but it can ignore a cheaper road that looks farther at first. UCS does find the cheapest path, but it expands more nodes because it does not have a heuristic. A* uses g(n) + h(n), so it still finds the lowest cost path like UCS, but it expands fewer nodes because the heuristic points it toward the goal. I used straight line (haversine) distance for h(n), which should be less than or equal to the real road distance, so it is admissible.
- **Search Efficiency (Nodes expanded/time taken comparison):** I tested a few routes on my local graph. For Chicago, IL to Springfield, IL, BFS/UCS/IDS/Greedy/A* all found the same path (Chicago -> Joliet -> Bloomington -> Springfield, 205.43 miles). A* only expanded 11 nodes and greedy only expanded 4, while UCS expanded 22 and IDS expanded 70 because it restarts at every depth. DFS went a long way around (359.02 miles) through Evanston, Rockford, and Peoria. On Evanston, IL to Champaign, IL you can see greedy is not optimal: it cost 204.54 miles and expanded 5 nodes, but A* and UCS found a 172.0 mile path through Kankakee. A* expanded 14 nodes vs UCS 19. So greedy is usually fastest (least nodes) but can miss the cheapest road. DFS is also not great for this problem. A* was the best tradeoff for me: same cost as UCS, less work than UCS, and better path quality than greedy/DFS.
- **Link the idea of search algorithm to today Generative AI.** 
    Search is still a big part of how generative AI picks the next token. When a language model writes text it does not only take the single most likely next word every time. A lot of systems use beam search, which is kind of like keeping the best k partial sentences, similar to how UCS/A* keep the best partial paths in a priority queue. There is also greedy decoding, which just picks the locally best next token, and that is basically the same idea as greedy best first search. If you only look at the next step you can miss a better sentence later, same as greedy missing a cheaper route. A* is like scoring a partial answer with how good it is so far plus a guess of how good the rest will be. Even training/search for agents (like trying different tool calls or plans) is still expanding a tree of actions until you hit a goal. So the same BFS/DFS/A* ideas from this class show up in how models explore possible outputs, not only in map routing.
