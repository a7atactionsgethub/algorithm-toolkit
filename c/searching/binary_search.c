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

#include <stdio.h>
#include <assert.h>

int binarySearch(int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;

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

int main() {
    int testArr[] = {1, 3, 5, 7, 9, 11};
    int size = sizeof(testArr) / sizeof(testArr[0]);

    assert(binarySearch(testArr, size, 7) == 3);
    assert(binarySearch(testArr, size, 1) == 0);
    assert(binarySearch(testArr, size, 10) == -1);

    printf("C Binary Search: All tests passed!\n");
    return 0;
}
