import { binarySearch } from '../src/searching/binary_search';
import { depthFirstSearch } from '../src/searching/dfs';
import { Graph } from '../src/data-structures/graph';

describe('Searching Algorithms', () => {
  describe('Binary Search', () => {
    const sortedArray = [1, 3, 5, 7, 9, 11, 13, 15];

    test('should find target in sorted array', () => {
      expect(binarySearch(sortedArray, 7)).toBe(3);
      expect(binarySearch(sortedArray, 1)).toBe(0);
      expect(binarySearch(sortedArray, 15)).toBe(7);
    });

    test('should return -1 if target is not found', () => {
      expect(binarySearch(sortedArray, 4)).toBe(-1);
      expect(binarySearch(sortedArray, 0)).toBe(-1);
      expect(binarySearch(sortedArray, 16)).toBe(-1);
    });

    test('should work with empty array', () => {
      expect(binarySearch([], 10)).toBe(-1);
    });
  });

  describe('Depth First Search', () => {
    test('should traverse graph in DFS order', () => {
      const graph = new Graph<string>();
      graph.addEdge('A', 'B');
      graph.addEdge('A', 'C');
      graph.addEdge('B', 'D');
      graph.addEdge('C', 'E');

      const result = depthFirstSearch(graph, 'A');
      expect(result).toContain('A');
      expect(result).toContain('B');
      expect(result).toContain('C');
      expect(result).toContain('D');
      expect(result).toContain('E');
      expect(result.length).toBe(5);
    });
  });
});
