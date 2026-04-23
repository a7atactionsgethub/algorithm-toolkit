/**
 * Mergesort
 * 
 * A stable, comparison-based, divide-and-conquer sorting algorithm.
 * 
 * Time Complexity: O(n log n) (consistent performance)
 * Space Complexity: O(n) (requires extra space for merging)
 * 
 * Use when:
 * - Stable sorting is required.
 * - Predictable O(n log n) performance is needed.
 * - Sorting linked lists (can be done in O(1) extra space).
 * 
 * Avoid when:
 * - Memory is highly constrained (use Quicksort or Heapsort).
 */
export function mergesort<T>(arr: T[]): T[] {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergesort(arr.slice(0, mid));
  const right = mergesort(arr.slice(mid));

  return merge(left, right);
}

function merge<T>(left: T[], right: T[]): T[] {
  const result: T[] = [];
  let l = 0;
  let r = 0;

  while (l < left.length && r < right.length) {
    if (left[l] <= right[r]) {
      result.push(left[l]);
      l++;
    } else {
      result.push(right[r]);
      r++;
    }
  }

  return [...result, ...left.slice(l), ...right.slice(r)];
}
