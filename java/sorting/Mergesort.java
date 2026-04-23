package sorting;

import java.util.Arrays;

/**
 * Mergesort
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 * 
 * Description:
 * Stable sorting algorithm using divide-and-conquer.
 */
public class Mergesort {

    public static int[] sort(int[] arr) {
        if (arr.length <= 1) {
            return arr;
        }

        int mid = arr.length / 2;
        int[] left = sort(Arrays.copyOfRange(arr, 0, mid));
        int[] right = sort(Arrays.copyOfRange(arr, mid, arr.length));

        return merge(left, right);
    }

    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;

        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }

        while (i < left.length) {
            result[k++] = left[i++];
        }

        while (j < right.length) {
            result[k++] = right[j++];
        }

        return result;
    }

    public static void main(String[] args) {
        int[] testArr = {38, 27, 43, 3, 9, 82, 10};
        int[] sortedArr = sort(testArr);
        int[] expected = {3, 9, 10, 27, 38, 43, 82};
        assert Arrays.equals(sortedArr, expected);
        System.out.println("Java Mergesort: All tests passed!");
    }
}
