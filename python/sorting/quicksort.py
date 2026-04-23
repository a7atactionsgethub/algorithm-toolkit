"""
Quicksort
Time Complexity: O(n log n) average, O(n^2) worst
Space Complexity: O(log n)

Description:
Divide-and-conquer algorithm that picks a pivot and partitions the array around it.

Use when:
- High performance is needed.
- In-place sorting is preferred.
"""

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

if __name__ == "__main__":
    test_arr = [3, 6, 8, 10, 1, 2, 1]
    sorted_arr = quicksort(test_arr)
    assert sorted_arr == [1, 1, 2, 3, 6, 8, 10]
    print("Python Quicksort: All tests passed!")
