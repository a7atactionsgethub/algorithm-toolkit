/**
 * Binary Search
 * 
 * Searches for a target value within a sorted array.
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 * 
 * Use when:
 * - Array is sorted.
 * - Fast lookup is required for large datasets.
 * 
 * Avoid when:
 * - Data is unsorted (use linear search instead or sort first).
 * - Data is constantly changing (overhead of keeping it sorted might outweigh search benefits).
 */
export function binarySearch<T>(arr: T[], target: T): number {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor(left + (right - left) / 2);

    if (arr[mid] === target) {
      return mid;
    }

    if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1;
}
