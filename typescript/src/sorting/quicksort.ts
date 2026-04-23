/**
 * Quicksort
 * 
 * An efficient, in-place, divide-and-conquer sorting algorithm.
 * 
 * Time Complexity: 
 * - Average: O(n log n)
 * - Worst: O(n^2) (can be avoided with good pivot selection)
 * Space Complexity: O(log n) (stack space for recursion)
 * 
 * Use when:
 * - Average-case performance is critical.
 * - In-place sorting is preferred to save memory.
 * 
 * Avoid when:
 * - Stable sorting is required (Quicksort is not stable).
 * - Worst-case O(n^2) is unacceptable (use Mergesort or Heapsort).
 */
export function quicksort<T>(arr: T[]): T[] {
  const result = [...arr]; // Avoid mutating original array for functional approach
  
  const sort = (low: number, high: number) => {
    if (low < high) {
      const p = partition(low, high);
      sort(low, p);
      sort(p + 1, high);
    }
  };

  const partition = (low: number, high: number): number => {
    const pivot = result[Math.floor((low + high) / 2)];
    let i = low - 1;
    let j = high + 1;

    while (true) {
      do { i++; } while (result[i] < pivot);
      do { j--; } while (result[j] > pivot);
      
      if (i >= j) return j;
      
      [result[i], result[j]] = [result[j], result[i]];
    }
  };

  sort(0, result.length - 1);
  return result;
}
