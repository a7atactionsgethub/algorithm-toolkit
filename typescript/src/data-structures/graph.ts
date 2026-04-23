/**
 * Graph (Adjacency List)
 * 
 * A non-linear data structure consisting of nodes (vertices) and edges.
 * 
 * Time Complexity:
 * - Add Vertex: O(1)
 * - Add Edge: O(1)
 * - Remove Vertex: O(V + E)
 * - Remove Edge: O(E)
 * - Search (DFS/BFS): O(V + E)
 * 
 * Use when:
 * - Modeling relationships between entities (social networks, maps, dependencies).
 * 
 * Avoid when:
 * - Data is strictly hierarchical (use a Tree).
 * - Relationship is dense (consider Adjacency Matrix for O(1) edge lookups).
 */
export class Graph<T> {
  private adjacencyList: Map<T, Set<T>> = new Map();

  addVertex(vertex: T): void {
    if (!this.adjacencyList.has(vertex)) {
      this.adjacencyList.set(vertex, new Set());
    }
  }

  addEdge(v1: T, v2: T, directed: boolean = false): void {
    this.addVertex(v1);
    this.addVertex(v2);
    this.adjacencyList.get(v1)!.add(v2);
    if (!directed) {
      this.adjacencyList.get(v2)!.add(v1);
    }
  }

  getNeighbors(vertex: T): T[] {
    return Array.from(this.adjacencyList.get(vertex) || []);
  }

  getVertices(): T[] {
    return Array.from(this.adjacencyList.keys());
  }

  removeEdge(v1: T, v2: T): void {
    this.adjacencyList.get(v1)?.delete(v2);
    this.adjacencyList.get(v2)?.delete(v1);
  }

  removeVertex(vertex: T): void {
    for (const neighbor of this.adjacencyList.get(vertex) || []) {
      this.removeEdge(neighbor, vertex);
    }
    this.adjacencyList.delete(vertex);
  }
}
