# Robot Motion Planner Report

## Pseudo Steps: 

Preprocessing: 

1. choose a set of random points in the configuration space
2. check if the points are in collision with the obstacles- if so, don't add them 
3. connect the points to their nearest neighbors: use the vector distance of each point to every other point
4. sort these points by nearest distance, and loop through them 
5. for each point, check if the straightline path from that point to its nearest neighbor is in collision with the obstacles
6. if not add path, repeat until K paths are added

Querying: 
1. First, treat them as if they are the two components being considered for addition to the graph above: use the local planner to check if the path is in collision with the obstacles. 
2. If so, this is a solution. 
3. If not, order the points in the graph by distance.
4. For each point (starting with the nearest), use local search to see if you can connect it to the other component. if so, do this and add the path to the graph.
5. Once added to the graph, use a search algorithm to find the path from the start to the goal. 
