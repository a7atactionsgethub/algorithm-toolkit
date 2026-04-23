package sorting;

import java.util.Arrays;

/**
 * Quicksort
 * Time Complexity: O(n log n) average, O(n^2) worst
 * Space Complexity: O(log n)
 * 
 * Description:
 * Divide-and-conquer algorithm that partitions the array.
 */
public class Quicksort {

    public static void sort(int[] arr, int low, int high) {
        if (low < high) {
            int p = partition(arr, low, high);
            sort(arr, low, p);
            sort(arr, p + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[low + (high - low) / 2];
        int i = low - 1;
        int j = high + 1;

        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            
            if (i >= j) return j;
            
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    public static void main(String[] args) {
        int[] testArr = {3, 6, 8, 10, 1, 2, 1};
        sort(testArr, 0, testArr.length - 1);
        int[] expected = {1, 1, 2, 3, 6, 8, 10};
        assert Arrays.equals(testArr, expected);
        System.out.println("Java Quicksort: All tests passed!");
    }
}
