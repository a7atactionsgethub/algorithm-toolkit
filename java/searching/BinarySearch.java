package searching;

/**
 * Binary Search
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 * 
 * Description:
 * Searches for a target value within a sorted array.
 * 
 * Use when:
 * - Array is sorted.
 */
public class BinarySearch {

    public static int search(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (arr[mid] == target) {
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

    public static void main(String[] args) {
        int[] testArr = {1, 3, 5, 7, 9, 11};
        assert search(testArr, 7) == 3;
        assert search(testArr, 1) == 0;
        assert search(testArr, 10) == -1;
        System.out.println("Java Binary Search: All tests passed!");
    }
}
