UNL Parking Graph Search Tool
Project Overview

Finding parking on UNL’s campus is confusing and expensive — especially when different parking passes grant access to different lots. This project uses graph analysis to help students quickly determine where they can legally park or which pass they need for a specific lot.

The system models parking as a graph:

Nodes = parking lots + parking passes

Edges = which passes allow access to which lots (permissions graph)

Users can perform directional queries:

Choose a pass → find all valid parking lots

Choose a parking lot → find all passes that work there

This allows a clear visualization of campus parking accessibility.

Technologies & Libraries
Purpose	Tool
Graph structure + BFS/DFS search	NetworkX
Visualization (Progress Report 2)	NetworkX + Matplotlib
Data management	Python dictionaries / CSV (mock dataset)
Documentation	Sphinx + GitHub Pages

Data Source

Initial data will be created manually using a small set of UNL parking lots and passes:

Example mock dataset:

Passes: A, C, R, Metered

Lots: Lot A1, A2, C1, Stadium, Library Garage, etc.

Pricing rules vary by day of week (placeholder for future real data integration)

Later improvements may use real UNL parking map data or API access if approved.

Graph Algorithms Used
Algorithm	Purpose
Breadth-First Search (BFS)	Find all valid lots reachable from a pass
Depth-First Search (DFS)	Validate connectivity + check access graph structure
Optional extension:	Weighted graph search for pricing optimization

The tool will ensure graph-based searching instead of simple list lookups — meeting project constraints.

Expected Output / Visuals

Milestone outputs include:

Progress Report 1:

Working command-line interface:

Do you want to search by (P)ass or (L)ot?
→ P
Enter Pass: C
You can park in: Lot C1, Lot A2, Library Garage


Progress Report 2:

Graph visualization showing pass→lot edges with colored node types

Final Submission:

Milestones & Timeline
Milestone	Goals	Due
Progress Report 1	Build graph structure + BFS search + CLI	Dec 2
Progress Report 2	Add visualization + DFS checks + pricing logic prototype	Dec 5
Final Code + Docs	Fully built, documented, hosted	Dec 8

Student pass sharing marketplace

Pricing engine based on demand (peak vs non-peak)

Integrate geolocation + walking distance calculations

Mobile UI for real campus navigation
