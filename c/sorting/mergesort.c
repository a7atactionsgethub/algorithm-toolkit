/**
 * Mergesort
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 * 
 * Description:
 * Stable sorting algorithm using divide-and-conquer.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int main() {
    int testArr[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(testArr) / sizeof(testArr[0]);

    mergeSort(testArr, 0, n - 1);

    int expected[] = {3, 9, 10, 27, 38, 43, 82};
    for (int i = 0; i < n; i++) {
        assert(testArr[i] == expected[i]);
    }

    printf("C Mergesort: All tests passed!\n");
    return 0;
}
