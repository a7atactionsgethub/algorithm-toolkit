import { Graph } from '../data-structures/graph';

/**
 * Depth First Search (DFS)
 * 
 * Traverses or searches tree or graph data structures.
 * 
 * Time Complexity: O(V + E)
 * Space Complexity: O(V) (stack space for recursion/visited set)
 * 
 * Use when:
 * - Exploring all paths (e.g., finding all solutions in a puzzle).
 * - Detecting cycles in a graph.
 * - Topological sorting.
 * 
 * Avoid when:
 * - Finding the shortest path in an unweighted graph (use BFS instead).
 * - Graph is very deep (potential stack overflow).
 */
export function depthFirstSearch<T>(
  graph: Graph<T>,
  startVertex: T,
  visited: Set<T> = new Set()
): T[] {
  const result: T[] = [];
  
  if (!visited.has(startVertex)) {
    visited.add(startVertex);
    result.push(startVertex);

    for (const neighbor of graph.getNeighbors(startVertex)) {
      result.push(...depthFirstSearch(graph, neighbor, visited));
    }
  }

  return result;
}
