/**
 * Sliding Window Template
 * 
 * A common pattern for problems involving subarrays or substrings.
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1) or O(k) depending on the problem.
 * 
 * Use when:
 * - Looking for a longest/shortest subarray/substring with certain properties.
 * - Calculating metrics over a fixed-size window.
 */

/**
 * Fixed-size Sliding Window example: Max sum of k consecutive elements.
 */
export function maxSubarraySum(arr: number[], k: number): number | null {
  if (arr.length < k) return null;

  let maxSum = 0;
  let windowSum = 0;

  // Initialize first window
  for (let i = 0; i < k; i++) {
    windowSum += arr[i];
  }
  maxSum = windowSum;

  // Slide the window
  for (let i = k; i < arr.length; i++) {
    windowSum = windowSum - arr[i - k] + arr[i];
    maxSum = Math.max(maxSum, windowSum);
  }

  return maxSum;
}

/**
 * Dynamic Sliding Window template for reference:
 * 
 * function dynamicSlidingWindow(arr: T[]) {
 *   let left = 0;
 *   let right = 0;
 *   let state = initial_state;
 * 
 *   while (right < arr.length) {
 *     // 1. Expand the window
 *     updateState(state, arr[right]);
 * 
 *     // 2. Shrink if condition is met
 *     while (condition(state)) {
 *       updateStateBeforeShrink(state, arr[left]);
 *       left++;
 *     }
 * 
 *     right++;
 *   }
 * }
 */
