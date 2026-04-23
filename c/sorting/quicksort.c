/**
 * Quicksort
 * Time Complexity: O(n log n) average, O(n^2) worst
 * Space Complexity: O(log n)
 * 
 * Description:
 * Divide-and-conquer algorithm that partitions the array.
 */

#include <stdio.h>
#include <assert.h>

void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[low + (high - low) / 2];
    int i = low - 1;
    int j = high + 1;

    while (1) {
        do { i++; } while (arr[i] < pivot);
        do { j--; } while (arr[j] > pivot);
        
        if (i >= j) return j;
        
        swap(&arr[i], &arr[j]);
    }
}

void quicksort(int arr[], int low, int high) {
    if (low < high) {
        int p = partition(arr, low, high);
        quicksort(arr, low, p);
        quicksort(arr, p + 1, high);
    }
}

int main() {
    int testArr[] = {3, 6, 8, 10, 1, 2, 1};
    int n = sizeof(testArr) / sizeof(testArr[0]);
    
    quicksort(testArr, 0, n - 1);
    
    int expected[] = {1, 1, 2, 3, 6, 8, 10};
    for (int i = 0; i < n; i++) {
        assert(testArr[i] == expected[i]);
    }

    printf("C Quicksort: All tests passed!\n");
    return 0;
}
